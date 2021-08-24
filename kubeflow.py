import kfp
import kfp.components as comp

create_step_get_lines = comp.load_component_from_file('preprocess_component/component.yaml')
second_component=comp.load_component_from_file('second_component/component.yaml')


def my_pipeline():
    get_lines_step = create_step_get_lines(input_1='minio://example/example1.pdf')
                                           #output_1='minio://example/txt',
                                           #output_2='minio://example/images')
    print_file = second_component(input_1=get_lines_step.outputs['output_1'],
                                  input_2=get_lines_step.outputs['output_2'])
    print_file.execution_options.caching_strategy.max_cache_staleness = "P0D"






#client = kfp.Client(host='http://127.0.0.1:8080')
kfp.compiler.Compiler().compile(
    pipeline_func=my_pipeline,
    package_path='pipeline.yaml')

#client.create_run_from_pipeline_func(my_pipeline, arguments={})