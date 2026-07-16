# Alarm Clock CLI --- MVP Design

## Original Task

> **Build an alarm clock as a Python CLI application.**
>
> -   CLI only
> -   No web UI
> -   No React
> -   No database
> -   There is no detailed specification; decide what to build within
>     the available time.

The lack of a detailed specification means the exercise is primarily
about making sensible engineering decisions, defining an appropriate
MVP, and delivering a complete, maintainable solution within a limited
time budget.

------------------------------------------------------------------------

# Scope Decision

After exploring both a very minimal implementation (single-file script)
and a much larger feature set, the chosen scope targets a realistic
**60--90 minute implementation**.

The goal is to build a **real CLI application**, not just a one-shot
script, while deliberately avoiding features that add disproportionate
complexity.

------------------------------------------------------------------------

# Final MVP Scope

## Supported Commands

``` text
alarm add HH:MM
alarm list
alarm delete <id>
alarm run
```

### `add`

-   Accepts a time in `HH:MM` format.
-   If the time has already passed today, schedules it for tomorrow.
-   Persists the alarm to `alarms.json`.

### `list`

-   Displays all scheduled alarms.
-   Sorted by scheduled time.
-   Shows alarm IDs so they can be deleted.

### `delete`

-   Removes an alarm by ID.
-   Persists the updated alarm list.

### `run`

Acts as a simple scheduler.

1.  Load alarms from storage.
2.  Find the next upcoming alarm.
3.  Sleep exactly until that alarm.
4.  Ring the alarm.
5.  Remove the fired alarm.
6.  Save the updated alarm list.
7.  Repeat indefinitely until interrupted.

------------------------------------------------------------------------

# Alarm Model

-   One-time alarms only.
-   Fired alarms are removed immediately.
-   No extra metadata beyond scheduling information.

------------------------------------------------------------------------

# Persistence

Uses a single JSON file:

``` text
alarms.json
```

No database is required.

------------------------------------------------------------------------

# Project Structure

``` text
alarm/
    cli.py
    models.py
    scheduler.py
    storage.py
```

## `models.py`

-   `Alarm` dataclass
-   Serialization/deserialization helpers

## `storage.py`

Provides a small storage API:

``` python
load_alarms()
save_alarms(alarms)
add_alarm(alarm)
delete_alarm(id)
```

This keeps JSON handling out of `cli.py`.

## `cli.py`

Responsible for:

-   Argument parsing
-   Command dispatch
-   User-facing output

## `scheduler.py`

Responsible for:

-   Finding the next alarm
-   Sleeping until it is due
-   Ringing the alarm
-   Removing fired alarms
-   Continuing to wait

------------------------------------------------------------------------

# Features Deliberately Excluded

## Recurring alarms

-   Adds recurrence logic and unnecessary complexity.

## Snooze

-   Requires runtime interaction and extra state.

## Labels

-   Adds metadata without improving the core scheduling behavior.

## Custom sound files

-   Platform-specific complexity.
-   Terminal bell and console output are sufficient.

------------------------------------------------------------------------

# Scheduler Design

``` text
while running
    load alarms
    find earliest future alarm

    if none exist
        wait briefly
        continue

    sleep until alarm
    ring
    remove alarm
    save
```

------------------------------------------------------------------------

# Known Limitation

If `alarm run` is sleeping until the currently selected alarm, alarms
added from another terminal will **not** be detected until that wait
completes.

This is an intentional trade-off to keep the scheduler simple and is
documented in the README.

------------------------------------------------------------------------

# Design Goals

-   Clear command structure
-   Simple JSON persistence
-   Clean separation of responsibilities
-   Maintainable code
-   Predictable scheduling behavior
-   Deliverable within approximately one hour
