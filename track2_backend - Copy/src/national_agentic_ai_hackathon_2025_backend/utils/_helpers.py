
def _generate_random_id(length: int = 6) -> str:
    """Generate a random alphanumeric ID."""
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def _generate_random_number_id(length: int = 6) -> str:
    """Generate a random numeric ID of given length."""
    import random
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def _get_date_and_time(dt_str: str) -> tuple[str, str]:
    """Extract date and formatted time from an ISO 8601 datetime string."""
    from datetime import datetime
    dt = datetime.fromisoformat(dt_str)
    date = dt.date().isoformat()
    time = dt.strftime("%I:%M %p")  
    return date, time

def _get_current_time():
    """Internal: current datetime in Karachi timezone as ISO string."""
    from datetime import datetime
    import pytz
    karachi_tz = pytz.timezone("Asia/Karachi")
    return datetime.now(karachi_tz).isoformat()


def should_enable_degraded_mode(status) -> bool:
    """
    Decide whether degraded mode should be enabled based on
    network and battery thresholds.
    """
    if status is None:
        return False
        
    # Handle both dict and Pydantic model objects
    if hasattr(status, 'connection'):
        # Pydantic model object
        connection = status.connection
        battery = status.battery
        downlink = connection.downlink
        effective_type = connection.effectiveType.lower()
        rtt = connection.rtt
        level = battery.level
        charging = battery.charging
    else:
        # Dictionary object
        connection = status.get("connection", {})
        battery = status.get("battery", {})
        downlink = connection.get("downlink", 0)       # Mbps
        effective_type = connection.get("effectiveType", "").lower()
        rtt = connection.get("rtt", 9999)              # ms
        level = battery.get("level", 100)              # %
        charging = battery.get("charging", False)

    # ---- Battery Rules ----
    if level < 10:
        return True
    if level < 20 and not charging:
        return True

    # ---- Network Rules ----
    if effective_type in ["slow-2g", "2g"]:
        return True
    if effective_type == "3g" and (downlink < 1.5 or rtt > 300):
        return True
    if effective_type == "4g" and (downlink < 2 or rtt > 250):
        return True
    if effective_type == "wifi" and downlink < 5:
        return True

    # ---- Default ----
    return False