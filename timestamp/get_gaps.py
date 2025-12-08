#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from .models import LogEntry
from datetime import timedelta

CONFIDENCE_INTERVAL = (5 * 60, 3 * 60 * 60)


def seconds_as_time(seconds: int) -> str:
    td = timedelta(seconds=seconds)
    time_str = str(td)
    if len(time_str.split(":")) == 2:
        time_str = "0:" + time_str
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def get_gaps(entries: list[LogEntry]) -> tuple[int, int]:
    min_gap, max_gap = 200000000, -1
    prev_entry: LogEntry or None = None
    for e in entries.filter(action="pee").order_by("timestamp"):
        d: int = -1
        if prev_entry is not None:
            d = timedelta.total_seconds(e.timestamp - prev_entry.timestamp)
        if CONFIDENCE_INTERVAL[0] <= d <= CONFIDENCE_INTERVAL[1]:
            if d > max_gap:
                max_gap = d
            if d < min_gap:
                min_gap = d
        prev_entry = e
    return min_gap, max_gap
