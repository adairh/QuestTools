"""Standalone launcher for the QuestTools web UI."""

from __future__ import annotations

import argparse
from pathlib import Path

from .server import run_server


def default_data_file() -> Path:
    here = Path(__file__).resolve().parent.parent
    candidate = here / "data" / "quests" / "tan_thu.json"
    return candidate


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Launch the QuestTools management UI")
    parser.add_argument(
        "--data",
        type=Path,
        default=default_data_file(),
        help="Quest data JSON file (mặc định: bộ nhiệm vụ Tân thủ)",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument(
        "--open",
        dest="open_browser",
        action="store_true",
        help="Tự mở trình duyệt sau khi khởi động",
    )
    parser.add_argument(
        "--no-open",
        "--no-browser",
        dest="open_browser",
        action="store_false",
        help="Không tự mở trình duyệt",
    )
    parser.set_defaults(open_browser=True)
    args = parser.parse_args(argv)

    run_server(args.data, host=args.host, port=args.port, open_browser=args.open_browser)


if __name__ == "__main__":  # pragma: no cover
    main()
