# core/__init__.py
# Initializes the core package for JobPulse 24x7

from .job_checker import check_and_notify

__all__ = ["check_and_notify"]
