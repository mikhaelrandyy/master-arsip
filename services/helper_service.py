from datetime import datetime
import pytz


class HelperService:
    
    def no_timezone(self, date_time:datetime) -> datetime:
        trans_at = date_time.astimezone(pytz.utc)
        trans_at = trans_at.replace(tzinfo=None)
        return trans_at

