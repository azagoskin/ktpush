from __future__ import annotations
import json
import re
from dataclasses import dataclass, fields as dataclass_fields
from datetime import datetime
from typing import Dict, List, Optional, Sequence, Any, Tuple

__all__ = ("Config", "TimeTrackingItemDC")


DATEFORMAT = "%Y%m%dT%H%M%SZ"
TAG_HEADER = "tags"
ANNOTATION_HEADER = "annotation"
START_HEADER = "start"
END_HEADER = "end"


@dataclass(init=False)
class Config:
    url: str
    token: str
    issue_pattern: str
    username: str

    def __init__(self, raw_configuration: str):
        fields = {field.name for field in dataclass_fields(self)}

        for line in raw_configuration.split("\n"):
            key, value = line.split(": ")
            cleaned_key = key.replace("kaiten.", "")
            if cleaned_key in fields:
                setattr(self, cleaned_key, value)


@dataclass
class TimeTrackingItemDC:
    issue_name: str
    date: datetime
    minutes: int
    annotation: Optional[str]
    type: Optional[str]

    def as_body(self) -> Dict[str, Any]:
        if self.annotation and self.type:
            annotation = (
                f'{self.type if self.type else ""}: '
                f'{self.annotation if self.annotation else ""}'
            )
        elif self.annotation and not self.type:
            annotation = self.annotation
        else:
            annotation = "-"
        return {
            "role_id": 1,
            "time_spent": self.minutes,
            "for_date": datetime.strftime(self.date, "%Y-%m-%d"),
            "comment": annotation,
        }

    @staticmethod
    def _convert_datetimes(start: str, end: str) -> Tuple[int, datetime]:
        start_dt = datetime.strptime(start, DATEFORMAT)
        end_dt = datetime.strptime(end, DATEFORMAT)
        interval = end_dt - start_dt
        minutes = interval.seconds // 60 if interval.seconds > 60 else 1
        return minutes, start_dt

    @staticmethod
    def _get_issue_params(
        tags: Sequence[str], pattern: str
    ) -> Tuple[Optional[str], Optional[str]]:
        issue_ids = [re.search(pattern, tag) for tag in tags]
        issue_ids = [issue_id for issue_id in issue_ids if issue_id]
        if len(issue_ids) > 1:
            raise AttributeError(f"More than one tag: {issue_ids}")

        if issue_ids:
            timetrack_types = [
                tag for tag in tags if not re.search(pattern, tag)
            ]
            if len(timetrack_types) > 1:
                raise AttributeError(f"More than one type: {timetrack_types}")
        else:
            timetrack_types = []

        issue_id = issue_ids[0][0] if issue_ids and issue_ids[0] else None
        timetrack_type = timetrack_types[0] if timetrack_types else None

        return issue_id, timetrack_type

    @classmethod
    def load_many(
        cls, tw_body: str, config: Config
    ) -> List[TimeTrackingItemDC]:
        timetracks: List[TimeTrackingItemDC] = []
        for raw_timetrack in json.loads(tw_body):
            tags = raw_timetrack.get(TAG_HEADER, ())
            issue_name, timetrack_type = cls._get_issue_params(
                tags, config.issue_pattern
            )
            minutes, date = cls._convert_datetimes(
                raw_timetrack.get(START_HEADER), raw_timetrack.get(END_HEADER)
            )

            if issue_name:
                timetracks.append(
                    cls(
                        issue_name=issue_name,
                        annotation=raw_timetrack.get(ANNOTATION_HEADER),
                        minutes=minutes,
                        date=date,
                        type=timetrack_type,
                    )
                )

        return timetracks
