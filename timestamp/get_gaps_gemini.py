#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from django.db.models import F, Window, ExpressionWrapper, FloatField, Avg, Min, Max
from django.db.models.functions import Lag
from django.db.models.query import QuerySet
from datetime import timedelta


CONFIDENCE_INTERVAL = (5 * 60, 4 * 60 * 60)


def get_gaps(entries: QuerySet) -> tuple[float | None, float | None]:
    if not entries.exists():
        return None, None
    avg_gap_seconds = (
        entries.filter(action="pee")
        .order_by("timestamp")
        .annotate(
            prev_timestamp=Window(
                expression=Lag(F("timestamp")),
                order_by=F("timestamp").asc(),
            )
        )
        .exclude(prev_timestamp__isnull=True)
        .annotate(
            gap_seconds=ExpressionWrapper(
                (F("timestamp") - F("prev_timestamp")) / timedelta(seconds=1),
                output_field=FloatField(),
            )
        )
        .filter(
            gap_seconds__gte=CONFIDENCE_INTERVAL[0],
            gap_seconds__lte=CONFIDENCE_INTERVAL[1],
        )
        .aggregate(
            average_gap=Avg("gap_seconds"),
            min_gap=Min("gap_seconds"),
            max_gap=Max("gap_seconds"),
        )
    )
    return avg_gap_seconds["min_gap"], avg_gap_seconds["max_gap"]
