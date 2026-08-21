from dataclasses import dataclass


@dataclass
class MonitoringRow:
    id: str
    name: str
    target: str
    description: str | None
