from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta

from alarm import scheduler
from alarm.models import Alarm
from alarm.storage import add_alarm, delete_alarm, load_alarms


def parse_time(value: str) -> datetime:
    try:
        parsed = datetime.strptime(value, "%H:%M")
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"invalid time '{value}', expected HH:MM (e.g. 07:30)"
        )
    now = datetime.now()
    scheduled = now.replace(
        hour=parsed.hour, minute=parsed.minute, second=0, microsecond=0
    )
    if scheduled <= now:
        scheduled += timedelta(days=1)
    return scheduled


def cmd_add(args: argparse.Namespace) -> None:
    alarms = load_alarms()
    next_id = max((a.id for a in alarms), default=0) + 1
    alarm = Alarm(id=next_id, time=args.time)
    add_alarm(alarm)
    print(f"Added alarm {alarm.id} for {alarm.time.strftime('%Y-%m-%d %H:%M')}")


def cmd_list(args: argparse.Namespace) -> None:
    alarms = sorted(load_alarms(), key=lambda a: a.time)
    if not alarms:
        print("No alarms scheduled.")
        return
    for alarm in alarms:
        print(f"[{alarm.id}] {alarm.time.strftime('%Y-%m-%d %H:%M')}")


def cmd_delete(args: argparse.Namespace) -> None:
    alarms = load_alarms()
    if not any(a.id == args.id for a in alarms):
        print(f"No alarm with id {args.id}", file=sys.stderr)
        sys.exit(1)
    delete_alarm(args.id)
    print(f"Deleted alarm {args.id}")


def cmd_run(args: argparse.Namespace) -> None:
    scheduler.run()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="alarm")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Schedule a new alarm")
    add_parser.add_argument("time", type=parse_time, help="Time in HH:MM format")
    add_parser.set_defaults(func=cmd_add)

    list_parser = subparsers.add_parser("list", help="List scheduled alarms")
    list_parser.set_defaults(func=cmd_list)

    delete_parser = subparsers.add_parser("delete", help="Delete an alarm by id")
    delete_parser.add_argument("id", type=int, help="Alarm id to delete")
    delete_parser.set_defaults(func=cmd_delete)

    run_parser = subparsers.add_parser("run", help="Run the alarm scheduler")
    run_parser.set_defaults(func=cmd_run)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
