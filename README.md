# Alarm Clock CLI

A simple one-time-alarm scheduler. No recurrence, no snooze, no labels — alarms
fire once and are removed. State is persisted to `alarms.json` in the current
directory.

## Usage

```
python -m alarm.cli add HH:MM   # schedule an alarm; rolls to tomorrow if HH:MM already passed today
python -m alarm.cli list        # list scheduled alarms, sorted by time
python -m alarm.cli delete ID   # delete an alarm by id
python -m alarm.cli run         # run the scheduler; sleeps until the next alarm, rings it, repeats
```

`run` is a foreground process — leave it running in a terminal and use
`add`/`list`/`delete` from other terminals to manage alarms while it waits.

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

Both are accepted for this scope — supporting live updates would require
polling, file watching, interruptible sleeps, or another synchronization
mechanism, none of which are worth the added complexity here.
