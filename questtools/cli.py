"""Command line interface for QuestTools."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .models import Quest, QuestDocument
from .parser import parse_document
from .storage import load_document, save_document


def _load_or_empty(path: Path) -> QuestDocument:
    if path.exists():
        return load_document(path)
    return QuestDocument(title=None, overview="", quests=[])


def _print_quest(quest: Quest) -> None:
    print(f"Quest {quest.id}: {quest.title}")
    if quest.description:
        print(f"  Description: {quest.description}")
    if quest.accept_npc:
        print(f"  Accept NPC: {quest.accept_npc}")
    if quest.complete_npc:
        print(f"  Complete NPC: {quest.complete_npc}")
    if quest.dialog_accept:
        print("  Dialog (accept):")
        for line in quest.dialog_accept:
            print(f"    - {line}")
    if quest.dialog_complete:
        print("  Dialog (complete):")
        for line in quest.dialog_complete:
            print(f"    - {line}")
    if quest.targets:
        print("  Targets:")
        for line in quest.targets:
            print(f"    - {line}")
    if quest.notes:
        print("  Notes:")
        for line in quest.notes:
            print(f"    - {line}")
    if quest.extra_fields:
        print("  Extra fields:")
        for key, value in quest.extra_fields.items():
            print(f"    {key}: {value}")


def cmd_convert(args: argparse.Namespace) -> None:
    input_path = Path(args.input)
    output_path = Path(args.output)

    text = input_path.read_text(encoding="utf-8")
    document = parse_document(text)
    if args.title:
        document.title = args.title
    save_document(output_path, document)
    print(f"Converted {input_path} -> {output_path}")


def cmd_list(args: argparse.Namespace) -> None:
    path = Path(args.data)
    document = load_document(path)

    print(f"Document: {document.title or 'Untitled'}")
    print(f"Overview length: {len(document.overview.splitlines())} lines")
    print("Quests:")
    for quest in sorted(document.quests, key=lambda q: q.id):
        accept = f" (accept: {quest.accept_npc})" if quest.accept_npc else ""
        print(f"  {quest.id:>2}: {quest.title}{accept}")


def _parse_list_argument(values: Optional[List[str]]) -> Optional[List[str]]:
    if values is None:
        return None
    return [value.strip() for value in values if value.strip()]


def cmd_add(args: argparse.Namespace) -> None:
    path = Path(args.data)
    document = _load_or_empty(path)

    next_id = max([quest.id for quest in document.quests], default=0) + 1
    quest = Quest(id=next_id, title=args.title)

    if args.description:
        quest.description = args.description
    if args.accept_npc:
        quest.accept_npc = args.accept_npc
    if args.complete_npc:
        quest.complete_npc = args.complete_npc

    dialog_accept = _parse_list_argument(args.dialog_accept)
    if dialog_accept:
        quest.dialog_accept = dialog_accept

    dialog_complete = _parse_list_argument(args.dialog_complete)
    if dialog_complete:
        quest.dialog_complete = dialog_complete

    targets = _parse_list_argument(args.targets)
    if targets:
        quest.targets = targets

    notes = _parse_list_argument(args.notes)
    if notes:
        quest.notes = notes

    document.quests.append(quest)
    save_document(path, document)
    print(f"Added quest {quest.id}: {quest.title}")


def _find_quest(document: QuestDocument, quest_id: int) -> Quest:
    for quest in document.quests:
        if quest.id == quest_id:
            return quest
    raise SystemExit(f"Quest with id {quest_id} not found")


def cmd_update(args: argparse.Namespace) -> None:
    path = Path(args.data)
    document = load_document(path)
    quest = _find_quest(document, args.id)

    if args.title:
        quest.title = args.title
    if args.description is not None:
        quest.description = args.description
    if args.accept_npc is not None:
        quest.accept_npc = args.accept_npc
    if args.complete_npc is not None:
        quest.complete_npc = args.complete_npc

    if args.dialog_accept is not None:
        quest.dialog_accept = _parse_list_argument(args.dialog_accept) or []
    if args.dialog_complete is not None:
        quest.dialog_complete = _parse_list_argument(args.dialog_complete) or []
    if args.targets is not None:
        quest.targets = _parse_list_argument(args.targets) or []
    if args.notes is not None:
        quest.notes = _parse_list_argument(args.notes) or []

    save_document(path, document)
    print(f"Updated quest {quest.id}: {quest.title}")


def cmd_remove(args: argparse.Namespace) -> None:
    path = Path(args.data)
    document = load_document(path)
    before = len(document.quests)
    document.quests = [quest for quest in document.quests if quest.id != args.id]
    after = len(document.quests)
    if before == after:
        raise SystemExit(f"Quest with id {args.id} not found")
    save_document(path, document)
    print(f"Removed quest {args.id}")


def cmd_show(args: argparse.Namespace) -> None:
    path = Path(args.data)
    document = load_document(path)
    quest = _find_quest(document, args.id)
    _print_quest(quest)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Quest management utilities")
    subparsers = parser.add_subparsers(dest="command")

    convert_parser = subparsers.add_parser("convert", help="Convert a raw document to JSON")
    convert_parser.add_argument("input", help="Path to the raw text document")
    convert_parser.add_argument("output", help="Output JSON file")
    convert_parser.add_argument("--title", help="Override document title", default=None)
    convert_parser.set_defaults(func=cmd_convert)

    list_parser = subparsers.add_parser("list", help="List quests in a data file")
    list_parser.add_argument("data", help="Quest JSON data file")
    list_parser.set_defaults(func=cmd_list)

    show_parser = subparsers.add_parser("show", help="Show a quest in detail")
    show_parser.add_argument("data", help="Quest JSON data file")
    show_parser.add_argument("id", type=int, help="Quest identifier")
    show_parser.set_defaults(func=cmd_show)

    add_parser = subparsers.add_parser("add", help="Add a new quest")
    add_parser.add_argument("data", help="Quest JSON data file")
    add_parser.add_argument("title", help="Title for the new quest")
    add_parser.add_argument("--description")
    add_parser.add_argument("--accept-npc")
    add_parser.add_argument("--complete-npc")
    add_parser.add_argument("--dialog-accept", action="append", help="Dialog lines for accepting")
    add_parser.add_argument("--dialog-complete", action="append", help="Dialog lines for completion")
    add_parser.add_argument("--targets", action="append", help="Quest targets")
    add_parser.add_argument("--notes", action="append", help="Additional notes")
    add_parser.set_defaults(func=cmd_add)

    update_parser = subparsers.add_parser("update", help="Update an existing quest")
    update_parser.add_argument("data", help="Quest JSON data file")
    update_parser.add_argument("id", type=int, help="Quest identifier")
    update_parser.add_argument("--title")
    update_parser.add_argument("--description")
    update_parser.add_argument("--accept-npc")
    update_parser.add_argument("--complete-npc")
    update_parser.add_argument("--dialog-accept", action="append")
    update_parser.add_argument("--dialog-complete", action="append")
    update_parser.add_argument("--targets", action="append")
    update_parser.add_argument("--notes", action="append")
    update_parser.set_defaults(func=cmd_update)

    remove_parser = subparsers.add_parser("remove", help="Remove a quest")
    remove_parser.add_argument("data", help="Quest JSON data file")
    remove_parser.add_argument("id", type=int, help="Quest identifier")
    remove_parser.set_defaults(func=cmd_remove)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
