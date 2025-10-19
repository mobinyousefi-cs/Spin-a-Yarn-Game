#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Spin a Yarn Game
File: story_engine.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
    Core game logic for Spin a Yarn: manages prompts, players/turns, story text, and undo.

Usage:
    from spin_a_yarn.story_engine import StoryEngine

Notes:
    - Pure Python, no GUI/IO side effects; unit-test friendly.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class StoryEngine:
    prompts: List[str]
    players: List[str] = field(default_factory=lambda: ["Player 1", "Player 2"])
    max_turns: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.prompts:
            raise ValueError("At least one prompt must be provided.")
        self._selected_prompt_idx: int = 0
        self._turn_index: int = 0
        self._lines: List[str] = []
        self._history: List[str] = []  # for undo (stores last added line)

    # ----- Prompt selection -----
    @property
    def selected_prompt(self) -> str:
        return self.prompts[self._selected_prompt_idx]

    def select_prompt(self, idx: int) -> None:
        if not (0 <= idx < len(self.prompts)):
            raise IndexError("Prompt index out of range.")
        self._selected_prompt_idx = idx
        self.reset_story()

    # ----- Player/turn handling -----
    @property
    def current_player(self) -> str:
        return self.players[self._turn_index % len(self.players)]

    @property
    def turn_number(self) -> int:
        return len(self._lines) + 1

    def set_players(self, players_csv: str) -> None:
        names = [p.strip() for p in players_csv.split(",") if p.strip()]
        if names:
            self.players = names
            self._turn_index = 0

    def set_max_turns(self, max_turns: Optional[int]) -> None:
        if max_turns is not None and max_turns <= 0:
            raise ValueError("max_turns must be positive if provided.")
        self.max_turns = max_turns

    # ----- Story editing -----
    def can_add_line(self) -> bool:
        if self.max_turns is None:
            return True
        return len(self._lines) < self.max_turns

    def add_line(self, text: str) -> None:
        text = text.strip()
        if not text:
            raise ValueError("Cannot add empty line.")
        if not self.can_add_line():
            raise RuntimeError("Maximum number of turns reached.")
        self._lines.append(text)
        self._history.append(text)
        self._turn_index += 1

    def undo(self) -> bool:
        if not self._lines:
            return False
        last = self._lines.pop()
        self._history.append(f"UNDO:{last}")
        self._turn_index = max(0, self._turn_index - 1)
        return True

    def reset_story(self) -> None:
        self._turn_index = 0
        self._lines.clear()
        self._history.clear()

    # ----- Output -----
    def build_story(self) -> str:
        parts = [self.selected_prompt.strip(), "\n"]
        if self._lines:
            parts.append("\n".join(self._lines))
        return "".join(parts).strip() + "\n"

    def history(self) -> List[str]:
        return list(self._history)
