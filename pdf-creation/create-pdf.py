import numpy as np
import pandas as pd
from fpdf import FPDF
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

pdf = FPDF(orientation = 'P', unit = 'mm', format = 'A4')
pdf.add_page()
pdf.set_font('helvetica', 'B', 10)
pdf.set_text_color(255, 255, 255)
pdf.image('pdf-creation/samplepdf-image.png', x = 0, y = 0, w = 210, h = 297)

pdf.output('Automated PDF Report.pdf')