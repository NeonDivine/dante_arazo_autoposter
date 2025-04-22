from datetime import datetime

def should_post_now():
    now = datetime.utcnow()
    local_hour = (now.hour + 2) % 24  # Slovenia = UTC+2 (CEST)
    return local_hour in [11, 16]
