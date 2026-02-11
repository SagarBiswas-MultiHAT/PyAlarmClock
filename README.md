# Python Alarm Clock

<div align="right">

![Python Versions](https://img.shields.io/badge/python-3.9%2B-blue)
![CI](https://github.com/SagarBiswas-MultiHAT/PyAlarmClock/actions/workflows/python-ci.yml/badge.svg?label=CI)
![License](https://img.shields.io/badge/license-MIT-blue)
![Tests](https://img.shields.io/badge/tests-pytest-brightgreen)
![Ruff](https://img.shields.io/badge/lint-ruff-101010)
![Last commit](https://img.shields.io/github/last-commit/SagarBiswas-MultiHAT/PyAlarmClock)

</div>

A small, focused alarm clock that waits for a specific time and then plays a sound. It is optimized for Windows (using `winsound` for `.wav` files) and otherwise uses Windows MCI to support files like `alarm.mp3`.

## What This Project Does

- **Set a time** in `HH:MM:SS AM/PM` format.
- **Show live time** updates while waiting.
- **Play a sound** at the exact second the alarm triggers.
- **Play mp3-ready sounds** via Windows MCI (and fall back to a console beep).
- **Stop cleanly** with `Ctrl+C`.

---

<div align="center">

![](https://imgur.com/DGCjXfI.png)

</div>

---

## Quick Start (No Install)

Make sure you have a sound file named `alarm.mp3` (or your preferred `.mp3/.wav`) in the project root, then run:

```bash
python alarm_clock-v1.1.py
```

You will be prompted for a time like `07:30:00 AM`.

## Full Install (Recommended)

```bash
python -m venv venv
venv\Scripts\activate
pip install -e .[dev]
```

Run the CLI with an mp3 sound file (default `alarm.mp3`):

```bash
alarm-clock --time "07:30:00 AM"
```

Or:

```bash
python -m alarm_clock --time "07:30:00 AM"
```

## CLI Options

```
--time           Alarm time in HH:MM:SS AM/PM format.
--sound          Path to a supported audio file (defaults to alarm.mp3 in the current folder).
--once           Ring only once (no loop).
--poll           Polling interval in seconds (default: 1.0).
--ring-interval  Delay between rings in seconds (default: 1.0).
```

## Sound File

- The default sound path is `alarm.mp3` in the current working directory (Windows falls back to `alarm.wav` if provided).
- You can pass a `.wav` or any supported `.mp3`/`.wav` using `--sound path/to/alarm.mp3`.
- If the file is missing, the app prints a warning and uses a short console beep.

## Project Structure

```
.
├─ alarm_clock-v1.1.py      # Legacy entry point (thin wrapper)
├─ src/
│  └─ alarm_clock/
│     ├─ core.py            # Parsing and alarm logic
│     ├─ cli.py             # Command-line interface
│     └─ __main__.py         # python -m alarm_clock
├─ tests/
│  └─ test_core.py          # Unit tests for parsing and matching
├─ pyproject.toml           # Package metadata and test config
└─ .github/workflows/
   └─ python-ci.yml         # GitHub Actions CI
```

## Design Notes

- Core logic is in `alarm_clock.core` to keep it testable.
- The CLI is a thin layer that validates inputs and manages the loop.
- Platform-specific sound playback is isolated behind a single function.

## Testing

```bash
pytest
```

Tests focus on time parsing and trigger logic to keep them stable across platforms.

## CI (GitHub Actions)

The workflow in `.github/workflows/python-ci.yml` runs tests on Ubuntu for Python 3.9 to 3.12.

## Troubleshooting

- **Time format error**: Make sure you are using `HH:MM:SS AM/PM` (e.g., `07:05:00 PM`).
- **No sound**: Ensure your `.wav` file exists or pass `--sound path/to/file.wav`.
- **Windows only sound API**: On non-Windows systems, the app uses a console beep.

## Contributing

Issues and pull requests are welcome. If you add new features, please include tests and update the README.

