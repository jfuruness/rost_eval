import logging
import time

from .sims import WithdrawalSuppressionSim, get_scenario_configs

logger = logging.getLogger("withdrawal_suppression_eval")
logger.setLevel(logging.INFO)


def main():
    """Runs the defaults"""

    start = time.perf_counter()
    sim = WithdrawalSuppressionSim(scenario_configs=get_scenario_configs())
    sim.run()
    logging.info(f"{time.perf_counter() - start}s for {sim.sim_name}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    logging.info(f"{time.perf_counter() - start}s for all sims")
