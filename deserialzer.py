# -------------------------------------------------------------------------------------
#  Description:
# -------------------------------------------------------------------------------------
#  Author: Nik Henri
# -------------------------------------------------------------------------------------
import pathlib
import sys
import subprocess
import yaml

class Deserialzer:
    # -------------------------------------------------------------------------------------
    def __init__(self):
        pass

    # -------------------------------------------------------------------------------------
    def deserialze(self, filename):
       ext = pathlib.Path(filename).suffix
       if ext == ".yaml" or ext == ".yml":
           return self._deserialze_yaml(filename)
       else:
           raise ValueError(ext)

    # -------------------------------------------------------------------------------------
    def _deserialze_yaml(self, filename):
        # Import install
        # try:
        #      import yaml
        # except ImportError:
        #     print("Installing 'pyyaml'")
        #     subprocess.check_call([sys.executable, "-m", "pip", "install", 'pyyaml'])
        # finally:
        #      import yaml

        # read yaml
        with open(filename, 'r') as stream:
            data = yaml.load(stream, Loader=yaml.FullLoader)
            return data