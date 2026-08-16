#!/usr/bin/env python3

import argparse
import os
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


URL = "http://localhost:8086"
ORG = os.getenv("INFLUX_ORG", "Iot")
BUCKET = os.getenv("INFLUX_BUCKET", "LoadTest")
TOKEN = os.getenv("INFLUX_TOKEN")


def query():
    flux = f'''
from(bucket: "{BUCKET}")
  |> range(start: -1h)
  |> limit(n: 1000)
'''

    start = time.perf_counter()

    try:
        r = requests.post(
            f"{URL}/api/v2/query",
            params={"org": ORG},
            headers={
                "Authorization": f"Token {TOKEN}",
                "Content-Type": "application/vnd.flux",
            },
            data=flux,
            timeout=10,
        )

        latency = (time.perf_counter() - start) * 1000
        return r.status_code == 200, latency

    except requests.RequestException:
        return False, (time.perf_counter() - start) * 1000


def write_result(requests_count, successes, errors, avg_ms, p95_ms):
    data = (
        "loadtest "
        f"requests={requests_count}i,"
        f"successes={successes}i,"
        f"errors={errors}i,"
        f"avg_latency_ms={avg_ms:.2f},"
        f"p95_latency_ms={p95_ms:.2f}"
    )

    requests.post(
        f"{URL}/api/v2/write",
        params={
            "org": ORG,
            "bucket": BUCKET,
            "precision": "s",
        },
        headers={
            "Authorization": f"Token {TOKEN}",
            "Content-Type": "text/plain",
        },
        data=data,
        timeout=5,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--requests", type=int, default=1000)
    parser.add_argument("--workers", type=int, default=50)
    args = parser.parse_args()

    if not TOKEN:
        raise SystemExit("INFLUX_TOKEN ist nicht gesetzt.")

    print(f"Starte {args.requests} Requests mit {args.workers} Workern ...")

    results = []

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(query) for _ in range(args.requests)]

        for future in as_completed(futures):
            results.append(future.result())

    successes = sum(1 for success, _ in results if success)
    errors = len(results) - successes
    latencies = [latency for _, latency in results]

    avg_ms = statistics.mean(latencies)
    p95_ms = sorted(latencies)[int(len(latencies) * 0.95) - 1]

    write_result(
        len(results),
        successes,
        errors,
        avg_ms,
        p95_ms,
    )

    print()
    print(f"Requests:      {len(results)}")
    print(f"Erfolgreich:   {successes}")
    print(f"Fehler:        {errors}")
    print(f"Ø Antwortzeit: {avg_ms:.2f} ms")
    print(f"P95:           {p95_ms:.2f} ms")


if __name__ == "__main__":
    main()