"""Strategy base class.

Members subclass ``Strategy`` and implement ``on_bar(ctx)``, which is called
on every bar and decides whether to buy or sell. Only the base class lives
here; members' own strategies live in their own scripts.
"""
