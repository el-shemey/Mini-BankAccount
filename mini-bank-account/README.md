# Mini Bank Account 🏦

A beginner-friendly **Python command-line wallet application** built to practice object-oriented programming (OOP), encapsulation, input validation, and basic financial operations.

> **Educational project only.** This is not a real banking system. All data is stored in memory and disappears when the program exits. Do not use real account credentials or real money.

## Features

- Create a wallet with an account holder name, opening balance, and PIN
- Check balance with PIN verification
- Deposit and withdraw money with input validation
- Prevent overdrafts and negative/zero transactions
- Change the PIN after verifying the current one
- View an in-session transaction history
- Use `Decimal` for currency amounts instead of floating-point arithmetic
- Store a salted PBKDF2 hash of the PIN rather than the PIN itself

## Getting started

**Requirements:** Python 3.9+ (standard library only).

```bash
python wallet.py
```

Follow the prompts in the terminal. PIN input uses `getpass`, which may behave differently in some IDE consoles; run in a regular terminal if needed.

## Project structure

```text
mini-bank-account/
├── wallet.py
├── README.md
└── .gitignore
```

## OOP concepts practiced

- Classes and objects
- Constructors (`__init__`)
- Encapsulation and private attributes
- Instance and static methods
- Exception handling

## Limitations / future improvements

- Accounts and transactions are not persisted between runs
- Single wallet per program session
- No lockout or rate limiting after incorrect PIN attempts
- No real authentication, banking integrations, or production security guarantees
- Future ideas: automated tests, persistence, multiple users, and a GUI

## Author

**Muhammad Elshemey** · [GitHub](https://github.com/el-shemey)
