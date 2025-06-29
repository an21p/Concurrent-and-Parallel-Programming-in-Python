import yaml

with open('pipelines/wiki_yahoo_db_pipe.yaml', 'r') as f:
    yaml_data = yaml.safe_load(f)
    print(yaml_data)
