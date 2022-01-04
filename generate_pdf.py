# Import FPDF class
from fpdf import FPDF
import report_generation.plotting_functions
import os
import sys

def main(p_id, season):

    goal_stats_list, player_info, player_stats_list = report_generation.plotting_functions.generate_all_plots(p_id = p_id, season = season)

    class PDF(FPDF):

        def __init__(self, player_name, season, organization, team_id):
            FPDF.__init__(self) #initializes parent class
            self.player_name = player_name
            self.season = season
            self.organization = organization
            self.team_id = team_id

        def header(self):
            # Logo (name, x, y, w = 0, h = 0)
            # w,h = 0 means automatic
            self.image('./imgs/team_logos/{}.jpg'.format(self.team_id), 10, 8, 15, 0)
            # font (font,bold,size)
            self.set_font('Arial', 'B', 15)
            # Move to the right
            self.cell(80)
            # Title (w,h,text,border,ln,align)
            if self.page_no()==1:
                pass
            elif self.page_no()==2:
                self.cell(30, 10, '{} - Goals / Shots'.format(self.player_name), 0, 0, 'C')
            elif self.page_no()==3:
                self.cell(30, 10, '{} - Shots / Rank / Other'.format(self.player_name), 0, 0, 'C')
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

    # ----------  Instantiation of Inherited Class ----------
    pdf = PDF(player_info["fullName"], player_info["season"], player_info["team_name"], player_info["team_id"])
    pdf.alias_nb_pages()

    # ---------- First Page ----------
    pdf.add_page()
    pdf.set_font('Times', '', 18)
    pdf.ln(h = 30)
    pdf.cell(w=0, h=10, txt="Annual Player Report", border=0, ln=1, align="C")
    pdf.cell(w=0, h=10, txt=pdf.season[:4] + " / " + pdf.season[4:], border=0, ln=1, align="C")
    pdf.cell(w=0, h=10, txt=pdf.organization, border=0, ln=1, align="C")
    pdf.cell(w=0, h=10, txt=pdf.player_name, border=0, ln=1, align="C")
    pdf.image('./tmp/player.jpg', x = 85, y = 110, w = 40, h = 0, type = '', link = '')

    # ---------- Second Page ----------
    
    # Since we do not need to draw lines anymore, there is no need to separate
    # headers from data matrix.

    pdf.add_page()
    pdf.set_font('Times', '', 12)

    table_cell_height = 9
    table_cell_width_col1 = 60
    table_cell_width_col2 = 20

    # Here we add more padding by passing 2*th as height
    pdf.set_fill_color(189,210,236) #(r,g,b)
    pdf.cell(table_cell_width_col1, table_cell_height, "Goal Statistics", border=1, align='C', fill=True)
    pdf.cell(table_cell_width_col2, table_cell_height, "Count", border=1, ln=1, align='C', fill=True)

    pdf.set_fill_color(235,241,249)
    for row in goal_stats_list:
        for i, datum in enumerate(row):
            # Enter data in colums
            if i == 0:
                pdf.cell(table_cell_width_col1, table_cell_height, str(datum), border=1, fill=True)
            else:
                pdf.cell(table_cell_width_col2, table_cell_height, str(datum), border=1, align='C', fill=True)
    
        pdf.ln(table_cell_height)

    WIDTH = 210
    HEIGHT = 297
    pdf.image('./tmp/pie_plot1.jpg', x = 120, y = 20, w = (WIDTH-60)//2, h = 0, type = '', link = '')
    pdf.image('./tmp/pie_plot2.jpg', x = 120, y = 95, w = (WIDTH-60)//2, h = 0, type = '', link = '')
    pdf.image('./tmp/rink_image1.jpg', x = 50, y = 180, w = 110, h = 0, type = '', link = '')

    # ---------- Third Page ----------
    # Shot plot and other stats
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    pdf.ln(100)

    table_cell_height = 9
    table_cell_width_col1 = 60
    table_cell_width_col2 = 20

    # Here we add more padding by passing 2*th as height
    pdf.set_fill_color(189,210,236) #(r,g,b)
    pdf.cell(table_cell_width_col1, table_cell_height, "Other Statistics", border=1, align='C', fill=True)
    pdf.cell(table_cell_width_col2, table_cell_height, "Count", border=1, ln=1, align='C', fill=True)

    pdf.set_fill_color(235,241,249)
    for row in player_stats_list:
        for i, datum in enumerate(row):
            # Enter data in colums
            if i == 0:
                pdf.cell(table_cell_width_col1, table_cell_height, str(datum), border=1, fill=True)
            else:
                pdf.cell(table_cell_width_col2, table_cell_height, str(datum), border=1, align='C', fill=True)
    
        pdf.ln(table_cell_height)

    pdf.image('./tmp/rink_image2.jpg', x = 50, y = 30, w = 110, h = 0, type = '', link = '')
    pdf.image('./tmp/rank_hbar_plot1.jpg', x = 110, y = 130, w = 76, h = 0, type = '', link = '')

    # Clear tmp directory
    for file in os.listdir("./tmp"):
        os.remove("./tmp/" + file)

    # ---------- Save PDF to Output ---------- 
    pdf.output('report.pdf','F')
    print(" --- Complete --- ")

if __name__ == "__main__":
    try:
        p_id = int(sys.argv[1].strip())
        season = int(sys.argv[2].strip())
        if len(sys.argv[2].strip()) != 8:
            sys.exit(" --------- Check input format --------- ")
    except:
        sys.exit(" --------- Check input format --------- ")

    main(p_id, season)