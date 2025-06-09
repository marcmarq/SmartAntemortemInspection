from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from pathlib import Path

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12
        )
        self.normal_style = self.styles['Normal']

    def _create_header(self, title):
        """Create document header with title and date"""
        elements = []
        elements.append(Paragraph(title, self.title_style))
        elements.append(Spacer(1, 12))
        return elements

    def _create_inspection_table(self, data):
        """Create a table for inspection data"""
        table_data = [
            ['Field', 'Value'],
            ['Inspection ID', data.get('id', 'N/A')],
            ['Date', data.get('date', 'N/A')],
            ['Inspector', data.get('inspector', 'N/A')],
            ['Animal Type', data.get('animal_type', 'N/A')],
            ['Health Status', data.get('health_status', 'N/A')],
            ['Observations', data.get('observations', 'N/A')]
        ]

        table = Table(table_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table

    def generate_inspection_report(self, inspection_data, output_path):
        """Generate PDF report for a single inspection"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        elements = []
        
        # Add header
        elements.extend(self._create_header("Antemortem Inspection Report"))
        
        # Add inspection details
        elements.append(Paragraph("Inspection Details", self.heading_style))
        elements.append(Spacer(1, 12))
        elements.append(self._create_inspection_table(inspection_data))
        
        # Add images if available
        if 'images' in inspection_data and inspection_data['images']:
            elements.append(Spacer(1, 20))
            elements.append(Paragraph("Inspection Images", self.heading_style))
            elements.append(Spacer(1, 12))
            for img_path in inspection_data['images']:
                if os.path.exists(img_path):
                    img = Image(img_path, width=4*inch, height=3*inch)
                    elements.append(img)
                    elements.append(Spacer(1, 12))

        # Build PDF
        doc.build(elements)

    def generate_monthly_report(self, month_data, output_path):
        """Generate PDF report for monthly inspections"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        elements = []

        # Add header
        month_year = datetime.strptime(month_data['month'], '%Y-%m').strftime('%B %Y')
        elements.extend(self._create_header(f"Monthly Inspection Report - {month_year}"))

        # Add summary statistics
        elements.append(Paragraph("Summary Statistics", self.heading_style))
        elements.append(Spacer(1, 12))

        stats_data = [
            ['Metric', 'Count'],
            ['Total Inspections', str(month_data['total_inspections'])],
            ['Passed Inspections', str(month_data['passed_inspections'])],
            ['Failed Inspections', str(month_data['failed_inspections'])],
            ['Pending Actions', str(month_data['pending_actions'])]
        ]

        stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 20))

        # Add inspection list
        elements.append(Paragraph("Inspection List", self.heading_style))
        elements.append(Spacer(1, 12))

        inspections_data = [['Date', 'ID', 'Animal Type', 'Status']]
        for inspection in month_data['inspections']:
            inspections_data.append([
                inspection['date'],
                inspection['id'],
                inspection['animal_type'],
                inspection['status']
            ])

        inspections_table = Table(inspections_data, colWidths=[1.5*inch, 1.5*inch, 2*inch, 1*inch])
        inspections_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(inspections_table)

        # Build PDF
        doc.build(elements) 