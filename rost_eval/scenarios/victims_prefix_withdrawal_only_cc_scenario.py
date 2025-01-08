from typing import TYPE_CHECKING

from bgpy.shared.enums import SpecialPercentAdoptions
from bgpy.simulation_framework import ScenarioConfig

from .victims_prefix_withdrawal_scenario import VictimsPrefixWithdrawalScenario

if TYPE_CHECKING:
    from bgpy.simulation_engine import BaseSimulationEngine


class VictimsPrefixWithdrawalOnlyCCScenario(VictimsPrefixWithdrawalScenario):
    """Same as parent but only tracks attackers customer cone"""

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
        suppressor_customer_cone_asns: set[int] = set()
        for suppressor_asn in self.scenario_config.hardcoded_asn_cls_dict:
            suppressor_as_obj = engine.as_graph.as_dict[suppressor_asn]
            assert suppressor_as_obj.customer_cone_asns, "for mypy"
            suppressor_customer_cone_asns.update(suppressor_as_obj.customer_cone_asns)
        asns = set(engine.as_graph.as_dict)
        self._extra_untracked_asns = asns.difference(suppressor_customer_cone_asns)

    @property
    def untracked_asns(self) -> frozenset[int]:
        return super().untracked_asns | self._extra_untracked_asns
