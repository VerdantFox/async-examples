"""Download the first 20 pokemon with threads."""
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

import requests
from bs4 import BeautifulSoup
from rich import print


def main() -> None:
    t0 = time.time()
    print("Starting coordinating function...", flush=True)
    results = download_pokemon_list()
    total_seconds = time.time() - t0
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )
    print(f"\n{results=}", flush=True)


TaskType = tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]


def download_pokemon_list() -> list[tuple[int, str]]:
    """Download a list of pokemon from 'pokemondb'."""
    print("Defining tasks...", flush=True)
    tasks: list[TaskType] = [
        # Function, args, kwargs
        (download_single_pokemon, (num,), {})
        for num in range(1, 21)
    ]
    print("Kick off threaded tasks...", flush=True)
    with ThreadPoolExecutor() as executor:
        work = [executor.submit(func, *args, **kwargs) for func, args, kwargs in tasks]
        print("Waiting for downloads...", flush=True)
    print("Done", flush=True)
    return [future.result() for future in work]


def download_single_pokemon(pokemon_num: int = 1) -> tuple[int, str]:
    """Get a pokemon from 'pokemondb' by its pokedex number."""
    print(
        f"[yellow]Downloading pokemon {pokemon_num:02}... [/yellow]",
        flush=True,
    )
    url = f"https://pokemondb.net/pokedex/{pokemon_num}"
    resp = requests.get(url, allow_redirects=True)
    resp.raise_for_status()
    header = get_h1(resp.text)
    print(
        f"[green]Retrieved [magenta]{pokemon_num:02}={header}",
        flush=True,
    )
    return (pokemon_num, header)


def get_h1(html: str) -> str:
    """Parse the HTML and return the first H1 tag."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.h1.text


if __name__ == "__main__":
    main()
