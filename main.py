import logging
import os

from yaml_reader import YamlPipelineExecutor

def main() -> None:
    pipeline_location = os.environ.get('PIPELINE_LOCATION')
    if pipeline_location is None:
        logging.error('pipeline location not defined "> source .env-local"')
        exit(1)
    yamlExecutor = YamlPipelineExecutor(pipeline_location)
    yamlExecutor.start()
    yamlExecutor.join()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
