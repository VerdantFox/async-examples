"""Do some CPU bound work synchronously."""
import time
from concurrent.futures.process import ProcessPoolExecutor

from rich import print


def main():
    print("Starting tasks...", flush=True)
    t0 = time.time()
    results = do_lots_of_math()
    total_seconds = time.time() - t0
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )
    print(f"\n{results=}", flush=True)


def do_lots_of_math() -> list[float]:
    return [do_math_once(num) for num in range(1, 21)]


def do_math_once(starting_number: int = 1) -> float:
    """Do some CPU bound work."""
    print(f"[yellow]Doing math, {starting_number=}...", flush=True)
    x = starting_number
    for _ in range(2_000_000):
        x **= 4
        x **= 0.25
        x **= 2
        x **= 0.5
        x += 1
    print(f"[green]Done with math, {starting_number=}.", flush=True)
    return x


if __name__ == "__main__":
    main()
