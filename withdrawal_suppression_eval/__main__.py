import logging
import time

from .sims import SIMS_TO_RUN

logger = logging.getLogger("withdrawal_suppression_eval")
logger.setLevel(logging.INFO)

def main():
    """Runs the defaults"""

    for sim in SIMS_TO_RUN:
        start = time.perf_counter()
        sim.run()
        logging.info(f"{time.perf_counter() - start}s for {sim.sim_name}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    logging.info(f"{time.perf_counter() - start}s for all sims")
