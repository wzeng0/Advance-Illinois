
import numpy as np
import pandas as pd
from fpdf import FPDF
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

repname = "ABDELNASSER RASHID"

pdf = FPDF(orientation = 'P', unit = 'mm', format = 'A4')
pdf.add_font(family='Gotham', style='', fname='pdf-creation/font/GothamMedium.ttf', uni='DEPRECATED')
pdf.add_font(family='Gotham', style='B', fname='pdf-creation/font/GothamBold.ttf', uni='DEPRECATED')
pdf.add_page()
pdf.set_font('Gotham', 'B', 12)
pdf.set_text_color(240, 86.5, 41)
pdf.image('pdf-creation/samplepdf-image.png', x = 0, y = 0, w = 210, h = 297)
pdf.text(17.25, 47.5, "REPRESENTATIVE {name}".format(name = repname))

pdf.output('{name}.pdf'.format(name=repname))


#if we want to create headers and stuff
"""
from fpdf import FPDF
class PDF(FPDF):
    def header(self):
        self.add_font(family='Gotham', style='B', fname='pdf-creation/font/GothamBold.ttf', uni='DEPRECATED')
        # Setting font: helvetica bold 15
        self.set_font("Gotham", "B", 12)
        # Calculating width of title and setting cursor position:
        width = self.get_string_width(self.title) + 6
        self.set_x((210 - width) / 2)
        # Setting colors for frame, background and text:
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(240, 86, 41)

        # Setting thickness of the frame (1 mm)
        #self.set_line_width(1)
        # Printing title:
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
        # Performing a line break:
        self.ln(10)

pdf = PDF()
#pdf.add_page()
#pdf.image('pdf-creation/samplepdf-image.png', x = 0, y = 0, w = 210, h = 297)
pdf.set_title("REPRESENTATIVE")
pdf.image('pdf-creation/samplepdf-image.png', x = 0, y = 0, w = 210, h = 297)
pdf.output("tuto3.pdf")
"""
