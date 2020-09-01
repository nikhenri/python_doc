# pip install docx
# pip install docxtpl


from docx import Document
from docx.shared import RGBColor
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches

document = Document()

document.add_heading('Super Nik', 0)

# p = document.add_paragraph('A plain paragraph having some ')
# p.add_run('bold').bold = True
# p.add_run(' and some ')
# p.add_run('italic.').italic = True
#
# document.add_heading('Heading, level 1', level=1)
#
# document.add_paragraph('Intense quote', style='Intense Quote')
#
# document.add_paragraph(
#     'first item in unordered list', style='List Bullet'
# )
#
# document.add_paragraph(
#     'first item in ordered list', style='List Number'
# )

#document.add_picture('write-word-using-python.jpg', width=Inches(1.25))

#print(recordset[0]['id'])


#hdr_cells = table.rows[0].cells
#hdr_cells[0].text = 'Id'
#hdr_cells[1].text = 'Quantity'
#hdr_cells[2].text = 'Description'
#a = hdr_cells[2].add_paragraph("woof")
#r = a.add_run("tt")
#font = r.font
#font.highlight_color = WD_COLOR_INDEX.YELLOW



#r = a.add_run()
#
#for item in recordset:
	# #print(item)
	# row_cells = table.add_row().cells
	# row_cells[0].text = str(item['id'])
	# row_cells[1].text = str(item['qty'])
	# row_cells[2].text = str(item['desc'])

# -------------
def MarkIndexEntry(entry,paragraph):
    run = paragraph.add_run()
    r = run._r
    font = run.font
    font.color.rgb = RGBColor(255, 192, 0)
    fldChar = OxmlElement('w:fldChar')
    fldChar.set(qn('w:fldCharType'), 'begin')
    r.append(fldChar)

    run = paragraph.add_run()
    r = run._r
    font = run.font
    font.color.rgb = RGBColor(255, 192, 0)
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = ' XE "%s" '%(entry)
    r.append(instrText)

    run = paragraph.add_run()
    r = run._r
    font = run.font
    font.color.rgb = RGBColor(255, 192, 0)
    fldChar = OxmlElement('w:fldChar')
    fldChar.set(qn('w:fldCharType'), 'end')
    r.append(fldChar)

table = document.add_table(rows=1, cols=5)
#shading_elm_1 = parse_xml(r'<w:shd {} w:fill="d9d9d9"/>'.format(nsdecls('w')))
#table.rows[0].cells[0]._tc.get_or_add_tcPr().append(shading_elm_1)
shading_elm = []
for i in range(5):
    shading_elm.append(parse_xml(r'<w:shd {} w:fill="d9d9d9"/>'.format(nsdecls('w'))))
    table.rows[0].cells[i]._tc.get_or_add_tcPr().append(shading_elm[i])

table.style = 'Table Grid'
hdr_cells = table.rows[0].cells
hdr_cells[0].width = Cm(1.0)
hdr_cells[0].text = 'Bits'
hdr_cells[1].text = 'Field Name'
hdr_cells[2].text = 'Default Value'
hdr_cells[3].width = Cm(1.0)
hdr_cells[3].text = 'Type'
hdr_cells[4].width = Cm(7.0)
hdr_cells[4].text = 'Description'

row_cells = table.add_row().cells

# BITS
row_cells[0].width = Cm(1.0)
p = row_cells[0].paragraphs[0]
MarkIndexEntry("OtiRegField:Bits", p)
p.add_run("[31:0]")

# NAME
p = row_cells[1].paragraphs[0]
MarkIndexEntry("OtiRegField:Name", p)
p.add_run("IP_ADDR")
MarkIndexEntry("Oti", p)

# Default
p = row_cells[2].paragraphs[0]
MarkIndexEntry("OtiRegField:Default", p)
p.add_run("0x13356219")
MarkIndexEntry("Oti", p)

# Type
row_cells[3].width = Cm(1.0)
p = row_cells[3].paragraphs[0]
MarkIndexEntry("OtiRegField:Type", p)
p.add_run("RW")
MarkIndexEntry("Oti", p)


row_cells[4].width = Cm(7.0)
p = row_cells[4].paragraphs[0]
p.add_run("IP address of offload engine")



document.save('simple.docx')