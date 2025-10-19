#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Spin a Yarn Game
File: test_story_engine.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================
"""
from spin_a_yarn.story_engine import StoryEngine


def make_engine():
    return StoryEngine(
        prompts=["p1", "p2"],
        players=["A", "B"],
        max_turns=None,
    )


def test_initial_state():
    eng = make_engine()
    assert eng.selected_prompt == "p1"
    assert eng.turn_number == 1
    assert eng.current_player == "A"


def test_add_and_undo():
    eng = make_engine()
    eng.add_line("hello")
    assert "hello" in eng.build_story()
    assert eng.current_player == "B"
    assert eng.turn_number == 2

    assert eng.undo() is True
    assert "hello" not in eng.build_story()
    assert eng.current_player == "A"


def test_max_turns():
    eng = make_engine()
    eng.set_max_turns(1)
    eng.add_line("one")
    try:
        eng.add_line("two")
    except RuntimeError:
        pass
    else:
        raise AssertionError("Expected RuntimeError when exceeding max turns")


def test_select_prompt_resets():
    eng = make_engine()
    eng.add_line("x")
    eng.select_prompt(1)
    assert eng.selected_prompt == "p2"
    assert "x" not in eng.build_story()
