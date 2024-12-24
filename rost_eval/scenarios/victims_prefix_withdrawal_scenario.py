from functools import cached_property
from typing import TYPE_CHECKING

from bgpy.shared.enums import Prefixes, SpecialPercentAdoptions
from bgpy.simulation_framework import ValidPrefix

if TYPE_CHECKING:
    from bgpy.simulation_engine import BaseSimulationEngine


class VictimsPrefixWithdrawalScenario(ValidPrefix):
    """Valid ann from victim that later is withdrawa, routing loop from attacker

    This is to test that the attacker's ann (with loop) will not get chosen in r2
    """

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
            for victim_asn in self.victim_asns:
                as_obj = engine.as_graph.as_dict[victim_asn]
                withdraw_ann = as_obj.policy.local_rib.pop(Prefixes.PREFIX.value).copy(
                    {"withdraw": True}
                )
                as_obj.policy.withdraw_ann_from_neighbors(withdraw_ann)

    @cached_property
    def _default_adopters(self) -> frozenset[int]:
        """We don't want the victim to adopt here"""

        return frozenset()
