from datetime import datetime
from dataclasses import replace

from frozendict import frozendict

from bgpy.as_graphs import CAIDAASGraphConstructor
from bgpy.shared.constants import SINGLE_DAY_CACHE_DIR
from bgpy.simulation_framework import Simulation

class DebugASGraphConstructor(CAIDAASGraphConstructor):
    key_asn = 211909
    def _get_as_graph(self, as_graph_info):
        as_graph = super()._get_as_graph(as_graph_info)
        provider_cone_asns = as_graph.as_dict[self.key_asn].provider_cone_asns
        asns_to_keep = frozenset({self.key_asn}) | provider_cone_asns
        # customers_of_asns_to_keep = set()
        # for provider_cone_asn in asns_to_keep:
        #     as_obj = as_graph.as_dict[provider_cone_asn]
        #     for customer_asn in as_obj.customer_asns:
        #         customers_of_asns_to_keep.add(customer_asn)
        # asns_to_keep = asns_to_keep | customers_of_asns_to_keep
        peers_of_asns_to_keep = set()
        for provider_cone_asn in asns_to_keep:
            as_obj = as_graph.as_dict[provider_cone_asn]
            for i, peer_asn in enumerate(as_obj.peer_asns):
                peers_of_asns_to_keep.add(peer_asn)
                if i + 1 > 9:
                    break
        asns_to_keep = asns_to_keep | peers_of_asns_to_keep

        as_graph_info = replace(
            as_graph_info,
            peer_links=frozenset(
                [
                    x for x in as_graph_info.peer_links
                    if all(y in asns_to_keep for y in x.asns)
                ]
            ),
            customer_provider_links=frozenset(
                [
                    x for x in as_graph_info.customer_provider_links
                    if all(y in asns_to_keep for y in x.asns)
                ]
            ),
            unlinked_asns=frozenset(
                [
                    x for x in as_graph_info.unlinked_asns if x in asns_to_keep
                ]
            ),
            ixp_asns=frozenset(
                [
                    x for x in as_graph_info.ixp_asns if x in asns_to_keep
                ]
            ),
            input_clique_asns=frozenset(
                [
                    x for x in as_graph_info.input_clique_asns if x in asns_to_keep
                ]
            )
        )
        new_as_graph = super()._get_as_graph(as_graph_info)
        print(len(new_as_graph.as_dict))
        return new_as_graph


class RoSTSim(Simulation):
    """SimulationClass customized for Withdrawal Suppression sims"""

    def __init__(self, *args, **kwargs) -> None:
        kwargs["python_hash_seed"] = 0
        kwargs["ASGraphConstructorCls"] = DebugASGraphConstructor
        kwargs["as_graph_constructor_kwargs"] = frozendict(
            {
                "as_graph_collector_kwargs": frozendict(
                    {
                        "cache_dir": SINGLE_DAY_CACHE_DIR,
                        "dl_time": datetime(2024, 12, 11, 0, 0),
                    }
                ),
                "as_graph_kwargs": frozendict(
                    {
                        "store_customer_cone_size": True,
                        "store_customer_cone_asns": True,
                        "store_provider_cone_size": True,
                        "store_provider_cone_asns": True,
                    }
                )

            }
        )
        # Uncomment this if you're having RAM problems
        # total_cpus = cpu_count()
        # MAX_CPUS = 80
        # if total_cpus > MAX_CPUS:
        #     kwargs["parse_cpus"] = min(kwargs.get("parse_cpus", total_cpus), MAX_CPUS)
        super().__init__(*args, **kwargs)

    @property
    def default_sim_name(self) -> str:
        return "rost_sims"
