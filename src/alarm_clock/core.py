from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time as dt_time
from pathlib import Path
import sys
import time as time_mod

TIME_FORMAT = "%I:%M:%S %p"
DEFAULT_SOUND = "alarm.mp3"


class AlarmError(ValueError):
    """Raised when alarm input or configuration is invalid."""


@dataclass(frozen=True)
class AlarmConfig:
    alarm_time: dt_time
    sound_path: Path
    repeat: bool = True


def parse_alarm_time(value: str) -> dt_time:
    """Parse an alarm time string in HH:MM:SS AM/PM format."""
    try:
        return datetime.strptime(value.strip(), TIME_FORMAT).time()
    except ValueError as exc:
        raise AlarmError(
            "Invalid time format. Use HH:MM:SS AM/PM (e.g., 07:30:00 AM)."
        ) from exc


def format_time(value: datetime) -> str:
    return value.strftime(TIME_FORMAT)


def should_trigger(now: datetime, alarm_time: dt_time) -> bool:
    return now.time().replace(microsecond=0) == alarm_time


def resolve_sound_path(sound_path: str, base_dir: Path | None = None) -> Path:
    base = base_dir or Path.cwd()
    path = Path(sound_path)
    return path if path.is_absolute() else base / path


def _console_beep() -> None:
    print("\a", end="", flush=True)


def _mci_command(command: str) -> None:
    from ctypes import create_unicode_buffer, windll, wintypes

    buffer_length = 256
    buffer = create_unicode_buffer(buffer_length)
    error_code = windll.winmm.mciSendStringW(command, buffer, buffer_length - 1, 0)
    if error_code:
        error_buffer = create_unicode_buffer(buffer_length)
        windll.winmm.mciGetErrorStringW(error_code, error_buffer, buffer_length - 1)
        raise OSError(error_buffer.value or command)


def _win_play(sound_path: Path) -> None:
    alias = "alarm_clock_sound"
    suffix = sound_path.suffix.lower()
    media_type = "waveaudio" if suffix == ".wav" else "mpegvideo"
    path = str(sound_path.resolve())

    _mci_command(f"open \"{path}\" type {media_type} alias {alias}")
    try:
        _mci_command(f"play {alias} wait")
    finally:
        try:
            _mci_command(f"close {alias}")
        except OSError:
            pass


def play_sound(sound_path: Path) -> None:
    if not sound_path.exists():
        _console_beep()
        return

    if sys.platform == "win32":
        try:
            _win_play(sound_path)
            return
        except Exception:
            pass

    _console_beep()


def ring_alarm(sound_path: Path, repeat: bool = True, interval_seconds: float = 1.0) -> None:
    while True:
        play_sound(sound_path)
        if not repeat:
            break
        time_mod.sleep(interval_seconds)


COLUMN_WIDTHS = [15, 11, 15, 9]
COLUMN_HEADERS = ["Current Time", "Alarm Time", "Sound", "Status"]


def _table_border() -> str:
    return "+" + "+".join("-" * (width + 2) for width in COLUMN_WIDTHS) + "+"


def _table_row(values: list[str]) -> str:
    return (
        "|"
        + "|".join(f" {value:^{COLUMN_WIDTHS[idx]}} " for idx, value in enumerate(values))
        + "|"
    )


def run_alarm_loop(
    config: AlarmConfig,
    poll_interval_seconds: float = 1.0,
    ring_interval_seconds: float = 1.0,
) -> None:
    border = _table_border()
    header = _table_row(COLUMN_HEADERS)

    print()
    print(border)
    print(header)
    print(border)

    alarm_label = config.alarm_time.strftime(TIME_FORMAT)

    while True:
        now = datetime.now()
        current_time = format_time(now)
        status = "RINGING" if should_trigger(now, config.alarm_time) else "WAITING"
        row = _table_row([current_time, alarm_label, config.sound_path.name, status])
        print(f"\r{row}", end="", flush=True)

        if status == "RINGING":
            # Print a closing border directly after the row, then the alert line
            print("\n" + border)
            print("\nWake Up!")
            ring_alarm(
                config.sound_path,
                repeat=config.repeat,
                interval_seconds=ring_interval_seconds,
            )

        time_mod.sleep(poll_interval_seconds)
