from fpdf import FPDF

WIDTH = 210
HEIGHT = 297

class PDF(FPDF):

    def __init__(self, player_name, season, organization):
        FPDF.__init__(self) #initializes parent class
        self.player_name = player_name
        self.season = season
        self.organization = organization

    def header(self):
        # Logo (name, x, y, w = 0, h = 0)
        # w,h = 0 means automatic
        self.image('./imgs/canucks_logo.png', 10, 8, 15, 0)
        # font (font,bold,size)
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title (w,h,text,border,ln,align)
        if self.page_no()==1:
            pass
        elif self.page_no()==2:
            self.cell(30, 10, '{} Goals + Shots'.format(self.player_name), 0, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        if self.page_no()!=1:
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()-1), 0, 0, 'R')

# Instantiation of inherited class
pdf = PDF("Nils Hoglander", "20202021", "Vancouver Canucks")
#pdf = PDF()
pdf.alias_nb_pages()

# ---------- First Page ----------
pdf.add_page()
pdf.set_font('Times', '', 18)

#(w, h = 0, txt = '', border = 0, ln = 0, align = '', fill = False, link = '')
pdf.ln(h = 30)
pdf.cell(w=0, h=10, txt="Annual Player Report", border=0, ln=1, align="C")
pdf.cell(w=0, h=10, txt=pdf.season[:4] + " / " + pdf.season[4:], border=0, ln=1, align="C")
pdf.cell(w=0, h=10, txt=pdf.organization, border=0, ln=1, align="C")
pdf.cell(w=0, h=10, txt=pdf.player_name, border=0, ln=1, align="C")

# pdf.cell(0, 10, pdf.season[:4] + " " + pdf.season[4:],0,0,'C')
# pdf.cell(0, 10, pdf.player_name + " Season Report",0,0,'C')

# ---------- Second Page ----------
pdf.add_page()
pdf.image('rink_image1.png', x = 10, y = 30, w = (WIDTH-30)//2, h = 0, type = '', link = '')
pdf.image('pie_plot1.png', x = (WIDTH + 20)//2, y = 35, w = (WIDTH-80)//2, h = 0, type = '', link = '')
pdf.image('rink_image2.png', x = 10, y = 120, w = (WIDTH-30)//2, h = 0, type = '', link = '')
pdf.image('pie_plot2.png', x = (WIDTH + 20)//2, y = 125, w = (WIDTH-80)//2, h = 0, type = '', link = '')
pdf.image('bar_plot1.png', x = 10, y = 210, w = (WIDTH-30)//2, h = 0, type = '', link = '')
pdf.image('bar_plot2.png', x = (WIDTH + 10)//2, y = 210, w = (WIDTH-30)//2, h = 0, type = '', link = '')
pdf.output('test.pdf', 'F')