from .bgp_allow_invalid_full import BGPAllowInvalidFull


class DropWithdrawalsFull(BGPAllowInvalidFull):
    def process_incoming_anns(self, *args, **kwargs):  # type: ignore
        """Removes withdrawals, then calls super"""

        for prefix, anns in self.recv_q.copy().items():
            self.recv_q[prefix] = [x for x in anns if not x.withdraw]
        super().process_incoming_anns(*args, **kwargs)
