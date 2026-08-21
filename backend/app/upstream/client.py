import logging

import httpx

from app.config import STATUS_SERVICE_URL

logger = logging.getLogger("service_monitor.upstream")
UPSTREAM_TIMEOUT_SECONDS = 3.0
VALID_STATUSES = {"healthy", "degraded", "down"}


async def fetch_status(target: str, request_id: str) -> tuple[dict | None, str | None]:
    url = f"{STATUS_SERVICE_URL}/api/v1/status/{target}"
    try:
        async with httpx.AsyncClient(timeout=UPSTREAM_TIMEOUT_SECONDS) as client:
            response = await client.get(url)
    except httpx.TimeoutException:
        logger.warning("upstream_timeout target=%s request_id=%s", target, request_id)
        return None, "timeout"
    except httpx.HTTPError:
        logger.warning("upstream_unavailable target=%s request_id=%s", target, request_id)
        return None, "unavailable"

    if response.status_code != 200:
        logger.warning(
            "upstream_bad_status target=%s http_status=%s request_id=%s",
            target,
            response.status_code,
            request_id,
        )
        return None, "upstream_error"

    logger.info("upstream_ok target=%s request_id=%s", target, request_id)
    return response.json(), None
