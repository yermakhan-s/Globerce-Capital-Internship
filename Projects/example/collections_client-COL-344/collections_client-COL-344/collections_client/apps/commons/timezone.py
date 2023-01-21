from datetime import datetime

import pytz

from collections_client.config.config import settings


def now():
    """Return an aware or naive datetime.datetime, depending on settings.USE_TZ."""
    if settings.USE_TZ:
        return datetime.now(tz=pytz.timezone(settings.TZ)).replace(tzinfo=None)
    else:
        return datetime.now()
