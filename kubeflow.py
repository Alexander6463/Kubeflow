import kfp
import kfp.components as comp

create_step_get_lines = comp.load_component_from_file('component.yaml')


def my_pipeline():
    get_lines_step = create_step_get_lines(
        input_1='minio://example/train.pdf'
        #input_1='http://10.98.26.56:9000/example/train.pdf',
        #output_1='minio://example/img',
        #output_2='minio://example/text',
    )

client = kfp.Client(host='http://127.0.0.1:8080')

client.create_run_from_pipeline_func(my_pipeline, arguments={})