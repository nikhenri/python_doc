#pip install pyyaml
import yaml

with open("config.yml", 'r') as stream:
    try:
        #print(yaml.safe_load(stream))
        #a = yaml.safe_load(stream)
        #a= yaml.load(stream, Loader=yaml.FullLoader)
        a = yaml.load(stream, default_flow_style=False)
        pass
    except yaml.YAMLError as exc:
        print(exc)