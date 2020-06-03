from datetime import datetime

from properties import Constants


class MatchHelper:
    @staticmethod
    def get_age(match_id: str) -> float:
        time_now = datetime.now()
        list_time_str = match_id[: -Constants.EXPECTED_ID_LEN]
        year_str = time_now.strftime("%Y-")
        list_time = datetime.strptime(f"{year_str}{list_time_str}", "%Y-%m-%d-%H-%M-%S")
        return (time_now - list_time).total_seconds()
