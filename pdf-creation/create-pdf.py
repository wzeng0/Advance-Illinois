from fpdf import FPDF
from fpdf.fonts import FontFaces
import pandas as pd

repname = "ABDELNASSER RASHID"
df = pd.DataFrame(
    {
        "First name": ["Jules", "Mary", "Carlson", "Lucas"],
        "Last name": ["Smith", "Ramos", "Banks", "Cimon"],
        "Age": [34, 45, 19, 31],
        "City": ["San Juan", "Orlando", "Los Angeles", "Saint-Mahturin-sur-Loire"],
    }
)

class PDF(FPDF):
    def header(self):
        title = "REPRESENTATIVE {name}".format(name = repname)
        self.add_font(family='Gotham', style='B', fname='pdf-creation/font/GothamBold.ttf', uni='DEPRECATED')
        self.set_font("Gotham", "B", 12)
        self.set_text_color(240, 86.5, 41)
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(255, 255, 255)
        self.set_line_width(1)
        width = self.get_string_width(title)
        self.set_xy(17.25, 41)
        # Printing page number
        self.cell(
            width,
            9,
            title,
            border=0,
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
            fill=True,
        )
    
    """
    def table_container(self, df):
        self.set_xy(17.25, 41)

        df = df.applymap(str)  # Convert all data inside dataframe into string type
        columns = [list(df)]  # Get list of dataframe columns
        rows = df.values.tolist()  # Get list of dataframe rows
        data = columns + rows  # Combine columns and rows in one list
        self.add_font(family='GothamLight', style='', fname='pdf-creation/font/GothamBold.ttf', uni='DEPRECATED')
        self.set_font('GothamLight', '', 12)
        self.set_text_color(0, 0, 0)
        
        with self.table(borders_layout="MINIMAL",
                       cell_fill_color=200,  # grey
                       cell_fill_mode="ROWS",
                       line_height=self.font_size * 2.5,
                       text_align="CENTER",
                       width=160) as table:
            for data_row in data:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

        #headings_style = FontFace(emphasis="BOLD", color=255, fill_color=(255, 100, 0))
    """

    def print_elements(self):
        self.add_page()
        self.image('pdf-creation/samplepdf-image.png', x = 0, y = 0, w = 210, h = 297)
        self.set_line_width(17.5)
        self.header()
        self.ln(10)
        self.ln(10)
        self.ln(10)
        self.ln(10)
        
pdf = PDF(orientation = 'P', unit = 'mm', format = 'A4')
pdf.print_elements()

df = df.applymap(str)  # Convert all data inside dataframe into string type

columns = [list(df)]  # Get list of dataframe columns
rows = df.values.tolist()  # Get list of dataframe rows
data = columns + rows  # Combine columns and rows in one list

pdf.add_font(family='GothamLight', style='', fname='pdf-creation/font/GothamLight.ttf', uni='DEPRECATED')
pdf.add_font(family='GothamLight', style='B', fname='pdf-creation/font/GothamMedium.ttf', uni='DEPRECATED')
pdf.set_font('GothamLight', '', 12)
pdf.set_text_color(0, 0, 0)
with pdf.table(borders_layout="MINIMAL",
               cell_fill_color=200,  # grey
               cell_fill_mode="ROWS",
               line_height=pdf.font_size * 2.5,
               text_align="CENTER",
               width=160) as table:
    for data_row in data:
        row = table.row()
        for datum in data_row:
            row.cell(datum)

pdf.output('{name}.pdf'.format(name=repname))

