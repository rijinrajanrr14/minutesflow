from fpdf import FPDF
from utils.constants import HEADER_TEXT, LAB_INFO


def clean_text(text):
    """
    Cleans unsupported Unicode characters for FPDF latin-1 encoding.
    """

    if not text:
        return ""

    text = str(text)

    replacements = {
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "–": "-",
        "—": "-",
        "…": "...",
        "\u00a0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.encode(
        "latin-1",
        errors="ignore"
    ).decode("latin-1")


def generate_pdf(data):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    # ---------------- HEADER ---------------- #

    pdf.set_font("Arial", 'B', 16)

    pdf.cell(
        0,
        10,
        clean_text(HEADER_TEXT),
        ln=True,
        align='C'
    )

    pdf.set_font("Arial", 'I', 10)

    pdf.cell(
        0,
        10,
        clean_text(LAB_INFO),
        ln=True,
        align='C'
    )

    pdf.ln(5)

    # ---------------- PROJECT ---------------- #

    pdf.set_font("Arial", 'B', 12)

    pdf.cell(
        30,
        10,
        "Project:",
        ln=0
    )

    pdf.set_font("Arial", '', 12)

    pdf.cell(
        0,
        10,
        clean_text(data['project']),
        ln=True
    )

    pdf.ln(5)

    # ---------------- OVERVIEW ---------------- #

    pdf.set_font("Arial", 'B', 14)

    pdf.cell(
        0,
        10,
        "MEETING OVERVIEW",
        ln=True
    )

    pdf.set_font("Arial", '', 11)

    pdf.cell(
        0,
        7,
        f"Meeting Title: {clean_text(data['title'])}",
        ln=True
    )

    pdf.cell(
        0,
        7,
        f"Date: {clean_text(data['date'])}",
        ln=True
    )

    pdf.cell(
        0,
        7,
        (
            f"Time: "
            f"{clean_text(data['time_start'])} - "
            f"{clean_text(data['time_end'])}"
        ),
        ln=True
    )

    pdf.cell(
        0,
        7,
        f"Location: {clean_text(data['location'])}",
        ln=True
    )

    pdf.cell(
        0,
        7,
        f"Notetaker: {clean_text(data['notetaker'])}",
        ln=True
    )

    pdf.ln(5)

    # ---------------- ATTENDEES ---------------- #

    pdf.set_font("Arial", 'B', 14)

    pdf.cell(
        0,
        10,
        "ATTENDEES",
        ln=True
    )

    # -------- Present -------- #

    pdf.set_font("Arial", 'B', 11)

    pdf.cell(
        0,
        7,
        "Present",
        ln=True
    )

    pdf.set_font("Arial", '', 11)

    for attendee in data['present']:

        if attendee['name']:

            pdf.multi_cell(
                0,
                7,
                (
                    f"- {clean_text(attendee['name'])} "
                    f"({clean_text(attendee['role'])})"
                )
            )

    pdf.ln(2)

    # -------- Absent -------- #

    if any(a['name'] for a in data['absent']):

        pdf.set_font("Arial", 'B', 11)

        pdf.cell(
            0,
            7,
            "Absent",
            ln=True
        )

        pdf.set_font("Arial", '', 11)

        for attendee in data['absent']:

            if attendee['name']:

                pdf.multi_cell(
                    0,
                    7,
                    (
                        f"- {clean_text(attendee['name'])} "
                        f"({clean_text(attendee['role'])})"
                    )
                )

    pdf.ln(5)

    # ---------------- OBJECTIVE ---------------- #

    pdf.set_font("Arial", 'B', 14)

    pdf.cell(
        0,
        10,
        "MEETING OBJECTIVE",
        ln=True
    )

    pdf.set_font("Arial", '', 11)

    pdf.multi_cell(
        0,
        7,
        clean_text(data['objective'])
    )

    pdf.ln(5)

    # ---------------- AGENDA ---------------- #

    # ---------------- AGENDA ---------------- #

    pdf.set_font("Arial", 'B', 14)

    pdf.cell(
        0,
        10,
        "AGENDA & DISCUSSION POINTS",
        ln=True
    )

    for i, item in enumerate(data['agenda_items'], 1):

        if item['title']:

            # Agenda Title
            pdf.set_font("Arial", 'B', 11)

            pdf.cell(
                0,
                7,
                f"{i}. {clean_text(item['title'])}",
                ln=True
            )

            # Presenter
            pdf.set_font("Arial", '', 11)

            pdf.cell(
                0,
                7,
                (
                    f"Presenter: "
                    f"{clean_text(item['presenter'])}"
                ),
                ln=True
            )

            # Key Discussion Heading
            pdf.cell(
                0,
                7,
                "Key Discussion:",
                ln=True
            )

            # Bullet Points
            discussion_lines = item['discussion'].split("\n")

            for line in discussion_lines:

                if line.strip():

                    pdf.cell(5)

                    pdf.multi_cell(
                        0,
                        7,
                        f"* {clean_text(line.strip())}"
                    )

            pdf.ln(3)
    # ---------------- DECISIONS ---------------- #

    pdf.set_font("Arial", 'B', 14)

    pdf.cell(
        0,
        10,
        "DECISIONS MADE",
        ln=True
    )

    pdf.set_font("Arial", '', 11)

    for decision in data['decisions']:

        if decision.strip():

            pdf.multi_cell(
                0,
                7,
                f"- {clean_text(decision)}"
            )

    pdf.ln(5)

    # ---------------- ACTION ITEMS ---------------- #

    pdf.set_font("Arial", 'B', 14)

    pdf.cell(
        0,
        10,
        "ACTION ITEMS",
        ln=True
    )

    # Table Header
    pdf.set_font("Arial", 'B', 10)

    pdf.cell(70, 7, "Action Item", 1)
    pdf.cell(40, 7, "Responsible", 1)
    pdf.cell(40, 7, "Due Date", 1)
    pdf.cell(40, 7, "Status", 1, ln=True)

    # Table Rows
    pdf.set_font("Arial", '', 9)

    for action in data['action_items']:

        if action['desc']:

            start_y = pdf.get_y()

            pdf.multi_cell(
                70,
                7,
                clean_text(action['desc']),
                1
            )

            end_y = pdf.get_y()

            h = end_y - start_y

            pdf.set_xy(80, start_y)

            pdf.cell(
                40,
                h,
                clean_text(action['who']),
                1
            )

            pdf.cell(
                40,
                h,
                clean_text(action['due']),
                1
            )

            pdf.cell(
                40,
                h,
                clean_text(action['status']),
                1,
                ln=True
            )

    pdf.ln(5)

    # ---------------- NEXT MEETING ---------------- #

    pdf.set_font("Arial", 'B', 14)

    pdf.cell(
        0,
        10,
        "NEXT MEETING",
        ln=True
    )

    pdf.set_font("Arial", '', 11)

    pdf.cell(
        0,
        7,
        (
            f"Date & Time: "
            f"{clean_text(data['next_date'])} at "
            f"{clean_text(data['next_time'])}"
        ),
        ln=True
    )

    pdf.cell(
        0,
        7,
        f"Location: {clean_text(data['next_location'])}",
        ln=True
    )

    # ---------------- OUTPUT ---------------- #

    return pdf.output(
        dest='S'
    ).encode(
        'latin-1',
        errors='ignore'
    )