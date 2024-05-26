from app.models.repository_data_transfer_objs import ServerStats


class StatusResult:
    """
    Api status response template.
    """
    def __init__(self, message: str) -> None:
        self.message = message


class ServerStatsResult:
    """
    Server statistics response template.
    """
    def __init__(self, message: str, statistics: dict) -> None:
        self.message = message
        self.statistics = statistics
