# -------------------------------------------------------------------------------------
#  Description:
# -------------------------------------------------------------------------------------
#  Author: Nik Henri
# -------------------------------------------------------------------------------------
import os
import sys
import subprocess
import re

try:
    import docx
except ImportError:
    print("Installing 'docx' and 'docxtpl'")
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'docx'])
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'docxtpl'])
finally:
    import docx

from docx.shared import Cm
from docx.enum.dml import MSO_THEME_COLOR_INDEX
from docx.oxml import OxmlElement
#from docx.oxml.ns import qn

# -------------------------------------------------------------------------------------


class GenDocx:
    DOC_PARSER_CAPTION = 1

    # -------------------------------------------------------------------------------------
    def __init__(self, register_obj):
        self.register_obj = register_obj
        self.document = None

    # -------------------------------------------------------------------------------------
    def generate(self, filename, open_generate_file=False):
        self.document = docx.Document()
        sections = self.document.sections
        for section in sections:
            section.left_margin = Cm(2.0)

        for ip in self.register_obj.get_ip_list():
            self.add_ip_docmentation(ip)

        self.document.save(f'{filename}.docx')
        if open_generate_file:
            os.startfile(f'{filename}.docx')

    # -------------------------------------------------------------------------------------
    def add_ip_docmentation(self, ip):
        self.add_summary_table(ip)
        self.add_register_table(ip)

    # -------------------------------------------------------------------------------------
    def add_summary_table(self, ip):
        print(f"Generate summary table for '{ip}'")
        self.add_summary_table_title(ip)
        self.add_summary_table_content(ip)
        self.document.add_paragraph()

    # -------------------------------------------------------------------------------------
    def add_register_table(self, ip):
        for addr in self.register_obj.get_ip_addr_list(ip):
            print(f"Generate register table for '{ip}' of addr '{addr}'")
            self.add_register_table_title(ip, addr)
            self.add_register_table_content(ip, addr)
            self.document.add_paragraph()

    # -------------------------------------------------------------------------------------
    def add_register_table_title(self, ip, addr):
        paragraph = self.add_summary_table_title(ip)
        # paragraph.paragraph_format.left_indent = -Cm(0.25)
        paragraph.add_run(': ')
        self.markindexentry("OtiRegister:Name", paragraph)
        paragraph.add_run(f'{self.register_obj.get_ip_addr_name(ip, addr)} (')
        self.markindexentry(f"OtiBaseAddress:{self.register_obj.get_ip_docParser_base_str(ip)}", paragraph)
        self.markindexentry("OtiRegister:Addr", paragraph)
        paragraph.add_run(f'0x{addr:04X}')
        self.markindexentry("OtiRegister:AddrEnd", paragraph)
        paragraph.add_run(')')
        self.add_bookmark(paragraph=paragraph, bookmark_text="", bookmark_name=self.register_obj.get_ip_addr_name(ip, addr))

    # -------------------------------------------------------------------------------------
    def add_register_table_content(self, ip, addr):
        table = self.document.add_table(rows=1, cols=5)
        # table.left_margin  = Cm(2.25)
        shading_elm = []
        for i in range(5):  # bg in gray
            shading_elm.append(docx.oxml.parse_xml(r'<w:shd {} w:fill="d9d9d9"/>'.format(docx.oxml.ns.nsdecls('w'))))
            table.rows[0].cells[i]._tc.get_or_add_tcPr().append(shading_elm[i])

        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].width = Cm(1.0)
        hdr_cells[0].text = 'Bits'
        hdr_cells[1].text = 'Field Name'
        hdr_cells[2].text = 'Default Value'
        hdr_cells[3].width = Cm(1.0)
        hdr_cells[3].text = 'Type'
        hdr_cells[4].width = Cm(9.0)
        hdr_cells[4].text = 'Description'
        # for field in sorted(self.register_obj.get_ip_addr_field_list(ip, addr), key=lambda item: int(re.search(r"[0-9]+", item).group()), reverse=True):
        for field in sorted(self.register_obj.get_ip_addr_field_list(ip, addr)):
            row_cells = table.add_row().cells

            # BITS
            row_cells[0].width = Cm(1.0)
            p = row_cells[0].paragraphs[0]
            self.markindexentry("OtiRegField:Bits", p)
            p.add_run(f"[{str(field).replace('-',':')}]")

            # NAME
            p = row_cells[1].paragraphs[0]
            self.markindexentry("OtiRegField:Name", p)
            p.add_run(self.register_obj.get_ip_addr_field_name(ip, addr, field))
            self.markindexentry("Oti", p)

            # Default
            p = row_cells[2].paragraphs[0]
            self.markindexentry("OtiRegField:Default", p)
            p.add_run(self.register_obj.get_ip_addr_field_reset(ip, addr, field))
            self.markindexentry("Oti", p)

            # Type
            row_cells[3].width = Cm(1.0)
            p = row_cells[3].paragraphs[0]
            self.markindexentry("OtiRegField:Type", p)
            p.add_run(self.register_obj.get_ip_addr_field_type(ip, addr, field))
            self.markindexentry("Oti", p)

            row_cells[4].width = Cm(9.0)
            p = row_cells[4].paragraphs[0]
            p.add_run(self.register_obj.get_ip_addr_field_desc(ip, addr, field))

    # -------------------------------------------------------------------------------------
    def add_summary_table_title(self, ip, include_chapter_nb=False):
        # Create a paragraph
        paragraph = self.document.add_paragraph('Table ', style='Caption')
        paragraph.paragraph_format.left_indent = -Cm(0.25)

        # create a caption with text
        caption_list = [' STYLEREF 1 \s', ' SEQ Table \* ARABIC'] if include_chapter_nb else [' SEQ Table \* ARABIC']
        run = paragraph.add_run()
        r = run._r
        for caption in caption_list:
            fldchar = docx.oxml.OxmlElement('w:fldchar')
            fldchar.set(docx.oxml.ns.qn('w:fldcharType'), 'begin')
            r.append(fldchar)
            instrtext = docx.oxml.OxmlElement('w:instrtext')
            instrtext.text = caption
            r.append(instrtext)
            fldchar = docx.oxml.OxmlElement('w:fldchar')
            fldchar.set(docx.oxml.ns.qn('w:fldcharType'), 'end')
            r.append(fldchar)

            if include_chapter_nb:
                paragraph.add_run("-")

        paragraph.add_run(f': {ip} register set')
        return paragraph
    
    # -------------------------------------------------------------------------------------
    def add_summary_table_content(self, ip):
        table = self.document.add_table(rows=1, cols=3)
        shading_elm = []
        for i in range(len(table.columns)):  # put the background gray for the 1er row
            shading_elm.append(docx.oxml.parse_xml(r'<w:shd {} w:fill="d9d9d9"/>'.format(docx.oxml.ns.nsdecls('w'))))
            table.rows[0].cells[i]._tc.get_or_add_tcPr().append(shading_elm[i])

        table.style = 'Table Grid'  # add border
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Address (Hex)'
        hdr_cells[0].width = Cm(4.0)
        hdr_cells[1].text = 'Type'
        hdr_cells[1].width = Cm(1.0)
        hdr_cells[2].text = 'Name'
        hdr_cells[2].width = Cm(19.0)

        for addr in self.register_obj.get_ip_addr_list(ip):
            row_cells = table.add_row().cells
            row_cells[0].text = f'0x{addr:X}'
            row_cells[0].width = Cm(4.0)
            row_cells[1].text = self.register_obj.get_ip_addr_type(ip, addr)
            row_cells[1].width = Cm(1.0)
            reg_name = self.register_obj.get_ip_addr_name(ip, addr)
            self.add_link(paragraph=row_cells[2].paragraphs[0], link_to=reg_name, text=reg_name, tool_tip=reg_name)
            row_cells[2].width = Cm(19.0)

    # -------------------------------------------------------------------------------------
    @staticmethod
    def markindexentry(entry, paragraph):
        run = paragraph.add_run()
        r = run._r
        font = run.font
        font.color.rgb = docx.shared.RGBColor(255, 192, 0)
        fldChar = docx.oxml.OxmlElement('w:fldChar')
        fldChar.set(docx.oxml.ns.qn('w:fldCharType'), 'begin')
        r.append(fldChar)

        run = paragraph.add_run()
        r = run._r
        font = run.font
        font.color.rgb = docx.shared.RGBColor(255, 192, 0)
        instrText = docx.oxml.OxmlElement('w:instrText')
        instrText.set(docx.oxml.ns.qn('xml:space'), 'preserve')
        instrText.text = ' XE "%s" ' % (entry)
        r.append(instrText)

        run = paragraph.add_run()
        r = run._r
        font = run.font
        font.color.rgb = docx.shared.RGBColor(255, 192, 0)
        fldChar = docx.oxml.OxmlElement('w:fldChar')
        fldChar.set(docx.oxml.ns.qn('w:fldCharType'), 'end')
        r.append(fldChar)

    # -------------------------------------------------------------------------------------
    @staticmethod
    def add_bookmark(paragraph, bookmark_text, bookmark_name):
        run = paragraph.add_run()
        tag = run._r
        start = docx.oxml.OxmlElement('w:bookmarkStart')
        start.set(docx.oxml.ns.qn('w:id'), '0')
        start.set(docx.oxml.ns.qn('w:name'), bookmark_name)
        tag.append(start)

        text = docx.oxml.OxmlElement('w:r')
        text.text = bookmark_text
        tag.append(text)

        end = docx.oxml.OxmlElement('w:bookmarkEnd')
        end.set(docx.oxml.ns.qn('w:id'), '0')
        end.set(docx.oxml.ns.qn('w:name'), bookmark_name)
        tag.append(end)

    # -------------------------------------------------------------------------------------
    @staticmethod
    def add_link(paragraph, link_to, text, tool_tip=None):
        # create hyperlink node
        hyperlink = docx.oxml.shared.OxmlElement('w:hyperlink')

        # set attribute for link to bookmark
        hyperlink.set(docx.oxml.shared.qn('w:anchor'), link_to, )

        if tool_tip is not None:
            # set attribute for link to bookmark
            hyperlink.set(docx.oxml.shared.qn('w:tooltip'), tool_tip, )

        new_run = docx.oxml.shared.OxmlElement('w:r')
        rpr = docx.oxml.shared.OxmlElement('w:rPr')
        new_run.append(rpr)
        new_run.text = text
        hyperlink.append(new_run)
        r = paragraph.add_run()
        r._r.append(hyperlink)
        # r.font.name = "Calibri"
        r.font.color.theme_color = MSO_THEME_COLOR_INDEX.HYPERLINK
        # r.font.underline = True
    # -------------------------------------------------------------------------------------
