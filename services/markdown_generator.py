from utils.constants import HEADER_TEXT, LAB_INFO


def generate_markdown(data):

    md = f"# {HEADER_TEXT}\n"
    md += f"**{LAB_INFO}**\n\n"
    md += f"**Project:** {data['project']}\n\n"

    md += "## MEETING OVERVIEW\n"
    md += f"- **Meeting Title:** {data['title']}\n"
    md += f"- **Date:** {data['date']}\n"
    md += f"- **Time:** {data['time_start']} – {data['time_end']}\n"
    md += f"- **Location:** {data['location']}\n"
    md += f"- **Notetaker:** {data['notetaker']}\n\n"

    md += "## ATTENDEES\n"

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

    md += f"- **Present:** {present_str}\n"
    md += f"- **Absent:** {absent_str}\n\n"

    md += "## MEETING OBJECTIVE\n"
    md += f"{data['objective']}\n\n"

    md += "## AGENDA & DISCUSSION POINTS\n"

    for i, item in enumerate(data['agenda_items'], 1):
        if item['title']:
            md += f"{i}. **{item['title']}**\n"
            md += f"   - **Presenter:** {item['presenter']}\n"
            md += f"   - **Key Discussion:** {item['discussion']}\n"

    md += "\n"

    md += "## DECISIONS MADE\n"

    for decision in data['decisions']:
        if decision.strip():
            md += f"- {decision}\n"

    md += "\n"

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

    md += "## NEXT MEETING\n"
    md += f"- **Date & Time:** {data['next_date']} at {data['next_time']}\n"
    md += f"- **Location:** {data['next_location']}\n"

    return md
