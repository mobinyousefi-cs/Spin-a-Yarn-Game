#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Spin a Yarn Game
File: main.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
    Tkinter GUI for the Spin a Yarn collaborative storytelling game. Players take turns adding lines
    to a story starting from a chosen prompt. Includes undo, save, and offline TTS playback.

Usage:
    python -m spin_a_yarn

Notes:
    - GUI depends on Tkinter; audio via pyttsx3 (optional).
"""
from __future__ import annotations

import json
import os
import pathlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .story_engine import StoryEngine
from .tts import speak_text

APP_TITLE = "Spin a Yarn"
ASSETS_DIR = pathlib.Path(__file__).with_suffix("").parent / "assets"
PROMPTS_FILE = ASSETS_DIR / "prompts.json"


class SpinAYarnApp(ttk.Frame):
    def __init__(self, master: tk.Misc, engine: StoryEngine) -> None:
        super().__init__(master, padding=12)
        self.engine = engine
        self._build_ui()
        self._refresh_state()

    # ---------------- UI Build ----------------
    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        # Title
        title_lbl = ttk.Label(self, text=APP_TITLE, font=("Segoe UI", 16, "bold"))
        title_lbl.grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Prompt + players frame
        top_frm = ttk.Frame(self)
        top_frm.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        top_frm.columnconfigure(1, weight=1)

        ttk.Label(top_frm, text="Starter prompt:").grid(row=0, column=0, sticky="w")
        self.prompt_cmb = ttk.Combobox(top_frm, state="readonly", values=self.engine.prompts)
        self.prompt_cmb.current(0)
        self.prompt_cmb.grid(row=0, column=1, sticky="ew", padx=6)
        self.prompt_cmb.bind("<<ComboboxSelected>>", self._on_prompt_change)

        ttk.Label(top_frm, text="Players (comma‑sep):").grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.players_var = tk.StringVar(value=", ".join(self.engine.players))
        players_ent = ttk.Entry(top_frm, textvariable=self.players_var)
        players_ent.grid(row=1, column=1, sticky="ew", padx=6, pady=(6, 0))

        ttk.Label(top_frm, text="Max turns (optional):").grid(row=2, column=0, sticky="w", pady=(6, 0))
        self.max_turns_var = tk.StringVar(value="")
        max_turns_ent = ttk.Entry(top_frm, textvariable=self.max_turns_var, width=10)
        max_turns_ent.grid(row=2, column=1, sticky="w", padx=6, pady=(6, 0))

        apply_btn = ttk.Button(top_frm, text="Apply", command=self._apply_settings)
        apply_btn.grid(row=0, column=2, rowspan=3, padx=(8, 0))

        # Current player + input
        mid_frm = ttk.Frame(self)
        mid_frm.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        mid_frm.columnconfigure(1, weight=1)

        self.turn_lbl = ttk.Label(mid_frm, text="Turn 1 — Player 1")
        self.turn_lbl.grid(row=0, column=0, sticky="w")

        self.line_var = tk.StringVar()
        self.line_ent = ttk.Entry(mid_frm, textvariable=self.line_var)
        self.line_ent.grid(row=0, column=1, sticky="ew", padx=6)
        self.line_ent.bind("<Return>", lambda e: self._add_line())

        add_btn = ttk.Button(mid_frm, text="Add Line", command=self._add_line)
        add_btn.grid(row=0, column=2, padx=(6, 0))

        undo_btn = ttk.Button(mid_frm, text="Undo", command=self._undo)
        undo_btn.grid(row=0, column=3, padx=(6, 0))

        # Story preview
        story_frm = ttk.LabelFrame(self, text="Story")
        story_frm.grid(row=3, column=0, sticky="nsew")
        story_frm.rowconfigure(0, weight=1)
        story_frm.columnconfigure(0, weight=1)

        self.story_txt = tk.Text(story_frm, wrap="word", height=16)
        self.story_txt.grid(row=0, column=0, sticky="nsew")
        yscroll = ttk.Scrollbar(story_frm, orient="vertical", command=self.story_txt.yview)
        yscroll.grid(row=0, column=1, sticky="ns")
        self.story_txt.configure(yscrollcommand=yscroll.set)
        self.story_txt.insert("1.0", self.engine.selected_prompt + "\n\n")
        self.story_txt.configure(state="disabled")

        # Bottom controls
        bottom_frm = ttk.Frame(self)
        bottom_frm.grid(row=4, column=0, sticky="ew", pady=(8, 0))
        bottom_frm.columnconfigure(0, weight=1)

        read_btn = ttk.Button(bottom_frm, text="Read Story", command=self._read_story)
        save_btn = ttk.Button(bottom_frm, text="Save Story", command=self._save_story)
        clear_btn = ttk.Button(bottom_frm, text="Clear", command=self._clear_story)

        for i, btn in enumerate((read_btn, save_btn, clear_btn)):
            btn.grid(row=0, column=i, sticky="w", padx=(0, 8))

    # ---------------- UI Actions ----------------
    def _on_prompt_change(self, _event=None) -> None:
        self.engine.select_prompt(self.prompt_cmb.current())
        self._refresh_state()

    def _apply_settings(self) -> None:
        self.engine.set_players(self.players_var.get())
        raw = self.max_turns_var.get().strip()
        max_turns = int(raw) if raw.isdigit() else None
        self.engine.set_max_turns(max_turns)
        self._refresh_state()

    def _add_line(self) -> None:
        text = self.line_var.get()
        if not text.strip():
            return
        try:
            self.engine.add_line(text)
        except Exception as exc:  # max turns, etc.
            messagebox.showwarning(APP_TITLE, str(exc))
            return
        finally:
            self.line_var.set("")

        self._refresh_state()

    def _undo(self) -> None:
        if not self.engine.undo():
            messagebox.showinfo(APP_TITLE, "Nothing to undo.")
        self._refresh_state()

    def _read_story(self) -> None:
        ok = speak_text(self.engine.build_story())
        if not ok:
            messagebox.showwarning(APP_TITLE, "TTS engine not available on this system.")

    def _save_story(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Save Story As",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile="spin-a-yarn.txt",
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.engine.build_story())
        except Exception as exc:
            messagebox.showerror(APP_TITLE, f"Failed to save file: {exc}")
        else:
            messagebox.showinfo(APP_TITLE, f"Saved to: {path}")

    def _clear_story(self) -> None:
        if messagebox.askyesno(APP_TITLE, "Clear current story? This cannot be undone."):
            self.engine.reset_story()
            self._refresh_state()

    # ---------------- Helpers ----------------
    def _refresh_state(self) -> None:
        # Update text preview
        self.story_txt.configure(state="normal")
        self.story_txt.delete("1.0", "end")
        self.story_txt.insert("1.0", self.engine.build_story() + "\n")
        self.story_txt.configure(state="disabled")

        # Update turn label
        self.turn_lbl.configure(
            text=f"Turn {self.engine.turn_number} — {self.engine.current_player}"
        )


# ---------------- Entrypoint ----------------
def _load_prompts() -> list[str]:
    # Try packaged prompts first
    try:
        with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Fallback defaults
        return [
            "It was a rainy afternoon when the package finally arrived at the door...",
            "Under the old sycamore tree, a tiny glowing key hummed softly in the dirt...",
            "Everyone in the village knew not to ring the bell at midnight—until tonight.",
        ]


def main() -> None:
    prompts = _load_prompts()
    engine = StoryEngine(prompts=prompts)

    root = tk.Tk()
    root.title(APP_TITLE)
    # consistent theming
    try:
        root.call("source", str(pathlib.Path(__file__).parent / "azure.tcl"))  # optional theme
        root.call("set_theme", "dark")
    except Exception:
        pass

    app = SpinAYarnApp(root, engine)
    app.pack(fill="both", expand=True)

    # Center window
    root.update_idletasks()
    w, h = 760, 520
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
