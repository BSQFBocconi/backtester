# backtester

Official backtesting engine of **BSQF**.

An event-driven Python backtester: members write a trading strategy in their own script, run it on historical data gathered in advance, and get back performance metrics.

> **Status:** early development. The repository structure is in place; the components described below are being implemented.

---

## Design principles

- **Event-driven.** The engine moves through history one bar at a time, the way a strategy would run live.
- **No look-ahead.** At bar *t*, a strategy only sees data up to *t*. Orders placed at bar *t* are filled at the open of bar *t+1*.
- **Local data.** Data is gathered in advance and stored as files (CSV / Parquet). The engine doesn't download anything.
- **Simple to use.** Writing a strategy means subclassing one class and implementing one method.

---

## Setup

We use [**uv**](https://docs.astral.sh/uv/) to manage Python and dependencies. It replaces `pip` + `venv` and gives everyone the same environment through a lock file (`uv.lock`).

**1. Install uv** (once per machine)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# or: brew install uv

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**2. Clone and install**

```bash
git clone <repo-url>
cd backtester
uv sync            # creates .venv/ and installs all dependencies
```

**3. Run code**

```bash
uv run python examples/my_strategy.py
uv run pytest
```

### pip → uv cheat sheet

| What you want | pip | uv |
|---|---|---|
| Create a virtual env | `python -m venv .venv` + activate | automatic on `uv sync` |
| Install the project's deps | `pip install -r requirements.txt` | `uv sync` |
| Add a dependency | `pip install pandas` (then edit requirements by hand) | `uv add pandas` |
| Add a dev-only dependency | — | `uv add --dev pytest` |
| Remove a dependency | `pip uninstall pandas` | `uv remove pandas` |
| Run a script | `python script.py` (with venv active) | `uv run python script.py` |

`uv add` / `uv remove` update `pyproject.toml` and `uv.lock`. Commit both files.

---

## Usage (planned API)

Members import the package in their own script, define a strategy, and run it:

```python
from bsqf_backtester import Backtest, Strategy, load_csv


class SmaCross(Strategy):
    """Buy when the 20-bar SMA crosses above the 50-bar SMA, sell when it crosses below."""

    def on_bar(self, ctx):
        closes = ctx.history("close", 50)
        if len(closes) < 50:
            return

        fast, slow = closes[-20:].mean(), closes.mean()
        if fast > slow and ctx.position == 0:
            ctx.buy(size=100)
        elif fast < slow and ctx.position > 0:
            ctx.sell(size=ctx.position)


data = load_csv("data/AAPL.csv")
result = Backtest(data, SmaCross(), cash=100_000, commission_bps=1).run()

print(result.metrics)    # Sharpe, max drawdown, total return, ...
result.equity_curve      # pandas Series
result.trades            # pandas DataFrame
```

---

## Data

Data files go in the `data/` folder and are **not** committed to git (licensed data such as Bloomberg or Refinitiv exports must never be pushed). Each file holds OHLCV bars (`date, open, high, low, close, volume`) for one instrument.

See [docs/data.md](docs/data.md) for the full format and where to get the data.

---

## Architecture

```
DataHandler ──bar──▶ Strategy ──Order──▶ Broker (simulated) ──Fill──▶ Portfolio
     ▲                                                                   │
     └────────────── Engine loop (one bar at a time) ◀───────────────────┘
```

Modules live in `src/bsqf_backtester/` (`data`, `strategy`, `execution`, `portfolio`, `metrics`, `engine`). See [docs/architecture.md](docs/architecture.md) for the event loop, each module's role and the repository layout, and [docs/](docs/README.md) for all documentation.

---

## Roadmap

**v1: core**
- [ ] CSV / Parquet data loader with schema validation
- [ ] `Strategy` base class and strategy context (`history`, `position`, `buy`, `sell`)
- [ ] Simulated broker with market orders, filled at next bar open
- [ ] Commission and slippage models
- [ ] Portfolio accounting (cash, positions, equity curve, trades)
- [ ] Performance metrics
- [ ] `Backtest` engine and `Result` object
- [ ] Example strategy in `examples/`
- [ ] Tests for each module

**Later**
- Multiple instruments in one backtest
- Limit and stop orders
- Plots / HTML tearsheet
- Intraday data
- Parameter sweeps

---

## Contributing

We follow the [BSQF contributing guidelines](https://github.com/BSQFBocconi/.github/blob/main/CONTRIBUTING.md). In short:

1. Open (or pick) an issue and assign it to yourself.
2. Create a branch from `main`: `feature/...`, `fix/...` or `docs/...`.
3. Make your changes, add tests in `tests/`, and update `README.md` / `docs/` if behaviour changes.
4. Check that the tests pass: `uv run pytest`
5. Open a pull request linking the issue (`Closes #12`). Merging needs a review from a code owner (see `.github/CODEOWNERS`). Delete the branch after the merge.

Never commit secrets, licensed data or large files.

---

## Disclaimer

This project is for **educational and research purposes only** and does not constitute investment advice.
