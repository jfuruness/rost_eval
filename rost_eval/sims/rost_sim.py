from datetime import datetime
from dataclasses import replace
from pathlib import Path

from frozendict import frozendict

from bgpy.as_graphs import CAIDAASGraphConstructor
from bgpy.shared.constants import SINGLE_DAY_CACHE_DIR
from bgpy.simulation_framework import Simulation
from bgpy.utils.engine_runner.diagram import Diagram

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

        asns_to_remove = {
            13237,
            12779,
            8218,
            1120,
            3214,
            12637,
            50877,
            5398,
            5405,
            25394,
            1820,
            1101,
            1031,
            1103,
            137,
            999,
            6762,
            1299,
            9902,
            249,
            1257,
            3320,
            2914,
            250,
            #
            49289,
            1653,
            12874,
            173,
            9541,
            786,
            42,
            553,
            #
            8660,
            5392,
            2686,
            5713,
            297,
            286,
            101,
            #############################
            3216,
            1828,
            668,
            1836,
            1764,
            2854,
            1267,
            1241,
            112,
            766,
            57304,
            #
            209,
            702,
            703,
            #
            1239,
            701,
            #
            4455,
            #
            6939,
            #
            9002,
            852,
            #
            577,
            812,
            293,
            680,
            #
            983,
            2497,
            #
            559,
            #
            1221,

        }
        asns_to_keep = asns_to_keep.difference(asns_to_remove)

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

    def _collect_engine_run_data(
        self,
        engine,
        percent_adopt,
        trial: int,
        scenario,
        propagation_round: int,
        graph_data_aggregator,
    ) -> dict[int, dict[int, int]]:
        # Save all engine run info
        # The reason we aggregate info right now, instead of saving
        # the engine and doing it later, is because doing it all
        # in RAM is MUCH faster, and speed is important
        outcomes = self.ASGraphAnalyzerCls(
            engine=engine,
            scenario=scenario,
            data_plane_tracking=self.data_plane_tracking,
            control_plane_tracking=self.control_plane_tracking,
        ).analyze()

        graph_data_aggregator.aggregate_and_store_trial_data(
            engine=engine,
            percent_adopt=percent_adopt,
            trial=trial,
            scenario=scenario,
            propagation_round=propagation_round,
            outcomes=outcomes,
        )
        if propagation_round == 1:
            diagram_obj_ranks_mut = [
                list(x) for x in engine.as_graph.propagation_ranks
            ]
            diagram_ranks = tuple([tuple(x) for x in diagram_obj_ranks_mut])

            Diagram().generate_as_graph(
                engine=engine,
                scenario=scenario,
                traceback=outcomes[1],
                description="debug graph round 2",
                graph_data_aggregator=graph_data_aggregator,
                diagram_ranks=diagram_ranks,
                static_order=False,
                path=Path("/home/anon/Desktop/debug_graph.png"),
                view=True,
                dpi=100,
            )
        return outcomes

