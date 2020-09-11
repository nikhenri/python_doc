# -------------------------------------------------------------------------------------
#  Description:
# -------------------------------------------------------------------------------------
#  Author: Nik Henri
# -------------------------------------------------------------------------------------
import os
import sys
import subprocess


try:
    import docx
except ImportError:
    print("Installing 'docx' and 'docxtpl'")
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'docx'])
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'docxtpl'])
finally:
    import docx

# from docx.shared import RGBColor
# from docx.oxml.ns import nsdecls
# from docx.oxml import parse_xml
# from docx.oxml import OxmlElement
# from docx.oxml.ns import qn
# from docx.enum.dml import MSO_THEME_COLOR_INDEX


class GenDocx:
    # -------------------------------------------------------------------------------------
    def __init__(self):
        pass

    # -------------------------------------------------------------------------------------
    def generate(self, register_obj):
        document = docx.Document()
        sections = document.sections
        for section in sections:
            section.left_margin = docx.shared.Cm(2.0)
        document.save('simple.docx')


        os.startfile('simple.docx')