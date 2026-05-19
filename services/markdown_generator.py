from utils.constants import HEADER_TEXT, LAB_INFO


def generate_markdown(data):

    md = f"# {HEADER_TEXT}\n"
    md += f"**{LAB_INFO}**\n\n"

    md += f"**Project:** {data['project']}\n\n"

    # ---------------- MEETING OVERVIEW ---------------- #

    md += "## MEETING OVERVIEW\n"

    md += f"- **Meeting Title:** {data['title']}\n"
    md += f"- **Date:** {data['date']}\n"
    md += f"- **Time:** {data['time_start']} – {data['time_end']}\n"
    md += f"- **Location:** {data['location']}\n"
    md += f"- **Notetaker:** {data['notetaker']}\n\n"

    # ---------------- ATTENDEES ---------------- #

    md += "## ATTENDEES\n\n"

    # Present
    md += "### Present\n"

    for attendee in data['present']:

        if attendee['name']:

            md += (
                f"- {attendee['name']} "
                f"({attendee['role']})\n"
            )

    md += "\n"

    # Absent
    if any(a['name'] for a in data['absent']):

        md += "### Absent\n"

        for attendee in data['absent']:

            if attendee['name']:

                md += (
                    f"- {attendee['name']} "
                    f"({attendee['role']})\n"
                )

        md += "\n"

    # ---------------- OBJECTIVE ---------------- #

    md += "## MEETING OBJECTIVE\n"

    md += f"{data['objective']}\n\n"


    # ---------------- AGENDA ---------------- #

    md += "## AGENDA & DISCUSSION POINTS\n\n"

    for i, item in enumerate(data['agenda_items'], 1):

        if item['title']:

            # Agenda Title
            md += f"{i}. {item['title']}\n\n"

            # Presenter
            md += (
                f"Presenter: "
                f"{item['presenter']}\n\n"
            )

            # Key Discussion Heading
            md += "Key Discussion:\n\n"

            # Discussion Bullet Points
            discussion_lines = item['discussion'].split("\n")

            for line in discussion_lines:

                if line.strip():

                    md += f"● {line.strip()}\n"

            md += "\n\n"
        # ---------------- ACTION ITEMS ---------------- #

        md += "## ACTION ITEMS\n\n"

        md += "| Action Item | Responsible | Due Date | Status |\n"
        md += "| :--- | :--- | :--- | :--- |\n"

        for action in data['action_items']:

            if action['desc']:

                md += (
                    f"| {action['desc']} | "
                    f"{action['who']} | "
                    f"{action['due']} | "
                    f"{action['status']} |\n"
                )

        md += "\n"

    # ---------------- NEXT MEETING ---------------- #

    md += "## NEXT MEETING\n\n"

    md += (
        f"- **Date & Time:** "
        f"{data['next_date']} at {data['next_time']}\n"
    )

    md += (
        f"- **Location:** "
        f"{data['next_location']}\n"
    )

    return md