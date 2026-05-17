import streamlit as st
from datetime import date

from services.markdown_generator import generate_markdown
from services.pdf_generator import generate_pdf
from utils.constants import HEADER_TEXT, LAB_INFO

# --- Configuration ---
st.set_page_config(
    page_title="MinutesFlow Pro",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Load CSS ---
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- UI ---
st.markdown(f'<p class="header-style">MinutesFlow Pro</p>', unsafe_allow_html=True)
st.markdown(f'<p class="subheader-style">{LAB_INFO}</p>', unsafe_allow_html=True)

# Initialize session state for dynamic fields
if 'present_count' not in st.session_state:
    st.session_state.present_count = 1

if 'absent_count' not in st.session_state:
    st.session_state.absent_count = 1

if 'agenda_count' not in st.session_state:
    st.session_state.agenda_count = 1

if 'action_count' not in st.session_state:
    st.session_state.action_count = 1

if 'decision_count' not in st.session_state:
    st.session_state.decision_count = 1

with st.form("minutes_form"):

    # 1. Overview
    st.markdown('<div class="section-header">1. MEETING OVERVIEW</div>', unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            project = st.text_input("Project Name", value="Applied AI Innovations")
            title = st.text_input("Meeting Title", placeholder="e.g., Weekly Sync")
            meeting_date = st.date_input("Meeting Date", value=date.today())

        with col2:
            time_start = st.text_input("Start Time", placeholder="10:00 AM")
            time_end = st.text_input("End Time", placeholder="11:00 AM")
            location = st.text_input("Location", placeholder="Conference Room A / Google Meet Link")

        notetaker = st.text_input("Notetaker Name")

    # 2. Attendees
    st.markdown('<div class="section-header">2. ATTENDEES</div>', unsafe_allow_html=True)

    st.subheader("Present")
    present_list = []

    for i in range(st.session_state.present_count):
        c1, c2 = st.columns(2)

        with c1:
            name = st.text_input(f"Name #{i+1}", key=f"p_n_{i}")

        with c2:
            role = st.text_input(f"Role/Dept #{i+1}", key=f"p_r_{i}")

        present_list.append({"name": name, "role": role})

    if st.form_submit_button("➕ Add Present Attendee"):
        st.session_state.present_count += 1
        st.rerun()

    st.subheader("Absent")
    absent_list = []

    for i in range(st.session_state.absent_count):
        c1, c2 = st.columns(2)

        with c1:
            name = st.text_input(f"Name #{i+1}", key=f"a_n_{i}")

        with c2:
            role = st.text_input(f"Role/Dept #{i+1}", key=f"a_r_{i}")

        absent_list.append({"name": name, "role": role})

    if st.form_submit_button("➕ Add Absent Attendee"):
        st.session_state.absent_count += 1
        st.rerun()

    # 3. Objective
    st.markdown('<div class="section-header">3. MEETING OBJECTIVE</div>', unsafe_allow_html=True)

    objective = st.text_area(
        "Objective",
        placeholder="State the primary goal of this meeting..."
    )

    # 4. Agenda
    st.markdown('<div class="section-header">4. AGENDA & DISCUSSION</div>', unsafe_allow_html=True)

    agenda_items = []

    for i in range(st.session_state.agenda_count):
        with st.expander(f"Agenda Item {i+1}", expanded=True):
            a_title = st.text_input("Title", key=f"a_t_{i}")
            a_pres = st.text_input("Presenter", key=f"a_p_{i}")
            a_disc = st.text_area("Key Discussion", key=f"a_d_{i}")

            agenda_items.append({
                "title": a_title,
                "presenter": a_pres,
                "discussion": a_disc
            })

    if st.form_submit_button("➕ Add Agenda Item"):
        st.session_state.agenda_count += 1
        st.rerun()

    # 5. Decisions
    st.markdown('<div class="section-header">5. DECISIONS MADE</div>', unsafe_allow_html=True)

    decisions = []

    for i in range(st.session_state.decision_count):
        decision = st.text_input(f"Decision #{i+1}", key=f"dec_{i}")
        decisions.append(decision)

    if st.form_submit_button("➕ Add Decision"):
        st.session_state.decision_count += 1
        st.rerun()

    # 6. Action Items
    st.markdown('<div class="section-header">6. ACTION ITEMS</div>', unsafe_allow_html=True)

    action_items = []

    for i in range(st.session_state.action_count):
        with st.container():
            c1, c2, c3, c4 = st.columns([3, 2, 2, 2])

            with c1:
                desc = st.text_input("Task Description", key=f"ai_d_{i}")

            with c2:
                who = st.text_input("Responsible", key=f"ai_w_{i}")

            with c3:
                due = st.text_input(
                    "Due Date",
                    value=str(date.today()),
                    key=f"ai_dd_{i}"
                )

            with c4:
                status = st.selectbox(
                    "Status",
                    ["Open", "In Progress", "Completed"],
                    key=f"ai_s_{i}"
                )

            action_items.append({
                "desc": desc,
                "who": who,
                "due": due,
                "status": status
            })

    if st.form_submit_button("➕ Add Action Item"):
        st.session_state.action_count += 1
        st.rerun()

    # 7. Next Meeting
    st.markdown('<div class="section-header">7. NEXT MEETING</div>', unsafe_allow_html=True)

    n_col1, n_col2 = st.columns(2)

    with n_col1:
        next_date = st.text_input(
            "Next Date (YYYY-MM-DD)",
            placeholder="2026-03-28"
        )

        next_time = st.text_input(
            "Next Time",
            placeholder="10:00 AM"
        )

    with n_col2:
        next_location = st.text_input(
            "Next Location",
            placeholder="Same as above"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    submitted = st.form_submit_button("🚀 GENERATE MINUTES")

if submitted:

    data = {
        "project": project,
        "title": title,
        "date": str(meeting_date),
        "time_start": time_start,
        "time_end": time_end,
        "location": location,
        "notetaker": notetaker,
        "present": present_list,
        "absent": absent_list,
        "objective": objective,
        "agenda_items": agenda_items,
        "decisions": decisions,
        "action_items": action_items,
        "next_date": next_date,
        "next_time": next_time,
        "next_location": next_location
    }

    st.balloons()
    st.success("Minutes Generated Successfully!")

    col_dl1, col_dl2 = st.columns(2)

    md_content = generate_markdown(data)

    with col_dl1:
        st.download_button(
            label="📥 Download Markdown",
            data=md_content,
            file_name=f"Minutes_{meeting_date}.md",
            mime="text/markdown"
        )

    try:
        pdf_content = generate_pdf(data)

        with col_dl2:
            st.download_button(
                label="📥 Download PDF",
                data=pdf_content,
                file_name=f"Minutes_{meeting_date}.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Error generating PDF: {e}")

    st.markdown(
        '<div class="section-header">PREVIEW</div>',
        unsafe_allow_html=True
    )

    st.markdown(md_content)

st.markdown(
    '<div class="footer">Built for Applied AI Innovations & Research Lab • 2026</div>',
    unsafe_allow_html=True
)
