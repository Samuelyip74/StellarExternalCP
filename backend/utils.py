import re

COLON_MAC = re.compile(r"^(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$")


def mac_to_upper_nodelim(mac: str) -> str:
    # Convert to uppercase, remove non-hex chars
    hexchars = re.sub(r"[^0-9a-fA-F]", "", mac)
    return hexchars.upper()


def colon_mac_to_lower(mac: str) -> str:
    # Normalize to lowercase colon-delimited
    mac_clean = re.sub(r"[^0-9a-fA-F]", "", mac).lower()
    pairs = [mac_clean[i:i+2] for i in range(0, 12, 2)]
    return ":".join(pairs)


def called_station_id(ap_mac: str, ssid: str) -> str:
    # Format: APMAC(without delimiters, uppercase):SSID
    return f"{mac_to_upper_nodelim(ap_mac)}:{ssid}"


def require_params(q: dict, names: list[str]) -> list[str]:
    missing = [n for n in names if not q.get(n)]
    return missing