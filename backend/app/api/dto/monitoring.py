from pydantic import BaseModel


class MonitoringServiceResponse(BaseModel):
    id: str
    name: str
    target: str
    description: str | None = None


class CreateMonitoringServiceRequest(BaseModel):
    name: str
    target: str
    description: str | None = None


class MonitoringServiceListResponse(BaseModel):
    items: list[MonitoringServiceResponse]
    page: int
    page_size: int
    total: int
