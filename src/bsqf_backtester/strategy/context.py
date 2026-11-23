"""The ``StrategyContext`` passed to ``Strategy.on_bar`` on every bar."""

import numpy as np
import pandas as pd

FIELDS = ("open", "high", "low", "close", "volume")


class StrategyContext:
    """What a strategy can see on the current bar.

    The engine creates a context for every bar and passes it to
    ``Strategy.on_bar``. It only gives access to data up to and including
    the current bar, never later bars (no look-ahead).

    Args:
        data: price table with one row per bar, oldest first, and the
            columns ``open``, ``high``, ``low``, ``close`` and ``volume``.
        index: position of the current bar in ``data`` (0 is the first bar).
        position: number of shares currently held.

    Example::

        ctx = StrategyContext(data=df, index=4, position=0)
        ctx.history("close", 3)  # closes of bars 2, 3 and 4
    """

    def __init__(self, data: pd.DataFrame, index: int, position: int = 0) -> None:
        if not 0 <= index < len(data):
            raise ValueError(
                f"index must be between 0 and {len(data) - 1}, got {index}"
            )
        self._data = data
        self._index = index
        self._position = position

    @property
    def position(self) -> int:
        """Number of shares currently held (0 at the start)."""
        return self._position

    def history(self, field: str, n: int) -> np.ndarray:
        """Return the last ``n`` values of ``field``, oldest first.

        The current bar is included; later bars never are. At the start of
        the data, when fewer than ``n`` bars exist, only the available bars
        are returned.

        Args:
            field: ``"open"``, ``"high"``, ``"low"``, ``"close"`` or ``"volume"``.
            n: how many bars to return, counting back from the current one.

        Raises:
            ValueError: if ``field`` is not one of the columns above, or
                ``n`` is not a positive whole number.
        """
        if field not in FIELDS:
            raise ValueError(f"unknown field {field!r}, expected one of {FIELDS}")
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"n must be a positive whole number, got {n!r}")

        start = max(0, self._index - n + 1)
        end = self._index + 1  # stop right after the current bar: no look-ahead
        return self._data[field].iloc[start:end].to_numpy(copy=True)
