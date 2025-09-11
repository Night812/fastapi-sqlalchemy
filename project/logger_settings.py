import logging
import sys


formatter = logging.Formatter(
    fmt="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
file_handler = logging.FileHandler("logs/logs.log")
stream_handler = logging.StreamHandler(sys.stdout)

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)


def configure_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
    )
