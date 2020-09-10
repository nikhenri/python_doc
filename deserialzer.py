# -------------------------------------------------------------------------------------
#  Description:
# -------------------------------------------------------------------------------------
#  Author: Nik Henri
# -------------------------------------------------------------------------------------
import pathlib


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
        try:
             import yaml
        except ImportError:
            print("Installing 'pyyaml'")
            import pip
            pip.main(['install', '--user', 'pyyaml'])
        finally:
             import yaml

        # read yaml
        with open(filename, 'r') as stream:
            data = yaml.load(stream, Loader=yaml.FullLoader)
            return data