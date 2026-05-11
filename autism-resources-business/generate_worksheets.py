"""
SpectrumReady Fillable Worksheet Generator
Creates 5 interactive PDF worksheets with fillable form fields.
Run: python3 generate_worksheets.py
Output: autism-resources-business/products/worksheets/
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "products", "worksheets")
os.makedirs(OUT_DIR, exist_ok=True)

# Brand colours
PURPLE   = HexColor("#6366f1")
PURPLE_D = HexColor("#4f46e5")
PURPLE_L = HexColor("#ede9fe")
AMBER    = HexColor("#f59e0b")
DARK     = HexColor("#1e1b4b")
GREY     = HexColor("#6b7280")
LIGHT    = HexColor("#f9fafb")
SUCCESS  = HexColor("#10b981")
SUCCESS_L= HexColor("#d1fae5")


# ─────────────────────────────────────────────────────────────────────────────
# Shared canvas callback — draws brand header + page number
# ─────────────────────────────────────────────────────────────────────────────

def _make_page_callback(title, subtitle=""):
    def on_page(c, doc):
        w, h = letter
        # Purple top bar
        c.setFillColor(DARK)
        c.rect(0, h - 0.55 * inch, w, 0.55 * inch, fill=1, stroke=0)
        # Brand name
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.5 * inch, h - 0.35 * inch, "SpectrumReady")
        # Title
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(w / 2, h - 0.35 * inch, title)
        if subtitle:
            c.setFont("Helvetica", 8)
            c.setFillColor(HexColor("#a5b4fc"))
            c.drawRightString(w - 0.5 * inch, h - 0.35 * inch, subtitle)
        # Footer
        c.setFillColor(GREY)
        c.setFont("Helvetica", 7.5)
        c.drawCentredString(w / 2, 0.3 * inch,
            f"SpectrumReady · spectrumready.com · Page {doc.page}  |  "
            "Not legal advice — for educational use only.")
        c.line(0.5 * inch, 0.45 * inch, w - 0.5 * inch, 0.45 * inch)
    return on_page


def _base_doc(filename, title, subtitle=""):
    path = os.path.join(OUT_DIR, filename)
    doc = SimpleDocTemplate(
        path,
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.7 * inch,
    )
    doc._on_page = _make_page_callback(title, subtitle)
    return doc, path


def _styles():
    ss = getSampleStyleSheet()
    h1 = ParagraphStyle("H1", parent=ss["Normal"],
        fontSize=16, fontName="Helvetica-Bold",
        textColor=DARK, spaceAfter=4, spaceBefore=16)
    h2 = ParagraphStyle("H2", parent=ss["Normal"],
        fontSize=12, fontName="Helvetica-Bold",
        textColor=PURPLE_D, spaceAfter=4, spaceBefore=12)
    body = ParagraphStyle("Body", parent=ss["Normal"],
        fontSize=10, fontName="Helvetica",
        textColor=black, spaceAfter=4, leading=15)
    note = ParagraphStyle("Note", parent=ss["Normal"],
        fontSize=9, fontName="Helvetica-Oblique",
        textColor=GREY, spaceAfter=6, leading=13)
    label = ParagraphStyle("Label", parent=ss["Normal"],
        fontSize=9.5, fontName="Helvetica-Bold",
        textColor=DARK, spaceAfter=2)
    return h1, h2, body, note, label


def _section_header(text, color=PURPLE_D):
    h1, h2, body, note, label = _styles()
    return [
        HRFlowable(width="100%", thickness=2, color=color, spaceAfter=4),
        Paragraph(text, h1),
    ]


def _field_row(label_text, width=4.5):
    """Single labelled fill-in line."""
    return Table(
        [[label_text, ""]],
        colWidths=[2.2 * inch, width * inch],
        style=TableStyle([
            ("FONTNAME", (0, 0), (0, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("TEXTCOLOR", (0, 0), (0, 0), DARK),
            ("TEXTCOLOR", (1, 0), (1, 0), GREY),
            ("LINEBELOW", (1, 0), (1, 0), 0.5, GREY),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ])
    )


def _checkbox_table(items, cols=2):
    """Grid of checkbox items. □ Label"""
    rows = []
    row = []
    for i, item in enumerate(items):
        row.append(f"□  {item}")
        if len(row) == cols:
            rows.append(row)
            row = []
    if row:
        while len(row) < cols:
            row.append("")
        rows.append(row)

    col_w = [3.5 * inch] * cols
    style = TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LIGHT, white]),
    ])
    return Table(rows, colWidths=col_w, style=style)


def _rating_table(headers, rows_data, col_widths=None):
    all_rows = [headers] + rows_data
    if col_widths is None:
        col_widths = [1.5 * inch] * len(headers)
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("TEXTCOLOR", (0, 1), (-1, -1), DARK),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.3, HexColor("#e5e7eb")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ])
    return Table(all_rows, colWidths=col_widths, style=style)


# ─────────────────────────────────────────────────────────────────────────────
# WORKSHEET 1 — Benefits Audit Worksheet
# ─────────────────────────────────────────────────────────────────────────────

def ws_benefits_audit():
    doc, path = _base_doc(
        "01-benefits-audit-worksheet.pdf",
        "Benefits Audit Worksheet",
        "Complete with The Autism Benefits Navigator"
    )
    h1, h2, body, note, label = _styles()
    story = []

    story += _section_header("Benefits Audit Worksheet")
    story.append(Paragraph(
        "Use this worksheet to track your family's benefit status across all programs. "
        "Work through each program, check your eligibility, and log your action steps.",
        body
    ))
    story.append(Spacer(1, 0.1 * inch))

    # Family info fields
    story.append(Paragraph("Family Information", h2))
    for lbl in ["Child's Name", "Date of Birth", "Diagnosis & Date",
                "State of Residence", "Completed By / Date"]:
        story.append(_field_row(lbl))

    story.append(Spacer(1, 0.15 * inch))

    # Programs tracker table
    story.append(Paragraph("Program Status Tracker", h2))
    story.append(Paragraph(
        "For each program, circle or write: NOT ELIGIBLE / APPLIED / PENDING / "
        "RECEIVING / NOT APPLICABLE",
        note
    ))

    prog_rows = [
        ["Program", "Status", "Monthly Value", "Next Action / Notes"],
        ["SSI", "________", "$______/mo", ""],
        ["Medicaid (base)", "________", "Healthcare", ""],
        ["HCBS Waiver", "________", "$______/yr", "On waitlist: Y / N"],
        ["Early Intervention\n(under age 3)", "________", "Free services", ""],
        ["School IEP Services\n(ages 3–21)", "________", "Free services", ""],
        ["SNAP", "________", "$______/mo", ""],
        ["WIC (under age 5)", "________", "Food/nutrition", ""],
        ["Section 8 Housing", "________", "Rent subsidy", "On waitlist: Y / N"],
        ["ABLE Account", "________", "Savings vehicle", "Opened: Y / N"],
        ["Private Grants", "________", "$______/yr", "Applied to: ______"],
        ["Child Tax Credit", "________", "Tax benefit", ""],
        ["Medical Expense Ded.", "________", "Tax deduction", ""],
        ["Dependent Care FSA", "________", "$5,000 pre-tax", ""],
    ]
    col_widths = [1.7*inch, 1.1*inch, 1.3*inch, 3.1*inch]
    tbl = Table(prog_rows, colWidths=col_widths, style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#e5e7eb")),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(tbl)

    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Priority Actions (Top 3 This Month)", h2))
    for i in range(1, 4):
        story.append(_field_row(f"Priority {i}"))

    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Notes", h2))
    for _ in range(5):
        story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#d1d5db"), spaceAfter=18))

    doc.build(story, onFirstPage=doc._on_page, onLaterPages=doc._on_page)
    print(f"  ✓  01-benefits-audit-worksheet.pdf")


# ─────────────────────────────────────────────────────────────────────────────
# WORKSHEET 2 — IEP Meeting Prep Worksheet
# ─────────────────────────────────────────────────────────────────────────────

def ws_iep_prep():
    doc, path = _base_doc(
        "02-iep-meeting-prep-worksheet.pdf",
        "IEP Meeting Prep Worksheet",
        "Complete with IEP Mastery Guide"
    )
    h1, h2, body, note, label = _styles()
    story = []

    story += _section_header("IEP Meeting Prep Worksheet")
    story.append(Paragraph(
        "Complete this worksheet before every IEP meeting. Bring it with you. "
        "Taking notes in real time protects your rights.",
        body
    ))

    # Meeting info
    story.append(Paragraph("Meeting Information", h2))
    for lbl in ["Child's Name", "Meeting Date & Time", "Meeting Location",
                "My Advocate / Support Person", "School Contact Name"]:
        story.append(_field_row(lbl))

    # Team members expected
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Team Members Expected at This Meeting", h2))
    members = [
        "Special Ed Teacher", "General Ed Teacher", "Speech-Language Pathologist",
        "Occupational Therapist", "School Psychologist", "Administrator (LEA rep)",
        "District Special Ed Director", "ABA Provider / BCBA",
        "Private Therapist", "Parent Advocate / Attorney", "Other: ________", "Other: ________"
    ]
    story.append(_checkbox_table(members, cols=2))

    # Documents to bring
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Documents to Bring", h2))
    docs = [
        "Current IEP (review before meeting)",
        "Last year's progress reports",
        "Private provider reports/letters",
        "My written questions and requests",
        "Attendance record",
        "Notes from previous meetings",
        "This prep worksheet",
        "Pen and notepad / recording device",
    ]
    story.append(_checkbox_table(docs, cols=2))

    # My vision statement
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("My Vision Statement for My Child This Year", h2))
    story.append(Paragraph(
        "Write what you want your child to achieve. Read this at the start of the meeting.",
        note
    ))
    for _ in range(4):
        story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#d1d5db"), spaceAfter=18))

    # Services I'm requesting
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Services I Am Requesting", h2))
    svc_rows = [
        ["Service", "Hours/Freq Requested", "Current Hours", "Decision / Notes"],
        ["ABA Therapy", "", "", ""],
        ["Speech-Language Therapy", "", "", ""],
        ["Occupational Therapy", "", "", ""],
        ["Physical Therapy", "", "", ""],
        ["Social Skills Group", "", "", ""],
        ["Counseling / Psych services", "", "", ""],
        ["1:1 Aide / Paraprofessional", "", "", ""],
        ["Extended School Year (ESY)", "", "", ""],
        ["Transportation", "", "", ""],
        ["Other: __________________", "", "", ""],
    ]
    svc_tbl = Table(svc_rows, colWidths=[2.0*inch, 1.4*inch, 1.2*inch, 2.6*inch],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
            ("TEXTCOLOR", (0, 0), (-1, 0), white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
            ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#e5e7eb")),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ])
    )
    story.append(svc_tbl)

    # My questions
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("My Questions for This Meeting", h2))
    for i in range(1, 7):
        story.append(_field_row(f"Q{i}.", width=5.5))

    # After-meeting notes
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("After the Meeting — What Was Agreed / Denied", h2))
    story.append(Paragraph("Did I sign the IEP?  □ Yes  □ No  □ Took it home to review", body))
    story.append(Spacer(1, 0.05 * inch))
    story.append(Paragraph("Did I request Prior Written Notice for any denial?  □ Yes  □ No  □ Not applicable", body))
    story.append(Spacer(1, 0.05 * inch))
    story.append(Paragraph("Follow-up actions I need to take:", body))
    for _ in range(4):
        story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#d1d5db"), spaceAfter=18))

    doc.build(story, onFirstPage=doc._on_page, onLaterPages=doc._on_page)
    print(f"  ✓  02-iep-meeting-prep-worksheet.pdf")


# ─────────────────────────────────────────────────────────────────────────────
# WORKSHEET 3 — Therapy Provider Comparison Worksheet
# ─────────────────────────────────────────────────────────────────────────────

def ws_therapy_comparison():
    doc, path = _base_doc(
        "03-therapy-provider-comparison-worksheet.pdf",
        "Therapy Provider Comparison Worksheet",
        "Complete with The Complete Therapy Roadmap"
    )
    h1, h2, body, note, label = _styles()
    story = []

    story += _section_header("Therapy Provider Comparison Worksheet")
    story.append(Paragraph(
        "Use this worksheet to evaluate and compare ABA, SLT, OT, or any other therapy "
        "providers before making a decision. Complete one column per provider.",
        body
    ))
    story.append(Spacer(1, 0.05 * inch))

    # Therapy type + child info
    story.append(_field_row("Therapy Type Being Compared"))
    story.append(_field_row("Child's Name / Evaluation Date"))

    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Provider Comparison Grid", h2))
    story.append(Paragraph(
        "Rate each criterion: ✓ (meets standard), ~ (partially meets), ✗ (does not meet)",
        note
    ))

    rows = [
        ["Evaluation Criterion", "Provider A", "Provider B", "Provider C"],
        ["Provider Name", "", "", ""],
        ["Credentials (BCBA / SLP / OTR)", "", "", ""],
        ["Years of autism experience", "", "", ""],
        ["In-network with our insurance?", "", "", ""],
        ["Wait time for first appointment", "", "", ""],
        ["Location / telehealth available?", "", "", ""],
        ["Availability (days/hours)", "", "", ""],
        ["Session length and format", "", "", ""],
        ["Parent training included?", "", "", ""],
        ["Data collection & reporting", "", "", ""],
        ["BCBA supervision ratio (ABA)", "", "", ""],
        ["Individualized assessment first?", "", "", ""],
        ["Family feel / rapport with child", "", "", ""],
        ["References from other families?", "", "", ""],
        ["Cost / co-pay per session", "", "", ""],
        ["OVERALL RATING (1–10)", "", "", ""],
    ]
    col_widths = [2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch]
    tbl = Table(rows, colWidths=col_widths, style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [white, LIGHT]),
        ("BACKGROUND", (0, -1), (-1, -1), PURPLE_L),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#e5e7eb")),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ]))
    story.append(tbl)

    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Interview Questions to Ask Each Provider", h2))
    questions = [
        "How many current clients with autism do you serve?",
        "How will you measure and report progress toward goals?",
        "What parent training is included in your program?",
        "What happens if the current approach isn't working?",
        "Can I see an example of a progress report?",
        "What is the ratio of BCBA supervision to direct therapy hours? (ABA only)",
    ]
    for q in questions:
        story.append(Paragraph(f"□  {q}", body))

    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("My Decision", h2))
    story.append(_field_row("Provider Selected"))
    story.append(_field_row("Reason for Decision"))
    story.append(_field_row("Start Date"))
    story.append(_field_row("First Goal to Track"))

    doc.build(story, onFirstPage=doc._on_page, onLaterPages=doc._on_page)
    print(f"  ✓  03-therapy-provider-comparison-worksheet.pdf")


# ─────────────────────────────────────────────────────────────────────────────
# WORKSHEET 4 — Insurance Denial Tracker
# ─────────────────────────────────────────────────────────────────────────────

def ws_insurance_tracker():
    doc, path = _base_doc(
        "04-insurance-denial-tracker.pdf",
        "Insurance Denial & Appeal Tracker",
        "Complete with The Autism Insurance Battle Guide"
    )
    h1, h2, body, note, label = _styles()
    story = []

    story += _section_header("Insurance Denial & Appeal Tracker")
    story.append(Paragraph(
        "Track every denial, every appeal, and every deadline. Insurance companies count "
        "on families losing track. This worksheet ensures nothing falls through the cracks.",
        body
    ))

    # Policy info
    story.append(Paragraph("Policy Information", h2))
    for lbl in ["Insurance Company", "Member ID", "Group Number",
                "Member Services Phone", "Appeals Dept Phone / Fax",
                "State Department of Insurance Phone"]:
        story.append(_field_row(lbl))

    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Denial Log", h2))
    story.append(Paragraph(
        "Log every denial as soon as it arrives. Do not miss the 180-day appeal deadline.",
        note
    ))

    denial_rows = [
        ["#", "Service Denied", "Denial Date", "Denial Reason", "Appeal Deadline", "Status"],
        ["1", "", "", "", "", ""],
        ["2", "", "", "", "", ""],
        ["3", "", "", "", "", ""],
        ["4", "", "", "", "", ""],
        ["5", "", "", "", "", ""],
        ["6", "", "", "", "", ""],
    ]
    col_widths = [0.3*inch, 1.6*inch, 0.9*inch, 2.0*inch, 1.1*inch, 1.2*inch]
    denial_tbl = Table(denial_rows, colWidths=col_widths, style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#e5e7eb")),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(denial_tbl)

    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Appeal Progress Tracker", h2))
    story.append(Paragraph(
        "For each appeal, track every step. Note: if Level 1 internal appeal is denied, "
        "you are entitled to an External Independent Review — request it immediately.",
        note
    ))

    appeal_rows = [
        ["Denial #", "Level 1\nInternal Appeal", "Level 2\nExternal Review", "Level 3\nState Complaint", "Level 4\nLegal Action", "OUTCOME"],
        ["1", "Sent: ______\nDecision: ____", "", "", "", ""],
        ["2", "Sent: ______\nDecision: ____", "", "", "", ""],
        ["3", "Sent: ______\nDecision: ____", "", "", "", ""],
        ["4", "Sent: ______\nDecision: ____", "", "", "", ""],
    ]
    col_widths = [0.55*inch, 1.4*inch, 1.4*inch, 1.4*inch, 1.3*inch, 1.2*inch]
    appeal_tbl = Table(appeal_rows, colWidths=col_widths, style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#e5e7eb")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ]))
    story.append(appeal_tbl)

    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Annual Deductible / Out-of-Pocket Tracker", h2))
    ded_rows = [
        ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        ["Deductible Met?", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["OOP Max Met?", "", "", "", "", "", "", "", "", "", "", "", ""],
    ]
    col_w = [1.2*inch] + [0.48*inch]*12
    ded_tbl = Table(ded_rows, colWidths=col_w, style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#e5e7eb")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
    ]))
    story.append(ded_tbl)

    doc.build(story, onFirstPage=doc._on_page, onLaterPages=doc._on_page)
    print(f"  ✓  04-insurance-denial-tracker.pdf")


# ─────────────────────────────────────────────────────────────────────────────
# WORKSHEET 5 — Transition Planning Master Checklist
# ─────────────────────────────────────────────────────────────────────────────

def ws_transition_checklist():
    doc, path = _base_doc(
        "05-transition-planning-checklist.pdf",
        "Transition to Adulthood Master Checklist",
        "Complete with Transition to Adulthood Planner"
    )
    h1, h2, body, note, label = _styles()
    story = []

    story += _section_header("Transition to Adulthood Master Checklist")
    story.append(Paragraph(
        "Check off each item as it is completed. Date every action. "
        "This checklist covers ages 12 through adult.",
        body
    ))
    story.append(_field_row("Child's Name"))
    story.append(_field_row("Current Age / Grade"))
    story.append(_field_row("State of Residence"))

    def age_section(title, items):
        elements = []
        elements.append(Spacer(1, 0.12 * inch))
        elements.append(Paragraph(title, h2))
        rows = []
        for item in items:
            rows.append([f"□", item, "Date: __________"])
        t = Table(rows, colWidths=[0.25*inch, 4.8*inch, 1.8*inch], style=TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9.5),
            ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [white, LIGHT]),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("GRID", (0, 0), (-1, -1), 0.3, HexColor("#e5e7eb")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        elements.append(t)
        return elements

    story += age_section("Ages 12–14: Foundation", [
        "Get on state DD agency / HCBS waiver waiting list",
        "Open ABLE account at ABLENRC.org",
        "Begin vocational exploration (interests, strengths)",
        "Start self-advocacy skill building in IEP",
        "Research guardianship alternatives (supported decision-making)",
        "Review IEP — add transition language to goals",
        "Connect with other transition-age autism families",
    ])

    story += age_section("Ages 14–16: Building Toward Independence", [
        "First formal transition IEP completed",
        "Student participates meaningfully in own IEP meeting",
        "Community-based vocational experiences begin",
        "Contact Vocational Rehabilitation (VR) — enroll",
        "Research post-secondary options (college, vocational, day programs)",
        "Begin financial planning: SSI projections, SNT planning",
        "Meet with estate planning attorney — Special Needs Trust discussion",
        "Explore guardianship alternatives with attorney",
    ])

    story += age_section("Ages 16–18: Active Transition", [
        "Transition IEP specifies: post-secondary ed, employment, independent living goals",
        "Work experience with supports (school-based or community)",
        "Vocational Rehabilitation plan in place",
        "SSI pre-application planning completed",
        "Apply for SSI at age 17 years 9 months",
        "Adult medical team identified (pediatric → adult providers)",
        "Tour adult day programs / residential options",
        "Legal decisions made: guardianship / supported decision-making documents signed",
        "Selective Service registration planned (males — required within 30 days of 18th birthday)",
    ])

    story += age_section("Age 18: Major Transition Points", [
        "SSI application submitted",
        "Selective Service registered (males)",
        "Legal decision-making documents in place",
        "Healthcare transitioned to adult providers",
        "College disability services registered (if applicable)",
        "Representative Payee established (if needed for SSI)",
        "Medicaid continuation confirmed",
    ])

    story += age_section("Ages 18–22: Final School Years (IDEA Through Age 21/22)", [
        "Maximize remaining school-based transition services",
        "Paid work experience secured and supported",
        "Independent living skills training program enrolled",
        "Adult medical team fully established and functioning",
        "Post-secondary placement finalized and started",
        "Handoff from school to adult VR and DD services complete",
        "Special Needs Trust funded",
    ])

    story += age_section("Ages 22+: Adult Life Systems", [
        "HCBS waiver services activated",
        "Employment pathway established (supported, competitive, or self-employment)",
        "Housing arranged (family home, shared living, own home, group home)",
        "Annual SSI review completed",
        "Community participation and social connections in place",
        "Annual review of ABLE account and Special Needs Trust",
        "Letter of Intent updated annually",
    ])

    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Key Contacts & Agencies", h2))
    for row in [
        "State DD Agency Name & Phone",
        "Vocational Rehabilitation Counselor",
        "SSI / SSA Case Number & Phone",
        "Special Needs Trust Attorney",
        "ABLE Account Number / Plan",
        "Adult Medical Provider (Primary Care)",
        "Adult Psychiatrist / Behavioral Health",
    ]:
        story.append(_field_row(row))

    doc.build(story, onFirstPage=doc._on_page, onLaterPages=doc._on_page)
    print(f"  ✓  05-transition-planning-checklist.pdf")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\nGenerating SpectrumReady fillable worksheets...\n")
    ws_benefits_audit()
    ws_iep_prep()
    ws_therapy_comparison()
    ws_insurance_tracker()
    ws_transition_checklist()
    print(f"\nAll worksheets saved to: {OUT_DIR}\n")
