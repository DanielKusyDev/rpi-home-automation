from typing import Optional

import arpreq as arpreq


def get_mac_address(ip: str) -> Optional[str]:
    mac_with_colons = arpreq.arpreq(ip)
    if mac_with_colons:
        return mac_with_colons.lower().replace(":", "").replace("-", "")
    return mac_with_colons
