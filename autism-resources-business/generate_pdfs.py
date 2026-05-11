"""
SpectrumReady PDF Generator
Converts guide content into professionally styled PDF files using WeasyPrint.
Run: python3 generate_pdfs.py
Output: autism-resources-business/products/pdfs/
"""

import os
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# ── Output directory ──────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "products", "pdfs")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Brand palette ─────────────────────────────────────────────────────────────
PURPLE   = "#6366f1"
PURPLE_D = "#4f46e5"
PURPLE_L = "#ede9fe"
AMBER    = "#f59e0b"
DARK     = "#1e1b4b"
GREY     = "#6b7280"
LIGHT    = "#f9fafb"
WHITE    = "#ffffff"
TEXT     = "#111827"

# ── Shared CSS ────────────────────────────────────────────────────────────────
BASE_CSS = f"""
@page {{
  size: letter;
  margin: 0.75in 0.85in 0.85in 0.85in;
  @bottom-center {{
    content: counter(page) " of " counter(pages);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 9pt;
    color: {GREY};
  }}
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 10.5pt;
  color: {TEXT};
  line-height: 1.65;
  background: {WHITE};
}}

/* ── COVER ── */
.cover {{
  page: cover;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: linear-gradient(160deg, {DARK} 0%, {PURPLE_D} 60%, {PURPLE} 100%);
  padding: 2in 0.85in 0.7in;
  break-after: page;
}}

@page cover {{ margin: 0; @bottom-center {{ content: none; }} }}

.cover-badge {{
  display: inline-block;
  background: rgba(255,255,255,0.15);
  border: 1pt solid rgba(255,255,255,0.3);
  color: #c7d2fe;
  padding: 4pt 12pt;
  border-radius: 20pt;
  font-size: 9pt;
  font-weight: 600;
  letter-spacing: 0.04em;
  margin-bottom: 24pt;
  width: fit-content;
}}

.cover-title {{
  font-size: 32pt;
  font-weight: 900;
  color: {WHITE};
  line-height: 1.15;
  margin-bottom: 16pt;
}}

.cover-subtitle {{
  font-size: 14pt;
  color: rgba(255,255,255,0.75);
  font-weight: 400;
  line-height: 1.5;
  max-width: 5in;
  margin-bottom: 32pt;
}}

.cover-price-tag {{
  display: inline-block;
  background: {AMBER};
  color: {DARK};
  font-size: 13pt;
  font-weight: 800;
  padding: 6pt 18pt;
  border-radius: 6pt;
  margin-bottom: 40pt;
}}

.cover-footer {{
  border-top: 1pt solid rgba(255,255,255,0.2);
  padding-top: 16pt;
  display: flex;
  justify-content: space-between;
  align-items: center;
}}

.cover-brand {{
  color: {WHITE};
  font-size: 13pt;
  font-weight: 800;
}}

.cover-url {{
  color: rgba(255,255,255,0.55);
  font-size: 9pt;
}}

/* ── TABLE OF CONTENTS ── */
.toc-page {{
  break-after: page;
  padding: 0.3in 0;
}}

.toc-title {{
  font-size: 18pt;
  font-weight: 800;
  color: {PURPLE_D};
  margin-bottom: 20pt;
  padding-bottom: 10pt;
  border-bottom: 2pt solid {PURPLE_L};
}}

.toc-section {{
  margin-bottom: 6pt;
}}

.toc-main {{
  display: flex;
  justify-content: space-between;
  font-size: 11pt;
  font-weight: 600;
  color: {TEXT};
  padding: 5pt 0;
  border-bottom: 1pt dotted #d1d5db;
}}

.toc-sub {{
  display: flex;
  justify-content: space-between;
  font-size: 9.5pt;
  color: {GREY};
  padding: 3pt 0 3pt 14pt;
}}

/* ── CONTENT ── */
h1 {{
  font-size: 20pt;
  font-weight: 900;
  color: {PURPLE_D};
  margin: 24pt 0 10pt;
  padding-bottom: 8pt;
  border-bottom: 2.5pt solid {PURPLE};
  break-after: avoid;
}}

h2 {{
  font-size: 14pt;
  font-weight: 800;
  color: {DARK};
  margin: 22pt 0 8pt;
  break-after: avoid;
}}

h3 {{
  font-size: 12pt;
  font-weight: 700;
  color: {PURPLE_D};
  margin: 18pt 0 6pt;
  break-after: avoid;
}}

h4 {{
  font-size: 10.5pt;
  font-weight: 700;
  color: {TEXT};
  margin: 14pt 0 4pt;
  break-after: avoid;
}}

p {{
  margin-bottom: 9pt;
}}

strong {{ font-weight: 700; color: {TEXT}; }}
em {{ font-style: italic; }}

/* ── LISTS ── */
ul, ol {{
  margin: 6pt 0 12pt 18pt;
}}

li {{
  margin-bottom: 5pt;
  line-height: 1.6;
}}

/* ── TABLES ── */
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 14pt 0 18pt;
  font-size: 9.5pt;
  break-inside: avoid;
}}

th {{
  background: {PURPLE};
  color: {WHITE};
  padding: 7pt 10pt;
  text-align: left;
  font-weight: 700;
  font-size: 9pt;
}}

td {{
  padding: 6pt 10pt;
  border-bottom: 1pt solid {PURPLE_L};
  vertical-align: top;
}}

tr:nth-child(even) td {{ background: {LIGHT}; }}

/* ── CALLOUT BOXES ── */
.callout {{
  background: {PURPLE_L};
  border-left: 4pt solid {PURPLE};
  border-radius: 4pt;
  padding: 12pt 14pt;
  margin: 14pt 0;
  break-inside: avoid;
}}

.callout-warning {{
  background: #fef3c7;
  border-left-color: {AMBER};
}}

.callout-success {{
  background: #d1fae5;
  border-left-color: #10b981;
}}

.callout-title {{
  font-weight: 800;
  font-size: 9.5pt;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 5pt;
  color: {PURPLE_D};
}}

.callout-warning .callout-title {{ color: #92400e; }}
.callout-success .callout-title {{ color: #065f46; }}

/* ── CHECKLIST ── */
.checklist {{
  list-style: none;
  margin-left: 0;
  padding: 0;
}}

.checklist li {{
  padding: 4pt 0 4pt 22pt;
  position: relative;
  border-bottom: 1pt solid #e5e7eb;
  font-size: 10pt;
}}

.checklist li::before {{
  content: "☐";
  position: absolute;
  left: 0;
  color: {PURPLE};
  font-size: 12pt;
  top: 2pt;
}}

/* ── SECTION HEADER BAND ── */
.section-band {{
  background: {PURPLE_L};
  border-radius: 6pt;
  padding: 10pt 14pt;
  margin: 20pt 0 14pt;
  break-after: avoid;
}}

.section-band h2 {{
  margin: 0;
  font-size: 13pt;
  color: {PURPLE_D};
  border: none;
  padding: 0;
}}

/* ── FOOTER STRIP ── */
.page-footer {{
  position: fixed;
  bottom: 0.3in;
  left: 0.85in;
  right: 0.85in;
  font-size: 8pt;
  color: #9ca3af;
  text-align: right;
  border-top: 1pt solid #e5e7eb;
  padding-top: 4pt;
}}

/* ── BACK COVER ── */
.back-cover {{
  page: back;
  break-before: page;
  height: 100vh;
  background: {DARK};
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 1in;
}}

@page back {{ margin: 0; @bottom-center {{ content: none; }} }}

.back-brand {{ font-size: 22pt; font-weight: 900; color: {WHITE}; margin-bottom: 12pt; }}
.back-tagline {{ font-size: 12pt; color: rgba(255,255,255,0.65); margin-bottom: 30pt; }}
.back-url {{ font-size: 11pt; color: #a5b4fc; font-weight: 600; margin-bottom: 8pt; }}
.back-email {{ font-size: 10pt; color: rgba(255,255,255,0.5); margin-bottom: 30pt; }}
.back-disclaimer {{
  font-size: 8pt;
  color: rgba(255,255,255,0.3);
  max-width: 5in;
  line-height: 1.5;
  margin-top: 20pt;
}}
.back-copyright {{ font-size: 9pt; color: rgba(255,255,255,0.4); margin-top: 16pt; }}
"""


# ── HTML template builder ─────────────────────────────────────────────────────

