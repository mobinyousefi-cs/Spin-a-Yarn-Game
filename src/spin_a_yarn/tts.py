#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Spin a Yarn Game
File: tts.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
    Offline TTS utilities built on top of pyttsx3 with safe fallbacks for CI and headless envs.

Usage:
    from spin_a_yarn.tts import speak_text
    speak_text("Hello world")

Notes:
    - Honors CI=true env to disable actual audio speaking (no-op mode).
"""
from __future__ import annotations

import os
from typing import Optional

try:
    import pyttsx3  # type: ignore
except Exception:  # pragma: no cover
    pyttsx3 = None  # allow import even if missing at runtime


def _get_engine():  # pragma: no cover - tiny wrapper
    if pyttsx3 is None:
        return None
    try:
        return pyttsx3.init()
    except Exception:
        return None


def speak_text(text: str, *, rate: Optional[int] = None, volume: Optional[float] = None) -> bool:
    """Speak text using pyttsx3; returns True if spoken or safely skipped in CI.

    In CI or when audio driver is missing, this becomes a no-op and returns True.
    """
    text = (text or "").strip()
    if not text:
        return False

    if os.getenv("CI", "").lower() in {"1", "true", "yes"}:
        # In CI, pretend success without audio output.
        return True

    engine = _get_engine()
    if engine is None:
        return False

    if rate is not None:
        try:
            engine.setProperty("rate", int(rate))
        except Exception:
            pass
    if volume is not None:
        try:
            engine.setProperty("volume", float(volume))
        except Exception:
            pass

    try:
        engine.say(text)
        engine.runAndWait()
        return True
    except Exception:
        return False
