import click
import logging
import os
import sys
from pathlib import Path
from minio import Minio

from pdf_preprocesser import preprocess
from kfp.components import InputPath, OutputPath

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
@click.option('--input-path')
@click.option('--output-images-path')
@click.option('--output-text-path')
def run(input_path: InputPath(str),
        output_images_path: OutputPath(str),
        output_text_path: OutputPath(str)):
    LOGGER.info(f'Input variables {input_path}, '
                f'{output_images_path}, {output_text_path}')
    extension = os.path.splitext(input_path)[-1].lower()
    if extension == ".pdf":
        LOGGER.info(f'Run pdf preprocess on file {input_path} with result dir images - '
                    f'{output_images_path}'
                    f' and result dir text - {output_text_path}')
        bucket, file_path = input_path.lstrip('minio://').split('/', maxsplit=1)
        file_name = str(file_path.split('/')[-1])
        client.fget_object(bucket, file_path, file_name)
        preprocess(Path(file_name), Path(output_images_path), Path(output_text_path))
    else:
        raise ValueError(f"Not supported file format {input_path}, "
                         f"{output_images_path}, {output_text_path}")


if __name__ == '__main__':
    configure_logging()
    run()
