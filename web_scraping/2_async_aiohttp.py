"""Download the first 20 pokemon asynchronously using aiohttp."""
import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup
from rich import print


def main() -> None:
    print("Starting tasks...", flush=True)
    t0 = time.time()
    results = asyncio.run(download_pokemon_list_gather())
    total_seconds = time.time() - t0
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )
    print(f"\n{results=}", flush=True)


async def download_pokemon_list_gather() -> list[tuple[int, str]]:
    """Download a list of pokemon from 'pokemondb' using  `asyncio.gather`."""
    coroutines = [download_single_pokemon(num) for num in range(1, 21)]
    print("Gathering coroutines into tasks...", flush=True)
    tasks = asyncio.gather(*coroutines)
    print("Done gathering tasks. Running + awaiting tasks...", flush=True)
    results = await tasks
    print("Done gathering results.", flush=True)
    return results


async def download_pokemon_list_310_manual() -> list[tuple[int, str]]:
    """Download a list of pokemon from 'pokemondb'.

    Manually get the event loop, create and await tasks."""
    coroutines = [download_single_pokemon(num) for num in range(1, 21)]
    loop = asyncio.get_event_loop()
    print("Gathering coroutines into tasks...", flush=True)
    tasks = [loop.create_task(c) for c in coroutines]
    print("Done gathering tasks. Running + awaiting tasks...", flush=True)
    results = [await t for t in tasks]
    print("Done gathering results.", flush=True)
    return results


async def download_pokemon_list_task_group() -> list[tuple[int, str]]:
    """Download a list of pokemon from 'pokemondb' using  a task group.

    Task groups are only available in Python 3.11+.

    The advantage of a task group is that it automatically cancels all tasks
    if one task raises an exception or if the task group itself is cancelled.
    """
    async with asyncio.TaskGroup() as tg:
        print("Gathering coroutines into tasks...", flush=True)
        results = [tg.create_task(download_single_pokemon(num)) for num in range(1, 21)]
        print("Done gathering tasks. Running + awaiting tasks...", flush=True)
    print("Done awaiting results.", flush=True)
    return [result.result() for result in results]


async def download_single_pokemon(pokemon_num: int = 1) -> tuple[int, str]:
    """Get a pokemon from 'pokemondb' by its pokedex number."""
    print(
        f"[yellow]Downloading pokemon {pokemon_num:02}... [/yellow]",
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
