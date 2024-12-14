import random

from frozendict import frozendict

from bgpy.as_graphs import CAIDAASGraphConstructor
from bgpy.simulation_framework import ScenarioConfig
from withdrawal_suppression_eval.policies import (
    BGPAllowInvalidFull,
    DropWithdrawalsFull,
)
from withdrawal_suppression_eval.scenarios import VictimsPrefixWithdrawalScenario


def get_scenario_configs():
    bgp_dag = CAIDAASGraphConstructor(tsv_path=None).run()
    asns = tuple(bgp_dag.as_dict)

    def get_percentage_hardcoded_asn_cls_dict(percent):
        k = int(percent * len(asns))
        return frozendict({asn: DropWithdrawalsFull for asn in random.sample(asns, k)})

    one_tenth_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(
        0.001
    )
    one_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(0.01)
    five_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(0.05)

    return (
        ScenarioConfig(
            BasePolicyCls=BGPAllowInvalidFull,
            ScenarioCls=VictimsPrefixWithdrawalScenario,
            hardcoded_asn_cls_dict=one_tenth_percent_hardcoded_asn_cls_dict,
            scenario_label="0.1% Dropping Withdrawals",
        ),
        ScenarioConfig(
            BasePolicyCls=BGPAllowInvalidFull,
            ScenarioCls=VictimsPrefixWithdrawalScenario,
            hardcoded_asn_cls_dict=one_percent_hardcoded_asn_cls_dict,
            scenario_label="1% Dropping Withdrawals",
        ),
        ScenarioConfig(
            BasePolicyCls=BGPAllowInvalidFull,
            ScenarioCls=VictimsPrefixWithdrawalScenario,
            hardcoded_asn_cls_dict=five_percent_hardcoded_asn_cls_dict,
            scenario_label="5% Dropping Withdrawals",
        ),
    )
