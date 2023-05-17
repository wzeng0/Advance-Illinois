from fpdf import FPDF
import pandas as pd

###include first page

###will replace with different variables when iterating through the dataframes
repname = "ABDELNASSER RASHID" 
df = pd.DataFrame(
    {
        "SCHOOL DISTRICT": ["Jules", "Mary", "Carlson", "Lucas"],
        "ENROLLMENT": ["Smith", "Ramos", "Banks", "Cimon"],
        "% OF FULL FUNDING": ["34%", "45%", "19%", "31%"],
        "TOTAL GAP TO FULL FUNDING": ["San Juan", "Orlando", "Los Angeles", "Saint-Mahturin-sur-Loire"],
        "PER PUPIL GAP TO FULL FUNDING": ["San Juan", "Orlando", "Los Angeles", "Saint-Mahturin-sur-Loire"]
    }
)


class PDF(FPDF):
    """
    Class for representing PDF
    """
    def header(self):
        """
        Creates separate formatting for header
        """
        title = "REPRESENTATIVE {name}".format(name = repname) ###take out of class / add parameter
        self.add_font(family='Gotham', style='B', fname='pdf-creation/font/GothamBold.ttf', uni='DEPRECATED')
        self.set_font("Gotham", "B", 12)
        self.set_text_color(240, 86.5, 41)
        self.set_fill_color(255, 255, 255)
        #no clue why but this also sets the borders of the table
        self.set_line_width(0.01)
        width = self.get_string_width(title)
        self.set_xy(17.25, 41)
        # Creating a cell to help with positioning
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
        """
        Prints header, background, and line breaks onto page
        """
        self.add_page()
        self.image('pdf-creation/samplepdf-image.png', x = 0, y = 0, w = 210, h = 297)
        self.set_line_width(17.5)
        self.header()
        ###these may be unnecessary if we create separate image for header
        self.ln(10)
        self.ln(10)
        self.ln(10)
        self.ln(5)

#creates and prints pdf
pdf = PDF(orientation = 'P', unit = 'mm', format = 'A4')
pdf.print_elements()
pdf.set_auto_page_break(True, 40) #may need to turn background images into 
                                #header and footer for this to work properly

#TABLE#
df = df.applymap(str)  # Convert all data inside dataframe into string type

columns = [list(df)]  # Get list of dataframe columns
rows = df.values.tolist()  # Get list of dataframe rows
data = columns + rows  # Combine columns and rows in one list

#add fonts
pdf.add_font(family='GothamLight', style='', fname='pdf-creation/font/GothamLight.ttf', uni='DEPRECATED')
pdf.add_font(family='GothamLight', style='B', fname='pdf-creation/font/GothamMedium.ttf', uni='DEPRECATED')
#sets font type and size of table text
pdf.set_font('GothamLight', '', 10)
pdf.set_text_color(0, 0, 0)

#constructing table, need to add more parameters
with pdf.table(###find a way to adjust custom widths
               ###cell_fill_mode="ROWS",
               line_height=pdf.font_size * 1.5,
               text_align="CENTER",
               width=176) as table:

    for data_row in data:
        row = table.row()
        for datum in data_row:
            row.cell(datum)

###add support for different headings when printing out the table in subsequent 
#pages

#downloading pdf locally with representative name
pdf.output('{name}.pdf'.format(name=repname))

