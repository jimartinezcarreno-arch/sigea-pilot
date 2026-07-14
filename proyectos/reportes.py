import io
from django.http import HttpResponse
from django.db.models import Count
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import pandas as pd
from datetime import datetime, date

from .models import Aula, Clase, Docente, Edificio, Programa
from .middleware import get_current_tenant_id


def reporte_pdf(request):
    tenant_id = get_current_tenant_id()
    
    # Setup response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_consolidado_{date.today().strftime("%Y%m%d")}.pdf"'

    # Create document
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=45, bottomMargin=45)
    story = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.HexColor('#1e1b4b'),
        spaceAfter=15
    )
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor('#4f46e5'),
        spaceBefore=15,
        spaceAfter=10
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#334155'),
        leading=14
    )
    th_style = ParagraphStyle(
        'THStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.white
    )
    td_style = ParagraphStyle(
        'TDStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#0f172a')
    )

    # Document Header
    story.append(Paragraph("SIGEA - Reporte de Gestión e Infraestructura", title_style))
    story.append(Paragraph(f"Fecha de Generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", body_style))
    story.append(Spacer(1, 15))

    # Metric Cards Summary
    total_aulas = Aula.objects.count()
    total_clases = Clase.objects.count()
    total_docentes = Docente.objects.count()
    total_edificios = Edificio.objects.count()

    summary_data = [
        [
            Paragraph(f"<b>Aulas Totales:</b> {total_aulas}", body_style),
            Paragraph(f"<b>Edificios:</b> {total_edificios}", body_style)
        ],
        [
            Paragraph(f"<b>Docentes Registrados:</b> {total_docentes}", body_style),
            Paragraph(f"<b>Clases Programadas:</b> {total_clases}", body_style)
        ]
    ]
    summary_table = Table(summary_data, colWidths=[260, 260])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('PADDING', (0,0), (-1,-1), 12),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))

    # 1. Classroom Occupancy rates
    story.append(Paragraph("Tasa de Ocupación por Aula (Semanal)", subtitle_style))
    
    # Calculate occupancy. A classroom is open max 96 hours a week (16h per day * 6 days)
    aulas_list = Aula.objects.all()
    occupancy_rows = [[Paragraph("Aula", th_style), Paragraph("Edificio", th_style), Paragraph("Clases Semanales", th_style), Paragraph("Horas Ocupadas", th_style)]]
    
    for a in aulas_list:
        clases_count = Clase.objects.filter(aula=a).count()
        # Estimate total hours: count classes and multiply by average duration (e.g. 2 hours)
        horas_ocupadas = 0
        clases_aula = Clase.objects.filter(aula=a).select_related('horario')
        for c in clases_aula:
            dt_ini = datetime.combine(date.today(), c.horario.hora_inicio)
            dt_fin = datetime.combine(date.today(), c.horario.hora_fin)
            horas_ocupadas += (dt_fin - dt_ini).total_seconds() / 3600
        
        occupancy_rows.append([
            Paragraph(a.nombre, td_style),
            Paragraph(a.edificio.nombre if a.edificio else "-", td_style),
            Paragraph(str(clases_count), td_style),
            Paragraph(f"{horas_ocupadas:.1f} hrs", td_style)
        ])

    table_occ = Table(occupancy_rows, colWidths=[130, 130, 130, 130])
    table_occ.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4f46e5')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(table_occ)
    story.append(Spacer(1, 20))

    # 2. Cumulative hours per teacher
    story.append(Paragraph("Horas Acumuladas por Docente", subtitle_style))
    docentes_list = Docente.objects.all()
    docente_rows = [[Paragraph("Docente", th_style), Paragraph("Identificación", th_style), Paragraph("Total Clases", th_style), Paragraph("Horas Semanales", th_style)]]

    for d in docentes_list:
        clases_doc = Clase.objects.filter(docente=d)
        horas_doc = 0
        for c in clases_doc:
            dt_ini = datetime.combine(date.today(), c.horario.hora_inicio)
            dt_fin = datetime.combine(date.today(), c.horario.hora_fin)
            horas_doc += (dt_fin - dt_ini).total_seconds() / 3600

        docente_rows.append([
            Paragraph(d.nombre, td_style),
            Paragraph(d.identificacion, td_style),
            Paragraph(str(clases_doc.count()), td_style),
            Paragraph(f"{horas_doc:.1f} hrs", td_style)
        ])

    table_doc = Table(docente_rows, colWidths=[160, 120, 120, 120])
    table_doc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e1b4b')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(table_doc)

    # Build PDF
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    
    response.write(pdf)
    return response


def reporte_excel(request):
    tenant_id = get_current_tenant_id()
    
    # 1. Fetch data for Classroom occupancy sheet
    aulas_data = []
    for a in Aula.objects.all():
        clases_count = Clase.objects.filter(aula=a).count()
        horas_ocupadas = 0
        clases_aula = Clase.objects.filter(aula=a).select_related('horario')
        for c in clases_aula:
            dt_ini = datetime.combine(date.today(), c.horario.hora_inicio)
            dt_fin = datetime.combine(date.today(), c.horario.hora_fin)
            horas_ocupadas += (dt_fin - dt_ini).total_seconds() / 3600
        
        aulas_data.append({
            'ID Aula': a.id,
            'Nombre Aula': a.nombre,
            'Edificio': a.edificio.nombre if a.edificio else "-",
            'Sede': a.edificio.sede.nombre if (a.edificio and a.edificio.sede) else "-",
            'Tipo Espacio': a.get_tipo_espacio_display(),
            'Capacidad': a.capacidad,
            'Clases Programadas': clases_count,
            'Horas Ocupadas/Semana': horas_ocupadas
        })
    df_aulas = pd.DataFrame(aulas_data)

    # 2. Fetch data for Teachers hours sheet
    docentes_data = []
    for d in Docente.objects.all():
        clases_doc = Clase.objects.filter(docente=d)
        horas_doc = 0
        for c in clases_doc:
            dt_ini = datetime.combine(date.today(), c.horario.hora_inicio)
            dt_fin = datetime.combine(date.today(), c.horario.hora_fin)
            horas_doc += (dt_fin - dt_ini).total_seconds() / 3600
            
        docentes_data.append({
            'ID Docente': d.id,
            'Identificación': d.identificacion,
            'Nombre Docente': d.nombre,
            'Email': d.email,
            'Total Clases Semanales': clases_doc.count(),
            'Horas Totales Semanales': horas_doc
        })
    df_docentes = pd.DataFrame(docentes_data)

    # Write sheets in Excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_aulas.to_excel(writer, sheet_name='Ocupación Aulas', index=False)
        df_docentes.to_excel(writer, sheet_name='Horas Docentes', index=False)
    
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="reporte_consolidado_{date.today().strftime("%Y%m%d")}.xlsx"'
    output.close()
    
    return response
