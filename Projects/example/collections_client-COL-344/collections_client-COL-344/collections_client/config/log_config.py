import logging


def init_logger():
    logging.getLogger('collections_client')
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d; %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
