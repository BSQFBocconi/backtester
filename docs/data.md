# Data

## Format

Data files go in the `data/` folder. They are **not** committed to git.

Each file contains OHLCV bars for one instrument, sorted by date:

| column | type | description |
|---|---|---|
| `date` | datetime | bar timestamp |
| `open` | float | opening price |
| `high` | float | highest price |
| `low` | float | lowest price |
| `close` | float | closing price |
| `volume` | float | traded volume |

## Where the data comes from

The engine does not download anything: every member gathers data in advance and places the files in `data/` locally.

<!-- TODO: list the recommended sources (e.g. free sources such as Yahoo Finance via yfinance) and how to fetch them. -->

## What not to commit

The contents of `data/` are git-ignored. Never commit data files, in particular:

- **licensed or proprietary data** (exports from Bloomberg, Refinitiv/LSEG, FactSet or university databases): their licenses do not allow redistribution;
- **large files**: keep the repository light and document where to get the data instead.

Commit the code that fetches or processes the data, not the data itself.
