# import random

from frozendict import frozendict

from bgpy.as_graphs import CAIDAASGraphConstructor
from bgpy.shared.enums import ASGroups
from bgpy.simulation_engine import (
    BGPFullIgnoreInvalid,
    BGPFullSuppressWithdrawals,
    RoSTFull,
)
from bgpy.simulation_framework import ScenarioConfig
from rost_eval.scenarios import (
    VictimsPrefixWithdrawalOnlyCCScenario,
    # VictimsPrefixWithdrawalScenario,
)


def get_scenario_configs():
    bgp_dag = CAIDAASGraphConstructor(tsv_path=None).run()
    tier_1_ases = bgp_dag.as_groups[ASGroups.INPUT_CLIQUE.value]
    tier_1_ases = sorted(tier_1_ases, key=lambda x: x.customer_cone_size, reverse=True)
    hardcoded_asn_dicts = [
        (frozendict({x.asn: BGPFullSuppressWithdrawals}), f"{x.asn} suppressing")
        for x in tier_1_ases[:5]
    ]

    return [
        ScenarioConfig(
            BasePolicyCls=BGPFullIgnoreInvalid,
            AdoptPolicyCls=RoSTFull,
            ScenarioCls=VictimsPrefixWithdrawalOnlyCCScenario,
            hardcoded_asn_cls_dict=hardcoded_list,
            scenario_label=label,
        )
        for hardcoded_list, label in hardcoded_asn_dicts
    ]


    # asns = tuple(bgp_dag.as_dict)

    # one_t1_hardcoded_asn_cls_dict = frozendict(
    #     {
    #         asn: BGPFullSuppressWithdrawals
    #         for asn in random.sample(
    #             bgp_dag.asn_groups[ASGroups.INPUT_CLIQUE.value],
    #             1,
    #         )
    #     }
    # )

    # def get_percentage_hardcoded_asn_cls_dict(percent):
    #     k = int(percent * len(asns))
    #     return frozendict(
    #         {asn: BGPFullSuppressWithdrawals for asn in random.sample(asns, k)}
    #     )

    # one_tenth_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(
    #     0.001
    # )
    # one_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(0.01)
    # five_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(0.05)
    # twenty_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(0.2)
    # hundred_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(1)

    # def get_asns_hardcoded_asn_cls_dict(asns):
    #     return frozendict({asn: BGPFullSuppressWithdrawals for asn in asns})

    # peers_1 = get_asns_hardcoded_asn_cls_dict(
    #     [749, 14618, 36935, 12880, 46690, 36937, 17858, 37069, 11003, 3378]
    # )
    # peers_5 = get_asns_hardcoded_asn_cls_dict(
    #     [9808, 54574, 6713, 1659, 36925, 4249, 14962, 3561, 2764, 37075]
    # )
    # peers_10 = get_asns_hardcoded_asn_cls_dict(
    #     [55836, 7303, 9824, 47377, 2116, 37457, 8167, 36914, 12302, 12455]
    # )
    # peers_25 = get_asns_hardcoded_asn_cls_dict(
    #     [132825, 7539, 37168, 13489, 2828, 26599, 13094, 30990, 2381, 45543]
    # )
    # peers_50 = get_asns_hardcoded_asn_cls_dict(
    #     [4862, 29063, 135607, 12727, 25593, 42845, 39605, 198335, 207456, 62512]
    # )
    # peers_100 = get_asns_hardcoded_asn_cls_dict(
    #     [293, 36874, 2818, 8823, 35000, 31727, 39560, 58291, 61098, 196968]
    # )
    # peers_labels = [f"{x} peers" for x in (1, 5, 10, 25, 50, 100)]
    # hardcoded_peers_list = [peers_1, peers_5, peers_10, peers_25, peers_50, peers_100]

    # return (
    #     # ScenarioConfig(
    #     #     BasePolicyCls=BGPFull,
    #     #     ScenarioCls=VictimsPrefixWithdrawalScenario,
    #     #     scenario_label="0% Dropping Withdrawals (No RoST)",
    #     # ),
    #     # ScenarioConfig(
    #     #     BasePolicyCls=BGPFullIgnoreInvalid,
    #     #     AdoptPolicyCls=RoSTFull,
    #     #     ScenarioCls=VictimsPrefixWithdrawalScenario,
    #     #     scenario_label="0% Dropping Withdrawals",
    #     # ),
    #     # ScenarioConfig(
    #     #     BasePolicyCls=BGPFullIgnoreInvalid,
    #     #     AdoptPolicyCls=RoSTFull,
    #     #     ScenarioCls=VictimsPrefixWithdrawalOnlyCCScenario,
    #     #     hardcoded_asn_cls_dict=one_t1_hardcoded_asn_cls_dict,
    #     #     scenario_label="1 Tier-1 AS (only customer cone)",
    #     # ),
    #     # ScenarioConfig(
    #     #     BasePolicyCls=BGPFullIgnoreInvalid,
    #     #     AdoptPolicyCls=RoSTFull,
    #     #     ScenarioCls=VictimsPrefixWithdrawalScenario,
    #     #     hardcoded_asn_cls_dict=one_t1_hardcoded_asn_cls_dict,
    #     #     scenario_label="1 Tier-1 AS",
    #     # ),
    #     # ScenarioConfig(
    #     #     BasePolicyCls=BGPFullIgnoreInvalid,
    #     #     AdoptPolicyCls=RoSTFull,
    #     #     ScenarioCls=VictimsPrefixWithdrawalScenario,
    #     #     hardcoded_asn_cls_dict=one_tenth_percent_hardcoded_asn_cls_dict,
    #     #     scenario_label="0.1% Dropping Withdrawals",
    #     # ),
    #     # ScenarioConfig(
    #     #     BasePolicyCls=BGPFullIgnoreInvalid,
    #     #     AdoptPolicyCls=RoSTFull,
    #     #     ScenarioCls=VictimsPrefixWithdrawalScenario,
    #     #     hardcoded_asn_cls_dict=one_percent_hardcoded_asn_cls_dict,
    #     #     scenario_label="1% Dropping Withdrawals",
    #     # ),
    #     # ScenarioConfig(
    #     #     BasePolicyCls=BGPFullIgnoreInvalid,
    #     #     AdoptPolicyCls=RoSTFull,
    #     #     ScenarioCls=VictimsPrefixWithdrawalScenario,
    #     #     hardcoded_asn_cls_dict=five_percent_hardcoded_asn_cls_dict,
    #     #     scenario_label="5% Dropping Withdrawals",
    #     # ),
    #     #####################################################################
    #     # ScenarioConfig(
    #     #     BasePolicyCls=BGPFullIgnoreInvalid,
    #     #     AdoptPolicyCls=RoSTFull,
    #     #     ScenarioCls=VictimsPrefixWithdrawalScenario,
    #     #     hardcoded_asn_cls_dict=twenty_percent_hardcoded_asn_cls_dict,
    #     #     scenario_label="20% Dropping Withdrawals",
    #     # ),
    #     # ScenarioConfig(
    #     #     BasePolicyCls=BGPFullIgnoreInvalid,
    #     #     ScenarioCls=VictimsPrefixWithdrawalScenario,
    #     #     hardcoded_asn_cls_dict=hundred_percent_hardcoded_asn_cls_dict,
    #     #     scenario_label="100% Dropping Withdrawals, no RoST",
    #     # ),
    # )
