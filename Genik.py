# -------------------------------------------------------------------------------------
#  Description:
# -------------------------------------------------------------------------------------
#  Author: Nik Henri
# -------------------------------------------------------------------------------------
print("\nGenik @Nik\n")
# -------------------------------------------------------------------------------------
import sys
import os

import deserialzer
import register
import gen_docx

# -------------------------------------------------------------------------------------

FILENAME = "config.yaml"

sys.dont_write_bytecode = True  # Avoid the anoying *.pyc

# Change Working dir to script dir
path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
os.chdir(path)

print(f"")
### MAIN ###
print(f"Genik path: " + path)
print(f"Python path: " + sys.executable.replace('\\', '/') + f" (v{sys.version.split()[0]})")

print(f"Deserialzer {FILENAME}...")
dserialzer_obj = deserialzer.Deserialzer()
reg_dict = dserialzer_obj.deserialze(FILENAME)
print(f"Done!")

print(f"Validate config...")
register_obj = register.Register(reg_dict)
print(f"Done!")

print(f"Generate .docx...")
gen_docx_obj = gen_docx.GenDocx().generate(register_obj)
print(f"Done!")

#print(f"Generate .svh...")
#print(f"Done!")
#
#print(f"Generate .sv...")
#print(f"Done!")