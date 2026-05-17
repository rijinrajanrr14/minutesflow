from fpdf import FPDF
from utils.constants import HEADER_TEXT, LAB_INFO


def generate_pdf(data):

    pdf = FPDF()

    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, HEADER_TEXT, ln=True, align='C')

    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, LAB_INFO, ln=True, align='C')

    pdf.ln(5)

    # Project
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(30, 10, "Project: ", ln=0)

    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, data['project'], ln=True)

    pdf.ln(5)

    # Overview
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "MEETING OVERVIEW", ln=True)

    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 7, f"Meeting Title: {data['title']}", ln=True)
    pdf.cell(0, 7, f"Date: {data['date']}", ln=True)
    pdf.cell(0, 7, f"Time: {data['time_start']} - {data['time_end']}", ln=True)
    pdf.cell(0, 7, f"Location: {data['location']}", ln=True)
    pdf.cell(0, 7, f"Notetaker: {data['notetaker']}", ln=True)

    pdf.ln(5)

    # Attendees
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "ATTENDEES", ln=True)

    pdf.set_font("Arial", '', 11)

    present_str = ", ".join([
        f"{a['name']} ({a['role']})"
        for a in data['present']
        if a['name']
    ])

    absent_str = ", ".join([
        f"{a['name']} ({a['role']})"
        for a in data['absent']
        if a['name']
    ])

    pdf.multi_cell(0, 7, f"Present: {present_str}")
    pdf.multi_cell(0, 7, f"Absent: {absent_str}")

    pdf.ln(5)

    # Objective
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "MEETING OBJECTIVE", ln=True)

    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, data['objective'])

    pdf.ln(5)

    # Agenda
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "AGENDA & DISCUSSION POINTS", ln=True)

    pdf.set_font("Arial", '', 11)

    for i, item in enumerate(data['agenda_items'], 1):

        if item['title']:

            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 7, f"{i}. {item['title']}", ln=True)

            pdf.set_font("Arial", '', 11)

            pdf.cell(10)
            pdf.cell(0, 7, f"Presenter: {item['presenter']}", ln=True)

            pdf.cell(10)
            pdf.multi_cell(0, 7, f"Key Discussion: {item['discussion']}")

    pdf.ln(5)

    # Decisions
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "DECISIONS MADE", ln=True)

    pdf.set_font("Arial", '', 11)

    for decision in data['decisions']:
        if decision.strip():
            pdf.multi_cell(0, 7, f"- {decision}")

    pdf.ln(5)

    # Action Items
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "ACTION ITEMS", ln=True)

    pdf.set_font("Arial", 'B', 10)
    pdf.cell(70, 7, "Action Item", 1)
    pdf.cell(40, 7, "Responsible", 1)
    pdf.cell(40, 7, "Due Date", 1)
    pdf.cell(40, 7, "Status", 1, ln=True)

    pdf.set_font("Arial", '', 9)

    for action in data['action_items']:

        if action['desc']:

            start_y = pdf.get_y()

            pdf.multi_cell(70, 7, action['desc'], 1)

            end_y = pdf.get_y()

            h = end_y - start_y

            pdf.set_xy(80, start_y)

            pdf.cell(40, h, action['who'], 1)
            pdf.cell(40, h, action['due'], 1)
            pdf.cell(40, h, action['status'], 1, ln=True)

    pdf.ln(5)

    # Next Meeting
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "NEXT MEETING", ln=True)

    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 7, f"Date & Time: {data['next_date']} at {data['next_time']}", ln=True)
    pdf.cell(0, 7, f"Location: {data['next_location']}", ln=True)

    return pdf.output(dest='S').encode('latin-1')
