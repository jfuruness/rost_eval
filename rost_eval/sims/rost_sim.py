from datetime import datetime

from frozendict import frozendict

from bgpy.shared.constants import SINGLE_DAY_CACHE_DIR
from bgpy.simulation_framework import Simulation


class RoSTSim(Simulation):
    """SimulationClass customized for Withdrawal Suppression sims"""

    def __init__(self, *args, **kwargs) -> None:
        kwargs["python_hash_seed"] = 0
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
                        # When no ASNs are stored, .9gb/core
                        # When one set of cones is stored, 1.6gb/core
                        # When both sets of cones are stored, 2.3gb/core
                        # Unfortunately, we need both, since we use BGP-iSec
                        # and also use customer cones for ASRA
                        "store_customer_cone_size": True,
                        "store_customer_cone_asns": True,
                        "store_provider_cone_size": False,
                        "store_provider_cone_asns": False,
                    }
                ),
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
