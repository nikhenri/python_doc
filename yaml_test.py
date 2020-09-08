#pip install pyyaml

import subprocess
import sys

try:
    import yaml
except ImportError:
    print("yii")
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pyyaml'])
finally:
    import yaml

with open("config.yaml", 'r') as stream:
    try:
        #print(yaml.safe_load(stream))
        #a = yaml.load(stream)
        a= yaml.load(stream, Loader=yaml.FullLoader)
        pass
    except yaml.YAMLError as exc:
        print(exc)