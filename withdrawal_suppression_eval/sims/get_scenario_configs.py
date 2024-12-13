import random

from frozendict import frozendict

from bgpy.as_graphs import CAIDAASGraphConstructor
from bgpy.simulation_engine import BGPFull
from bgpy.simulation_framework import ScenarioConfig
from withdrawal_suppression_eval.policies import DropWithdrawalsFull
from withdrawal_suppression_eval.scenarios import VictimsPrefixWithdrawalScenario


def get_scenario_configs():
    bgp_dag = CAIDAASGraphConstructor(tsv_path=None).run()
    asns = tuple(bgp_dag.as_dict)

    def get_percentage_hardcoded_asn_cls_dict(percent):
        k = int(percent * len(asns))
        return frozendict({asn: DropWithdrawalsFull for asn in random.sample(asns, k)})

    five_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(0.05)
    ten_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(0.1)
    twenty_percent_hardcoded_asn_cls_dict = get_percentage_hardcoded_asn_cls_dict(0.2)

    return (
        ScenarioConfig(
            BasePolicyCls=BGPFull,
            ScenarioCls=VictimsPrefixWithdrawalScenario,
            hardcoded_asn_cls_dict=five_percent_hardcoded_asn_cls_dict,
            scenario_label="5% Dropping Withdrawals",
        ),
        ScenarioConfig(
            BasePolicyCls=BGPFull,
            ScenarioCls=VictimsPrefixWithdrawalScenario,
            hardcoded_asn_cls_dict=ten_percent_hardcoded_asn_cls_dict,
            scenario_label="10% Dropping Withdrawals",
        ),
        ScenarioConfig(
            BasePolicyCls=BGPFull,
            ScenarioCls=VictimsPrefixWithdrawalScenario,
            hardcoded_asn_cls_dict=twenty_percent_hardcoded_asn_cls_dict,
            scenario_label="20% Dropping Withdrawals",
        ),
    )
