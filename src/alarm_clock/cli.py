from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from .core import (
    AlarmConfig,
    AlarmError,
    DEFAULT_SOUND,
    format_time,
    parse_alarm_time,
    resolve_sound_path,
    run_alarm_loop,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simple alarm clock that triggers at a specified time.",
    )
    parser.add_argument(
        "--time",
        dest="alarm_time",
        help="Alarm time in HH:MM:SS AM/PM format.",
    )
    parser.add_argument(
        "--sound",
        default=DEFAULT_SOUND,
        help="Path to a .wav file. Defaults to alarm.wav in the current folder.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Ring only once instead of looping until stopped.",
    )
    parser.add_argument(
        "--poll",
        type=float,
        default=1.0,
        help="Polling interval in seconds.",
    )
    parser.add_argument(
        "--ring-interval",
        type=float,
        default=1.0,
        help="Interval between rings in seconds when repeating.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    alarm_input = args.alarm_time
    if not alarm_input:
        print(f"\nCurrent Time: {format_time(datetime.now())}")
        alarm_input = input(
            "\n\t..:: Enter the time of alarm to be set (HH:MM:SS AM/PM) ==> "
        )

    try:
        alarm_time = parse_alarm_time(alarm_input)
    except AlarmError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    sound_path = resolve_sound_path(args.sound, base_dir=Path.cwd())
    if not sound_path.exists():
        print(
            f"Warning: sound file not found at {sound_path}. Using a beep fallback.",
            file=sys.stderr,
        )

    print("\n\n\t\t\t..:: Setting up alarm ::..\n")

    config = AlarmConfig(
        alarm_time=alarm_time,
        sound_path=sound_path,
        repeat=not args.once,
    )

    try:
        run_alarm_loop(
            config,
            poll_interval_seconds=args.poll,
            ring_interval_seconds=args.ring_interval,
        )
    except KeyboardInterrupt:
        print("\n\n\t==> Alarm Stopped\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
