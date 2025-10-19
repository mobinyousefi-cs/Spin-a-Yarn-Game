# Spin a Yarn (Python, Tkinter, pyttsx3)

Spin a Yarn is a lightweight, offline, and GUI-based collaborative storytelling game. Players pick a starting prompt and add lines in turns to weave a fun short story. When finished, the story can be read aloud with text‑to‑speech (TTS) and exported as a `.txt` file.

---

## ✨ Features
- **Clean Tkinter GUI** with turn indicator and live story preview.
- **Starter prompts** (configurable via `prompts.json`).
- **Multi‑player turns** with input length guidance and undo.
- **Text‑to‑speech** playback via `pyttsx3` (offline).
- **Save / Export** story to `.txt`.
- **Robust core engine** (pure Python) with tests.
- **Packaged** with modern Python standards (PEP 621, `src/` layout, Ruff + Black + Pytest CI).

---

## 🧱 Project Structure
```
spin-a-yarn/
├─ src/
│  └─ spin_a_yarn/
│     ├─ __init__.py
│     ├─ main.py
│     ├─ story_engine.py
│     ├─ tts.py
│     └─ assets/
│        └─ prompts.json
├─ tests/
│  ├─ test_story_engine.py
│  └─ test_tts.py
├─ .github/
│  └─ workflows/
│     └─ ci.yml
├─ .editorconfig
├─ .gitignore
├─ LICENSE
├─ pyproject.toml
└─ requirements.txt
```

---

## 🚀 Quickstart

### 1) Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> **Note (Linux):** If `pyttsx3` uses `espeak` or other drivers, install system TTS engine if needed.

### 2) Run the app
```bash
python -m spin_a_yarn
```
Or via CLI entry point (after editable install):
```bash
pip install -e .
spin-a-yarn
```

---

## 🕹️ How to Play
1. Select a **Starter Prompt**.
2. Enter **players' names** (comma‑separated) or leave default.
3. Set optional **Max Turns**.
4. Each player adds a **line** and press **Add Line**.
5. Use **Undo** if needed.
6. Click **Read Story** to hear TTS or **Save Story** to export.

---

## 🧩 Configuration
Starter prompts live in `src/spin_a_yarn/assets/prompts.json`. You can safely add or remove items—GUI will load them at startup.

---

## 🧪 Tests
```bash
pytest -q
```

---

## 🛠️ Development
- Code style: **Ruff** + **Black** (run via CI or locally: `ruff check . && ruff format .`).
- Packaging: **PEP 621** in `pyproject.toml`, `src/` layout.
- Minimum Python version: **3.9**.

---

## 📦 Building a Standalone App (optional)
You can bundle a single‑file executable using **PyInstaller**:
```bash
pip install pyinstaller
pyinstaller -F -n spin-a-yarn src/spin_a_yarn/main.py
```
The binary will be under `dist/` (platform‑specific).

---

## 📜 License
This project is licensed under the **MIT License**. See [LICENSE](./LICENSE).

---

## 👤 Author
**Mobin Yousefi** — [GitHub: mobinyousefi-cs](https://github.com/mobinyousefi-cs)

