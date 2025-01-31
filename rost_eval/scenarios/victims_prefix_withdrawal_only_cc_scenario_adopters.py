from typing import TYPE_CHECKING

from bgpy.shared.enums import SpecialPercentAdoptions
from bgpy.simulation_framework import ScenarioConfig

from .victims_prefix_withdrawal_scenario import VictimsPrefixWithdrawalScenario

if TYPE_CHECKING:
    from bgpy.simulation_engine import BaseSimulationEngine


class VictimsPrefixWithdrawalOnlyCCScenarioAdopters(VictimsPrefixWithdrawalScenario):
    """Same as parent but only tracks adopters customer cone"""

    def __init__(
        self,
        *,
        scenario_config: ScenarioConfig,
        percent_adoption: float | SpecialPercentAdoptions = 0,
        engine: "BaseSimulationEngine | None" = None,
        attacker_asns: frozenset[int] | None = None,
        victim_asns: frozenset[int] | None = None,
        adopting_asns: frozenset[int] | None = None,
    ):
        super().__init__(
            scenario_config=scenario_config,
            percent_adoption=percent_adoption,
            engine=engine,
            attacker_asns=attacker_asns,
            victim_asns=victim_asns,
            adopting_asns=adopting_asns,
        )
        assert engine, "Need engine for customer cones"
        self.engine = engine


    @property
    def untracked_asns(self) -> frozenset[int]:
        adopters_customer_cone_asns: set[int] = set()

        for adopters_asn in self.adopting_asns:
            adopters_as_obj = self.engine.as_graph.as_dict[adopters_asn]
            if not adopters_as_obj.customer_cone_asns:
                continue
            # assert suppressor_as_obj.customer_cone_asns, "for mypy"
            adopters_customer_cone_asns.update(adopters_as_obj.customer_cone_asns)
        asns = set(self.engine.as_graph.as_dict)
        self._extra_untracked_asns = asns.difference(adopters_customer_cone_asns)
        return super().untracked_asns | self._extra_untracked_asns
