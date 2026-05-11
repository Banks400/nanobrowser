"""
SpectrumReady Letter Template Generator
Creates 7 ready-to-send .docx letter templates for autism families.
Run: python3 generate_templates.py
Output: autism-resources-business/products/templates/
"""

import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "products", "templates")
os.makedirs(OUT_DIR, exist_ok=True)

PURPLE = RGBColor(0x4F, 0x46, 0xE5)
DARK   = RGBColor(0x1E, 0x1B, 0x4B)
GREY   = RGBColor(0x6B, 0x72, 0x80)


def _set_font(run, size_pt, bold=False, color=None):
    run.font.name = "Calibri"
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color


def _heading(doc, text, size=13, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    _set_font(run, size, bold=True, color=color or DARK)
    return p


def _body(doc, text, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    _set_font(run, 11)
    return p


def _field(doc, label, placeholder=""):
    """Renders a fill-in line: Label: ____________________"""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    label_run = p.add_run(f"{label}:  ")
    _set_font(label_run, 11, bold=True)
    fill_run = p.add_run(placeholder if placeholder else "_" * 40)
    _set_font(fill_run, 11, color=GREY)
    return p


def _divider(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("─" * 72)
    _set_font(run, 9, color=RGBColor(0xD1, 0xD5, 0xDB))


def _header_block(doc, title):
    """Brand header + title banner."""
    brand = doc.add_paragraph()
    brand.paragraph_format.space_after = Pt(2)
    r = brand.add_run("SpectrumReady")
    _set_font(r, 10, bold=True, color=PURPLE)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(16)
    r2 = p.add_run(title)
    _set_font(r2, 18, bold=True, color=DARK)

    _divider(doc)


def _instruction_box(doc, text):
    """Grey italic instruction note."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run(f"📋  {text}")
    run.italic = True
    _set_font(run, 10, color=GREY)
    run.italic = True


def _footer(doc):
    _divider(doc)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    r = p.add_run(
        "Template provided by SpectrumReady · spectrumready.com · "
        "Not legal advice — consult an attorney for complex situations."
    )
    _set_font(r, 8, color=GREY)


# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATE 1 — IEP Evaluation Request Letter
# ─────────────────────────────────────────────────────────────────────────────

def tpl_iep_eval_request():
    doc = Document()
    doc.sections[0].left_margin = Inches(1.1)
    doc.sections[0].right_margin = Inches(1.1)
    doc.sections[0].top_margin = Inches(1.0)
    doc.sections[0].bottom_margin = Inches(1.0)

    _header_block(doc, "Letter: Request for Special Education Evaluation")
    _instruction_box(doc,
        "HOW TO USE: Fill in every [bracketed field]. Send via email AND certified mail. "
        "Keep a copy. This letter starts the legal 60-day evaluation clock."
    )

    _field(doc, "Today's Date")
    _field(doc, "Your Name")
    _field(doc, "Your Address")
    _field(doc, "City, State, ZIP")
    doc.add_paragraph()
    _field(doc, "Principal / Special Ed Director Name")
    _field(doc, "School Name")
    _field(doc, "School Address")

    doc.add_paragraph()
    _body(doc, "Dear [Principal/Director Name],")
    doc.add_paragraph()
    _body(doc,
        "I am writing to formally request a comprehensive special education evaluation "
        "for my child, [CHILD'S FULL NAME], date of birth [DOB], currently enrolled in "
        "[GRADE] at [SCHOOL NAME]."
    )
    _body(doc,
        "I am requesting this evaluation because I have observed the following concerns "
        "that may indicate the need for special education services:"
    )

    for concern in [
        "[Describe concern #1 — be specific, e.g., 'difficulty with social interaction with peers']",
        "[Describe concern #2 — e.g., 'significant delays in expressive language']",
        "[Describe concern #3 — e.g., 'difficulty transitioning between activities']",
    ]:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(concern)
        _set_font(run, 11, color=GREY)

    doc.add_paragraph()
    _body(doc,
        "My child has a diagnosis of [DIAGNOSIS, e.g., Autism Spectrum Disorder] from "
        "[DIAGNOSING PROVIDER], issued on [DATE]. I am enclosing a copy of the diagnostic "
        "report with this letter."
    )
    _body(doc,
        "I understand that under the Individuals with Disabilities Education Act (IDEA), "
        "the district has 60 days from the date you receive my written consent to complete "
        "the evaluation and provide me with the results. Please send me the Prior Written "
        "Notice and Parental Consent form as soon as possible."
    )
    _body(doc,
        "Please confirm receipt of this letter in writing. I look forward to working "
        "collaboratively with the school team to understand my child's needs."
    )

    doc.add_paragraph()
    _body(doc, "Sincerely,")
    doc.add_paragraph()
    _field(doc, "Your Name (Signature)")
    _field(doc, "Phone Number")
    _field(doc, "Email Address")
    _field(doc, "Relationship to Child")

    _footer(doc)
    path = os.path.join(OUT_DIR, "01-iep-evaluation-request.docx")
    doc.save(path)
    print(f"  ✓  01-iep-evaluation-request.docx")


# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATE 2 — IEP Meeting Follow-Up / Prior Written Notice Request
# ─────────────────────────────────────────────────────────────────────────────

def tpl_iep_followup():
    doc = Document()
    doc.sections[0].left_margin = Inches(1.1)
    doc.sections[0].right_margin = Inches(1.1)
    doc.sections[0].top_margin = Inches(1.0)
    doc.sections[0].bottom_margin = Inches(1.0)

    _header_block(doc, "Letter: IEP Meeting Follow-Up & Prior Written Notice Request")
    _instruction_box(doc,
        "HOW TO USE: Send within 48 hours of any IEP meeting where the school made a "
        "decision you disagree with, or where a service was denied. Always request a "
        "Prior Written Notice (PWN) in writing — it protects your appeal rights."
    )

    _field(doc, "Today's Date")
    _field(doc, "Your Name")
    doc.add_paragraph()
    _field(doc, "Special Education Director")
    _field(doc, "School District Name")

    doc.add_paragraph()
    _body(doc, "Dear [Special Education Director Name],")
    doc.add_paragraph()
    _body(doc,
        "I am writing to follow up on the IEP meeting held on [DATE] regarding my child, "
        "[CHILD'S NAME]. I want to confirm my understanding of the decisions made and "
        "formally request Prior Written Notice for the following:"
    )

    for item in [
        "[Decision or denial #1 — e.g., 'Denial of our request for 25 hours/week of ABA therapy']",
        "[Decision or denial #2 — e.g., 'Proposed placement in self-contained classroom']",
        "[Decision or denial #3 — if applicable]",
    ]:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(item)
        _set_font(run, 11, color=GREY)

    doc.add_paragraph()
    _body(doc,
        "Under IDEA, the school must provide Prior Written Notice before changing or "
        "refusing to change the identification, evaluation, educational placement, or "
        "provision of FAPE for my child. The PWN must include: (1) a description of the "
        "action proposed or refused, (2) an explanation of why the district proposes or "
        "refuses to take the action, and (3) a description of each evaluation procedure, "
        "assessment, record, or report used as a basis for the proposed or refused action."
    )
    _body(doc,
        "Please provide this Prior Written Notice within a reasonable timeframe. "
        "I reserve all rights under IDEA, including the right to request an Independent "
        "Educational Evaluation (IEE) at public expense if I disagree with the district's "
        "evaluation, and the right to file a state complaint or request a due process "
        "hearing if we cannot resolve our disagreement."
    )
    _body(doc, "I look forward to your written response.")

    doc.add_paragraph()
    _body(doc, "Sincerely,")
    doc.add_paragraph()
    _field(doc, "Your Name")
    _field(doc, "Phone / Email")

    _footer(doc)
    path = os.path.join(OUT_DIR, "02-iep-followup-pwn-request.docx")
    doc.save(path)
    print(f"  ✓  02-iep-followup-pwn-request.docx")


# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATE 3 — Letter of Medical Necessity (for physician signature)
# ─────────────────────────────────────────────────────────────────────────────

def tpl_lmn():
    doc = Document()
    doc.sections[0].left_margin = Inches(1.1)
    doc.sections[0].right_margin = Inches(1.1)
    doc.sections[0].top_margin = Inches(1.0)
    doc.sections[0].bottom_margin = Inches(1.0)

    _header_block(doc, "Letter of Medical Necessity (Physician Template)")
    _instruction_box(doc,
        "HOW TO USE: Bring this completed draft to your child's physician, developmental "
        "pediatrician, or psychiatrist and ask them to review, modify as needed, and sign "
        "on their letterhead. Submit to your insurance company with every prior "
        "authorization request and appeal."
    )

    _field(doc, "Date")
    _field(doc, "Physician Name / Practice")
    _field(doc, "Physician Address")
    doc.add_paragraph()
    _field(doc, "Insurance Company Name")
    _field(doc, "Member ID")
    _field(doc, "Group Number")

    doc.add_paragraph()
    _body(doc, "To Whom It May Concern,")
    doc.add_paragraph()
    _body(doc,
        "I am writing on behalf of my patient, [CHILD'S FULL NAME], date of birth [DOB], "
        "to establish medical necessity for [THERAPY TYPE, e.g., Applied Behavior Analysis "
        "(ABA) therapy] at the intensity of [NUMBER] hours per week."
    )

    _heading(doc, "Diagnosis and Clinical Background", 12)
    _body(doc,
        "[CHILD'S NAME] carries a confirmed diagnosis of Autism Spectrum Disorder (DSM-5-TR), "
        "Level [1/2/3], established by [EVALUATION TYPE, e.g., ADOS-2 and comprehensive "
        "neuropsychological evaluation] on [DATE OF DIAGNOSIS] by [EVALUATING CLINICIAN, "
        "CREDENTIALS, INSTITUTION]."
    )
    _body(doc,
        "The diagnosis is associated with the following clinically significant impairments:"
    )
    for item in [
        "[Impairment #1 — e.g., 'Severe expressive language delays; uses fewer than 20 functional words']",
        "[Impairment #2 — e.g., 'Significantly restricted social initiation and peer interaction']",
        "[Impairment #3 — e.g., 'Self-injurious behavior (head banging) occurring 15+ times/day']",
        "[Impairment #4 — as applicable]",
    ]:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(item)
        _set_font(run, 11, color=GREY)

    _heading(doc, "Treatment Requested and Clinical Rationale", 12)
    _body(doc,
        "I am requesting authorization for [NUMBER] hours per week of [THERAPY], "
        "provided by a Board Certified Behavior Analyst (BCBA) with RBT-supervised "
        "direct therapy sessions. This recommendation is consistent with:"
    )
    for item in [
        "American Academy of Pediatrics Clinical Report on ABA therapy for autism (2020)",
        "US Surgeon General's Report on Mental Health",
        "The evidence base for early intensive behavioral intervention (Lovaas, 1987; NASN, 2009; NAC, 2015)",
        "The clinical guidelines of [BCBA SUPERVISOR'S NAME]'s individualized treatment assessment",
    ]:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(item)
        _set_font(run, 11)

    _heading(doc, "Prognosis Without Treatment", 12)
    _body(doc,
        "Without the requested level of intervention, it is my clinical opinion that "
        "[CHILD'S NAME]'s functional deficits are expected to [worsen / fail to improve "
        "at a clinically meaningful rate], increasing the long-term burden of disability "
        "and reducing the probability of achieving meaningful functional independence."
    )

    doc.add_paragraph()
    _body(doc,
        "I am available to discuss this case with your medical director. Please contact "
        "me at [PHYSICIAN PHONE] or [PHYSICIAN EMAIL]."
    )
    doc.add_paragraph()
    _body(doc, "Sincerely,")
    doc.add_paragraph()
    _field(doc, "Physician Signature")
    _field(doc, "Printed Name & Credentials")
    _field(doc, "NPI Number")
    _field(doc, "Practice / Institution")
    _field(doc, "Phone / Fax")
    _field(doc, "Date")

    _footer(doc)
    path = os.path.join(OUT_DIR, "03-letter-of-medical-necessity.docx")
    doc.save(path)
    print(f"  ✓  03-letter-of-medical-necessity.docx")


# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATE 4 — Insurance Prior Authorization Request
# ─────────────────────────────────────────────────────────────────────────────

def tpl_insurance_prior_auth():
    doc = Document()
    doc.sections[0].left_margin = Inches(1.1)
    doc.sections[0].right_margin = Inches(1.1)
    doc.sections[0].top_margin = Inches(1.0)
    doc.sections[0].bottom_margin = Inches(1.0)

    _header_block(doc, "Letter: Insurance Prior Authorization Request")
    _instruction_box(doc,
        "HOW TO USE: Submit to your insurance company's Prior Authorization department "
        "by fax and certified mail. Attach: (1) Letter of Medical Necessity, "
        "(2) ABA assessment from BCBA, (3) autism diagnosis report. "
        "Keep fax confirmation receipts."
    )

    _field(doc, "Date")
    _field(doc, "Your Name")
    _field(doc, "Member ID")
    _field(doc, "Group Number")
    doc.add_paragraph()
    _field(doc, "Insurance Company Name")
    _field(doc, "Prior Authorization Department Address/Fax")

    doc.add_paragraph()
    _body(doc, "To the Prior Authorization Department,")
    doc.add_paragraph()
    _body(doc,
        "I am the parent/guardian of [CHILD'S NAME], DOB [DOB], a member under policy "
        "[POLICY NUMBER]. I am requesting prior authorization for the following services:"
    )

    _heading(doc, "Service Requested", 12)
    for row in [
        ("Service Type", "[e.g., Applied Behavior Analysis (ABA) Therapy]"),
        ("CPT Code(s)", "[e.g., 97151, 97153, 97155]"),
        ("Requesting Provider", "[BCBA Name, Credentials, NPI]"),
        ("Hours Requested", "[e.g., 30 hours/week]"),
        ("Duration", "[e.g., 12 months]"),
        ("Start Date Requested", "[Date]"),
    ]:
        _field(doc, row[0], row[1])

    _heading(doc, "Legal and Clinical Basis", 12)
    _body(doc,
        "This request is supported by: (1) a confirmed diagnosis of Autism Spectrum "
        "Disorder (see attached diagnosis report), (2) a Letter of Medical Necessity "
        "from [PHYSICIAN NAME], (3) an ABA assessment from [BCBA NAME] recommending "
        "this level of service, and (4) the following legal requirements:"
    )
    for item in [
        "State autism insurance mandate: [YOUR STATE] requires coverage of ABA therapy for autism",
        "Mental Health Parity and Addiction Equity Act (MHPAEA): behavioral health services must be covered no more restrictively than medical/surgical benefits",
        "ACA Essential Health Benefits: mental and behavioral health services are required EHBs",
    ]:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(item)
        _set_font(run, 11)

    doc.add_paragraph()
    _body(doc,
        "Please process this request within the timeframe required by law. If you intend "
        "to deny or modify this request, I request written Prior Authorization denial "
        "notice specifying the clinical criteria used to reach the decision and information "
        "about my appeal rights."
    )

    doc.add_paragraph()
    _body(doc, "Sincerely,")
    doc.add_paragraph()
    _field(doc, "Parent/Guardian Name")
    _field(doc, "Relationship to Member")
    _field(doc, "Phone / Email")

    _footer(doc)
    path = os.path.join(OUT_DIR, "04-insurance-prior-auth-request.docx")
    doc.save(path)
    print(f"  ✓  04-insurance-prior-auth-request.docx")


# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATE 5 — Insurance Appeal Letter (Level 1 Internal)
# ─────────────────────────────────────────────────────────────────────────────

def tpl_insurance_appeal():
    doc = Document()
    doc.sections[0].left_margin = Inches(1.1)
    doc.sections[0].right_margin = Inches(1.1)
    doc.sections[0].top_margin = Inches(1.0)
    doc.sections[0].bottom_margin = Inches(1.0)

    _header_block(doc, "Letter: Level 1 Internal Insurance Appeal")
    _instruction_box(doc,
        "HOW TO USE: Send within 180 days of your denial notice. Send by certified mail "
        "AND fax to the appeals department. Keep all receipts. If this appeal is denied, "
        "you are entitled to an External Independent Review — request it immediately."
    )

    _field(doc, "Date")
    _field(doc, "Your Name")
    _field(doc, "Member ID / Claim Number")
    doc.add_paragraph()
    _field(doc, "Insurance Company Appeals Department")
    _field(doc, "Address")

    doc.add_paragraph()
    _body(doc, "RE: Formal Appeal of Denial — Claim/Authorization # [NUMBER] — [CHILD'S NAME]")
    doc.add_paragraph()
    _body(doc, "To the Appeals Department,")
    doc.add_paragraph()
    _body(doc,
        "I am formally appealing the denial issued on [DENIAL DATE] for [SERVICE DENIED, "
        "e.g., Applied Behavior Analysis therapy for my child, [CHILD'S NAME], DOB [DOB]]. "
        "The stated reason for denial was: [QUOTE THE EXACT DENIAL REASON FROM THE LETTER]."
    )

    _heading(doc, "Why This Denial Is Incorrect", 12)
    _body(doc,
        "This denial is inconsistent with applicable law and clinical evidence for the "
        "following reasons:"
    )
    for item in [
        "Medical Necessity: ABA therapy is medically necessary for [CHILD'S NAME] as documented by the attached Letter of Medical Necessity from [PHYSICIAN NAME, CREDENTIALS].",
        "Not Experimental: ABA therapy has over 60 years of peer-reviewed research and is endorsed by the American Academy of Pediatrics, the US Surgeon General, and the American Psychological Association. It is not experimental.",
        "State Mandate: [YOUR STATE]'s autism insurance mandate requires coverage of ABA therapy. This denial violates state law.",
        "Federal Parity: Under MHPAEA, you cannot impose treatment limitations on ABA therapy that are more restrictive than limitations on analogous medical/surgical services.",
    ]:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(item)
        _set_font(run, 11)

    _heading(doc, "Documentation Attached", 12)
    for item in [
        "Letter of Medical Necessity — [PHYSICIAN NAME], dated [DATE]",
        "Autism diagnosis report — [EVALUATOR], dated [DATE]",
        "ABA assessment and treatment recommendation — [BCBA NAME], dated [DATE]",
        "[Any additional supporting documentation]",
    ]:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(item)
        _set_font(run, 11, color=GREY)

    doc.add_paragraph()
    _body(doc,
        "I request that you overturn this denial and authorize the requested services. "
        "If this appeal is denied, I request: (1) written explanation of the denial with "
        "specific clinical criteria, and (2) information about my right to an External "
        "Independent Review. I also reserve the right to file a complaint with the "
        "[YOUR STATE] Department of Insurance."
    )

    doc.add_paragraph()
    _body(doc, "Sincerely,")
    doc.add_paragraph()
    _field(doc, "Parent/Guardian Name")
    _field(doc, "Phone / Email")

    _footer(doc)
    path = os.path.join(OUT_DIR, "05-insurance-appeal-level1.docx")
    doc.save(path)
    print(f"  ✓  05-insurance-appeal-level1.docx")


# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATE 6 — SSI Application Cover Letter
# ─────────────────────────────────────────────────────────────────────────────

def tpl_ssi_application():
    doc = Document()
    doc.sections[0].left_margin = Inches(1.1)
    doc.sections[0].right_margin = Inches(1.1)
    doc.sections[0].top_margin = Inches(1.0)
    doc.sections[0].bottom_margin = Inches(1.0)

    _header_block(doc, "Letter: SSI Application Cover Letter & Document Checklist")
    _instruction_box(doc,
        "HOW TO USE: Submit this cover letter with your SSI application package at your "
        "local Social Security office. Keep a stamped copy. Apply at SSA.gov or call "
        "1-800-772-1213. Children can apply online or in person."
    )

    _field(doc, "Date")
    _field(doc, "Your Name")
    _field(doc, "Address")
    _field(doc, "Phone Number")
    doc.add_paragraph()
    _body(doc, "Social Security Administration")
    _field(doc, "Local SSA Office Address")

    doc.add_paragraph()
    _body(doc,
        "RE: SSI Disability Application for [CHILD'S FULL NAME], DOB [DOB], "
        "SSN [CHILD'S SSN]"
    )
    doc.add_paragraph()
    _body(doc, "To the Social Security Administration,")
    doc.add_paragraph()
    _body(doc,
        "I am submitting this application for Supplemental Security Income (SSI) on "
        "behalf of my child, [CHILD'S NAME], who has been diagnosed with [DIAGNOSIS]. "
        "I am [CHILD'S NAME]'s [mother/father/legal guardian]."
    )
    _body(doc,
        "My child meets the SSA's definition of disability based on significant functional "
        "limitations in multiple domains, including [LIST KEY DOMAINS, e.g., 'interacting "
        "and relating with others' and 'acquiring and using information']. These limitations "
        "are documented in the materials enclosed with this application."
    )

    _heading(doc, "Documents Included With This Application", 12)
    for item in [
        "Child's birth certificate",
        "Child's Social Security card",
        "Autism diagnosis report from [EVALUATOR NAME], dated [DATE]",
        "Completed Child Function Report (SSA-3375)",
        "Medical records from [PRIMARY PHYSICIAN], covering [DATE RANGE]",
        "School records / IEP, issued [DATE]",
        "Therapy records from [PROVIDER(S)]",
        "Parent household income documentation (pay stubs, tax return)",
        "[Any additional documentation]",
    ]:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(item)
        _set_font(run, 11, color=GREY)

    _heading(doc, "Most Important Functional Limitations", 12)
    _body(doc,
        "To assist your review, the following are the most significant daily functioning "
        "limitations my child experiences:"
    )
    for item in [
        "[Limitation #1 — describe worst-day behavior in detail, e.g., 'Cannot communicate basic needs verbally; uses gestures or cries only']",
        "[Limitation #2 — e.g., 'Requires physical prompting for all self-care tasks including dressing and toileting']",
        "[Limitation #3 — e.g., 'Has 3-5 meltdowns per day lasting 20-40 minutes each, triggered by sensory input or schedule changes']",
    ]:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(item)
        _set_font(run, 11, color=GREY)

    doc.add_paragraph()
    _body(doc,
        "Please contact me if you need additional information. I am available at "
        "[PHONE NUMBER] between [HOURS]."
    )

    doc.add_paragraph()
    _body(doc, "Sincerely,")
    doc.add_paragraph()
    _field(doc, "Parent/Guardian Name")
    _field(doc, "Relationship to Child")
    _field(doc, "Phone / Email")

    _footer(doc)
    path = os.path.join(OUT_DIR, "06-ssi-application-cover-letter.docx")
    doc.save(path)
    print(f"  ✓  06-ssi-application-cover-letter.docx")


# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATE 7 — SSI Denial Appeal Letter
# ─────────────────────────────────────────────────────────────────────────────

def tpl_ssi_appeal():
    doc = Document()
    doc.sections[0].left_margin = Inches(1.1)
    doc.sections[0].right_margin = Inches(1.1)
    doc.sections[0].top_margin = Inches(1.0)
    doc.sections[0].bottom_margin = Inches(1.0)

    _header_block(doc, "Letter: SSI Denial — Request for Reconsideration")
    _instruction_box(doc,
        "HOW TO USE: You have 60 days from the date of your denial notice to request "
        "reconsideration. Do not miss this deadline. Submit online at SSA.gov, by phone "
        "(1-800-772-1213), or in person. ~60% of reconsidered claims are approved."
    )

    _field(doc, "Date")
    _field(doc, "Your Name")
    _field(doc, "Address")
    _field(doc, "SSN of Claimant (Child)")
    doc.add_paragraph()
    _body(doc, "Social Security Administration")
    _field(doc, "Local SSA Office Address")

    doc.add_paragraph()
    _body(doc,
        "RE: Request for Reconsideration — SSI Claim for [CHILD'S NAME], DOB [DOB], "
        "Claim #[CLAIM NUMBER], Denied [DENIAL DATE]"
    )
    doc.add_paragraph()
    _body(doc, "To the Social Security Administration,")
    doc.add_paragraph()
    _body(doc,
        "I am formally requesting reconsideration of the denial of my child's SSI "
        "application. [CHILD'S NAME] has a confirmed diagnosis of Autism Spectrum Disorder "
        "and has significant functional limitations that meet the SSA's definition of "
        "childhood disability."
    )

    _heading(doc, "Basis for Appeal", 12)
    _body(doc,
        "The denial does not accurately reflect the severity of [CHILD'S NAME]'s "
        "functional limitations. Specifically:"
    )
    for item in [
        "[Reason #1 — e.g., 'The denial states my child has only mild limitations in interacting with others. In fact, [NAME] cannot initiate any peer interaction and requires constant adult supervision during all social situations, as documented in the enclosed school records.']",
        "[Reason #2 — e.g., 'The evaluation did not appear to consider the medical records from [PROVIDER], which document [specific limitation].']",
        "[Reason #3 — as applicable]",
    ]:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(item)
        _set_font(run, 11, color=GREY)

    _heading(doc, "Additional Documentation Enclosed", 12)
    for item in [
        "Updated letter from [PHYSICIAN NAME] documenting current functional limitations",
        "Updated school IEP or progress report, dated [DATE]",
        "Updated therapy records from [PROVIDER], dated [DATE]",
        "Completed updated Child Function Report (SSA-3375-F6) with detailed descriptions of worst-day functioning",
    ]:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(item)
        _set_font(run, 11, color=GREY)

    doc.add_paragraph()
    _body(doc,
        "I respectfully request that you reconsider this claim and approve SSI benefits "
        "for my child. If reconsideration is denied, I request a hearing before an "
        "Administrative Law Judge."
    )

    doc.add_paragraph()
    _body(doc, "Sincerely,")
    doc.add_paragraph()
    _field(doc, "Parent/Guardian Name")
    _field(doc, "Relationship to Child")
    _field(doc, "Phone / Email")

    _footer(doc)
    path = os.path.join(OUT_DIR, "07-ssi-denial-appeal.docx")
    doc.save(path)
    print(f"  ✓  07-ssi-denial-appeal.docx")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\nGenerating SpectrumReady letter templates...\n")
    tpl_iep_eval_request()
    tpl_iep_followup()
    tpl_lmn()
    tpl_insurance_prior_auth()
    tpl_insurance_appeal()
    tpl_ssi_application()
    tpl_ssi_appeal()
    print(f"\nAll templates saved to: {OUT_DIR}\n")
