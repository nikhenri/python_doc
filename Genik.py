# -------------------------------------------------------------------------------------
#  Description:
# -------------------------------------------------------------------------------------
#  Author: Nik Henri
# -------------------------------------------------------------------------------------
print("\nGenik @Nik\n")
# -------------------------------------------------------------------------------------
import sys


import os
import subprocess
import pathlib
import glob
import configparser
import zipfile
import shutil

import deserialzer
import register
import gen_docx
# import gen_tcl
# -------------------------------------------------------------------------------------
# Check version
MIN_PYTHON = (3, 6)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

# Change working dir to script dir
path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
os.chdir(path)

print(f"{pathlib.Path(__file__).name} path: " + path)
print(f"Python path: " + sys.executable.replace('\\', '/') + f" (v{sys.version.split()[0]})")

# -------------------------------------------------------------------------------------
reg_dict = {}
for filename in glob.glob('register/*.yaml'):
    print(f"Deserialzer {filename}...")
    reg_dict[pathlib.Path(filename).stem] = deserialzer.deserialze(filename)
    print(f"Done!")

# -------------------------------------------------------------------------------------
print(f"Validate ...")
full_reg_dict = register.get_register_dict(reg_dict)

# -------------------------------------------------------------------------------------
print(f"Clean ouput dir")
if os.path.isdir('output'):
    shutil.rmtree('output')
os.mkdir('output')

# -------------------------------------------------------------------------------------
print(f"Generate .docx")
if not os.path.isdir('output/doc'):
    os.mkdir('output/doc')
os.chdir("output/doc")
for module in full_reg_dict.keys():
    gen_docx.GenDocx(full_reg_dict[module]).generate(module, False)
# gen_docx.GenDocx(full_reg_dict["tcp_ip"]).generate("tcp_ip", True)
os.chdir("../../")
print(f"Done!")

# -------------------------------------------------------------------------------------
print(f"Generate docParser .xml & .ini...")
# .xml
for module in full_reg_dict.keys():
    with zipfile.ZipFile(f'output/doc/{module}.docx') as z:
        with open(f'output/{module}.xml', 'wb') as f:
            f.write(z.read('word/document.xml'))

# .ini
config = configparser.ConfigParser()
cfg_dict = {'OTI_BASE_ADD': f"{full_reg_dict['FX37']['ip']['tcp_ip']['addr']:08X}",
            'OTI_PORT_OFFSET': f"{full_reg_dict['FX37']['ip']['tcp_ip']['offset']:08X}",
            'OTI_NB_PORT': full_reg_dict['FX37']['ip']['tcp_ip']['nb'],
            }

for decoder in full_reg_dict['tcp_ip']['decoder'].keys():
    cfg_dict[f"OTI_{decoder.upper()}_BASE_ADD"] = f"0x{full_reg_dict['tcp_ip']['decoder'][decoder]['addr']:08X}"
config['DEFAULT'] = cfg_dict

with open('output/docParser.ini', 'w') as configfile:
    config.write(configfile)
print(f"Done!")

# -------------------------------------------------------------------------------------
print(f"Call docParser...")
os.chdir("output")
subprocess.check_call(["../docParser", "-c", "docParser.ini", "tcp_ip.xml", "docParser.txt"])
os.chdir("../")
print(f"Done!")
# -------------------------------------------------------------------------------------
print(f"Exit...")