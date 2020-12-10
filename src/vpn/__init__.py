from .vpn import VPN
from .nord import NordVPN

vpns = {
    'nord': NordVPN,
}


def get_vpn(name: str, *args, **kwargs) -> VPN:
    if name not in vpns:
        raise ValueError(f"Unknown VPN '{name}'")
    return vpns[name](*args, **kwargs)
