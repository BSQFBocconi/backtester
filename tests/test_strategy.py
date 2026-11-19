import pytest

from bsqf_backtester import Strategy


def test_strategy_with_on_bar_can_be_created():
    class MyStrategy(Strategy):
        def on_bar(self, ctx):
            pass

    strategy = MyStrategy()

    assert isinstance(strategy, Strategy)


def test_strategy_without_on_bar_raises_type_error():
    class IncompleteStrategy(Strategy):
        pass

    with pytest.raises(TypeError):
        IncompleteStrategy()
