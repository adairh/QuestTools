"""Entry point for running QuestTools as a module."""

from .cli import main


def run() -> None:
    """Execute the CLI."""

    main()


if __name__ == "__main__":  # pragma: no cover
    run()
