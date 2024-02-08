"""Run simulated banking transactions."""
import random
import time
from concurrent.futures import ThreadPoolExecutor

from rich import print

BANK_DATA = {
    "bank_1": 1000,
    "bank_2": 1000,
    "bank_3": 1000,
    "bank_4": 1000,
    "bank_5": 1000,
}


def main() -> None:
    """Run the main program."""
    t0 = time.time()
    print(f"\ninitial={BANK_DATA}\n", flush=True)
    run_transactions()
    total_seconds = time.time() - t0

    print(f"\n\nfinal={BANK_DATA}", flush=True)
    print(f"sum={sum(BANK_DATA.values())}", flush=True)
    print(
        f"\n[bold green]The code ran in [cyan]{total_seconds:,.2f}[green] seconds.",
        flush=True,
    )


def run_transactions() -> None:
    """Run a series of bank transactions."""
    tasks = []
    for _ in range(20):
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
        [executor.submit(func, *args, **kwargs) for func, args, kwargs in tasks]


def run_transaction(sending_bank: str, receiving_bank: str, amount) -> None:
    """Run a bank transaction."""
    verify_user()
    update_bank(sending_bank, -amount)
    update_bank(receiving_bank, amount)
    print(".", end="", flush=True)


def verify_user() -> None:
    """Simulate verifying the user can make the transaction."""
    time.sleep(0.1)


def update_bank(bank_name: str, amount: int) -> None:
    """Update the bank data."""
    amount_before = BANK_DATA[bank_name]
    time.sleep(0.0001)
    new_amount = amount_before + amount
    BANK_DATA[bank_name] = new_amount
    time.sleep(0.0001)


if __name__ == "__main__":
    main()
