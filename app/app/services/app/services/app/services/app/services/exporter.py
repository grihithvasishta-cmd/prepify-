from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class ExportEngine:
    @staticmethod
    def generate_cheatsheet_pdf(content: str, filename: str):
        doc = SimpleDocTemplate(filename, pagesize=A4, 
                                rightMargin=1*cm, leftMargin=1*cm,
                                topMargin=1*cm, bottomMargin=1*cm)
        
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Small', fontSize=8, leading=10))
        
        story = []
        
        # Title
        story.append(Paragraph("<b>PREPIFY CHEAT SHEET</b>", styles['Title']))
        story.append(Spacer(1, 0.2*cm))
        
        # RIZZ Topics Section (Example logic)
        story.append(Paragraph("<b>RIZZ TOPICS - DO NOT LEAVE</b>", styles['Heading2']))
        story.append(Spacer(1, 0.2*cm))
        
        # Two Column Layout using a Table
        col1_content = [Paragraph(line, styles['Small']) for line in content.split('\n') if line]
        
        # Simple implementation of columns (Real app uses Frames/Platypus)
        data = [[col1_content, ""]] # Placeholder for 2nd column
        
        t = Table(data, colWidths=[9*cm, 9*cm])
        t.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        
        story.append(t)
        doc.build(story)
        return filename
