from bgpy.simulation_engine import BGPFull


class BGPAllowInvalidFull(BGPFull):
    error_on_invalid_routes: bool = False
