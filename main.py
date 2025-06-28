import logging

from yaml_reader import YamlPipelineExecutor

def main() -> None:
    yamlExecutor = YamlPipelineExecutor('pipelines/wiki_yahoo_db_pipe.yaml')
    yamlExecutor.process_pipeline()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
