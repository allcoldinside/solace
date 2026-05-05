# Canonical BaseCollector is defined in collectors/base.py
# This module re-exports it so legacy imports keep working.
from collectors.base import BaseCollector  # noqa: F401

__all__ = ['BaseCollector']
