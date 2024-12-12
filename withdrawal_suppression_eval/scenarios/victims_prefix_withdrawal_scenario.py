from bgpy.simulation_framework import VictimsPrefixScenario


class VictimsPrefixWithdrawalScenario(VictimsPrefixScenario):

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
                as_obj.policy.prep_withdrawal_for_next_propagation(
                    Prefixes.PREFIX.value
                )
