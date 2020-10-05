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

import deserialzer
import register
import gen_docx

# -------------------------------------------------------------------------------------
MIN_PYTHON = (3, 6)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

FILENAME = "tcp_ip.yaml"
# FILENAME = "config.yaml"
FILENAME_NO_EXT = os.path.splitext(FILENAME)[0]

# Change Working dir to script dir
path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
os.chdir(path)

print(f"")
### MAIN ###
print(f"Genik path: " + path)
print(f"Python path: " + sys.executable.replace('\\', '/') + f" (v{sys.version.split()[0]})")

full_reg_dict = {}
for filename in glob.glob('*.yaml'):
    print(f"Deserialzer {filename}...")
    reg_dict = deserialzer.deserialze(filename)
    print(f"Validate ...")
    full_reg_dict[pathlib.Path(filename).stem] = register.get_register_dict(reg_dict)
    print(f"Done!")

print(f"Generate .docx...")
gen_docx_obj = gen_docx.GenDocx(full_reg_dict['tcp_ip']).generate(FILENAME_NO_EXT, True)
print(f"Done!")

subprocess.check_call(["docparser", "-c", "OTI_datasheet_parser.ini", f"{FILENAME_NO_EXT}.xml", "outputReg.txt"])

#print(f"Generate .svh...")
#print(f"Done!")
#
#print(f"Generate .sv...")
#print(f"Done!")