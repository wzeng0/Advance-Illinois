import PyPDF2 
from fpdf import FPDF
#Open sample pdf to replace text
pdf_file = PyPDF2.PdfReader(open('sample.pdf','rb'))
num_page = len(pdf_file.pages)
print(str(num_page))

page = pdf_file.pages[0]

text = page.extract_text()
text = text.replace("FY23","TEST")
print(text)

#create PDF object
pdf = FPDF()
#read text file
text2 = text.encode('utf-8').decode('latin-1')

#split text into pages
lines_per_page = 4000
text_pages = [text2[i:i+lines_per_page] for i in range(0, len(text2), lines_per_page)]

# Write text pages to PDF
pdf.set_font("Arial", size=12)
for text_page in text_pages:
    pdf.add_page()
    pdf.multi_cell(200, 10, txt=text_page, align="L")
 
# Save PDF
pdf.output("output_file.pdf", "F")