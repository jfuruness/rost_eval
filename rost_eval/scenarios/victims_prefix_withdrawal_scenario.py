from typing import TYPE_CHECKING

from bgpy.shared.enums import Prefixes, SpecialPercentAdoptions
from bgpy.simulation_framework import ValidPrefix

if TYPE_CHECKING:
    from bgpy.as_graph import AS
    from bgpy.simulation_engine import BaseSimulationEngine, Policy


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

    # NOTE Commented out code below is to make origin not adopting

    # @cached_property
    # def _default_adopters(self) -> frozenset[int]:
    #     """We don't want the victim to adopt here"""

    #     return frozenset()

    # @cached_property
    # def _default_non_adopters(self) -> frozenset[int]:
    #     """We don't want the victim to adopt here"""

    #     return super()._default_non_adopters | self.victim_asns

    # def get_policy_cls(self, as_obj: "AS") -> type["Policy"]:
    #     """Returns the policy class for a given AS to set"""

    #     asn = as_obj.asn
    #     if asn in self.victim_asns:
    #         if asn in self.adopting_asns:
    #             return self.scenario_config.AdoptPolicyCls
    #         else:
    #             return self.scenario_config.hardcoded_base_asn_cls_dict.get(
    #                 asn, self.scenario_config.BasePolicyCls
    #             )
    #     else:
    #         return super().get_policy_cls(as_obj)
