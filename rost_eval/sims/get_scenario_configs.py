import random

from frozendict import frozendict

from bgpy.as_graphs import CAIDAASGraphConstructor
from bgpy.shared.enums import ASGroups
from bgpy.simulation_engine import (
    BGPFullIgnoreInvalid,
    BGPFullSuppressWithdrawals,
    RoSTFull,
)
from bgpy.simulation_framework import ScenarioConfig
from rost_eval.scenarios import VictimsPrefixWithdrawalScenario


def get_scenario_configs():
    bgp_dag = CAIDAASGraphConstructor(tsv_path=None).run()
    asns = tuple(bgp_dag.as_dict)

    one_t1_hardcoded_asn_cls_dict = frozendict(
        {  # type: ignore
            asn: BGPFullSuppressWithdrawals
            for asn in random.sample(
                bgp_dag.asn_groups[ASGroups.INPUT_CLIQUE.value],
                1,  # type: ignore
            )
        }
    )

    def get_percentage_hardcoded_asn_cls_dict(percent):
        k = int(percent * len(asns))
        return frozendict(
            {asn: BGPFullSuppressWithdrawals for asn in random.sample(asns, k)}
        )

    one_tenth_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(
        0.001
    )
    one_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(0.01)
    five_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(0.05)
    # twenty_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(0.2)
    # hundred_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(1)

    return (
        # ScenarioConfig(
        #     BasePolicyCls=BGPFull,
        #     ScenarioCls=VictimsPrefixWithdrawalScenario,
        #     scenario_label="0% Dropping Withdrawals (No RoST)",
        # ),
        # ScenarioConfig(
        #     BasePolicyCls=BGPFullIgnoreInvalid,
        #     AdoptPolicyCls=RoSTFull,
        #     ScenarioCls=VictimsPrefixWithdrawalScenario,
        #     scenario_label="0% Dropping Withdrawals",
        # ),
        ScenarioConfig(
            BasePolicyCls=BGPFullIgnoreInvalid,
            AdoptPolicyCls=RoSTFull,
            ScenarioCls=VictimsPrefixWithdrawalScenario,
            hardcoded_asn_cls_dict=one_t1_hardcoded_asn_cls_dict,
            scenario_label="1 Tier-1 AS",
        ),
        ScenarioConfig(
            BasePolicyCls=BGPFullIgnoreInvalid,
            AdoptPolicyCls=RoSTFull,
            ScenarioCls=VictimsPrefixWithdrawalScenario,
            hardcoded_asn_cls_dict=one_tenth_percent_hardcoded_asn_cls_dict,
            scenario_label="0.1% Dropping Withdrawals",
        ),
        ScenarioConfig(
            BasePolicyCls=BGPFullIgnoreInvalid,
            AdoptPolicyCls=RoSTFull,
            ScenarioCls=VictimsPrefixWithdrawalScenario,
            hardcoded_asn_cls_dict=one_percent_hardcoded_asn_cls_dict,
            scenario_label="1% Dropping Withdrawals",
        ),
        ScenarioConfig(
            BasePolicyCls=BGPFullIgnoreInvalid,
            AdoptPolicyCls=RoSTFull,
            ScenarioCls=VictimsPrefixWithdrawalScenario,
            hardcoded_asn_cls_dict=five_percent_hardcoded_asn_cls_dict,
            scenario_label="5% Dropping Withdrawals",
        ),
        # ScenarioConfig(
        #     BasePolicyCls=BGPFullIgnoreInvalid,
        #     AdoptPolicyCls=RoSTFull,
        #     ScenarioCls=VictimsPrefixWithdrawalScenario,
        #     hardcoded_asn_cls_dict=twenty_percent_hardcoded_asn_cls_dict,
        #     scenario_label="20% Dropping Withdrawals",
        # ),
        # ScenarioConfig(
        #     BasePolicyCls=BGPFullIgnoreInvalid,
        #     ScenarioCls=VictimsPrefixWithdrawalScenario,
        #     hardcoded_asn_cls_dict=hundred_percent_hardcoded_asn_cls_dict,
        #     scenario_label="100% Dropping Withdrawals, no RoST",
        # ),
    )
