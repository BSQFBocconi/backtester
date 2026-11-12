"""Data loading.

Reads pre-gathered OHLCV files (CSV / Parquet), validates their columns,
and serves bars to the engine one at a time. Strategies can only access
past bars through this module (no look-ahead).
"""