def build_pdf(title: str, subtitle: str, price: str, badge: str, toc: list[tuple], body_html: str, filename: str):
    """Render one guide to PDF."""

    toc_html = "".join(
        f'<div class="toc-section"><div class="toc-main"><span>{t}</span><span>{p}</span></div></div>'
        for t, p in toc
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>{title}</title></head>
<body>

<!-- COVER -->
<div class="cover">
  <div>
    <div class="cover-badge">SpectrumReady Digital Guide</div>
    <div class="cover-title">{title}</div>
    <div class="cover-subtitle">{subtitle}</div>
    <div class="cover-price-tag">{price}</div>
  </div>
  <div class="cover-footer">
    <div class="cover-brand">SpectrumReady</div>
    <div class="cover-url">spectrumready.com</div>
  </div>
</div>

<!-- DISCLAIMER PAGE (page 2 of every guide) -->
<div style="break-before: page; padding: 0.3in 0; break-after: page;">
  <div style="border: 2pt solid #e5e7eb; border-radius: 8pt; padding: 24pt 28pt; background: #f9fafb;">
    <div style="font-size: 13pt; font-weight: 800; color: #1e1b4b; margin-bottom: 14pt; border-bottom: 2pt solid #6366f1; padding-bottom: 8pt;">
      Important Notice — Please Read Before Proceeding
    </div>
    <p style="margin-bottom: 10pt; font-size: 10pt;"><strong>Educational Information Only.</strong> This guide is for general informational and educational purposes only. It does not constitute legal, financial, or medical advice. The information in this guide is not a substitute for advice from a licensed attorney, financial advisor, healthcare provider, or other qualified professional.</p>
    <p style="margin-bottom: 10pt; font-size: 10pt;"><strong>No Professional Relationship.</strong> Reading this guide does not create an attorney-client, financial advisor-client, or any other professional relationship between you and SpectrumReady.</p>
    <p style="margin-bottom: 10pt; font-size: 10pt;"><strong>Time-Sensitive Information.</strong> Government benefit amounts, income thresholds, and program eligibility rules change regularly. Dollar figures and thresholds in this guide reflect information as of 2025. Always verify current amounts and rules directly with the relevant federal or state agency before making any decisions.</p>
    <p style="margin-bottom: 10pt; font-size: 10pt;"><strong>Individual Circumstances Vary.</strong> Eligibility for the programs discussed depends on your individual circumstances. This guide describes how programs generally work — not whether you or your child specifically qualifies.</p>
    <p style="font-size: 10pt;"><strong>Consult Professionals.</strong> For decisions about your child's specific situation — including SSI applications, IEP disputes, insurance appeals, or estate planning — consult a qualified special education attorney, disability benefits counselor, or other licensed professional.</p>
  </div>
  <p style="margin-top: 16pt; font-size: 8.5pt; color: #9ca3af; text-align: center;">© 2025 SpectrumReady | spectrumready.com | Content current as of 2025</p>
</div>

<!-- TABLE OF CONTENTS -->
<div class="toc-page">
  <div class="toc-title">Table of Contents</div>
  {toc_html}
</div>

<!-- BODY -->
{body_html}

<!-- BACK COVER -->
<div class="back-cover">
  <div class="back-brand">SpectrumReady</div>
  <div class="back-tagline">Empowering autism families with the knowledge they deserve.</div>
  <div class="back-url">spectrumready.com</div>
  <div class="back-email">support@spectrumready.com</div>
  <div class="back-disclaimer">
    This guide is for informational purposes only and does not constitute legal, financial, or medical advice.
    Program rules and benefit amounts are subject to change — verify current information with the relevant agency.
    For complex situations, consult a qualified professional.
  </div>
  <div class="back-copyright">© 2025 SpectrumReady. All rights reserved. For personal use only. Not for redistribution or resale.</div>
</div>

</body></html>"""

    font_config = FontConfiguration()
    css = CSS(string=BASE_CSS, font_config=font_config)
    out_path = os.path.join(OUT_DIR, filename)
    HTML(string=html).write_pdf(out_path, stylesheets=[css], font_config=font_config)
    size_kb = os.path.getsize(out_path) // 1024
    print(f"  ✓  {filename}  ({size_kb} KB)")
    return out_path


# ══════════════════════════════════════════════════════════════════════════════
# GUIDE 1 — THE AUTISM BENEFITS NAVIGATOR
# ══════════════════════════════════════════════════════════════════════════════

def guide_1():
    toc = [
        ("Welcome & How to Use This Guide", "3"),
        ("Section 1: The Big Picture — What Your Family Is Entitled To", "4"),
        ("Section 2: Supplemental Security Income (SSI)", "5"),
        ("Section 3: Medicaid", "9"),
        ("Section 4: Early Intervention (Birth to Age 3)", "13"),
        ("Section 5: Special Education Under IDEA", "14"),
        ("Section 6: SNAP (Food Assistance)", "15"),
        ("Section 7: WIC", "16"),
        ("Section 8: Housing Assistance", "16"),
        ("Section 9: ABLE Accounts", "17"),
        ("Section 10: Grants for Autism Families", "19"),
        ("Section 11: Tax Benefits", "20"),
        ("Master Action Checklist", "22"),
        ("Glossary & Resources", "23"),
    ]

    body = """
<h1>Welcome &amp; How to Use This Guide</h1>
<p>If you've recently received your child's autism diagnosis — or if you've had the diagnosis for years and still feel like you're missing something — this guide is for you.</p>
<p>The United States has a patchwork of programs, benefits, and funding sources designed to support families like yours. The problem is that no one hands you a roadmap. Programs are administered by different agencies, have different eligibility rules, and use different jargon. Families often miss out on <strong>thousands of dollars per year</strong> simply because they didn't know to ask.</p>
<p>This guide changes that.</p>

<div class="callout">
  <div class="callout-title">How to use this guide</div>
  <ol>
    <li>Read Section 1 first — it gives you the 30,000-foot view</li>
    <li>Use the Quick-Eligibility table to identify which programs apply to you</li>
    <li>Go deep on each applicable program in the detailed sections</li>
    <li>Use the Master Action Checklist at the end to track your progress</li>
  </ol>
</div>

<h1>Section 1: The Big Picture</h1>
<p>Every benefit available to your family falls into one of four buckets:</p>

<h2>The Four Categories of Support</h2>
<ul>
  <li><strong>Federal Entitlement Programs</strong> — If you meet the criteria, you ARE entitled to the benefit by law. No lottery, no waiting list. (SSI, Medicaid base, IDEA)</li>
  <li><strong>State Waiver Programs</strong> — Medicaid waivers that fund intensive support services. Often have waiting lists, but the services can be life-changing.</li>
  <li><strong>Federal Assistance Programs</strong> — Income-based support (SNAP, WIC, Section 8, LIHEAP)</li>
  <li><strong>Savings &amp; Asset Programs</strong> — Protect your child's financial future (ABLE Accounts, Special Needs Trusts)</li>
</ul>

<h2>Quick Eligibility Snapshot</h2>
<table>
  <tr><th>Benefit</th><th>Age Limit</th><th>Income Test</th><th>Waiting List?</th></tr>
  <tr><td>SSI</td><td>Under 18 (child rules)</td><td>Yes (family income)</td><td>No</td></tr>
  <tr><td>Medicaid</td><td>Under 19 (base)</td><td>Yes</td><td>No</td></tr>
  <tr><td>HCBS Waivers</td><td>Varies by state</td><td>No (usually)</td><td><strong>Often yes</strong></td></tr>
  <tr><td>Early Intervention</td><td>Birth to 3</td><td>No</td><td>No</td></tr>
  <tr><td>Special Education</td><td>3–21</td><td>No</td><td>No</td></tr>
  <tr><td>ABLE Account</td><td>Under 46 at diagnosis</td><td>No</td><td>No</td></tr>
</table>

<h1>Section 2: Supplemental Security Income (SSI)</h1>

<h2>What Is SSI?</h2>
<p>SSI is a federal cash benefit program run by the Social Security Administration. For children with autism, it can provide up to <strong>$943/month</strong> (2024 rate, adjusted annually).</p>
<p>More importantly: qualifying for SSI usually <strong>automatically qualifies your child for Medicaid</strong>, which covers therapies, medical equipment, and services worth tens of thousands of dollars per year.</p>

<h2>Does My Child Qualify?</h2>
<p>Your child must meet <strong>both</strong> tests:</p>

<h3>Test 1: Disability Test</h3>
<p>The SSA evaluates six domains of functioning. To qualify, your child needs either an "extreme" limitation in ONE domain, or "marked" limitations in TWO domains:</p>
<ol>
  <li>Acquiring and using information</li>
  <li>Attending and completing tasks</li>
  <li>Interacting and relating with others</li>
  <li>Moving about and manipulating objects</li>
  <li>Caring for yourself</li>
  <li>Health and physical well-being</li>
</ol>

<h3>Test 2: Financial Test (Under Age 18)</h3>
<p>The SSA counts part of the parents' income. Approximate 2024 income limits:</p>
<table>
  <tr><th>Household</th><th>Approx. Monthly Gross Limit</th></tr>
  <tr><td>1 parent, 1 child with disability</td><td>~$4,400/month</td></tr>
  <tr><td>2 parents, 1 child with disability</td><td>~$5,500/month</td></tr>
  <tr><td>Add per additional child</td><td>+~$400</td></tr>
</table>

<div class="callout">
  <div class="callout-title">Critical Rule: The Age-18 Reset</div>
  <p>When your child turns 18, <strong>parental income is NO LONGER counted.</strong> Almost every young adult with autism should apply for SSI on their 18th birthday — regardless of family income during childhood.</p>
</div>

<h2>How to Apply — Step by Step</h2>
<ol>
  <li><strong>Gather documents:</strong> Birth certificate, Social Security card, medical records, diagnosis report, school IEP/evaluations, proof of household income</li>
  <li><strong>Apply:</strong> Online at SSA.gov/benefits/ssi, by phone (1-800-772-1213), or in person at your local Social Security office</li>
  <li><strong>Complete the Child Function Report (SSA-3375):</strong> Describe your child's WORST days, not typical days. Be specific. Use the six functional domains above as your framework.</li>
</ol>

<div class="callout callout-warning">
  <div class="callout-title">If You Are Denied — Do Not Give Up</div>
  <p>~60% of initial SSI claims are denied. ~60% of appealed decisions are overturned. You have 60 days to appeal. Consider hiring a disability attorney — most work on contingency (no fee unless you win).</p>
</div>

<h1>Section 3: Medicaid</h1>

<h2>Two Paths to Medicaid</h2>
<ul>
  <li><strong>SSI-Linked:</strong> Most states auto-enroll SSI recipients in Medicaid. Most comprehensive coverage.</li>
  <li><strong>CHIP/State Medicaid:</strong> Even without SSI, your child may qualify based on family income. Many states cover families up to 200–400% of the Federal Poverty Level.</li>
</ul>

<h2>What Medicaid Must Cover for Children</h2>
<p>Under EPSDT (Early and Periodic Screening, Diagnostic and Treatment), Medicaid must cover all <strong>medically necessary</strong> treatment for children under 21:</p>
<ul>
  <li>ABA therapy (Applied Behavior Analysis)</li>
  <li>Speech therapy, Occupational therapy, Physical therapy</li>
  <li>Psychological evaluations and therapy</li>
  <li>Medical devices and assistive technology</li>
  <li>Dental care, Vision care</li>
</ul>

<h2>Medicaid HCBS Waivers — Where the Real Money Is</h2>
<p>HCBS waivers fund services traditional Medicaid doesn't cover:</p>
<table>
  <tr><th>Service</th><th>Example Value</th></tr>
  <tr><td>Respite care</td><td>30+ hours/month</td></tr>
  <tr><td>Day programs / habilitation</td><td>$15,000–$40,000/year</td></tr>
  <tr><td>Supported employment</td><td>$8,000–$20,000/year</td></tr>
  <tr><td>Home modifications</td><td>Up to $10,000</td></tr>
  <tr><td>Assistive technology</td><td>Varies</td></tr>
  <tr><td><strong>Total annual value</strong></td><td><strong>$20,000–$80,000+</strong></td></tr>
</table>

<div class="callout callout-warning">
  <div class="callout-title">Most Important Action in This Entire Guide</div>
  <p>Most states have HCBS waiver waiting lists of <strong>5–10+ years</strong>. Get on your state's list TODAY — even if your child is young. The list is first-come, first-served. Call your state's Developmental Disabilities agency now.</p>
</div>

<h1>Section 4: Early Intervention (Birth to Age 3)</h1>
<p>Under <strong>IDEA Part C</strong>, every child birth to age 3 with a developmental delay or disability is entitled to free early intervention services — in your home, at no cost.</p>
<ul>
  <li>Free developmental evaluation (within 45 days of referral)</li>
  <li>Free therapy services (speech, OT, PT, developmental specialist)</li>
  <li>Individualized Family Service Plan (IFSP)</li>
</ul>
<p><strong>How to access:</strong> Call your state's Early Intervention program or dial 2-1-1.</p>
<p><strong>Critical:</strong> At age 3, EI ends and children transition to school-based IEP services. A transition meeting should happen around the child's 2½ birthday. Don't let this happen without a plan.</p>

<h1>Section 5: Special Education Under IDEA</h1>
<p>Under <strong>IDEA Part B</strong> (ages 3–21), your child has the legal right to:</p>
<ul>
  <li>A <strong>Free Appropriate Public Education (FAPE)</strong></li>
  <li>An <strong>Individualized Education Program (IEP)</strong></li>
  <li>Related services (speech, OT, PT, counseling, transportation)</li>
  <li>Education in the <strong>Least Restrictive Environment (LRE)</strong></li>
</ul>
<p><em>The full IEP process is covered in depth in the companion guide "IEP Mastery: The Parent's Advocacy Bible."</em></p>

<h1>Section 6: SNAP (Food Assistance)</h1>
<h2>2024 Gross Monthly Income Limits</h2>
<table>
  <tr><th>Household Size</th><th>Monthly Limit</th></tr>
  <tr><td>1</td><td>$1,580</td></tr>
  <tr><td>2</td><td>$2,137</td></tr>
  <tr><td>3</td><td>$2,694</td></tr>
  <tr><td>4</td><td>$3,250</td></tr>
  <tr><td>5</td><td>$3,807</td></tr>
</table>
<p>Average SNAP benefit: ~$230/month per person. Apply online through your state's SNAP website.</p>
<p><strong>Autism tip:</strong> Households with a disabled member may be able to deduct excess medical/therapy expenses from income for SNAP purposes. Ask about the "medical deduction."</p>

<h1>Section 7: WIC</h1>
<p>For children under 5 with autism, WIC provides approved foods, formula support for feeding challenges, nutrition counseling, and service referrals. Income limit: 185% of federal poverty level.</p>

<h1>Section 8: Housing Assistance</h1>
<h2>Section 8 Housing Choice Voucher</h2>
<p>Subsidizes housing costs — covers the gap between reasonable market rent and 30% of family income. Waitlists are long (2–5+ years). <strong>Apply now</strong> through your local Public Housing Authority (HUD.gov).</p>

<h1>Section 9: ABLE Accounts</h1>
<div class="callout callout-success">
  <div class="callout-title">Game-Changer for Financial Planning</div>
  <p>ABLE accounts allow you to save up to <strong>$100,000</strong> without affecting SSI eligibility. Earnings grow tax-free. Anyone can contribute. Open in 15 minutes at <strong>ABLENRC.org</strong>.</p>
</div>
<table>
  <tr><th>Feature</th><th>Details</th></tr>
  <tr><td>SSI protection limit</td><td>Up to $100,000</td></tr>
  <tr><td>Annual contribution limit</td><td>$18,000/year (2024, all sources)</td></tr>
  <tr><td>Who qualifies</td><td>Autism diagnosis before age 46</td></tr>
  <tr><td>Allowed uses</td><td>Housing, education, transport, healthcare, technology, recreation</td></tr>
  <tr><td>Tax treatment</td><td>Contributions after-tax; earnings and withdrawals tax-free</td></tr>
</table>

<h1>Section 10: Grants for Autism Families</h1>
<table>
  <tr><th>Organization</th><th>Grant Amount</th><th>Focus Area</th></tr>
  <tr><td>Autism Care Today</td><td>Up to $1,500/quarter</td><td>Therapy, biomedical treatment</td></tr>
  <tr><td>ACT Today!</td><td>Varies</td><td>ABA therapy, equipment</td></tr>
  <tr><td>Doug Flutie Jr. Foundation</td><td>Varies</td><td>Family support services</td></tr>
  <tr><td>Organization for Autism Research</td><td>Up to $1,000</td><td>Research participation</td></tr>
  <tr><td>Autism Speaks Family Services</td><td>Varies</td><td>Crisis + emergency assistance</td></tr>
</table>

<h1>Section 11: Tax Benefits</h1>
<h2>Medical Expense Deduction</h2>
<p>If you itemize deductions, you can deduct medical expenses exceeding 7.5% of AGI. Deductible autism-related expenses include:</p>
<ul>
  <li>ABA therapy costs not covered by insurance</li>
  <li>Therapy co-pays and deductibles (speech, OT, PT)</li>
  <li>Transportation to medical appointments</li>
  <li>Special education tuition (in some cases)</li>
  <li>Specialized equipment when prescribed</li>
</ul>
<h2>Dependent Care FSA</h2>
<p>If your employer offers an FSA, contribute the maximum ($5,000) to pay for qualifying care with pre-tax dollars — saving 22–37% on those costs.</p>

<h1>Master Action Checklist</h1>
<h2>Do These First — Highest Impact</h2>
<ul class="checklist">
  <li>Apply for SSI if family income is below threshold, or if child is approaching 18</li>
  <li>Confirm Medicaid coverage and verify it covers ABA therapy</li>
  <li>Get on your state's HCBS waiver waiting list TODAY</li>
  <li>Open an ABLE account at ABLENRC.org</li>
</ul>
<h2>Within 30 Days</h2>
<ul class="checklist">
  <li>Request Early Intervention evaluation if child is under 3</li>
  <li>Contact school district to initiate IEP process (ages 3–21)</li>
  <li>Check SNAP eligibility and apply if qualified</li>
  <li>Apply for WIC if child is under 5 and income qualifies</li>
</ul>
<h2>Within 90 Days</h2>
<ul class="checklist">
  <li>Research private foundation grants and start applying</li>
  <li>Review tax situation for medical expense deductions</li>
  <li>Apply for Section 8 waiting list</li>
  <li>Connect with local autism parent support group</li>
</ul>

<h1>Resources</h1>
<table>
  <tr><th>Resource</th><th>Contact</th></tr>
  <tr><td>Social Security Administration</td><td>SSA.gov | 1-800-772-1213</td></tr>
  <tr><td>ABLE National Resource Center</td><td>ABLENRC.org</td></tr>
  <tr><td>Medicaid Information</td><td>Medicaid.gov</td></tr>
  <tr><td>Autism Speaks Resource Guide</td><td>autismspeaks.org/state-resource-guide</td></tr>
  <tr><td>Benefits.gov (all federal benefits)</td><td>Benefits.gov</td></tr>
  <tr><td>Local social services</td><td>Dial 2-1-1 or 211.org</td></tr>
</table>
"""
    build_pdf(
        title="The Autism Benefits Navigator",
        subtitle="Every Dollar, Program, and Benefit Your Family Is Entitled To — A Plain-English Guide for Parents of Children with Autism",
        price="$47",
        badge="Benefits & Financial Programs",
        toc=toc,
        body_html=body,
        filename="01-autism-benefits-navigator.pdf",
    )


# ══════════════════════════════════════════════════════════════════════════════
# GUIDE 2 — IEP MASTERY (condensed representative version)
# ══════════════════════════════════════════════════════════════════════════════

def guide_2():
    toc = [
        ("Welcome: Why This Guide Exists", "3"),
        ("Part 1: Your Legal Foundation (IDEA)", "4"),
        ("Part 2: The Evaluation Process", "6"),
        ("Part 3: The 13 Required IEP Components", "8"),
        ("Part 4: Placement Options", "14"),
        ("Part 5: The IEP Meeting Playbook", "15"),
        ("Part 6: When the School Says No", "18"),
        ("Part 7: Autism-Specific IEP Issues", "20"),
        ("IEP Advocacy Toolkit", "23"),
        ("Annual IEP Timeline Planner", "25"),
    ]

    body = """
<h1>Welcome: Why This Guide Exists</h1>
<p>Every year, thousands of children with autism sit in classrooms with IEPs that don't actually meet their needs — not because the system is always malicious, but because parents don't know what to ask for, what they're entitled to, or how the process works.</p>
<p>The IEP is the single most powerful document in your child's educational life. It is <strong>legally binding.</strong> It determines what services your child receives, how many hours, in what setting, and measured against what goals. Getting it right — or getting it wrong — can change the trajectory of your child's development.</p>

<h1>Part 1: Your Legal Foundation</h1>
<p>IDEA gives your child <strong>six core rights</strong>:</p>

<table>
  <tr><th>Right</th><th>What It Means</th></tr>
  <tr><td>FAPE</td><td>Free Appropriate Public Education — no cost to you, meets unique needs</td></tr>
  <tr><td>LRE</td><td>Least Restrictive Environment — alongside non-disabled peers to max extent</td></tr>
  <tr><td>Evaluation</td><td>Comprehensive, free, in native language, within 60 days of consent</td></tr>
  <tr><td>IEP</td><td>Written plan reviewed annually, developed with your participation</td></tr>
  <tr><td>Participation</td><td>You are a required member of the team — not a guest</td></tr>
  <tr><td>Procedural Safeguards</td><td>Right to inspect records, seek independent evaluation, mediation, due process</td></tr>
</table>

<div class="callout">
  <div class="callout-title">Landmark Case: Endrew F. v. Douglas County (2017)</div>
  <p>The Supreme Court ruled that FAPE requires "meaningful" educational progress — not merely "more than de minimis." Use this precedent when the school proposes goals that seem too low.</p>
</div>

<h1>Part 2: The Evaluation Process</h1>
<h2>How to Request an Evaluation (Template)</h2>
<div class="callout">
  <p><em>"I am writing to formally request a comprehensive special education evaluation for my child, [Name], DOB [date]. I am requesting this evaluation because [briefly describe concerns]. I understand I will receive a Prior Written Notice and Parental Consent form. Please confirm receipt of this letter."</em></p>
  <p><strong>Send via email AND certified mail.</strong> This starts the legal 60-day clock.</p>
</div>

<h2>What a Complete Autism Evaluation Covers</h2>
<ul>
  <li>Cognitive/intellectual functioning</li>
  <li>Academic achievement (reading, math, writing)</li>
  <li>Social-emotional and behavioral functioning</li>
  <li>Adaptive behavior (Vineland, ABAS)</li>
  <li>Communication — expressive, receptive, pragmatic</li>
  <li>Occupational performance and sensory processing</li>
  <li>Autism-specific assessment (ADOS-2, ADI-R preferred)</li>
</ul>

<h1>Part 3: The 13 Required IEP Components</h1>

<h2>1. PLAAFP — Present Levels of Academic Achievement and Functional Performance</h2>
<p>The foundation of the IEP. Describes where your child is right now, with specific data.</p>
<div class="callout callout-warning">
  <div class="callout-title">Red Flag</div>
  <p>Vague PLAAFP language like "Johnny struggles with social skills" with no data. Push for specifics: "Johnny initiates peer interaction in 2 of 10 observed opportunities and requires adult prompting 80% of the time."</p>
</div>

<h2>2. Measurable Annual Goals</h2>
<p>Every goal must follow this anatomy:</p>
<ul>
  <li><strong>Who:</strong> The student</li>
  <li><strong>Will do what:</strong> Observable behavior</li>
  <li><strong>Under what conditions:</strong> Context/setting</li>
  <li><strong>To what degree:</strong> Measurable criteria (%, frequency, accuracy)</li>
  <li><strong>By when:</strong> Timeline</li>
</ul>

<h3>Examples of Strong IEP Goals for Autism</h3>
<table>
  <tr><th>Domain</th><th>Example Goal</th></tr>
  <tr><td>Communication</td><td>"[Student] will use a 3–4 word phrase to make a request in 4 of 5 opportunities across 3 consecutive data periods, as measured by SLP data."</td></tr>
  <tr><td>Social</td><td>"[Student] will initiate a social interaction with a peer at least 2 times per 30-minute unstructured period, in 4 of 5 consecutive school days."</td></tr>
  <tr><td>Behavior</td><td>"[Student] will use a coping strategy (deep breathing, visual schedule, verbal break request) with no more than 2 prompts, in 8 of 10 opportunities."</td></tr>
  <tr><td>Self-care</td><td>"[Student] will independently complete a 5-step morning routine using a visual checklist without adult prompting, in 4 of 5 school days."</td></tr>
</table>

<h2>4. Special Education and Related Services</h2>
<p>Each service must specify: type, frequency, duration, location, start date. Common services for autism:</p>
<ul>
  <li>Applied Behavior Analysis / Behavioral support</li>
  <li>Speech-Language Therapy</li>
  <li>Occupational Therapy</li>
  <li>Physical Therapy</li>
  <li>Social skills training</li>
  <li>Assistive Technology (AAC devices)</li>
</ul>

<h2>6. Accommodations and Modifications</h2>
<p><strong>Accommodations</strong> change HOW your child learns. <strong>Modifications</strong> change WHAT they learn. High-value autism accommodations:</p>
<table>
  <tr><th>Accommodation</th><th>Why It Helps</th></tr>
  <tr><td>Extended time (1.5x–2x)</td><td>Processing time differences</td></tr>
  <tr><td>Preferential seating</td><td>Reduces sensory distraction</td></tr>
  <tr><td>Movement breaks every 20–30 min</td><td>Sensory regulation, focus</td></tr>
  <tr><td>Visual schedule at desk</td><td>Reduces transition anxiety</td></tr>
  <tr><td>Advance notice of changes</td><td>Reduces meltdowns from surprise</td></tr>
  <tr><td>Noise-canceling headphones</td><td>Auditory sensitivity</td></tr>
  <tr><td>Reduced homework load</td><td>Fatigue from masking all day</td></tr>
  <tr><td>AAC device access</td><td>Communication support</td></tr>
</table>

<h1>Part 4: Placement Options</h1>
<table>
  <tr><th>Setting (Most → Least Inclusive)</th><th>Description</th></tr>
  <tr><td>Full inclusion in general education</td><td>With aides and supports</td></tr>
  <tr><td>General ed + resource room pullout</td><td>30–50% of time in separate setting</td></tr>
  <tr><td>Self-contained special ed classroom</td><td>Full day with peers with disabilities</td></tr>
  <tr><td>Separate special education school</td><td>All special education population</td></tr>
  <tr><td>Residential school</td><td>Live-in placement</td></tr>
</table>
<p><strong>LRE principle:</strong> Placement must be as inclusive as possible while still meeting the child's needs. The school cannot choose a more restrictive setting simply because it is more convenient or cheaper.</p>

<h1>Part 5: The IEP Meeting Playbook</h1>

<h2>Before the Meeting</h2>
<ul class="checklist">
  <li>Request copies of all assessments 2–3 weeks in advance</li>
  <li>Review current IEP — what worked, what didn't</li>
  <li>Gather private provider reports and letters</li>
  <li>Write your parent vision statement</li>
  <li>Prepare questions and service requests in writing</li>
  <li>Consider bringing an advocate</li>
</ul>

<h2>At the Meeting — Scripts That Work</h2>
<div class="callout">
  <div class="callout-title">Opening Statement</div>
  <p><em>"Before we begin, I'd like to share my vision for [child's name]. I want [him/her] to [specific goal]. With the right support, I believe [he/she] can achieve this, and I'm here today as a partner."</em></p>
</div>
<div class="callout">
  <div class="callout-title">When a Service Seems Insufficient</div>
  <p><em>"I appreciate that recommendation, but [child's] private therapist has recommended [X hours/week]. Can we discuss why there's a difference, and what data supports the school's recommendation?"</em></p>
</div>
<div class="callout callout-warning">
  <div class="callout-title">You Are NEVER Required to Sign at the Meeting</div>
  <p>Take the IEP home. Review it. Consult an advocate if needed. You have 10 days to respond in writing.</p>
</div>

<h1>Part 6: When the School Says No</h1>
<h2>Escalation Path</h2>
<table>
  <tr><th>Level</th><th>Action</th><th>Cost</th><th>Timeline</th></tr>
  <tr><td>1</td><td>Document everything in writing</td><td>Free</td><td>Ongoing</td></tr>
  <tr><td>2</td><td>Request Prior Written Notice (PWN)</td><td>Free</td><td>Immediate</td></tr>
  <tr><td>3</td><td>Facilitated IEP meeting</td><td>Free</td><td>2–4 weeks</td></tr>
  <tr><td>4</td><td>State complaint</td><td>Free</td><td>60 days to resolve</td></tr>
  <tr><td>5</td><td>Mediation</td><td>Free</td><td>30–60 days</td></tr>
  <tr><td>6</td><td>Due process hearing</td><td>Attorney fees</td><td>45–75 days</td></tr>
</table>

<h1>Part 7: Autism-Specific IEP Issues</h1>
<h2>Behavioral Intervention Plans (BIPs)</h2>
<p>If your child's behavior impedes their learning, the team must consider a Functional Behavior Assessment (FBA) and BIP. Most behaviors serve one of four functions: to get something, to avoid something, for sensory input, or for social attention.</p>
<div class="callout callout-warning">
  <div class="callout-title">Red Flag</div>
  <p>A BIP that is all punishment/consequence with no teaching of replacement skills. Push for a BIP that primarily teaches what to DO instead of the challenging behavior.</p>
</div>

<h2>Extended School Year (ESY)</h2>
<p>ESY = continued IEP services during summer. Most schools will not offer it automatically. You must: (1) Keep data on regression over breaks, (2) Bring data to the IEP meeting, (3) Formally request ESY.</p>

<h2>Assistive Technology &amp; AAC</h2>
<p>For non-speaking or minimally verbal children, the IEP team must consider AAC. Research shows AAC does NOT reduce speech — it supports language development.</p>
<table>
  <tr><th>AAC Type</th><th>Examples</th></tr>
  <tr><td>Low-tech</td><td>PECS, communication boards</td></tr>
  <tr><td>Mid-tech</td><td>Proloquo2Go, TouchChat, LAMP Words for Life (iPad apps)</td></tr>
  <tr><td>High-tech</td><td>Dedicated speech-generating devices (SGDs)</td></tr>
</table>

<h1>IEP Advocacy Toolkit</h1>
<h2>Questions to Ask at Every IEP Meeting</h2>
<ol>
  <li>What data is being used to make this recommendation?</li>
  <li>How will progress toward each goal be measured and reported?</li>
  <li>Is my child receiving all services agreed to in the last IEP?</li>
  <li>What additional supports would be added if current supports aren't working?</li>
  <li>Are there any behaviors that need to be addressed in a BIP?</li>
  <li>What does my child's school day look like from their perspective?</li>
</ol>

<h2>IEP Red Flags</h2>
<ul>
  <li>Goals that aren't measurable ("will improve social skills")</li>
  <li>No baseline data in the PLAAFP</li>
  <li>Services listed without specific frequency/duration</li>
  <li>Placement decided before evaluation is complete</li>
  <li>Meeting starts with IEP already written — you just need to sign</li>
  <li>Team pressure to sign at the meeting</li>
</ul>

<h1>Annual IEP Timeline Planner</h1>
<table>
  <tr><th>When</th><th>Action</th></tr>
  <tr><td>3 months before annual review</td><td>Review current IEP, request updated assessment data, draft parent vision statement</td></tr>
  <tr><td>6 weeks before</td><td>Request evaluation results and draft IEP; contact private providers for updated reports</td></tr>
  <tr><td>2 weeks before</td><td>Review all documents; prepare questions; identify non-negotiables</td></tr>
  <tr><td>At the meeting</td><td>Follow the playbook; take notes; don't feel pressured to sign</td></tr>
  <tr><td>After the meeting</td><td>Monitor service delivery; track goal progress monthly; address concerns in writing immediately</td></tr>
</table>

<h2>Key Resources</h2>
<table>
  <tr><th>Resource</th><th>Where</th></tr>
  <tr><td>Parent Training &amp; Information Centers</td><td>parentcenterhub.org</td></tr>
  <tr><td>Special Ed Law Reference</td><td>wrightslaw.com</td></tr>
  <tr><td>Council of Parent Attorneys &amp; Advocates</td><td>copaa.org</td></tr>
</table>
"""
    build_pdf(
        title="IEP Mastery",
        subtitle="The Parent's Advocacy Bible — How to Get Your Child the Education and Support They Deserve",
        price="$47",
        badge="Special Education & Legal Rights",
        toc=toc,
        body_html=body,
        filename="02-iep-mastery.pdf",
    )


# ══════════════════════════════════════════════════════════════════════════════
# GUIDE 3 — FREE LEAD MAGNET
# ══════════════════════════════════════════════════════════════════════════════

def guide_free():
    toc = [
        ("Welcome", "2"),
        ("Program #1: Supplemental Security Income (SSI)", "3"),
        ("Program #2: HCBS Medicaid Waiver", "4"),
        ("Program #3: IDEA — Free School Services", "5"),
        ("Program #4: ABLE Accounts", "6"),
        ("Program #5: Insurance Coverage for ABA Therapy", "7"),
        ("What to Do Next", "8"),
    ]

    body = """
<h1>Welcome</h1>
<p>If you're reading this, you're already doing something most parents don't: you're seeking out the information your child needs to thrive.</p>
<p>The programs in this guide are funded by federal and state governments — specifically to help families like yours. No one is required to tell you about them. Many families spend years missing out simply because they never knew to ask.</p>
<p><strong>This guide changes that.</strong></p>

<div class="callout callout-success">
  <div class="callout-title">Your Next Step After Reading</div>
  <p>The most impactful action you can take this week: <strong>Call your state's Developmental Disabilities agency and ask to be placed on the HCBS Medicaid waiver waiting list.</strong> Waiting lists can be 5–10 years. Every day you wait is a day lost.</p>
</div>

<h1>Program #1: Supplemental Security Income (SSI)</h1>
<h2>Up to $943/Month — Plus Medicaid Coverage</h2>
<p>SSI is a federal cash benefit from the Social Security Administration for children with disabilities whose family income falls below a certain threshold.</p>

<table>
  <tr><th>Key Fact</th><th>Detail</th></tr>
  <tr><td>Monthly benefit</td><td>Up to $943/month (2024)</td></tr>
  <tr><td>Bonus</td><td>Automatically triggers Medicaid in most states</td></tr>
  <tr><td>Age-18 rule</td><td>Parental income no longer counted — apply at 18 regardless of prior denial</td></tr>
  <tr><td>How to apply</td><td>SSA.gov or call 1-800-772-1213</td></tr>
</table>

<div class="callout callout-warning">
  <div class="callout-title">If You're Denied</div>
  <p>~60% of initial claims are denied. ~60% of appeals are won. You have 60 days to appeal. Do not give up after the first denial.</p>
</div>

<h1>Program #2: HCBS Medicaid Waiver</h1>
<h2>$20,000–$80,000+ Per Year in Services</h2>
<p>Home and Community Based Services waivers fund intensive support that traditional Medicaid doesn't cover: respite care, day programs, supported employment, home modifications, assistive technology, and more.</p>

<div class="callout callout-warning">
  <div class="callout-title">Waiting Lists Are Long — Act Now</div>
  <p>Most states have HCBS waiver waiting lists of <strong>5–10+ years.</strong> The families who get services are the ones who got in line earliest. Call your state's Developmental Disabilities agency today and ask to be placed on the waiting list.</p>
</div>

<p><strong>How to find your state's agency:</strong> Search "[Your State] developmental disabilities agency" or dial 2-1-1.</p>

<h1>Program #3: IDEA — Free School Services</h1>
<h2>Federally Mandated, 100% Free to Your Family</h2>
<p>Under the Individuals with Disabilities Education Act, your child between ages 3 and 21 is entitled to a Free Appropriate Public Education with all needed special education services — at no cost to you.</p>

<table>
  <tr><th>Service</th><th>Covered?</th></tr>
  <tr><td>ABA therapy through school</td><td>Yes — if educationally necessary</td></tr>
  <tr><td>Speech-Language Therapy</td><td>Yes</td></tr>
  <tr><td>Occupational Therapy</td><td>Yes</td></tr>
  <tr><td>Physical Therapy</td><td>Yes</td></tr>
  <tr><td>Transportation</td><td>Yes</td></tr>
  <tr><td>Assistive Technology (AAC)</td><td>Yes</td></tr>
</table>

<p><strong>For children 0–3:</strong> Call your state's Early Intervention program — similar free services are available for infants and toddlers.</p>
<p><strong>Your right:</strong> You can request a free special education evaluation from your school district at any time, in writing.</p>

<h1>Program #4: ABLE Accounts</h1>
<h2>Save Up to $100,000 Without Losing Benefits</h2>
<p>The ABLE Act created tax-advantaged savings accounts for people with disabilities. For autism families, this is one of the most powerful financial tools available.</p>

<table>
  <tr><th>Feature</th><th>Details</th></tr>
  <tr><td>SSI-protected savings</td><td>Up to $100,000 — invisible to SSI</td></tr>
  <tr><td>Annual contributions</td><td>Up to $18,000/year from all sources</td></tr>
  <tr><td>Who can contribute</td><td>Family, friends, anyone — not just the person with disability</td></tr>
  <tr><td>How to open</td><td>ABLENRC.org — takes about 15 minutes</td></tr>
</table>

<div class="callout callout-success">
  <div class="callout-title">Smart Move</div>
  <p>Ask grandparents and relatives to contribute to the ABLE account instead of giving cash gifts. Over 18 years at $200/month = $43,000+ before any investment growth.</p>
</div>

<h1>Program #5: Insurance Coverage for ABA Therapy</h1>
<h2>All 50 States Require It — Here's How to Get It</h2>
<p>All 50 states have passed autism insurance reform laws requiring most health insurance plans to cover ABA therapy and other autism treatments. Your insurer cannot categorically refuse coverage.</p>

<table>
  <tr><th>Therapy</th><th>Typical Monthly Value</th></tr>
  <tr><td>ABA Therapy (20–40 hrs/wk)</td><td>$5,000–$15,000</td></tr>
  <tr><td>Speech Therapy (3x/wk)</td><td>$600–$1,200</td></tr>
  <tr><td>Occupational Therapy (2x/wk)</td><td>$400–$800</td></tr>
</table>

<p><strong>If your insurer denies coverage:</strong> You have the right to appeal — through internal appeal, then external independent review. The companion guide "The Autism Insurance Battle Guide" covers the complete 4-level appeal process with exact scripts.</p>

<h1>What to Do Next — Your Action List</h1>
<ul class="checklist">
  <li>TODAY: Call your state's DD agency — get on the HCBS waiver waiting list</li>
  <li>THIS WEEK: Check SSI eligibility at SSA.gov or call 1-800-772-1213</li>
  <li>THIS WEEK: Open an ABLE account at ABLENRC.org (15 minutes)</li>
  <li>THIS MONTH: Contact your school district about special education services</li>
  <li>THIS MONTH: Call your insurance company — confirm ABA therapy coverage</li>
</ul>

<div class="callout callout-success">
  <div class="callout-title">Want to Go Deeper?</div>
  <p>This free guide is just the beginning. Our full <strong>Autism Benefits Navigator ($47)</strong> covers every program in step-by-step detail. The <strong>Complete Autism Parent Toolkit ($127)</strong> includes all 6 guides — benefits, IEPs, therapies, insurance, diagnosis, and transition planning. Visit <strong>spectrumready.com</strong> to see everything.</p>
</div>
"""
    build_pdf(
        title="5 Programs Every Autism Parent Must Know About",
        subtitle="The Free Guide That Could Change Your Family's Financial Future",
        price="FREE",
        badge="Free Resource — SpectrumReady",
        toc=toc,
        body_html=body,
        filename="00-free-guide-5-programs.pdf",
    )


# ══════════════════════════════════════════════════════════════════════════════
# GUIDE 3 — THE COMPLETE THERAPY ROADMAP
# ══════════════════════════════════════════════════════════════════════════════

def guide_3():
    toc = [
        ("Introduction: Building the Right Therapy Team", "3"),
        ("Part 1: How to Evaluate Any Therapy", "4"),
        ("Part 2: Applied Behavior Analysis (ABA)", "5"),
        ("Part 3: Speech-Language Therapy", "8"),
        ("Part 4: Occupational Therapy", "10"),
        ("Part 5: Additional Therapies — Evidence Review", "12"),
        ("Part 6: Finding and Vetting Providers", "15"),
        ("Part 7: Funding Your Therapy Plan", "18"),
        ("Part 8: Building Your Therapy Schedule", "20"),
        ("Master Therapy Tracker", "22"),
    ]

    body = """
<h1>Introduction: Building the Right Therapy Team</h1>
<p>Your child's therapy plan will be the single largest investment of time and money your family makes over the next decade. Getting it right — knowing what to pursue, what to skip, and how to fund it — is what this guide is about.</p>
<p>The landscape of autism therapies is enormous and confusing. Some have decades of research behind them. Others are aggressively marketed with little or no evidence. A few are actively harmful. This guide cuts through the noise with an honest, evidence-based review of every major approach.</p>

<div class="callout">
  <div class="callout-title">Evidence Rating System Used in This Guide</div>
  <p>⭐ = No credible evidence / anecdotal only<br>
  ⭐⭐ = Preliminary / emerging evidence<br>
  ⭐⭐⭐ = Moderate evidence, some methodological limitations<br>
  ⭐⭐⭐⭐ = Strong evidence, well-replicated studies<br>
  ⭐⭐⭐⭐⭐ = Extensive evidence, recognized by major medical/behavioral bodies</p>
</div>

<h1>Part 1: How to Evaluate Any Therapy</h1>
<h2>The Four Questions to Ask Before Starting Any Intervention</h2>
<ol>
  <li><strong>What does the research say?</strong> Ask for peer-reviewed studies, not testimonials or theory.</li>
  <li><strong>What specific outcomes are we targeting?</strong> Every intervention should have measurable goals tied to your child's individual needs.</li>
  <li><strong>How will we know if it's working?</strong> Data collection, progress monitoring, and defined timeframes matter.</li>
  <li><strong>What is the opportunity cost?</strong> Every hour in one therapy is an hour not in another. Prioritize highest-evidence approaches first.</li>
</ol>

<div class="callout callout-warning">
  <div class="callout-title">Red Flags for Any Therapy Provider</div>
  <ul>
    <li>Claims their therapy "cures" autism</li>
    <li>Cannot explain the evidence base for their approach</li>
    <li>Discourages data collection or progress monitoring</li>
    <li>Discourages you from consulting other professionals</li>
    <li>Requires long-term prepaid contracts before demonstrating results</li>
  </ul>
</div>

<h1>Part 2: Applied Behavior Analysis (ABA)</h1>
<h2>Evidence Rating: ⭐⭐⭐⭐⭐</h2>
<p>ABA is the most researched behavioral intervention for autism. It is endorsed by the American Academy of Pediatrics, the US Surgeon General, and required to be covered by insurance in all 50 states. It uses principles of learning and motivation to teach skills and reduce barriers to learning.</p>

<h2>What ABA Can Address</h2>
<table>
  <tr><th>Domain</th><th>Examples</th></tr>
  <tr><td>Communication</td><td>Requesting, labeling, conversation, AAC</td></tr>
  <tr><td>Social skills</td><td>Joint attention, play, peer interaction, perspective-taking</td></tr>
  <tr><td>Adaptive behavior</td><td>Toileting, dressing, grooming, mealtime</td></tr>
  <tr><td>Reduction of barriers</td><td>Self-injurious behavior, aggression, elopement, severe tantrums</td></tr>
  <tr><td>Academic readiness</td><td>Attending, instruction following, pre-academic skills</td></tr>
</table>

<h2>Types of ABA</h2>
<ul>
  <li><strong>Discrete Trial Training (DTT):</strong> Structured, table-based teaching. Best for teaching new skills efficiently.</li>
  <li><strong>Natural Environment Teaching (NET):</strong> Learning in natural contexts (play, daily routines). Promotes generalization.</li>
  <li><strong>Verbal Behavior (VB):</strong> Language-focused ABA based on Skinner's analysis of verbal behavior.</li>
  <li><strong>Pivotal Response Treatment (PRT):</strong> Child-led, naturalistic. Targets "pivotal" areas (motivation, self-initiation) that affect broader development.</li>
</ul>

<h2>Hours of Therapy — What the Research Says</h2>
<table>
  <tr><th>Child Profile</th><th>Research-Supported Range</th></tr>
  <tr><td>Younger children with significant needs (2–5)</td><td>25–40 hours/week (intensive)</td></tr>
  <tr><td>School-age children with moderate needs</td><td>10–20 hours/week</td></tr>
  <tr><td>Children with higher functioning profiles</td><td>5–15 hours/week (targeted)</td></tr>
</table>
<p><em>Note: "More hours" is not always better. Quality, specificity of goals, and family involvement matter as much as quantity.</em></p>

<h2>Questions to Ask an ABA Provider</h2>
<ul class="checklist">
  <li>Is the supervising clinician a BCBA (Board Certified Behavior Analyst)?</li>
  <li>What is the ratio of BCBA supervision hours to RBT direct hours?</li>
  <li>How are goals developed — is it individualized to my child?</li>
  <li>How is data collected and shared with parents?</li>
  <li>What parent training do you provide?</li>
  <li>What is your approach to reducing challenging behaviors?</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">Important: ABA Quality Varies Enormously</div>
  <p>A good ABA program with experienced BCBAs and appropriate ratios produces excellent outcomes. A high-hours program with poor supervision and inadequate individualization does not. Credential the team, review the data, and trust your observations of your child's engagement.</p>
</div>

<h1>Part 3: Speech-Language Therapy (SLT)</h1>
<h2>Evidence Rating: ⭐⭐⭐⭐⭐</h2>
<p>Speech-Language Pathologists (SLPs) address communication across all modalities. For autism, SLT is almost always indicated and is one of the highest-impact investments you can make.</p>

<h2>What SLT Addresses for Autism</h2>
<table>
  <tr><th>Area</th><th>Description</th></tr>
  <tr><td>Functional communication</td><td>Requesting needs, commenting, answering questions</td></tr>
  <tr><td>Language development</td><td>Vocabulary, sentence structure, comprehension</td></tr>
  <tr><td>Pragmatic/social language</td><td>Conversation, perspective-taking, understanding humor/sarcasm</td></tr>
  <tr><td>Feeding and oral motor</td><td>Food selectivity, chewing, swallowing</td></tr>
  <tr><td>AAC implementation</td><td>PECS, speech-generating devices, communication apps</td></tr>
</table>

<h2>AAC Is NOT a Last Resort</h2>
<p>Research consistently shows that AAC (Augmentative and Alternative Communication) does not inhibit speech development — it supports it. For children who are non-speaking or minimally verbal, early AAC access is critical. Do not wait for speech to "see if it develops" before pursuing AAC.</p>

<h2>Frequency Recommendations</h2>
<table>
  <tr><th>Child Profile</th><th>Typical Recommendation</th></tr>
  <tr><td>Minimally verbal / AAC user</td><td>3–5x/week with intensive parent training</td></tr>
  <tr><td>Verbal but with significant pragmatic deficits</td><td>2–3x/week</td></tr>
  <tr><td>Maintenance/generalization phase</td><td>1x/week with home practice</td></tr>
</table>

<h1>Part 4: Occupational Therapy (OT)</h1>
<h2>Evidence Rating: ⭐⭐⭐⭐</h2>
<p>OT addresses the skills needed for daily living and participation. For autism, OT commonly targets sensory processing, fine motor skills, self-care, and handwriting.</p>

<h2>Sensory Processing — What OT Can Do</h2>
<p>Many children with autism experience sensory differences — hyper or hypo sensitivity to touch, sound, movement, taste, or sight. OT using Sensory Integration Therapy works to help the brain better process and regulate sensory input.</p>

<table>
  <tr><th>Sensory Challenge</th><th>OT Strategies</th></tr>
  <tr><td>Tactile hypersensitivity</td><td>Desensitization, deep pressure, weighted blankets</td></tr>
  <tr><td>Auditory sensitivity</td><td>Noise management, auditory integration programs</td></tr>
  <tr><td>Proprioceptive seeking</td><td>Heavy work activities, movement breaks</td></tr>
  <tr><td>Vestibular sensitivity</td><td>Swinging, balance activities (graded)</td></tr>
  <tr><td>Food texture sensitivity</td><td>Feeding therapy, systematic desensitization</td></tr>
</table>

<h2>Fine Motor and Daily Living Skills</h2>
<ul>
  <li>Handwriting (often significantly impacted in autism)</li>
  <li>Dressing, buttoning, zipping</li>
  <li>Scissor skills and tool use</li>
  <li>Feeding (fork, spoon, cup)</li>
  <li>Organizational skills and executive function strategies</li>
</ul>

<h1>Part 5: Additional Therapies — Evidence Review</h1>

<h2>DIR/Floortime — ⭐⭐⭐</h2>
<p>Developmental, Individual Difference, Relationship-based model. Emphasizes following the child's lead, emotional engagement, and relationship-building. Good evidence for social-emotional development. Often used to complement ABA. Best with a trained DIR clinician plus significant parent training.</p>

<h2>Social Skills Groups — ⭐⭐⭐</h2>
<p>Structured groups targeting peer interaction, conversation, and social problem-solving. Most effective for verbal children in middle childhood and adolescence. PEERS (Program for the Education and Enrichment of Relational Skills) has the strongest evidence base.</p>

<h2>Physical Therapy (PT) — ⭐⭐⭐⭐ (for motor goals)</h2>
<p>Many children with autism have co-occurring developmental coordination disorder. PT addresses gross motor development, balance, coordination, and functional mobility. Indicated when there are significant motor delays or coordination challenges.</p>

<h2>RDI (Relationship Development Intervention) — ⭐⭐</h2>
<p>Parent-mediated approach focused on dynamic intelligence and relationship skills. Limited controlled research but conceptually aligned with current developmental approaches. Requires intensive parent training.</p>

<h2>Music Therapy — ⭐⭐⭐</h2>
<p>Evidence supports music therapy for social and communication outcomes. Particularly useful for children who respond strongly to music. Best as a complement to primary therapies, not a replacement.</p>

<h2>Animal-Assisted Therapy — ⭐⭐</h2>
<p>Emerging evidence for social engagement, anxiety reduction, and motivation. Best as a supplement with a clear therapeutic goal. Costs not typically covered by insurance.</p>

<h2>Therapies Lacking Evidence — Approach With Caution</h2>
<table>
  <tr><th>Therapy</th><th>Evidence Status</th><th>Notes</th></tr>
  <tr><td>Facilitated Communication</td><td>Discredited</td><td>AAP and ASHA advise against</td></tr>
  <tr><td>Detoxification / chelation</td><td>No evidence, risky</td><td>Serious health risks documented</td></tr>
  <tr><td>Hyperbaric oxygen</td><td>No reliable evidence</td><td>FDA warns against off-label use</td></tr>
  <tr><td>Gluten-free / casein-free diet</td><td>Limited evidence</td><td>May help some with GI issues; consult pediatrician</td></tr>
</table>

<h1>Part 6: Finding and Vetting Providers</h1>

<h2>Where to Find Qualified Providers</h2>
<ul>
  <li><strong>BACB.com</strong> — Verify BCBA credentials, find certified behavior analysts</li>
  <li><strong>ASHA ProFind</strong> — Find certified speech-language pathologists</li>
  <li><strong>AOTA Practitioner Finder</strong> — Occupational therapists</li>
  <li><strong>Autism Speaks Provider Directory</strong> — Multi-specialty autism providers</li>
  <li><strong>Insurance provider directory</strong> — In-network providers for billing</li>
  <li><strong>Parent recommendations</strong> in local autism parent groups — often the best source</li>
</ul>

<h2>First Appointment Interview Guide</h2>
<p>Use these questions for any new provider before committing:</p>
<ol>
  <li>What is your experience specifically with autism? How many clients with autism do you currently serve?</li>
  <li>What certifications or specialized training do you have for autism?</li>
  <li>How will you involve me as a parent in my child's treatment?</li>
  <li>How will you measure and report progress?</li>
  <li>What is your wait time and scheduling flexibility?</li>
  <li>Do you accept our insurance? What is the billing process?</li>
  <li>What happens if the current approach isn't working?</li>
</ol>

<h1>Part 7: Funding Your Therapy Plan</h1>

<h2>Funding Source Priority Order</h2>
<table>
  <tr><th>Priority</th><th>Source</th><th>Why</th></tr>
  <tr><td>1st</td><td>Private health insurance</td><td>Required by law to cover ABA in all 50 states</td></tr>
  <tr><td>2nd</td><td>Medicaid / CHIP</td><td>EPSDT covers all medically necessary services</td></tr>
  <tr><td>3rd</td><td>School district (IDEA)</td><td>Covers educationally necessary services at no cost</td></tr>
  <tr><td>4th</td><td>Medicaid HCBS Waiver</td><td>Covers services not otherwise funded</td></tr>
  <tr><td>5th</td><td>Private grants</td><td>Fill gaps in other coverage</td></tr>
  <tr><td>6th</td><td>Out of pocket</td><td>Only after maximizing all other sources</td></tr>
</table>

<h2>Insurance Appeals for Therapy</h2>
<p>The most common insurance denials for therapy:</p>
<ul>
  <li>"Not medically necessary" — Counter with a Letter of Medical Necessity from the diagnosing physician and therapy provider</li>
  <li>"Experimental/investigational" — ABA is not experimental; cite ACA mandates and state law</li>
  <li>"Exceeded visit limits" — Request a medical exception; file an internal appeal, then external review</li>
</ul>
<p><em>The complete insurance appeals process is covered in the companion guide "The Autism Insurance Battle Guide."</em></p>

<h1>Part 8: Building Your Therapy Schedule</h1>

<h2>Age-Based Scheduling Guidelines</h2>
<table>
  <tr><th>Age</th><th>Priority Therapies</th><th>Key Considerations</th></tr>
  <tr><td>0–3 years</td><td>Early Intervention SLT, OT, developmental specialist, ABA</td><td>Home-based, family-centered; IFSP drives services</td></tr>
  <tr><td>3–6 years</td><td>ABA (intensive), SLT, OT, school special ed</td><td>Peak brain plasticity — maximize hours; coordinate school + private</td></tr>
  <tr><td>6–12 years</td><td>ABA (skill-focused), SLT, social skills group, OT for school</td><td>Balance therapy with school social inclusion; fatigue management</td></tr>
  <tr><td>12–18 years</td><td>Social skills, vocational prep, SLT for pragmatics, OT for independence</td><td>Transition planning; self-advocacy skills; independence targets</td></tr>
</table>

<h2>Preventing Therapy Fatigue</h2>
<ul>
  <li>Schedule therapy at your child's highest energy times (typically morning for most children)</li>
  <li>Build in free, unstructured time every day</li>
  <li>Watch for signs of burnout: increased meltdowns, school refusal, loss of skills</li>
  <li>Quality of sessions matters more than total hours — a burned-out child doesn't learn</li>
</ul>

<h1>Master Therapy Tracker</h1>
<table>
  <tr><th>Therapy</th><th>Provider</th><th>Days/Hours</th><th>Current Goals</th><th>Progress Rating</th></tr>
  <tr><td>ABA</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
  <tr><td>Speech-Language</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
  <tr><td>Occupational Therapy</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
  <tr><td>Physical Therapy</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
  <tr><td>Social Skills Group</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
  <tr><td>Other:</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
</table>

<h2>Resources</h2>
<table>
  <tr><th>Resource</th><th>URL</th></tr>
  <tr><td>BACB (Behavior Analyst Certification)</td><td>bacb.com</td></tr>
  <tr><td>ASHA (Speech-Language Pathology)</td><td>asha.org</td></tr>
  <tr><td>National Autism Center — Evidence Review</td><td>nationalautismcenter.org</td></tr>
  <tr><td>PEERS Program</td><td>semel.ucla.edu/autism/peers</td></tr>
</table>
"""
    build_pdf(
        title="The Complete Therapy Roadmap",
        subtitle="Evidence-Based Guide to Every Major Autism Therapy — What Works, What Doesn't, and How to Build the Right Team",
        price="$47",
        badge="Therapies & Interventions",
        toc=toc,
        body_html=body,
        filename="03-therapy-roadmap.pdf",
    )


# ══════════════════════════════════════════════════════════════════════════════
# GUIDE 4 — NAVIGATING THE DIAGNOSIS JOURNEY
# ══════════════════════════════════════════════════════════════════════════════

def guide_4():
    toc = [
        ("Introduction: The Diagnosis Changed Everything", "3"),
        ("Part 1: Understanding the Diagnostic Process", "4"),
        ("Part 2: DSM-5-TR Criteria — What Evaluators Look For", "6"),
        ("Part 3: The Evaluation Types Explained", "8"),
        ("Part 4: Getting an Evaluation — Your Action Plan", "10"),
        ("Part 5: After the Diagnosis — First 30 Days", "12"),
        ("Part 6: Processing the Emotional Journey", "15"),
        ("Part 7: Talking to Siblings and Family", "17"),
        ("Part 8: Building Your Support Network", "19"),
        ("90-Day Action Checklist", "21"),
    ]

    body = """
<h1>Introduction: The Diagnosis Changed Everything</h1>
<p>If you just received your child's autism diagnosis — or if you're still in the process of seeking one — this guide is written for you. The period around diagnosis is one of the most emotionally intense and practically overwhelming phases of the autism parenting journey.</p>
<p>You are flooded with information, unsure where to start, uncertain what this means for your child's future, and possibly processing grief, fear, and hope all at once.</p>
<p>This guide organizes the chaos. It tells you what the diagnosis actually means, what evaluators are looking for, how to get the most complete evaluation possible, and exactly what to do in the first 30, 60, and 90 days after diagnosis.</p>

<div class="callout callout-success">
  <div class="callout-title">The Most Important Thing to Know Right Now</div>
  <p>An autism diagnosis is the beginning of access — not the end of possibility. It opens the door to services, funding, legal protections, and a community of families who understand what you're going through. The earlier the diagnosis, the earlier the support begins, and the research on early intervention outcomes is genuinely hopeful.</p>
</div>

<h1>Part 1: Understanding the Diagnostic Process</h1>
<h2>Who Can Diagnose Autism?</h2>
<table>
  <tr><th>Professional</th><th>Setting</th><th>Notes</th></tr>
  <tr><td>Developmental Pediatrician</td><td>Hospital, specialty clinic</td><td>Gold standard; often long wait times</td></tr>
  <tr><td>Child Psychiatrist</td><td>Psychiatric clinic, hospital</td><td>Strong for complex presentations</td></tr>
  <tr><td>Neuropsychologist</td><td>Private practice, hospital</td><td>Most comprehensive cognitive picture</td></tr>
  <tr><td>Psychologist (PhD/PsyD)</td><td>Private practice</td><td>Accessible; quality varies widely</td></tr>
  <tr><td>School district team</td><td>Your child's school</td><td>Free; determines educational eligibility — may not be the same as clinical diagnosis</td></tr>
</table>

<div class="callout callout-warning">
  <div class="callout-title">Two Separate Evaluations May Be Needed</div>
  <p>A school district's educational evaluation determines whether your child qualifies for special education services. This is separate from a clinical diagnosis. You may need both. Get the clinical diagnosis first — it strengthens the school evaluation request.</p>
</div>

<h2>How Long Does Evaluation Take?</h2>
<ul>
  <li>Wait time for appointment: 3 months to 2+ years depending on your location</li>
  <li>Evaluation process itself: 1–3 days of testing spread over multiple visits</li>
  <li>Report delivery: 2–8 weeks after testing</li>
</ul>

<h2>Strategies to Reduce Wait Times</h2>
<ul class="checklist">
  <li>Get on multiple waiting lists simultaneously (don't wait for one to say no)</li>
  <li>Ask your pediatrician to initiate a referral — often speeds up the process</li>
  <li>Ask specifically about cancellation lists — many families get earlier appointments this way</li>
  <li>Check university training clinics — often shorter waits at reduced cost</li>
  <li>Contact your regional autism center (search "autism center of excellence near me")</li>
  <li>For school services: refer to the school district now, don't wait for clinical diagnosis</li>
</ul>

<h1>Part 2: DSM-5-TR Criteria — What Evaluators Look For</h1>
<p>The DSM-5-TR (2022) requires impairment in two core domains:</p>

<h2>Domain A: Social Communication and Interaction</h2>
<p>Must show deficits across all three of these areas:</p>
<ul>
  <li><strong>Social-emotional reciprocity</strong> — difficulty with back-and-forth conversation, reduced sharing of interests/emotions, failure to initiate/respond to social interactions</li>
  <li><strong>Nonverbal communication</strong> — difficulty integrating verbal and nonverbal communication, abnormal eye contact, limited facial expression, difficulty understanding gestures</li>
  <li><strong>Relationships</strong> — difficulties adjusting behavior to different social contexts, trouble making friends, absent interest in peers</li>
</ul>

<h2>Domain B: Restricted, Repetitive Behaviors</h2>
<p>Must show at least two of four:</p>
<table>
  <tr><th>Criterion</th><th>Examples</th></tr>
  <tr><td>Stereotyped/repetitive speech or behavior</td><td>Echolalia, lining up toys, hand flapping, spinning</td></tr>
  <tr><td>Insistence on sameness</td><td>Distress at minor changes, rigid routines, ritualized behavior</td></tr>
  <tr><td>Restricted interests</td><td>Intense preoccupation with specific topics or objects</td></tr>
  <tr><td>Sensory differences</td><td>Hyper or hypo-reactivity to sensory input, unusual interest in sensory aspects of environment</td></tr>
</table>

<h2>Additional Requirements</h2>
<ul>
  <li>Symptoms present in early developmental period (even if not fully apparent until later)</li>
  <li>Symptoms cause significant impairment in social, occupational, or other important functioning</li>
  <li>Not better explained by intellectual disability or global developmental delay alone</li>
</ul>

<h2>Severity Levels</h2>
<table>
  <tr><th>Level</th><th>Social Communication</th><th>Restricted/Repetitive Behaviors</th></tr>
  <tr><td>Level 1 — "Requiring Support"</td><td>Noticeable difficulties without supports; limited initiation</td><td>Inflexibility causes significant interference</td></tr>
  <tr><td>Level 2 — "Requiring Substantial Support"</td><td>Marked deficits; limited initiation; atypical responses</td><td>Inflexibility causes significant interference; distress when disrupted</td></tr>
  <tr><td>Level 3 — "Requiring Very Substantial Support"</td><td>Severe deficits; very limited initiation; minimal response</td><td>Extreme difficulty coping with change; marked interference</td></tr>
</table>

<h1>Part 3: The Evaluation Types Explained</h1>

<h2>Autism-Specific Assessments</h2>
<table>
  <tr><th>Tool</th><th>What It Is</th><th>Best For</th></tr>
  <tr><td>ADOS-2</td><td>Observational assessment; gold standard</td><td>All ages; most reliable diagnostic tool</td></tr>
  <tr><td>ADI-R</td><td>Structured parent interview</td><td>Developmental history; complements ADOS</td></tr>
  <tr><td>SCQ</td><td>Parent questionnaire</td><td>Screening; not diagnostic alone</td></tr>
  <tr><td>CARS-2</td><td>Clinician-rated severity scale</td><td>Additional severity characterization</td></tr>
</table>

<h2>Cognitive and Academic Testing</h2>
<ul>
  <li>WISC-V or WPPSI-IV (intelligence testing) — important for understanding learning profile and setting IEP goals</li>
  <li>Woodcock-Johnson or WIAT (academic achievement) — identifies learning disabilities co-occurring with autism</li>
</ul>

<h2>Adaptive Behavior Assessment</h2>
<p>Vineland-3 or ABAS-3 measures how the child functions in daily life — self-care, communication, socialization, motor skills. Often diverges significantly from cognitive scores. Critical for determining service needs.</p>

<div class="callout">
  <div class="callout-title">Push for a Comprehensive Evaluation</div>
  <p>A diagnosis-only evaluation (autism yes/no) is not enough. You want cognitive testing, adaptive behavior assessment, and ideally speech and OT screening. This complete picture drives better IEP goals and clearer service recommendations.</p>
</div>

<h1>Part 4: Getting an Evaluation — Your Action Plan</h1>

<h2>Before the Evaluation</h2>
<ul class="checklist">
  <li>Gather all previous developmental records: baby book, immunization records, any prior evaluations</li>
  <li>Write a developmental history summary: when child walked, talked, first words, any regression</li>
  <li>Video your child in natural settings: play, mealtime, transitions — evaluators often only see "best behavior" in clinic</li>
  <li>Request that your child's teachers complete rating scales before the evaluation</li>
  <li>Prepare a list of your specific concerns — be concrete and specific, not general</li>
</ul>

<h2>At the Evaluation</h2>
<ul>
  <li>Bring food and comfort items your child prefers — a comfortable child performs more naturally</li>
  <li>Disclose medications, sleep status, recent illness — all affect test performance</li>
  <li>Ask the evaluator what they observed that was most informative — good evaluators will tell you</li>
  <li>Request a copy of the full report, not just the summary</li>
</ul>

<h2>After You Receive the Report</h2>
<ul class="checklist">
  <li>Read the complete report — not just the summary or diagnosis page</li>
  <li>Make a list of questions before the feedback session</li>
  <li>Ask: "What are the top three things my child needs right now?"</li>
  <li>Ask for specific service recommendations and referrals in writing</li>
  <li>Get multiple copies — you will share this with the school, insurance, and multiple providers</li>
</ul>

<h1>Part 5: After the Diagnosis — First 30 Days</h1>

<h2>Week 1: The Immediate Priorities</h2>
<ul class="checklist">
  <li>Take a breath. You don't have to do everything at once.</li>
  <li>Share the diagnosis with immediate family as you're ready — on your timeline</li>
  <li>Contact your school district in writing — start the IEP evaluation process</li>
  <li>Get on your state's HCBS Medicaid waiver waiting list (this cannot wait)</li>
  <li>Contact your pediatrician — get referrals for ABA, SLT, and OT in one call</li>
</ul>

<h2>Weeks 2–4</h2>
<ul class="checklist">
  <li>Research ABA providers in your area (BACB.com for credential verification)</li>
  <li>Check insurance coverage: call member services, ask specifically about ABA therapy benefits</li>
  <li>Apply for SSI if family income is below threshold</li>
  <li>Open an ABLE account (15 minutes at ABLENRC.org)</li>
  <li>Find a local autism parent support group (Facebook, Autism Speaks local chapter, Arc)</li>
</ul>

<h2>Days 30–90</h2>
<ul class="checklist">
  <li>IEP meeting with school district (should happen within 60 days of referral)</li>
  <li>First ABA and/or SLT evaluation appointments scheduled</li>
  <li>Research and select primary providers</li>
  <li>Review and understand your insurance explanation of benefits</li>
  <li>Connect with other autism families — peer support is invaluable</li>
</ul>

<h1>Part 6: Processing the Emotional Journey</h1>
<p>The autism diagnosis journey doesn't follow a straight emotional path. Most parents cycle through a complex mix of emotions — sometimes grief and relief in the same hour, sometimes clarity and confusion on the same day.</p>

<h2>What Many Parents Experience</h2>
<ul>
  <li><strong>Relief</strong> — finally having an explanation. "We weren't imagining it."</li>
  <li><strong>Grief</strong> — mourning expectations. This is normal and valid.</li>
  <li><strong>Fear</strong> — for your child's future, for what comes next.</li>
  <li><strong>Determination</strong> — the drive to do everything you can.</li>
  <li><strong>Exhaustion</strong> — from navigating systems while managing grief.</li>
  <li><strong>Hope</strong> — because outcomes with early support are genuinely encouraging.</li>
</ul>

<div class="callout">
  <div class="callout-title">This Is Not Linear</div>
  <p>Many parents find that the grief resurfaces at transition points — starting school, middle school, approaching 18. This doesn't mean you haven't "accepted" the diagnosis; it means you're processing a new set of realities. Both things are true: your child is exactly who they are, and the challenges are real.</p>
</div>

<h2>Protecting Your Mental Health</h2>
<ul>
  <li>Your capacity to advocate depends on your wellbeing. Put on your own oxygen mask.</li>
  <li>Find at least one person — a spouse, friend, parent group — who can witness your experience without trying to fix it.</li>
  <li>Consider therapy for yourself. Processing this professionally is not weakness.</li>
  <li>Limit comparison — every autistic child is different. Your child's trajectory is their own.</li>
</ul>

<h1>Part 7: Talking to Siblings and Family</h1>

<h2>Talking to Siblings</h2>
<p>Children often already know their sibling is different — they need words for it. Age-appropriate, honest conversations reduce confusion and support healthy sibling relationships.</p>

<table>
  <tr><th>Age</th><th>What to Say</th></tr>
  <tr><td>Under 5</td><td>"Your brother/sister's brain works differently. It makes some things harder and some things really special."</td></tr>
  <tr><td>5–10</td><td>Introduce the word "autism." Explain specific differences simply. Validate their feelings about the extra attention their sibling needs.</td></tr>
  <tr><td>11+</td><td>More complete explanation. Answer honest questions. Discuss what this means for the family and for their sibling's future.</td></tr>
</table>

<h2>Talking to Extended Family</h2>
<p>Not everyone will respond well. Some common reactions and how to handle them:</p>
<ul>
  <li><strong>"He'll grow out of it"</strong> → "It's a neurological difference, not a phase. But early support does make a significant difference in outcomes."</li>
  <li><strong>"All kids are a little like that"</strong> → "The diagnosis means it significantly affects his daily functioning. We're getting him the support he needs."</li>
  <li><strong>Blame/guilt → </strong>"Autism is genetic — no one is to blame. What matters now is what we do next."</li>
</ul>

<h1>Part 8: Building Your Support Network</h1>

<h2>Your Core Team</h2>
<table>
  <tr><th>Person</th><th>Role</th></tr>
  <tr><td>Developmental pediatrician or psychiatrist</td><td>Medical management, co-occurring conditions, medication if needed</td></tr>
  <tr><td>BCBA (ABA supervisor)</td><td>Behavioral programming, parent training</td></tr>
  <tr><td>Speech-Language Pathologist</td><td>Communication development, AAC</td></tr>
  <tr><td>Occupational Therapist</td><td>Sensory, fine motor, daily living</td></tr>
  <tr><td>Special Education Teacher / IEP team</td><td>Educational programming</td></tr>
  <tr><td>Other autism parents</td><td>Peer support, provider recommendations, been-there advice</td></tr>
</table>

<h2>Finding Your Community</h2>
<ul>
  <li>Autism Speaks local chapters — autismspeaks.org</li>
  <li>The Arc — thearc.org</li>
  <li>Local Facebook groups: search "[Your City] autism parents"</li>
  <li>Autism Society of America — autism-society.org</li>
  <li>Online communities: Reddit r/autism (autistic perspective), r/autisticparents</li>
</ul>

<h1>90-Day Action Checklist</h1>
<h2>Days 1–7</h2>
<ul class="checklist">
  <li>Contact school district in writing to request special education evaluation</li>
  <li>Call state developmental disabilities agency — get on HCBS waiver list</li>
  <li>Contact pediatrician for therapy referrals (ABA, SLT, OT)</li>
  <li>Breathe. You are on it.</li>
</ul>
<h2>Days 8–30</h2>
<ul class="checklist">
  <li>Research and contact ABA providers</li>
  <li>Call insurance — confirm ABA and therapy coverage</li>
  <li>Apply for SSI (if income eligible)</li>
  <li>Open ABLE account at ABLENRC.org</li>
  <li>Find local parent support group and attend once</li>
</ul>
<h2>Days 31–90</h2>
<ul class="checklist">
  <li>Attend IEP meeting with school district</li>
  <li>Start first therapy (usually ABA and/or SLT)</li>
  <li>Schedule 3-month check-in with diagnosing provider</li>
  <li>Review and understand insurance billing and EOBs</li>
  <li>Connect with at least one other autism parent</li>
</ul>
"""
    build_pdf(
        title="Navigating the Diagnosis Journey",
        subtitle="From First Concerns Through the Diagnosis and Into Action — A Complete Guide for Autism Parents",
        price="$37",
        badge="Diagnosis & First Steps",
        toc=toc,
        body_html=body,
        filename="04-diagnosis-guide.pdf",
    )


# ══════════════════════════════════════════════════════════════════════════════
# GUIDE 5 — THE AUTISM INSURANCE BATTLE GUIDE
# ══════════════════════════════════════════════════════════════════════════════

def guide_5():
    toc = [
        ("Introduction: Why Insurance Is a Battle — And How to Win It", "3"),
        ("Part 1: Your Legal Rights — Federal and State Law", "4"),
        ("Part 2: Know Your Insurance Plan", "7"),
        ("Part 3: Getting Prior Authorization", "9"),
        ("Part 4: The Five Types of Denials and How to Fight Each", "11"),
        ("Part 5: The Letter of Medical Necessity", "14"),
        ("Part 6: The Complete 4-Level Appeal Process", "16"),
        ("Part 7: State-by-State Mandate Summary", "20"),
        ("Part 8: When Insurance Isn't Enough", "22"),
        ("Master Insurance Tracker", "24"),
    ]

    body = """
<h1>Introduction: Why Insurance Is a Battle — And How to Win It</h1>
<p>ABA therapy for autism costs $50,000–$150,000 per year. Speech therapy, occupational therapy, and other interventions add tens of thousands more. Without insurance coverage, most families cannot access the intensive services their children need.</p>
<p>Here's the truth: your insurer is legally required to cover autism treatment in most cases. But insurance companies routinely deny, delay, and limit coverage in ways that are illegal. They do it because most families don't know their rights and don't appeal.</p>
<p>This guide teaches you to fight back — and win.</p>

<div class="callout callout-success">
  <div class="callout-title">The Numbers on Appeals</div>
  <p>Studies show that 50–60% of insurance denials for autism therapy are overturned on appeal when families pursue them. Most families never appeal. If you appeal nothing else, appeal every denial for your child's therapy.</p>
</div>

<h1>Part 1: Your Legal Rights</h1>

<h2>Federal Law: The ACA and MHPAEA</h2>
<h3>Mental Health Parity and Addiction Equity Act (MHPAEA)</h3>
<p>Requires insurers to cover mental health and behavioral health conditions (including autism) no more restrictively than physical health conditions. This means:</p>
<ul>
  <li>Cannot impose visit limits on ABA if there are no visit limits on physical therapy</li>
  <li>Cannot require higher prior authorization requirements for autism therapy than for other conditions</li>
  <li>Cannot impose higher co-pays for behavioral health than medical/surgical services</li>
</ul>

<h3>Affordable Care Act (ACA)</h3>
<ul>
  <li>Plans sold in the individual/small group market (since 2014) must cover mental health and behavioral health as Essential Health Benefits</li>
  <li>Cannot have annual or lifetime dollar limits on EHB coverage</li>
  <li>Cannot deny coverage based on pre-existing conditions (including autism)</li>
</ul>

<h2>State Autism Mandates</h2>
<p>All 50 states and DC have passed laws requiring most insurance plans to cover autism treatment — including ABA. State laws vary in:</p>
<ul>
  <li>Which plans must comply (fully insured, small employer, large employer)</li>
  <li>Age limits (some end at 18 or 21)</li>
  <li>Dollar caps (some have annual or lifetime limits)</li>
  <li>Which providers are covered (BCBA vs. BCBA-D vs. BcaBA)</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">Self-Funded (ERISA) Plans Are Different</div>
  <p>If your employer self-funds its health plan (common at large companies), state autism mandates may NOT apply. Federal law (MHPAEA) still applies. Check your Summary Plan Description — it will say "self-funded" or "ERISA plan" if so. This makes the federal parity argument even more important.</p>
</div>

<h2>IDEA Requires Schools to Cover Educational Services</h2>
<p>Services that are "educationally necessary" must be provided by the school at no cost to you. Insurance can cover medically necessary therapy <em>in addition to</em> school services — not instead of.</p>

<h1>Part 2: Know Your Insurance Plan</h1>

<h2>Documents You Must Have</h2>
<ul class="checklist">
  <li>Summary of Benefits and Coverage (SBC) — one-page overview of what's covered</li>
  <li>Certificate of Coverage or Evidence of Coverage — full policy details</li>
  <li>Summary Plan Description (SPD) — for employer plans</li>
  <li>Your state's autism insurance mandate (search your state department of insurance website)</li>
</ul>

<h2>Key Questions to Ask Member Services</h2>
<ol>
  <li>"Does my plan cover ABA therapy for autism? Under what billing codes?"</li>
  <li>"Is there a visit limit or dollar cap on behavioral health services?"</li>
  <li>"What is the prior authorization process for ABA therapy?"</li>
  <li>"What documentation is required?"</li>
  <li>"Is there a network requirement — must the provider be in-network?"</li>
  <li>"Does my state's autism insurance mandate apply to my plan?"</li>
</ol>
<p><strong>Always document:</strong> Date, time, name of representative, and exactly what they told you. Follow up every call with a written email or letter confirming what you were told.</p>

<h2>Understanding Your Cost Structure</h2>
<table>
  <tr><th>Term</th><th>What It Means</th></tr>
  <tr><td>Deductible</td><td>Amount you pay before insurance starts — often $500–$5,000</td></tr>
  <tr><td>Out-of-pocket maximum</td><td>Maximum you pay per year — after this, insurance covers 100%</td></tr>
  <tr><td>Co-pay</td><td>Fixed dollar amount per visit ($20–$60 typical)</td></tr>
  <tr><td>Co-insurance</td><td>Percentage you pay after deductible (often 20–30%)</td></tr>
  <tr><td>In-network vs. out-of-network</td><td>In-network costs significantly less; out-of-network may not be covered</td></tr>
</table>

<h1>Part 3: Getting Prior Authorization</h1>
<h2>The Prior Authorization Playbook</h2>
<p>For ABA therapy, insurance will require prior authorization before approving services. The process typically goes:</p>
<ol>
  <li>Provider submits authorization request with supporting documentation</li>
  <li>Insurance medical director reviews request</li>
  <li>Decision within 15 business days (or 3 for urgent)</li>
  <li>Authorization approved, denied, or modified (fewer hours)</li>
</ol>

<h2>Documentation That Strengthens Authorization</h2>
<ul class="checklist">
  <li>Autism diagnosis report (from licensed diagnostician)</li>
  <li>Letter of Medical Necessity from diagnosing physician or psychiatrist</li>
  <li>ABA assessment from BCBA with specific treatment recommendations</li>
  <li>Current functional behavior assessment (FBA)</li>
  <li>Medical records documenting autism diagnosis and functional impairment</li>
  <li>Previous progress data if this is a re-authorization request</li>
</ul>

<div class="callout">
  <div class="callout-title">Get the Denial in Writing — Always</div>
  <p>If authorization is denied verbally, demand written notice of the denial with the specific reason and clinical criteria used to make the decision. You cannot effectively appeal a denial you don't have in writing.</p>
</div>

<h1>Part 4: The Five Types of Denials</h1>

<h2>Denial Type 1: "Not Medically Necessary"</h2>
<p><strong>What they're doing:</strong> Claiming the treatment isn't needed or appropriate for your child.</p>
<p><strong>How to fight it:</strong></p>
<ul>
  <li>Request a peer-to-peer review — your child's physician speaks directly to the insurance medical director</li>
  <li>Submit a Letter of Medical Necessity from the diagnosing physician</li>
  <li>Cite EPSDT (if Medicaid) which requires all medically necessary treatment</li>
  <li>Cite your state's autism mandate — most eliminate the "medical necessity" barrier for autism</li>
  <li>Reference clinical guidelines from BACB, AAP, or the US Surgeon General's report</li>
</ul>

<h2>Denial Type 2: "Experimental or Investigational"</h2>
<p><strong>What they're doing:</strong> Claiming ABA or other established autism therapies aren't proven.</p>
<p><strong>How to fight it:</strong> ABA is not experimental. It has 60+ years of peer-reviewed research and is endorsed by:</p>
<ul>
  <li>American Academy of Pediatrics</li>
  <li>US Surgeon General</li>
  <li>American Psychological Association</li>
  <li>National Institute of Mental Health</li>
</ul>
<p>Include these endorsements in your appeal letter. This type of denial is particularly vulnerable to appeal.</p>

<h2>Denial Type 3: "Exceeded Visit or Hour Limit"</h2>
<p><strong>What they're doing:</strong> Capping therapy at fewer hours than recommended.</p>
<p><strong>How to fight it:</strong></p>
<ul>
  <li>Invoke MHPAEA — if there's no comparable visit limit for physical therapy or other medical treatment, the behavioral health limit violates federal parity law</li>
  <li>Request a "medical exception" or "continuity of care" exception</li>
  <li>File a complaint with your state Department of Insurance for parity violations</li>
</ul>

<h2>Denial Type 4: "Out of Network — No Coverage"</h2>
<p><strong>What they're doing:</strong> Denying coverage because your provider isn't in-network.</p>
<p><strong>How to fight it:</strong></p>
<ul>
  <li>Request a network adequacy exception — if there are no in-network ABA providers in your area who can take your child, they must cover out-of-network at in-network rates</li>
  <li>Document all in-network providers who are unavailable (waitlists, not accepting new patients)</li>
</ul>

<h2>Denial Type 5: "Reduction of Hours"</h2>
<p><strong>What they're doing:</strong> Approving some hours but fewer than recommended (e.g., BCBA recommends 25 hours, insurer approves 10).</p>
<p><strong>How to fight it:</strong></p>
<ul>
  <li>Request the specific clinical criteria used to determine the hour limit</li>
  <li>Provide a counter-report from the BCBA explaining why the recommended hours are necessary</li>
  <li>Submit peer-reviewed research supporting the recommended intensity for your child's profile</li>
  <li>Compare to physical health equivalents — parity law applies</li>
</ul>

<h1>Part 5: The Letter of Medical Necessity</h1>
<h2>What It Is</h2>
<p>The Letter of Medical Necessity (LMN) is a physician letter stating that the requested treatment is medically necessary for your child. It is one of the most powerful documents in your arsenal.</p>

<h2>Who Writes It</h2>
<p>The LMN must come from a licensed physician (developmental pediatrician, psychiatrist, or pediatrician). Your child's BCBA can write the clinical recommendation; the physician signs and submits it.</p>

<h2>What a Strong LMN Includes</h2>
<ul class="checklist">
  <li>Confirmed autism diagnosis with date, diagnostic tool used, and severity level</li>
  <li>Specific functional impairments (with examples and data)</li>
  <li>Current treatment being requested (e.g., "40 hours/week ABA therapy")</li>
  <li>Clinical rationale citing research and guidelines</li>
  <li>Statement that without this treatment, the child's condition will deteriorate or fail to improve</li>
  <li>Prior treatments tried and outcomes (if applicable)</li>
  <li>Signature, credentials, contact information, date</li>
</ul>

<div class="callout">
  <div class="callout-title">Template Language for LMN</div>
  <p><em>"[Child name] carries a diagnosis of Autism Spectrum Disorder (Level [X]), established by [evaluation type] on [date]. The diagnosis is associated with significant impairments in [specific areas]. I am requesting authorization for [X] hours/week of [specific therapy] as this level of intensity is medically necessary to address [specific functional needs]. This recommendation is consistent with published guidelines from the American Academy of Pediatrics and the evidence base for intensive early behavioral intervention. Without this level of care, [child's name]'s functional deficits are expected to [worsen/fail to improve]."</em></p>
</div>

<h1>Part 6: The Complete 4-Level Appeal Process</h1>

<h2>Level 1: Internal Appeal</h2>
<p><strong>What it is:</strong> Formal written appeal to the insurance company's internal review department.</p>
<p><strong>Deadline:</strong> Generally 180 days from the denial notice.</p>
<p><strong>What to include:</strong></p>
<ul>
  <li>Written appeal letter citing specific legal basis (state mandate, MHPAEA, ACA)</li>
  <li>Letter of Medical Necessity</li>
  <li>Supporting clinical documentation</li>
  <li>Evidence from clinical literature supporting the treatment</li>
</ul>
<p><strong>Timeline:</strong> Non-urgent: 30 days. Urgent/concurrent care: 72 hours to 30 days.</p>

<h2>Level 2: External Independent Review</h2>
<p><strong>What it is:</strong> Review by an independent organization not affiliated with your insurer.</p>
<p><strong>Your right:</strong> Required by ACA for most plans. Request it when internal appeal is denied.</p>
<p><strong>Why it matters:</strong> External reviewers overturn insurance denials at rates significantly higher than internal appeals. The insurance company must accept the external reviewer's decision.</p>

<h2>Level 3: State Regulatory Complaint</h2>
<p><strong>What it is:</strong> Formal complaint to your state's Department of Insurance.</p>
<p><strong>When to use:</strong> Violations of state autism mandates or parity laws.</p>
<p><strong>Impact:</strong> State regulators can fine insurers and require coverage — and insurance companies know this.</p>
<p><strong>Where to file:</strong> Your state's Department of Insurance website.</p>

<h2>Level 4: Federal Complaint or Legal Action</h2>
<p><strong>What it is:</strong> ERISA complaint to US Department of Labor (employer plans), or legal action through an attorney.</p>
<p><strong>When to use:</strong> Systematic parity violations, bad faith denials after exhausting other options.</p>
<p><strong>Finding attorneys:</strong> Many disability and insurance attorneys work on contingency. Search for "health insurance appeal attorney" in your state, or contact your state's Protection &amp; Advocacy organization.</p>

<h1>Part 7: State-by-State Mandate Summary</h1>
<table>
  <tr><th>State Group</th><th>Coverage Level</th><th>Age Limit</th></tr>
  <tr><td>Most comprehensive (CA, NY, TX, FL, IL, PA)</td><td>No dollar cap, all behavioral services</td><td>Varies (18–21 most common)</td></tr>
  <tr><td>Strong mandates (most other states)</td><td>ABA required; some dollar caps</td><td>Typically 18 or 21</td></tr>
  <tr><td>Limited mandates</td><td>Diagnosis/assessment only; some older laws</td><td>Varies</td></tr>
</table>
<p><strong>Find your state's specific law:</strong> Search "[Your State] autism insurance mandate" or visit the Autism Speaks website's insurance state resource guide.</p>

<h1>Part 8: When Insurance Isn't Enough</h1>
<h2>Supplemental Funding Sources</h2>
<table>
  <tr><th>Source</th><th>What It Covers</th></tr>
  <tr><td>Medicaid / CHIP</td><td>Must cover all medically necessary care (EPSDT) for children under 21</td></tr>
  <tr><td>HCBS Waiver</td><td>Services insurance and Medicaid don't cover — get on waiting list NOW</td></tr>
  <tr><td>School district (IDEA)</td><td>Educationally necessary therapy at no cost</td></tr>
  <tr><td>Private foundations</td><td>Autism Care Today, ACT Today! — gap-fill grants</td></tr>
  <tr><td>Hospital financial assistance</td><td>Many providers have sliding-scale or charity care programs</td></tr>
</table>

<h1>Master Insurance Tracker</h1>
<table>
  <tr><th>Field</th><th>Your Information</th></tr>
  <tr><td>Insurance company name</td><td>&nbsp;</td></tr>
  <tr><td>Member ID number</td><td>&nbsp;</td></tr>
  <tr><td>Group number</td><td>&nbsp;</td></tr>
  <tr><td>Member services phone</td><td>&nbsp;</td></tr>
  <tr><td>Appeals department phone/fax</td><td>&nbsp;</td></tr>
  <tr><td>ABA prior auth status and dates</td><td>&nbsp;</td></tr>
  <tr><td>Annual deductible / met to date</td><td>&nbsp;</td></tr>
  <tr><td>Out-of-pocket maximum / met to date</td><td>&nbsp;</td></tr>
  <tr><td>Current open appeals</td><td>&nbsp;</td></tr>
  <tr><td>State insurance department contact</td><td>&nbsp;</td></tr>
</table>

<h2>Key Resources</h2>
<table>
  <tr><th>Resource</th><th>Contact</th></tr>
  <tr><td>Your state Insurance Department</td><td>Search "[state] department of insurance"</td></tr>
  <tr><td>Autism Speaks Insurance Resource</td><td>autismspeaks.org/insurance-coverage</td></tr>
  <tr><td>Patient Advocate Foundation</td><td>patientadvocate.org</td></tr>
  <tr><td>US Dept of Labor (ERISA complaints)</td><td>dol.gov/agencies/ebsa</td></tr>
</table>
"""
    build_pdf(
        title="The Autism Insurance Battle Guide",
        subtitle="How to Get Your Child's Therapy Covered — Fighting Denials, Winning Appeals, and Knowing Your Rights",
        price="$37",
        badge="Insurance & Coverage Rights",
        toc=toc,
        body_html=body,
        filename="05-insurance-battle.pdf",
    )


# ══════════════════════════════════════════════════════════════════════════════
# GUIDE 6 — TRANSITION TO ADULTHOOD PLANNER
# ══════════════════════════════════════════════════════════════════════════════

def guide_6():
    toc = [
        ("Introduction: The Transition Cliff", "3"),
        ("Part 1: The Adult Services Ecosystem", "4"),
        ("Part 2: Year-by-Year Planning Timeline (Ages 12–22)", "7"),
        ("Part 3: Guardianship vs. Alternatives", "11"),
        ("Part 4: Financial Planning for the Future", "14"),
        ("Part 5: SSI at Age 18 — The Most Important Application", "17"),
        ("Part 6: Post-Secondary Education and Training", "19"),
        ("Part 7: Employment Pathways", "21"),
        ("Part 8: Housing Options for Adults with Autism", "24"),
        ("Master Transition Checklist by Age", "27"),
    ]

    body = """
<h1>Introduction: The Transition Cliff</h1>
<p>Parents of children with autism often speak of a "transition cliff" — the moment when the intensive school-based services that supported their child for 18 years end, and the adult service system (underfunded, fragmented, and difficult to navigate) must pick up the pieces.</p>
<p>The statistics are sobering: only 58% of autistic young adults are employed in their first two years after high school. Nearly half live with parents as adults. Waitlists for adult residential and day services often stretch 5–15 years.</p>
<p>But families who plan early — starting at age 12 or even younger — arrive at that cliff with a bridge already built. This guide is your bridge-building manual.</p>

<div class="callout callout-warning">
  <div class="callout-title">The Single Most Important Insight in This Guide</div>
  <p>Adult services have waiting lists measured in years and sometimes decades. The families who get services are the ones who got on the waiting list years before they needed them. Start today, regardless of your child's age.</p>
</div>

<h1>Part 1: The Adult Services Ecosystem</h1>

<h2>How Adult Services Differ from Children's Services</h2>
<table>
  <tr><th>Children's System</th><th>Adult System</th></tr>
  <tr><td>Entitlement-based (IDEA, EPSDT)</td><td>Largely needs-based with waiting lists</td></tr>
  <tr><td>School-led coordination</td><td>Self/family navigated</td></tr>
  <tr><td>Many free services</td><td>Primarily insurance/Medicaid-funded</td></tr>
  <tr><td>One primary contact (IEP team)</td><td>Multiple agencies, no coordinator</td></tr>
  <tr><td>Services guaranteed by law</td><td>Services subject to funding and availability</td></tr>
</table>

<h2>The Major Adult Service Categories</h2>

<h3>1. Medicaid-Funded Adult Services</h3>
<p>Medicaid remains the backbone of adult disability services. Two main types:</p>
<ul>
  <li><strong>State Plan Services:</strong> Outpatient therapy, mental health, medical care</li>
  <li><strong>HCBS Waivers:</strong> The critical funding source for day programs, residential, employment supports, respite</li>
</ul>

<h3>2. Vocational Rehabilitation (VR)</h3>
<p>Federally funded, state-administered program that funds job training, supported employment, assistive technology, and college support. Must apply — not automatic. Most states start VR services at age 16 while student is still in school.</p>

<h3>3. Developmental Disabilities (DD) Agency</h3>
<p>Your state's DD agency coordinates adult services including residential options, day programs, employment supports, and crisis services. This is the agency that manages HCBS waiver waiting lists.</p>

<h3>4. Social Security (SSI/SSDI)</h3>
<p>At age 18, parental income is no longer counted. Almost every autistic young adult should apply for SSI on or just before their 18th birthday. This is frequently the largest source of income and also triggers Medicaid continuation.</p>

<h3>5. Supported Employment Programs</h3>
<p>Customized Employment and Supported Employment programs match autistic adults with jobs suited to their strengths and provide job coaching. Funded through VR and HCBS waivers.</p>

<h1>Part 2: Year-by-Year Planning Timeline</h1>

<h2>Ages 12–14: Laying the Foundation</h2>
<ul class="checklist">
  <li>Start transition-focused IEP goals — IDEA requires transition planning to begin by age 16, but starting at 12–14 gives you more time</li>
  <li>Get on your state's DD agency waiting list NOW if not already on it</li>
  <li>Apply for ABLE account if not already open</li>
  <li>Begin vocational exploration — what does your child enjoy? What are they good at?</li>
  <li>Start building self-advocacy skills</li>
  <li>Explore guardianship alternatives — decision support, supported decision-making</li>
</ul>

<h2>Ages 14–16: Building Toward Independence</h2>
<ul class="checklist">
  <li>First formal transition IEP — include vocational goals, post-secondary vision</li>
  <li>Invite the student to participate meaningfully in their own IEP meeting</li>
  <li>Begin community-based vocational experiences</li>
  <li>Contact Vocational Rehabilitation — students can be enrolled while still in school</li>
  <li>Research post-secondary options: college, trade programs, day programs, supported employment</li>
  <li>Begin financial planning: SSI projections, Special Needs Trust planning</li>
</ul>

<h2>Ages 16–18: Active Transition Work</h2>
<ul class="checklist">
  <li>Transition IEP must specify: post-secondary education goals, employment goals, independent living goals</li>
  <li>Increase work experience and community participation</li>
  <li>Active VR enrollment and service plan</li>
  <li>Consult an attorney about guardianship options (18th birthday planning)</li>
  <li>Begin SSI application at age 17 years and 9 months (can apply up to 3 months early)</li>
  <li>Tour adult day programs and residential options — even years ahead of need</li>
  <li>Meet with estate planning attorney about Special Needs Trust</li>
</ul>

<h2>Age 18: The Major Transition Points</h2>
<ul class="checklist">
  <li><strong>SSI APPLICATION</strong> — file as close to the 18th birthday as possible; parental income no longer counted</li>
  <li>Medicaid continuation (SSI triggers Medicaid in most states)</li>
  <li>Legal decisions: who can make healthcare and financial decisions? Guardianship? Supported decision-making?</li>
  <li>Selective Service registration (required for males within 30 days of 18th birthday)</li>
  <li>Healthcare transition — move from pediatric to adult providers</li>
  <li>College: disability services registration (very different process than K-12)</li>
</ul>

<h2>Ages 18–22: Final School Years (IDEA Extends to Age 21/22)</h2>
<ul class="checklist">
  <li>Maximize school-based transition services — this is the last free intensive support</li>
  <li>Paid work experience with supports</li>
  <li>Independent living skills training</li>
  <li>Finalize post-secondary placement (job, program, college, or combination)</li>
  <li>Establish adult medical team before school ends</li>
  <li>Handoff from school-based services to adult VR and DD services</li>
</ul>

<h2>Age 22+: Adult Life Launch</h2>
<ul class="checklist">
  <li>HCBS waiver services begin (if on waiting list since childhood)</li>
  <li>Employment: supported, competitive integrated, self-employment</li>
  <li>Housing: family home, shared living, supervised residential, own home</li>
  <li>Ongoing medical, behavioral, and mental health support</li>
  <li>Annual SSI review and update</li>
  <li>Community participation and social connections</li>
</ul>

<h1>Part 3: Guardianship vs. Alternatives</h1>

<h2>What Is Guardianship?</h2>
<p>Legal guardianship gives you the court-authorized right to make legal, financial, and/or medical decisions for another adult who is determined to lack decision-making capacity. It is not automatic — you must petition the court.</p>

<div class="callout callout-warning">
  <div class="callout-title">Guardianship Is Not Always the Right Answer</div>
  <p>Full guardianship removes all legal rights from your child. Many autistic adults can make their own decisions in some or most areas — they just need support and accessibility accommodations to do so. Removing all rights can undermine self-determination and dignity. Consider alternatives first.</p>
</div>

<h2>Guardianship Types</h2>
<table>
  <tr><th>Type</th><th>What It Covers</th><th>Best For</th></tr>
  <tr><td>Full/Plenary Guardianship</td><td>All decisions — medical, financial, residential</td><td>Individuals who truly cannot make any decisions independently</td></tr>
  <tr><td>Limited Guardianship</td><td>Specific areas only (e.g., medical only)</td><td>Individuals with partial decision-making capacity</td></tr>
  <tr><td>Guardianship of the Person</td><td>Personal/medical decisions</td><td>When financial decisions are not in question</td></tr>
  <tr><td>Guardianship of the Estate</td><td>Financial decisions only</td><td>When financial management is the concern</td></tr>
</table>

<h2>Alternatives to Guardianship</h2>
<table>
  <tr><th>Alternative</th><th>Description</th><th>Cost</th></tr>
  <tr><td>Supported Decision-Making Agreement</td><td>Formal agreement naming trusted people to support decision-making without removing rights</td><td>Low — template agreements available</td></tr>
  <tr><td>Healthcare Proxy / Medical POA</td><td>Designates a decision-maker for medical situations only</td><td>Free to low cost</td></tr>
  <tr><td>Durable Power of Attorney</td><td>Financial decision-making support</td><td>Attorney fees — $200–$500</td></tr>
  <tr><td>Representative Payee</td><td>SSA program — manages SSI payments; does not require guardianship</td><td>Free</td></tr>
</table>

<h1>Part 4: Financial Planning for the Future</h1>

<h2>The Special Needs Trust (SNT)</h2>
<p>A Special Needs Trust allows you to leave money to your child without disqualifying them from SSI and Medicaid. Without a properly structured SNT, an inheritance over $2,000 disqualifies your child from SSI.</p>

<h3>Types of Special Needs Trusts</h3>
<table>
  <tr><th>Type</th><th>Funded By</th><th>Best For</th></tr>
  <tr><td>First-Party / Self-Settled SNT</td><td>Child's own assets (personal injury settlement, inheritance directly to child)</td><td>When child receives direct inheritance or legal award</td></tr>
  <tr><td>Third-Party SNT</td><td>Family members, estate planning</td><td>Most families — funded through will, life insurance, gifting</td></tr>
  <tr><td>Pooled SNT</td><td>Non-profit manages pool of beneficiary funds</td><td>Smaller trusts where private trustee isn't practical</td></tr>
</table>

<div class="callout callout-warning">
  <div class="callout-title">Critical: Use an Attorney</div>
  <p>A poorly drafted Special Needs Trust can disqualify your child from benefits. Use an attorney who specializes in special needs planning. Find one through the Academy of Special Needs Planners (specialneedsanswers.com).</p>
</div>

<h2>ABLE Account (Supplement to SNT)</h2>
<p>ABLE accounts (covered in the Benefits Navigator) complement Special Needs Trusts. Use for smaller, flexible expenses. SNT for larger, managed assets.</p>

<h2>Life Insurance Considerations</h2>
<p>Your child may depend on you financially long after most adults are independent. Consider:</p>
<ul>
  <li>Sufficient life insurance to fund the SNT</li>
  <li>Name the Special Needs Trust as beneficiary — never name the child directly</li>
  <li>Term vs. permanent insurance: consult a fee-only financial planner</li>
</ul>

<h2>Letter of Intent</h2>
<p>Not a legal document, but equally important: a Letter of Intent is a detailed guide for future caregivers describing your child's medical needs, communication style, preferences, behaviors, routines, relationships, and what matters most to them. Write this and update it annually.</p>

<h1>Part 5: SSI at Age 18</h1>
<p>This is the highest-impact financial action most autism families can take. When your child turns 18:</p>
<ul>
  <li>Parental income is NO LONGER counted — even high-income families may now qualify</li>
  <li>Only the child's own income and assets are considered</li>
  <li>Benefit: up to $943/month (2024, adjusted annually)</li>
  <li>SSI triggers Medicaid in most states — maintaining healthcare coverage</li>
</ul>

<h2>How to Apply at 18</h2>
<ol>
  <li>Apply at SSA.gov or by calling 1-800-772-1213 — can apply up to 3 months before 18th birthday</li>
  <li>Gather: proof of age, Social Security card, medical records documenting autism and functional limitations, proof of income/assets</li>
  <li>Complete the Adult Disability Report — describe your child's WORST days, not average days</li>
  <li>If denied: appeal immediately. Do not accept the initial denial without appealing.</li>
</ol>

<h2>Protecting SSI Eligibility</h2>
<ul>
  <li>Keep countable resources under $2,000 (ABLE account and SNT assets are excluded)</li>
  <li>Report all income and resource changes to SSA within 10 days</li>
  <li>Understand what counts as income: wages, gifts, in-kind support</li>
  <li>Get a Representative Payee if your child cannot manage their SSI payments</li>
</ul>

<h1>Part 6: Post-Secondary Education</h1>

<h2>Types of Post-Secondary Programs</h2>
<table>
  <tr><th>Program Type</th><th>Examples</th><th>Best For</th></tr>
  <tr><td>Inclusive college programs</td><td>Think College network</td><td>Students who want college experience with supports</td></tr>
  <tr><td>Certificate/vocational programs</td><td>Community college, trade school</td><td>Career-focused, specific skill development</td></tr>
  <tr><td>Transition programs (18–22)</td><td>School-based, often campus-hosted</td><td>Students completing IDEA-funded transition services</td></tr>
  <tr><td>Adult learning programs</td><td>Community-based, non-credit</td><td>Life skills, social, community participation</td></tr>
</table>

<h2>College Disability Services — Key Differences from K-12</h2>
<ul>
  <li>Colleges do NOT have to develop IEPs or provide FAPE</li>
  <li>Students must self-identify and self-advocate — the system will not find them</li>
  <li>Documentation of disability must be provided by the student</li>
  <li>Accommodations are reasonable modification, not specialized education</li>
  <li>Register with the disability services office before classes start</li>
</ul>

<h1>Part 7: Employment Pathways</h1>

<h2>Employment Models</h2>
<table>
  <tr><th>Model</th><th>Description</th><th>Who It's Best For</th></tr>
  <tr><td>Competitive Integrated Employment</td><td>Regular job at minimum wage or higher, working alongside non-disabled peers</td><td>All autistic adults should be given the opportunity</td></tr>
  <tr><td>Supported Employment</td><td>Competitive employment with ongoing job coaching support</td><td>Those who need support to maintain employment</td></tr>
  <tr><td>Customized Employment</td><td>Job carved or created to match individual's specific strengths</td><td>Individuals with complex needs</td></tr>
  <tr><td>Self-Employment / Microenterprise</td><td>Own business, often using special interest as foundation</td><td>Individuals with strong specific interests and entrepreneurial potential</td></tr>
</table>

<h2>The Role of Vocational Rehabilitation</h2>
<p>VR provides: career assessment, job training, supported employment funding, workplace accommodations, college funding, and more. Free for eligible individuals with disabilities. Apply as early as age 16 in most states.</p>

<h2>Autism-Friendly Employers</h2>
<p>Many major employers have active neurodiversity hiring programs including Microsoft, SAP, JPMorgan Chase, EY, and others. These programs provide structured onboarding and ongoing support for autistic employees.</p>

<h1>Part 8: Housing Options for Adults with Autism</h1>

<h2>The Housing Spectrum</h2>
<table>
  <tr><th>Setting</th><th>Level of Support</th><th>Funding Sources</th></tr>
  <tr><td>Family home</td><td>Family-provided support</td><td>SSI, VR, day programs</td></tr>
  <tr><td>Shared living / Host home</td><td>Adult lives with and is supported by a trained family</td><td>HCBS waiver</td></tr>
  <tr><td>Supported living / ILS</td><td>Own home or apartment with scheduled support staff</td><td>HCBS waiver, SSI, Section 8</td></tr>
  <tr><td>Group home / CLA</td><td>Shared home with 24-hour residential staff</td><td>HCBS waiver</td></tr>
  <tr><td>ICF/IDD</td><td>Institutional setting with intensive medical support</td><td>Medicaid</td></tr>
</table>

<div class="callout callout-success">
  <div class="callout-title">The Goal: Supported Independence</div>
  <p>Research consistently shows that autistic adults do best with the least restrictive setting that still meets their needs. Supported independent living — own or shared home with paid support staff — is the preferred model for most autistic adults and is significantly less expensive than institutional settings.</p>
</div>

<h2>Section 8 / Housing Choice Voucher for Adults</h2>
<p>Disabled adults can receive Section 8 vouchers — subsidizing rent in private housing. Waiting lists are long. If your child is on a Section 8 waiting list from childhood, confirm they can transfer to an adult voucher. Apply at your local PHA today if not already on the list.</p>

<h1>Master Transition Checklist by Age</h1>
<h2>Age 12–14</h2>
<ul class="checklist">
  <li>Get on state DD agency waiting list</li>
  <li>Open ABLE account</li>
  <li>Begin vocational exploration</li>
  <li>Start self-advocacy skill building</li>
  <li>Research guardianship alternatives</li>
</ul>
<h2>Age 14–16</h2>
<ul class="checklist">
  <li>Transition IEP begins</li>
  <li>Contact Vocational Rehabilitation</li>
  <li>Community work experiences begin</li>
  <li>Research post-secondary options</li>
  <li>Begin Special Needs Trust planning</li>
</ul>
<h2>Age 16–18</h2>
<ul class="checklist">
  <li>Apply for SSI at 17 years 9 months</li>
  <li>Meet with estate planning attorney</li>
  <li>Tour adult day programs and residential options</li>
  <li>Active VR enrollment</li>
  <li>Make guardianship decisions</li>
</ul>
<h2>Age 18</h2>
<ul class="checklist">
  <li>SSI application submitted</li>
  <li>Selective Service registration (males)</li>
  <li>Legal decision-making structure in place</li>
  <li>Healthcare transition to adult providers</li>
  <li>College disability services registration if applicable</li>
</ul>
<h2>Ages 18–22</h2>
<ul class="checklist">
  <li>Maximize school-based transition services</li>
  <li>Paid work experience with supports</li>
  <li>Independent living skills training</li>
  <li>Adult medical team established</li>
  <li>Post-secondary placement finalized</li>
</ul>

<h2>Key Resources</h2>
<table>
  <tr><th>Resource</th><th>Where</th></tr>
  <tr><td>Think College (post-secondary programs)</td><td>thinkcollege.net</td></tr>
  <tr><td>Autism Speaks Adult Services</td><td>autismspeaks.org/adult-services</td></tr>
  <tr><td>Academy of Special Needs Planners</td><td>specialneedsanswers.com</td></tr>
  <tr><td>ABLE National Resource Center</td><td>ablenrc.org</td></tr>
  <tr><td>US Dept of Labor — Disability Resources</td><td>dol.gov/agencies/odep</td></tr>
</table>
"""
    build_pdf(
        title="Transition to Adulthood Planner",
        subtitle="The Complete Year-by-Year Guide to Adult Services, SSI, Housing, Employment, and Financial Planning for Autism Families",
        price="$47",
        badge="Adult Transition & Planning",
        toc=toc,
        body_html=body,
        filename="06-transition-planning.pdf",
    )


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\nGenerating SpectrumReady PDF guides...\n")
    guide_free()
    guide_1()
    guide_2()
    guide_3()
    guide_4()
    guide_5()
    guide_6()
    print(f"\nAll PDFs saved to: {OUT_DIR}\n")
