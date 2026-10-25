"""Autonomous development production-line engine (command-line runner).

Standard library only. The engine drives the deterministic half: state machine, stage
progression, gates, budget, pause / resume and the activity log. Producing a stage's
artifacts is delegated to a pluggable driver (see driver.py).
"""
__version__ = "0.1.0"
