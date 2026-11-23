import numpy as np
import pandas as pd
import pytest

from bsqf_backtester.strategy import StrategyContext

FIELDS = ["open", "high", "low", "close", "volume"]


@pytest.fixture
def data():
    """Five bars with easy prices: bar i closes at 100 + i."""
    return pd.DataFrame(
        {
            "date": pd.date_range("2026-01-05", periods=5, freq="D"),
            "open": [99.0, 100.0, 101.0, 102.0, 103.0],
            "high": [101.0, 102.0, 103.0, 104.0, 105.0],
            "low": [98.0, 99.0, 100.0, 101.0, 102.0],
            "close": [100.0, 101.0, 102.0, 103.0, 104.0],
            "volume": [1000.0, 1100.0, 1200.0, 1300.0, 1400.0],
        }
    )


# --- history -------------------------------------------------------------


def test_history_returns_last_n_values_oldest_first(data):
    ctx = StrategyContext(data=data, index=4, position=0)

    result = ctx.history("close", 3)

    assert isinstance(result, np.ndarray)
    np.testing.assert_array_equal(result, [102.0, 103.0, 104.0])


def test_history_includes_the_current_bar(data):
    ctx = StrategyContext(data=data, index=2)

    assert ctx.history("close", 1)[-1] == 102.0


@pytest.mark.parametrize("field", FIELDS)
def test_history_works_for_every_field(data, field):
    ctx = StrategyContext(data=data, index=4)

    np.testing.assert_array_equal(ctx.history(field, 2), data[field].iloc[3:5])


def test_history_returns_fewer_values_at_the_start(data):
    ctx = StrategyContext(data=data, index=1)

    np.testing.assert_array_equal(ctx.history("close", 50), [100.0, 101.0])


def test_history_never_includes_future_bars(data):
    for index in range(len(data)):
        # Overwrite every bar after the current one with an obvious fake price.
        poisoned = data.copy()
        poisoned.loc[index + 1 :, FIELDS] = 999.0
        ctx = StrategyContext(data=poisoned, index=index)

        for field in FIELDS:
            values = ctx.history(field, 100)
            assert len(values) == index + 1
            assert 999.0 not in values


def test_invalid_field_raises_value_error(data):
    ctx = StrategyContext(data=data, index=4)

    with pytest.raises(ValueError):
        ctx.history("price", 3)


@pytest.mark.parametrize("n", [0, -3, 2.5])
def test_invalid_n_raises_value_error(data, n):
    ctx = StrategyContext(data=data, index=4)

    with pytest.raises(ValueError):
        ctx.history("close", n)


def test_history_returns_a_copy(data):
    ctx = StrategyContext(data=data, index=4)

    values = ctx.history("close", 3)
    values[:] = 0.0  # a strategy changing the numbers it was given

    assert data["close"].iloc[4] == 104.0
    np.testing.assert_array_equal(ctx.history("close", 3), [102.0, 103.0, 104.0])


# --- position ------------------------------------------------------------


def test_position_returns_the_value_it_was_given(data):
    ctx = StrategyContext(data=data, index=0, position=100)

    assert ctx.position == 100


def test_position_is_zero_by_default(data):
    ctx = StrategyContext(data=data, index=0)

    assert ctx.position == 0


def test_position_cannot_be_changed_by_the_strategy(data):
    ctx = StrategyContext(data=data, index=0, position=100)

    with pytest.raises(AttributeError):
        ctx.position = 0


# --- creating the context ------------------------------------------------


@pytest.mark.parametrize("index", [-1, 5])
def test_index_outside_the_data_raises_value_error(data, index):
    with pytest.raises(ValueError):
        StrategyContext(data=data, index=index)
