from typing import Optional
import getmac as gm


def get_mac_address(*args, **kwargs) -> Optional[str]:
    mac_with_colons = gm.get_mac_address(*args, **kwargs)
    if mac_with_colons:
        return mac_with_colons.lower().replace(":", "").replace("-", "")
    return mac_with_colons
