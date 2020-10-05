# -------------------------------------------------------------------------------------
#  Description:
# -------------------------------------------------------------------------------------
#  Author: Nik Henri
# -------------------------------------------------------------------------------------
import pathlib
import sys
import subprocess


# -------------------------------------------------------------------------------------
def deserialze(filename):
   ext = pathlib.Path(filename).suffix
   if ext == ".yaml" or ext == ".yml":
       return deserialze_yaml(filename)
   else:
       raise ValueError(ext)


# -------------------------------------------------------------------------------------
def deserialze_yaml(filename):
    # Import install
    try:
         import yaml
    except ImportError:
        print("Installing 'pyyaml'")
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'pyyaml'])
    finally:
         import yaml

    # read yaml
    with open(filename, 'r') as stream:
        data = yaml.load(stream, Loader=yaml.FullLoader)
        return data
