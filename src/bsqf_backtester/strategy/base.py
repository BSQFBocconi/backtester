"""The ``Strategy`` base class that every trading strategy inherits from."""

from abc import ABC, abstractmethod


class Strategy(ABC):
    """Base class for trading strategies.

    To write a strategy, subclass ``Strategy`` and implement ``on_bar``.
    The backtester calls ``on_bar`` once for every bar in the data, in
    chronological order.

    Example::

        from bsqf_backtester import Strategy

        class MyStrategy(Strategy):
            def on_bar(self, ctx):
                ...  # decide whether to buy or sell
    """

    @abstractmethod
    def on_bar(self, ctx) -> None:
        """Called by the backtester once for every bar.

        Args:
            ctx: the strategy context. It gives access to past prices and
                the current position, and is used to place orders.
        """
