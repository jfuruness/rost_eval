import logging
import time
from typing import Iterable

from bgpy.shared.enums import (
    ASGroups,
    InAdoptingASNs,
    Outcomes,
    Plane,
    SpecialPercentAdoptions,
)
from bgpy.simulation_framework.graph_data_aggregator.graph_category import GraphCategory
from rost_eval.scenarios import (
    VictimsPrefixWithdrawalOnlyCCScenario,
    VictimsPrefixWithdrawalScenario,
)

from .sims import RoSTSim, get_scenario_configs


def get_all_graph_categories() -> Iterable[GraphCategory]:
    """Returns all possible metric key combos"""

    for plane in [Plane.DATA, Plane.CTRL]:
        for as_group in [ASGroups.ALL_WOUT_IXPS]:
            for outcome in [x for x in Outcomes if x != Outcomes.UNDETERMINED]:
                for in_adopting_asns_enum in list(InAdoptingASNs):
                    yield GraphCategory(
                        plane=plane,
                        as_group=as_group,
                        outcome=outcome,
                        in_adopting_asns=in_adopting_asns_enum,
                    )


logger = logging.getLogger("rost_eval")
logger.setLevel(logging.INFO)


def main():
    """Runs the defaults"""

    start = time.perf_counter()
    for ScenarioCls in (
        VictimsPrefixWithdrawalOnlyCCScenario,
        VictimsPrefixWithdrawalScenario,
    ):
        sim = RoSTSim(
            percent_adoptions=(
                SpecialPercentAdoptions.ONLY_ONE,
                0.1,
                0.2,
                0.5,
                0.8,
                0.99,
            ),
            scenario_configs=get_scenario_configs(ScenarioCls=ScenarioCls),
            control_plane_tracking=True,
            graph_categories=tuple(get_all_graph_categories()),
            sim_name=ScenarioCls.__name__,
        )
        sim.run()
    logging.info(f"{time.perf_counter() - start}s for {sim.sim_name}")


if __name__ == "__main__":
    # logger.info("26m for 100 trials on 10 cores")
    start = time.perf_counter()
    main()
    logging.info(f"{time.perf_counter() - start}s for all sims")
