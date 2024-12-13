from typing import TYPE_CHECKING

from bgpy.shared.enums import Prefixes, SpecialPercentAdoptions
from bgpy.shared.exceptions import AnnouncementNotFoundError
from bgpy.simulation_framework import VictimsPrefix

if TYPE_CHECKING:
    from bgpy.simulation_engine import BaseSimulationEngine


class VictimsPrefixWithdrawalScenario(VictimsPrefix):
    min_propagation_rounds: int = 2

    def post_propagation_hook(
        self,
        engine: "BaseSimulationEngine",
        percent_adopt: float | SpecialPercentAdoptions,
        trial: int,
        propagation_round: int,
    ) -> None:
        """Useful hook for post propagation"""

        if propagation_round == 0:
            # Adopting ASNs withdraw no matter what since they always see it
            for asn in self.victim_asns | self.adopting_asns:
                as_obj = engine.as_graph.as_dict[asn]
                try:
                    # We can clear this since there are no alternatives
                    for k in as_obj.policy.ribs_in:
                        as_obj.policy.ribs_in[k].clear()
                    as_obj.policy.prep_withdrawal_for_next_propagation(
                        Prefixes.PREFIX.value
                    )
                # Some ASes may not have recieved the announcement
                # But all victims should have it
                except AnnouncementNotFoundError:
                    if asn in self.victim_asns:
                        raise
