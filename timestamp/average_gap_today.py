#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from datetime import timedelta
from django.db.models import QuerySet, Avg, F, Window, FloatField
from django.db.models.functions import Lag
from django.db.models.expressions import ExpressionWrapper

from django.utils import timezone


def get_average_gap_today(entries: QuerySet) -> float | None:
    """
    Calculates the average time gap (in seconds) between adjoining 'pee' logs recorded today.
    """
    now = timezone.now()
    local_now = timezone.localtime(now)
    today_start = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)
    pee_entries = entries.filter(action="pee").filter(timestamp__gte=yesterday_start)
    annotated_gaps = pee_entries.order_by("timestamp").annotate(
        prev_timestamp=Window(
            expression=Lag("timestamp"),
            order_by=F("timestamp").asc(),
        )
    )
    gaps_today = annotated_gaps.filter(
        prev_timestamp__isnull=False,
        timestamp__gte=today_start,
    ).annotate(
        gap_seconds=ExpressionWrapper(
            (F("timestamp") - F("prev_timestamp")) / timedelta(seconds=1),
            output_field=FloatField(),
        )
    )
    average_gap_result = gaps_today.aggregate(
        average_gap_seconds=Avg("gap_seconds", output_field=FloatField())
    )
    return average_gap_result.get("average_gap_seconds")
