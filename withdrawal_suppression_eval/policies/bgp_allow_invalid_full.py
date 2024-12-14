from bgpy.simulation_engine import BGPFull


class BGPAllowInvalidFull(BGPFull):
    @property
    def error_on_invalid_routes(self) -> bool:
        """Invalid routes caused by ASes dropping attrs is not a bug in this case"""
        return False
