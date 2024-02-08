"""Download the first 20 Pokémon synchronously."""
import time

import requests
from bs4 import BeautifulSoup
from rich import print


def main() -> None:
    t0 = time.time()
    print("Starting coordinating function...", flush=True)
    results = download_pokemon_list()
    total_seconds = time.time() - t0
    print(
        f"\n[bold green]The code ran in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )
    print(f"\n{results=}", flush=True)


def download_pokemon_list() -> list[tuple[int, str]]:
    """Download a list of Pokémon from 'pokemondb.net'."""
    return [download_single_pokemon(num) for num in range(1, 21)]


def download_single_pokemon(pokemon_num: int = 1) -> tuple[int, str]:
    """Get a Pokémon from 'pokemondb.net' by its pokedex number."""
    print(
        f"[yellow]Downloading Pokémon {pokemon_num:02}... [/yellow]",
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
