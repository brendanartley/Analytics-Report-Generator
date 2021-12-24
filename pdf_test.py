from fpdf import FPDF

WIDTH = 210
HEIGHT = 297

class PDF(FPDF):
    #'w': 210, 'h': 297
    def header(self):
        # Logo (name, x, y, w = 0, h = 0)
        # w,h = 0 means automatic
        self.image('./imgs/canucks_logo.png', 10, 8, 15, 0)
        # font (font,bold,size)
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title (w,h,text,border,ln,align)
        self.cell(30, 10, 'Analytics Report', 0, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'R')

# Instantiation of inherited class
pdf = PDF()
pdf.alias_nb_pages()

# ---------- First Page ----------
pdf.add_page()
pdf.set_font('Times', '', 12)
for i in range(1, 25):
    pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)

# ---------- Second Page ----------
pdf.add_page()
pdf.image('rink_image1.png', x = 10, y = 30, w = (WIDTH-30)//2, h = 0, type = '', link = '')
pdf.image('pie_plot1.png', x = (WIDTH + 20)//2, y = 35, w = (WIDTH-80)//2, h = 0, type = '', link = '')
pdf.image('rink_image2.png', x = 10, y = 120, w = (WIDTH-30)//2, h = 0, type = '', link = '')
pdf.image('pie_plot2.png', x = (WIDTH + 20)//2, y = 125, w = (WIDTH-80)//2, h = 0, type = '', link = '')
pdf.image('bar_plot1.png', x = 10, y = 210, w = (WIDTH-30)//2, h = 0, type = '', link = '')
pdf.image('bar_plot2.png', x = (WIDTH + 10)//2, y = 210, w = (WIDTH-30)//2, h = 0, type = '', link = '')
pdf.output('test.pdf', 'F')