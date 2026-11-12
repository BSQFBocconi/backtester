"""Simulated broker.

Turns orders placed by the strategy into fills: decides the fill price
(next bar's open) and the cost (commission, slippage). Does not track cash
or positions; that is the portfolio's job.
"""
