import click
import logging
from kfp.components import InputPath, OutputPath
from minio import Minio
from pathlib import Path

LOGGER = logging.getLogger(__file__)

LOGGING_FORMAT = "[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s"
client = Minio("minio-service:9000", "minio", "minio123", secure=False)


def configure_logging():
    formatter = logging.Formatter(LOGGING_FORMAT)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(
        str(
            Path(__file__)
            .parent.parent.joinpath("python_logging.log")
            .absolute()
        )
    )
    file_handler.setFormatter(formatter)
    logging.root.setLevel(logging.DEBUG)
    logging.root.addHandler(console_handler)
    logging.root.addHandler(file_handler)


@click.command()
@click.option('--input-path-1')
@click.option('--input-path-2')
def run(input_path_1: InputPath(str),
        input_path_2: OutputPath(str)):
    LOGGER.info(f'input_path={input_path_1}, {input_path_2}')
    """objects = client.list_objects(input_path_1, recursive=True)
    for obj in objects:
        LOGGER.info(f'object={obj})')
    objects = client.list_objects(input_path_2, recursive=True)
    for obj in objects:
        LOGGER.info(f'object={obj})')"""


