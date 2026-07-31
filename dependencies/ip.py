# FastAPI
from fastapi import HTTPException, Request, status

# IP Address
import ipaddress

# Application
from core.settings import settings  # Settings


# Parse network IP or IP Range
def _parse_network(net_str: str):
    net_str = net_str.strip()
    try:
        return ipaddress.ip_network(net_str, strict=False)
    except ValueError:
        return ipaddress.ip_network(f"{net_str}/32", strict=False)


# Tuple for allowed network range IPs
_ALLOWED_NETWORKS = tuple(
    _parse_network(net) for net in settings.allowed_ips.split(",") if net.strip()
)


# IP Dependency
async def ip_access(request: Request) -> bool:
    client_ip = ipaddress.ip_address(request.client.host)

    if not any(client_ip in network for network in _ALLOWED_NETWORKS):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Your IP is not allowed",
        )

    return True
