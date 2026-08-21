from pydantic import BaseModel


class StatusResponse(BaseModel):
    service_id: str
    status: str
    data_state: str
    observed_at: str | None
    age_seconds: float | None
    request_id: str


class MetricsResponse(BaseModel):
    service_id: str
    as_of: str
    window_seconds: int
    known_seconds: float
    unknown_seconds: float
    durations_seconds: dict[str, float]
    data_state: str
    request_id: str
