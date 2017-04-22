"""
Scoring is what the `revscoring` library was designed to do.  The basics of
scoring are :class:`revscoring.Model` that implement
:func:`~revscoring.Model.score` and :class:`revscoring.scoring.Statistics` that
are :func:`~revscoring.scoring.Statistics.fit` using the scores generated by a
:class:`revscoring.Model`.  Prediction models are fragile, so models keep track
of their :class:`revscoring.scoring.Environment` and you can
:func:`revscoring.scoring.Environment.check` them against the current
environment.

See :mod:`revscoring.scoring.models` and :mod:`revscoring.scoring.statistics`
for more information.
"""
from .models.model import Model
from .statistics.statistics import Statistics
from .environment import Environment

__all__ = [Model, Statistics, Environment]
