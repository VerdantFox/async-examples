"""Download the first 20 Pokémon asynchronously using aiohttp."""
import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup
from rich import print


def main() -> None:
    t0 = time.time()
    print("Starting coordinating coroutine...", flush=True)
    results = asyncio.run(download_pokemon_list())
    total_seconds = time.time() - t0
    print(
        f"\n[bold green]The code ran in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )
    print(f"\n{results=}", flush=True)


async def download_pokemon_list() -> list[tuple[int, str]]:
    """Download a list of Pokémon from 'pokemondb.net'."""
    print("Creating coroutine objects...", flush=True)
    coroutines = [download_single_pokemon(num) for num in range(1, 21)]
    print("Gathering coroutines into tasks...", flush=True)
    tasks = asyncio.gather(*coroutines)
    print("Done gathering tasks. Running + awaiting tasks...", flush=True)
    results = await tasks
    print("Done gathering results.", flush=True)
    return results


async def download_single_pokemon(pokemon_num: int = 1) -> tuple[int, str]:
    """Get a Pokémon from 'pokemondb.net' by its pokedex number."""
    print(
        f"[yellow]Downloading Pokémon {pokemon_num:02}... [/yellow]",
        flush=True,
    )
    url = f"https://pokemondb.net/pokedex/{pokemon_num}"
    async with aiohttp.ClientSession() as session, session.get(url) as resp:
        resp.raise_for_status()
        text = await resp.text()
    resp.raise_for_status()
    header = get_h1(text)
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
