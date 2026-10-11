"""Educational command-line wallet application (not for real money)."""
from decimal import Decimal, InvalidOperation
from getpass import getpass
from hashlib import pbkdf2_hmac
from hmac import compare_digest
from secrets import token_bytes


class Wallet:
    """A simple in-memory wallet with basic PIN-protected operations."""

    def __init__(self, name: str, balance: Decimal, pin: str) -> None:
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        if balance < 0 or not balance.is_finite():
            raise ValueError("Starting balance must be non-negative and finite.")
        if balance.as_tuple().exponent < -2:
            raise ValueError("Use no more than two decimal places.")
        self.name = name.strip()
        self.__balance = balance
        self.__salt = token_bytes(16)
        self.__pin_hash = self.__hash_pin(pin, self.__salt)
        self.__transactions: list[str] = []

    @staticmethod
    def __hash_pin(pin: str, salt: bytes) -> bytes:
        if not (pin.isascii() and pin.isdigit() and 4 <= len(pin) <= 8):
            raise ValueError("PIN must be 4 to 8 digits.")
        return pbkdf2_hmac("sha256", pin.encode(), salt, 200_000)

    def check_pin(self, pin: str) -> bool:
        if not (pin.isascii() and pin.isdigit() and 4 <= len(pin) <= 8):
            return False
        return compare_digest(self.__pin_hash, self.__hash_pin(pin, self.__salt))

    def change_pin(self, old_pin: str, new_pin: str) -> None:
        if not self.check_pin(old_pin):
            raise PermissionError("Incorrect PIN.")
        new_salt = token_bytes(16)
        new_hash = self.__hash_pin(new_pin, new_salt)
        self.__salt, self.__pin_hash = new_salt, new_hash

    def show_balance(self, pin: str) -> Decimal:
        self.__authorize(pin)
        return self.__balance

    def deposit(self, amount: Decimal, pin: str) -> Decimal:
        self.__authorize(pin)
        self.__validate_amount(amount)
        self.__balance += amount
        self.__transactions.append(f"Deposit: +{amount:.2f}")
        return self.__balance

    def withdraw(self, amount: Decimal, pin: str) -> Decimal:
        self.__authorize(pin)
        self.__validate_amount(amount)
        if amount > self.__balance:
            raise ValueError("Insufficient balance.")
        self.__balance -= amount
        self.__transactions.append(f"Withdrawal: -{amount:.2f}")
        return self.__balance

    def transaction_history(self, pin: str) -> tuple[str, ...]:
        self.__authorize(pin)
        return tuple(self.__transactions)

    def __authorize(self, pin: str) -> None:
        if not self.check_pin(pin):
            raise PermissionError("Incorrect PIN.")

    @staticmethod
    def __validate_amount(amount: Decimal) -> None:
        if not amount.is_finite() or amount <= 0 or amount.as_tuple().exponent < -2:
            raise ValueError("Amount must be positive with at most two decimal places.")


def read_amount(prompt: str) -> Decimal:
    try:
        return Decimal(input(prompt).strip())
    except InvalidOperation as exc:
        raise ValueError("Enter a valid number.") from exc


def main() -> None:
    print("\n=== Mini Bank Account ===")
    name = input("Account holder name: ").strip()
    try:
        initial_balance = read_amount("Starting balance: ")
        pin = getpass("Create a 4-8 digit PIN: ")
        wallet = Wallet(name, initial_balance, pin)
    except (ValueError, EOFError, KeyboardInterrupt) as exc:
        print(f"Could not create account: {exc}")
        return

    while True:
        print("\n1. Check balance  2. Deposit  3. Withdraw")
        print("4. Change PIN     5. History  6. Exit")
        try:
            choice = input("Choose an option: ").strip()
            if choice == "6":
                print("Goodbye!")
                break
            if choice not in {"1", "2", "3", "4", "5"}:
                print("Invalid option.")
                continue
            pin = getpass("Enter PIN: ")
            if choice == "1":
                print(f"Balance: {wallet.show_balance(pin):.2f}")
            elif choice == "2":
                if not wallet.check_pin(pin):
                    raise PermissionError("Incorrect PIN.")
                print(f"New balance: {wallet.deposit(read_amount('Deposit amount: '), pin):.2f}")
            elif choice == "3":
                if not wallet.check_pin(pin):
                    raise PermissionError("Incorrect PIN.")
                print(f"New balance: {wallet.withdraw(read_amount('Withdrawal amount: '), pin):.2f}")
            elif choice == "4":
                wallet.change_pin(pin, getpass("New PIN: "))
                print("PIN changed successfully.")
            else:
                history = wallet.transaction_history(pin)
                print("\n".join(history) if history else "No transactions yet.")
        except (ValueError, PermissionError) as exc:
            print(f"Error: {exc}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
