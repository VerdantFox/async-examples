"""Interact."""
import random
import time
from concurrent.futures import ThreadPoolExecutor
from threading import RLock

from rich import print

BANK_DATA = {
    "bank_1": 1000,
    "bank_2": 1000,
    "bank_3": 1000,
    "bank_4": 1000,
    "bank_5": 1000,
}

TRANSACTION_LOCK = RLock()


def main() -> None:
    """Run the main program."""
    t0 = time.time()
    print(f"\ninitial={BANK_DATA}\n", flush=True)
    validate_bank()
    run_transactions()
    total_seconds = time.time() - t0

    print(f"\n\nfinal={BANK_DATA}", flush=True)
    print(f"sum={sum(BANK_DATA.values())}", flush=True)
    validate_bank()
    print(
        f"\n[bold green]Code run in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )


def run_transactions() -> None:
    """Run a series of bank transactions synchronously."""
    tasks = []
    for _ in range(50):
        banks = list(BANK_DATA.keys())
        sending_bank = random.choice(banks)
        banks.remove(sending_bank)
        receiving_bank = random.choice(list(banks))
        amount = random.randint(1, 100)
        tasks.append(
            # func, args, kwargs
            (run_transaction, (sending_bank, receiving_bank), {"amount": amount})
        )
    with ThreadPoolExecutor() as executor:
        for task in tasks:
            func, args, kwargs = task
            executor.submit(func, *args, **kwargs)


def run_transaction(sending_bank: str, receiving_bank: str, amount) -> None:
    """Run a bank transaction."""
    print(".", end="", flush=True)
    verify_user()

    with TRANSACTION_LOCK:
        update_bank(sending_bank, -amount)
        update_bank(receiving_bank, amount)
    validate_bank()


def verify_user() -> None:
    """Simulate verifying the user can make the transaction."""
    time.sleep(0.1)


def update_bank(bank_name: str, amount: int) -> None:
    """Update the bank data."""
    BANK_DATA[bank_name] += amount


def validate_bank() -> None:
    """Validate bank data."""
    bank_sum = sum(BANK_DATA.values())
    if bank_sum != 5000:
        print(f"Bank data is incorrect: {bank_sum=}", flush=True)


if __name__ == "__main__":
    main()