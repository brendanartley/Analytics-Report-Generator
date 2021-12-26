# Import FPDF class
from fpdf import FPDF

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
pdf = PDF("Nils Hoglander", "20202021", "Vancouver Canucks")
pdf.add_page()
pdf.set_font('Times', '', 12)# Instantiation of inherited class
pdf.alias_nb_pages()
 
# Since we do not need to draw lines anymore, there is no need to separate
# headers from data matrix.
 
data =  [["goalsInFirstPeriod", 5],
        ["goalsInSecondPeriod", 2],
        ["goalsInThirdPeriod", 6],
        ["gameWinningGoals", 1],
        ["emptyNetGoals", 0],
        ["shootOutGoals", 0],
        ["shootOutShots", 1],
        ["goalsTrailingByOne", 1],
        ["goalsTrailingByThreePlus", 1],
        ["goalsWhenTied", 5],
        ["goalsLeadingByOne", 4],
        ["goalsLeadingByTwo", 1],
        ["goalsLeadingByThreePlus", 1],
        ["penaltyGoals", 0],
        ["penaltyShots", 0],
]
table_cell_height = 9
table_cell_width_col1 = 60
table_cell_width_col2 = 20

 
# Here we add more padding by passing 2*th as height
pdf.set_fill_color(200,212,227) #(r,g,b)
pdf.cell(table_cell_width_col1, table_cell_height, "Goal Stat", border=1, align='C', fill=True)
pdf.cell(table_cell_width_col2, table_cell_height, "Count", border=1, ln=1, align='C', fill=True)

pdf.set_fill_color(235,240,248)
for row in data:
    for i, datum in enumerate(row):
        # Enter data in colums
        if i == 0:
            pdf.cell(table_cell_width_col1, table_cell_height, str(datum), border=1, fill=True)
        else:
            pdf.cell(table_cell_width_col2, table_cell_height, str(datum), border=1, align='C', fill=True)
 
    pdf.ln(table_cell_height)

WIDTH = 210
HEIGHT = 297
pdf.image('rink_image1.png', x = 40, y = 180, w = 130, h = 0, type = '', link = '')
pdf.image('pie_plot1.png', x = 110, y = 20, w = (WIDTH-40)//2, h = 0, type = '', link = '')
pdf.image('pie_plot2.png', x = 115, y = 95, w = (WIDTH-50)//2, h = 0, type = '', link = '')
 
pdf.output('table-using-cell-borders.pdf','F')