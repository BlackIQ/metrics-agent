# IP Address
import ipaddress

# FastAPI
from fastapi import HTTPException, Request, status

# Application
from core.settings import settings  # Settings

# Tuple for allowed network range IPs
_ALLOWED_NETWORKS = tuple(
    ipaddress.ip_network(network) for network in settings.allowed_ips.split(",")
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
