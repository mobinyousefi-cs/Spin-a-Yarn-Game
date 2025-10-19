#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Spin a Yarn Game
File: test_tts.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================
"""
import os
from spin_a_yarn.tts import speak_text


def test_tts_noop_in_ci(monkeypatch):
    monkeypatch.setenv("CI", "true")
    assert speak_text("hello world") is True


def test_tts_reject_empty():
    assert speak_text("") is False
    assert speak_text("   ") is False
