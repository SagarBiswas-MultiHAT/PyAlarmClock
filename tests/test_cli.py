from alarm_clock.cli import build_parser


def test_build_parser_parses_args() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "--time",
            "07:30:00 AM",
            "--sound",
            "custom.wav",
            "--once",
            "--poll",
            "0.5",
            "--ring-interval",
            "2",
        ]
    )

    assert args.alarm_time == "07:30:00 AM"
    assert args.sound == "custom.wav"
    assert args.once is True
    assert args.poll == 0.5
    assert args.ring_interval == 2.0
