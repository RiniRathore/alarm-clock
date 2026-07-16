# Alarm Clock CLI

A simple one-time-alarm scheduler. No recurrence, no snooze, no labels — alarms
fire once and are removed. State is persisted to `alarms.json` in the current
directory.

## Requirements

- Python 3.9+
- No third-party dependencies for the CLI itself; running the test suite needs `pytest`.

## Architecture

```
CLI (alarm/cli.py)  ->  Scheduler (alarm/scheduler.py)  ->  Storage (alarm/storage.py)  ->  alarms.json
```

- `cli.py` — argument parsing, command dispatch, user-facing output.
- `scheduler.py` — the `run` loop: find the next alarm, sleep until it's due, ring it, remove it, repeat.
- `storage.py` — load/save/add/delete against `alarms.json`, with atomic writes (temp file + `os.replace`).
- `models.py` — the `Alarm` dataclass and its JSON (de)serialization.

## Why JSON, not a database

The task ruled out a database, and a single JSON file is enough to persist a small, flat list of alarms — no queries, joins, or concurrent writers beyond the two CLI processes this app supports. Atomic writes (write to a temp file, then `os.replace`) keep a crash or concurrent `run`/`add` from corrupting `alarms.json`.

## Usage

```
python -m alarm.cli add HH:MM   # schedule an alarm; rolls to tomorrow if HH:MM already passed today
python -m alarm.cli list        # list scheduled alarms, sorted by time
python -m alarm.cli delete ID   # delete an alarm by id
python -m alarm.cli run         # run the scheduler; sleeps until the next alarm, rings it, repeats
```

`run` is a foreground process — leave it running in a terminal and use
`add`/`list`/`delete` from other terminals to manage alarms while it waits.

## Running tests

```
python3 -m pytest
```

## What was deliberately left out

- **Recurring alarms** — adds recurrence logic and unnecessary complexity for this scope.
- **Snooze** — requires runtime interaction and extra state.
- **Labels** — adds metadata without improving the core scheduling behavior.
- **Custom sound files** — platform-specific complexity; the terminal bell and console output are sufficient.

## Known limitations

- **`run` doesn't notice changes made to other alarms while it's asleep.**
  It sleeps exactly until the next alarm it knew about when it last checked.
  If you `add` a new, earlier alarm from another terminal while `run` is
  mid-sleep, it won't be picked up until the current wait completes.
- **`run` doesn't notice if the alarm it's currently sleeping on gets deleted.**
  Same root cause as above: there's no live cancellation of an in-progress
  wait. If another terminal deletes the exact alarm `run` is waiting for, it
  will still wake up and ring it; the subsequent delete is a harmless no-op
  since the alarm is already gone.
- **Two concurrent `add` calls can produce a duplicate id.** `cli.py` computes
  the next id by reading the current alarms before calling
  `storage.add_alarm`, so two `add` invocations racing each other could both
  compute the same id. Fixing this properly would mean pushing id generation
  into `storage.add_alarm` itself, changing its already-tested signature.

All three are accepted for this scope. The first two would require polling,
file watching, interruptible sleeps, or another synchronization mechanism to
fix, none of which are worth the added complexity here. The third is a much
lower-severity worst case (a duplicate id) than the `run`-loop races (which
risk silently resurrecting or losing alarms), and reworking a tested
interface for it isn't worth the churn.
