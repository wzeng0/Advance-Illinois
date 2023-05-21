import os
from fastapi import Response
from fpdf import FPDF
import pandas as pd
import io
from PyPDF2 import PdfMerger, PdfReader
import zipfile

class PDF(FPDF):
    """
    Class for representing PDF
    """
    def header(self):
        """
        Creates separate formatting for header
        """
        self.image('pdf_creation/samplepdf-image.png', x = 0, y = 0, w = 210, h = 297)
        self.add_font(family='Gotham', style='B', fname='pdf_creation/font/GothamBold.ttf', uni='DEPRECATED')
        self.set_font("Gotham", "B", 12)
        self.set_text_color(240, 86.5, 41)
        self.set_fill_color(255, 255, 255)
        self.set_line_width(0.01)
        width = self.get_string_width(self.title)
        self.set_xy(17.25, 41)
        # Creating a cell to help with positioning
        self.cell(
            width,
            9,
            self.title,
            border=0,
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
            fill=True,
        )
        self.ln(10)
        self.ln(10)
        self.ln(10)
        self.ln(5)

    def print_elements(self):
        """
        Prints header, background, and line breaks onto page
        """
        self.add_page()
        self.set_line_width(17.5)
        self.header()

#saving file locally
#pdf.output('{name}.pdf'.format(name=repname))

def second_page(pdf): 
    return io.BytesIO(pdf.output())

###Merge pages here

def final_pdf(repname, df):
    ###will replace with different variables when iterating through the dataframes
    # replst = ["ABDELNASSER RASHID1"]
    # df = pd.DataFrame(
    #     {  
    #         "SCHOOL DISTRICT": ["Jules", "Mary", "Carlson", "Lucas", "sample5", "sample6"],
    #         "ENROLLMENT": ["Smith", "Ramos", "Banks", "Cimon", "sample5", "sample6"],
    #         "% OF FULL FUNDING": ["4%", "67%", "70%", "85%", "92%", "121%"],
    #         "TOTAL GAP TO FULL FUNDING": ["San Juan", "Orlando", "Los Angeles", "Saint-Mahturin-sur-Loire", "sample5", "sample6"],
    #         "PER PUPIL GAP TO FULL FUNDING": ["San Juan", "Orlando", "Los Angeles", "Saint-Mahturin-sur-Loire", "sample5", "sample6"]
    #     }
    # )
        #repeats pdf creation
    # for repname in replst:
        #creates and prints pdf
    pdf = PDF(orientation = 'P', unit = 'mm', format = 'A4')
    pdf.set_title("REPRESENTATIVE {name}".format(name = repname))
    pdf.print_elements()
    pdf.set_auto_page_break(True, 40) #may need to turn background images into 
                                    #header and footer for this to work properly

    #TABLE#
    df = df.applymap(str)  # Convert all data inside dataframe into string type

    columns = [list(df)]  # Get list of dataframe columns                                                      
    rows = df.values.tolist()  # Get list of dataframe rows
    data = columns + rows  # Combine columns and rows in one list

    #gets col idx of % OF FULL FUNDING
    #using try and except to make sure value error doesn't break code?
    # print(columns[0].index(""))
    try:
        percent_col_idx = columns[0].index("% OF FULL \nFUNDING") 
    except ValueError as ve:
        print("must have column % OF FULL FUNDING")

    #add fonts
    pdf.add_font(family='GothamLight', style='', fname='pdf_creation/font/GothamLight.ttf', uni='DEPRECATED')
    pdf.add_font(family='GothamLight', style='B', fname='pdf_creation/font/GothamMedium.ttf', uni='DEPRECATED')
    #sets font type and size of table text
    pdf.set_font('GothamLight', '', 10)
    pdf.set_text_color(0, 0, 0)

    #constructing table, need to add more parameters
    with pdf.table(###find a way to adjust custom widths
                ###cell_fill_mode="ROWS",
                line_height=pdf.font_size * 1.5,
                text_align="CENTER",
                width=176) as table:

        for row_idx, data_row in enumerate(data):
            if 0 < row_idx:
                row_lst = rows[row_idx - 1] #attribute the row to next index
            row = table.row()
            for datum in data_row:
                #creating colors
                if 0 < row_idx:
                    #percent total funding as an integer
                    percent = float(row_lst[percent_col_idx][:-1]) 
                else:
                    percent = "moot"
                
                if percent != "moot": ### I know this is bad style so fix later
                    if percent < .6: 
                        pdf.set_fill_color(172, 41, 0)
                    elif .60 <= percent < .7:
                        pdf.set_fill_color(245, 131, 76)
                    elif .70 <= percent < .8:
                        pdf.set_fill_color(249, 173, 86)
                    elif .80 <= percent < .9:
                        pdf.set_fill_color(240, 199, 110)
                    elif .90 <= percent < 1.0:
                        pdf.set_fill_color(154, 198, 151)
                    else:
                        pdf.set_fill_color(86, 181, 168)
                
                row.cell(datum)
                    
                ###colors are a little sus so ill change them later
                ###also will need to change bg img

    IN_FILEPATH = "pdf_creation/FY_page_1.pdf"
    ON_PAGE_INDEX = 1  # Index at which the page will be inserted (starts at zero)

    merger = PdfMerger()
    merger.merge(position=0, fileobj=IN_FILEPATH)
    merger.merge(position=ON_PAGE_INDEX, fileobj=second_page(pdf))
    output_stream = io.BytesIO()
    # Below line was previously commented out
    merger.write(output_stream)
    output_stream.seek(0)
    #merger.write('{name}.pdf'.format(name=repname))
    return output_stream

def get_all_pdf_bytes(dict):
    bytes_lst = []
    names_lst = []
    for repname, df in dict.items():
        bytes_lst.append(final_pdf(repname, df))
        names_lst.append(repname)
    return (bytes_lst, names_lst)

def get_all_pdf(dict):
    (byte_list, name_list) = get_all_pdf_bytes(dict)
    zip_io = io.BytesIO()

    # Create a zip archive containing all the PDF files
    with zipfile.ZipFile(zip_io, "w") as zipf:
        for i, pdf_data in enumerate(byte_list):
            zipf.writestr(f"{name_list[i]}.pdf", pdf_data.getvalue())

    zip_io.seek(0)  # Seek back to the beginning of the BytesIO object
    return zip_io

'''
def generate_pdf(pdf_data, output_path):
    with open(output_path, "wb") as file: 
        file.write(pdf_data.getvalue()) 
'''