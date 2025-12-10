#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from django.db.models import Count, Case, When, F, IntegerField
from django.utils import timezone
from django.db.models.query import QuerySet
from datetime import timedelta


def get_daily_counts(entries: QuerySet) -> tuple[int | None, int | None]:
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)
    daily_counts = (
        entries.filter(action="pee")
        .filter(
            timestamp__gte=yesterday_start,
        )
        .aggregate(
            count_today=Count(
                Case(
                    When(
                        timestamp__gte=today_start,
                        then=F("id"),
                    ),
                    default=None,
                    output_field=IntegerField(),
                )
            ),
            count_yesterday=Count(
                Case(
                    When(
                        timestamp__gte=yesterday_start,
                        timestamp__lt=today_start,
                        then=F("id"),
                    ),
                    default=None,
                    output_field=IntegerField(),
                )
            ),
        )
    )
    return daily_counts["count_today"], daily_counts["count_yesterday"]
