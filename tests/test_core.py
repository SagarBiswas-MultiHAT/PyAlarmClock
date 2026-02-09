from datetime import datetime, time as dt_time
from pathlib import Path

import pytest

from alarm_clock import core
from alarm_clock.core import AlarmError, parse_alarm_time, resolve_sound_path, should_trigger


def test_parse_alarm_time_valid() -> None:
    parsed = parse_alarm_time("07:30:00 AM")
    assert parsed == dt_time(7, 30, 0)


def test_parse_alarm_time_invalid() -> None:
    with pytest.raises(AlarmError):
        parse_alarm_time("25:61:00")


def test_should_trigger_matches_time() -> None:
    now = datetime(2024, 1, 1, 7, 30, 0)
    assert should_trigger(now, dt_time(7, 30, 0))


def test_should_trigger_mismatch() -> None:
    now = datetime(2024, 1, 1, 7, 30, 1)
    assert not should_trigger(now, dt_time(7, 30, 0))


def test_resolve_sound_path_relative() -> None:
    base = Path("C:/tmp")
    resolved = resolve_sound_path("alarm.wav", base_dir=base)
    assert resolved == base / "alarm.wav"


def test_play_sound_uses_win_play(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    called: list[Path] = []

    def fake_win_play(path: Path) -> None:
        called.append(path)

    monkeypatch.setattr(core, "_win_play", fake_win_play)
    monkeypatch.setattr(core.sys, "platform", "win32")
    sound_file = tmp_path / "alarm.mp3"
    sound_file.write_bytes(b"")

    core.play_sound(sound_file)

    assert called == [sound_file]


def test_play_sound_missing_file_beeps(monkeypatch: pytest.MonkeyPatch) -> None:
    called = {"beep": False}

    def fake_beep() -> None:
        called["beep"] = True

    monkeypatch.setattr(core, "_console_beep", fake_beep)
    monkeypatch.setattr(core.sys, "platform", "linux")

    core.play_sound(Path("missing.wav"))

    assert called["beep"] is True
