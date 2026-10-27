"""Builds the site's HTML pages from one shared header and footer.

Run:  python _build/build.py   (from the site folder, or pass the site folder as an argument)
Edit page content below, then re-run to regenerate the .html files.
"""
import hashlib
import os
import sys

SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAV = [("index.html", "Home"), ("services.html", "Services"), ("about.html", "About"),
       ("owner.html", "Owner"), ("contact.html", "Contact")]

SHIELD = '<svg class="shield" viewBox="0 0 14 16" aria-hidden="true"><path d="M7 0 14 3v5c0 4-3 7-7 8-4-1-7-4-7-8V3z" fill="currentColor"/></svg>'


def ver(path):
    with open(os.path.join(SITE, path), 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def head(title, desc):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;1,500&family=Mulish:wght@400;600;700&display=swap">
<link rel="stylesheet" href="assets/styles.css?v={ver('assets/styles.css')}">
</head>
<body>
'''


def header(active):
    links = "\n".join(
        f'      <li><a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a></li>'
        for href, label in NAV)
    return f'''<header class="site">
  <div class="wrap">
    <a class="brand" href="index.html"><img class="logo" src="assets/logo.png" alt="Jurgen Software Solutions" width="520" height="139"></a>
    <nav aria-label="Main"><ul>
{links}
    </ul></nav>
  </div>
</header>
'''


FOOTER = lambda: f'''<footer>
  <div class="wrap">
    <div class="foot-top">
      <a class="brand" href="index.html"><img class="logo" src="assets/logo.png" alt="Jurgen Software Solutions" width="520" height="139"></a>
      <div>
        <div class="links-title">Our other work</div>
        <ul class="links">
          <li><a href="https://github.com/gameovercheeseburger/AnthropicJobHunt" target="_blank" rel="noopener">Anthropic Job Hunt</a></li>
        </ul>
      </div>
    </div>
    <p class="copy">© 2026 Jurgen Software Solutions. All rights reserved.</p>
  </div>
</footer>
<script src="assets/site.js?v={ver('assets/site.js')}"></script>
</body>
</html>
'''


def quote_band(text, who):
    return f'''<section class="quote" aria-label="Quotation">
  <div class="wrap reveal">
    <span class="orn">◆ ◆ ◆</span>
    <blockquote>“{text}”</blockquote>
    <cite>{who}</cite>
  </div>
</section>
'''


def page_hero(eyebrow, title, lead):
    return f'''<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <div class="gold-rule"></div>
    <p class="lead">{lead}</p>
  </div>
</section>
'''


CTA_BAND = '''<section class="block">
  <div class="wrap reveal" style="justify-items:center;text-align:center">
    <h2>Have a project in mind?</h2>
    <p class="muted">Tell us what you need and we will reply with a clear plan and an honest estimate.</p>
    <div class="cta" style="justify-content:center"><a class="btn solid" href="contact.html" data-quote>Request a quote</a><a class="btn ghost-dark" href="contact.html">Contact us</a></div>
  </div>
</section>
'''


def svc(title, text, tags, cls=""):
    t = "".join(f"<span>{x}</span>" for x in tags)
    c = f"svc {cls}".strip()
    return f'      <div class="{c} reveal"><h3>{title}</h3><p>{text}</p><div class="tags">{t}</div></div>\n'


SERVICES = [
    ("ETL &amp; Data Pipelines", "Our specialty. Reliable, secure pipelines that move data from your systems into a warehouse your team can trust.", ["SSIS", "AWS Glue", "Oracle Data Integrator", "Python", "PowerShell"], "etl-card"),
    ("AI &amp; Automation", "Practical AI that saves time: LLM features inside your apps, agentic workflows, and automation of repetitive work.", ["OpenAI APIs", "Claude", "Agentic AI", "Prompt engineering", "Python automation"], "ai"),
    ("Custom Software Development", "Backend services and business applications built to enterprise standards, from small tools to full systems.", ["C# / .NET", "Java", "Spring Boot", "Python", "Node.js"], ""),
    ("Web &amp; Front-End", "Fast, accessible websites, dashboards and web apps, including custom CMS solutions.", ["React", "TypeScript", "JavaScript", "HTML / CSS"], ""),
    ("APIs &amp; Systems Integration", "Connect your ERP, finance, CRM and reporting systems so data flows without manual work.", ["REST", "SOAP", "GraphQL", "Kafka", "RabbitMQ", "Apache Camel"], ""),
    ("Cloud &amp; DevOps", "Cloud setup, containers and automated build-and-release pipelines with reliable rollback.", ["AWS", "Azure", "Oracle Cloud", "OpenShift", "Docker", "CI/CD"], ""),
    ("Data Warehousing &amp; BI", "Warehouses, OLAP cubes and dashboards that turn raw records into decisions.", ["Power BI", "Infor DWD / EPM", "Oracle BI", "Crystal Reports"], ""),
    ("Database Design", "Well-structured databases, efficient queries and stored procedures that scale with you.", ["SQL Server", "Oracle", "PostgreSQL", "MySQL", "Azure SQL"], ""),
    ("Legacy Modernization", "Refactor ageing VB6, C++ and servlet code into clean, maintainable modern services.", ["Refactoring", "Design patterns", "Microservices"], ""),
    ("Security", "Authentication, access control and secure coding built in from the start, not bolted on.", ["OAuth", "JWT", "Encryption", "Secure coding"], ""),
    ("Testing &amp; Quality", "Test plans and automated tests that catch problems before your users do.", ["Unit &amp; integration", "Automated testing", "SIT / UAT", "Code review"], ""),
    ("Support &amp; Maintenance", "Production monitoring, incident investigation and root-cause fixes to keep systems running.", ["Splunk", "Monitoring", "Tier-1 &amp; 2 support"], ""),
]


def etl_stage(step, name, text, items, sec):
    it = "".join(f"<li>{x}</li>" for x in items)
    sc = "".join(f"<li>{x}</li>" for x in sec)
    return f'''      <div class="etl-stage">
        <div class="etl-top"><span class="step">{step}</span><h3>{name}</h3></div>
        <div class="etl-body"><p>{text}</p><ul class="etl-items">{it}</ul></div>
        <div class="etl-sec"><span class="lbl">{SHIELD} Security at this stage</span><ul>{sc}</ul></div>
      </div>
'''


ARROW = '      <div class="etl-arrow" aria-hidden="true"><i></i><i></i><i></i></div>\n'

ETL = f'''<section class="block" id="etl">
  <div class="wrap">
    <div class="two reveal">
      <div class="head">
        <span class="eyebrow">Our specialty</span>
        <h2>ETL: how your data gets from A to B, safely</h2>
      </div>
      <div class="stack">
        <p>ETL stands for Extract, Transform, Load. It is how data from many separate systems becomes one clean, reliable source for reporting and decisions.</p>
        <p class="muted">Security is not a single step at the end. Each stage has its own risks, so each stage gets its own protection, and the whole pipeline is watched from end to end.</p>
      </div>
    </div>
    <div class="etl reveal">
      <div class="etl-ends">
        <div class="etl-end"><b>Sources</b> ERP · databases · APIs · files &amp; SFTP · cloud storage (S3)</div>
        <div class="etl-end"><b>Destination</b> data warehouse · OLAP cubes · BI dashboards</div>
      </div>
      <div class="etl-flow">
{etl_stage("Step 1", "Extract", "Pull data from each source system on a schedule or as changes happen, without slowing those systems down.", ["SQL queries", "REST / SOAP APIs", "SFTP", "Amazon S3", "Change data capture"], ["Encrypted connections only (TLS, SFTP)", "Read-only service accounts with least privilege", "Credentials kept in a secrets vault, never in code"])}{ARROW}{etl_stage("Step 2", "Transform", "Clean, validate and reshape the data: fix formats, remove duplicates, apply business rules and join sources together.", ["Cleansing", "Validation", "Mapping", "Deduplication", "Business rules"], ["Sensitive fields masked or tokenized (PII)", "Validation rejects bad or tampered records", "Isolated staging area with restricted access"])}{ARROW}{etl_stage("Step 3", "Load", "Write the finished data into the warehouse and refresh cubes and dashboards so reports are always current.", ["Data warehouse", "OLAP cubes", "Power BI", "Scheduled refresh"], ["Encryption at rest in the warehouse", "Role-based access to reports and tables", "Backups with tested restores"])}      </div>
      <div class="etl-across">
        <span class="lbl">{SHIELD} Across the whole pipeline</span>
        <ul><li>Audit logs of every run</li><li>Monitoring &amp; failure alerts</li><li>Data lineage tracking</li><li>Compliance-ready controls</li></ul>
      </div>
    </div>
  </div>
</section>
'''

PAGES = {}

PAGES["index.html"] = ("Jurgen Software Solutions", "Custom software, ETL and data pipelines, AI, cloud and support from Jurgen Software Solutions.", f'''<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Custom software · Est. 2026</span>
    <h1>Software Built to Last</h1>
    <div class="gold-rule"></div>
    <p class="tagline">Careful engineering for businesses that expect it done properly.</p>
    <p class="lead">Jurgen Software Solutions handles every part of your technology, from custom code and websites to ETL pipelines, AI, cloud, data and ongoing support. Led by an engineer with enterprise experience at IBM, Infor and Accenture, we work in short, visible iterations, so you see progress every week and never wonder where your project stands.</p>
    <div class="cta"><a class="btn solid" href="contact.html" data-quote>Request a quote</a><a class="btn ghost" href="services.html">Our services</a></div>
  </div>
</section>

<section class="block">
  <div class="wrap two reveal">
    <div class="head">
      <span class="eyebrow">Our approach</span>
      <h2>The right tool for the right job</h2>
    </div>
    <div class="stack">
      <p>Every engagement starts with the problem, not the technology. We study how your people work today, where time is lost, and what a good result would look like before a single line of code is written.</p>
      <p class="muted">If an off-the-shelf product already solves your problem well, we will tell you so. Our aim is the right outcome for your business, even when that means less work for us.</p>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Our value promise</span>
      <h2>The client comes first</h2>
      <p class="muted">Three commitments we make on every project, large or small.</p>
    </div>
    <div class="promises reveal">
      <div class="promise"><span class="mark">i.</span><h3>Always reachable</h3><p class="muted">Clear lines of communication and prompt replies. When something matters to you, it matters to us.</p></div>
      <div class="promise"><span class="mark">ii.</span><h3>Broad problem-solving</h3><p class="muted">From database design to user interface, we cover the full stack so your project never stalls between specialists.</p></div>
      <div class="promise"><span class="mark">iii.</span><h3>Industry experience</h3><p class="muted">Oil and gas, retail, ERP, finance, banking, insurance and enterprise reporting. We learn your vocabulary quickly and build to fit it.</p></div>
    </div>
  </div>
</section>

{quote_band("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra")}
<section class="block">
  <div class="wrap">
    <div class="two reveal">
      <div class="head">
        <span class="eyebrow">What we do</span>
        <h2>From the first line of code to AI</h2>
      </div>
      <div class="stack">
        <p class="muted">Twelve service areas covering the whole technology stack, with a specialty in ETL and data pipelines.</p>
        <a class="more" href="services.html">See all services</a>
      </div>
    </div>
    <div class="services">
{"".join(svc(*s) for s in SERVICES[:6])}    </div>
  </div>
</section>

{CTA_BAND}''')

PAGES["services.html"] = ("Services · Jurgen Software Solutions", "ETL and data pipelines, AI, custom software, cloud, databases, security and support.", f'''{page_hero("Services", "Premium application development", "From the first line of code to AI, cloud and data, we cover the whole technology stack. Engage us for a complete build, or for the one part of it you need help with.")}
{ETL}
{quote_band("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson")}
<section class="block">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">All services</span>
      <h2>Everything your technology needs</h2>
    </div>
    <div class="services">
{"".join(svc(*s) for s in SERVICES)}    </div>
  </div>
</section>

{CTA_BAND}''')

PAGES["about.html"] = ("About · Jurgen Software Solutions", "About Jurgen Software Solutions: our mission, method and values.", f'''{page_hero("About us", "A small firm with high standards", "Founded on a simple idea: clients deserve software that works the first time, is easy to maintain, and is delivered by people who answer the phone.")}
<section class="block">
  <div class="wrap two">
    <div class="stack reveal">
      <div class="head">
        <span class="eyebrow">Who we are</span>
        <h2>Direct access to the people building your product</h2>
      </div>
      <p>We keep our team small on purpose. You work directly with the owner and the engineers building your product, with no layers of account management in between.</p>
      <p class="muted">Our background is enterprise software for ERP, finance, banking, insurance, oil and gas and retail. We bring that discipline to businesses of every size.</p>
    </div>
    <div class="about-card reveal">
      <dl>
        <dt>Mission</dt><dd>To build honest, well-crafted software that helps our clients do their best work.</dd>
        <dt>Method</dt><dd>Agile delivery in short iterations, with a working demo at every step.</dd>
        <dt>Values</dt><dd>Clarity, craftsmanship and accountability.</dd>
      </dl>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">How we work</span>
      <h2>The client comes first</h2>
    </div>
    <div class="promises reveal">
      <div class="promise"><span class="mark">i.</span><h3>Always reachable</h3><p class="muted">Clear lines of communication and prompt replies. When something matters to you, it matters to us.</p></div>
      <div class="promise"><span class="mark">ii.</span><h3>Broad problem-solving</h3><p class="muted">From database design to user interface, we cover the full stack so your project never stalls between specialists.</p></div>
      <div class="promise"><span class="mark">iii.</span><h3>Industry experience</h3><p class="muted">Oil and gas, retail, ERP, finance, banking, insurance and enterprise reporting. We learn your vocabulary quickly and build to fit it.</p></div>
    </div>
    <a class="more reveal" href="owner.html">Meet the owner</a>
  </div>
</section>

{quote_band("Quality is never an accident; it is always the result of intelligent effort.", "John Ruskin")}
{CTA_BAND}''')

PAGES["owner.html"] = ("Patrik Santiago · Jurgen Software Solutions", "Patrik Santiago, Founder and Owner of Jurgen Software Solutions.", f'''{page_hero("Meet the owner", "Patrik Santiago", "Founder &amp; Owner · Full-Stack Software Engineer")}
<section class="block">
  <div class="wrap">
    <div class="owner-top reveal">
      <img class="portrait" src="assets/patrik.jpg" alt="Patrik Santiago" width="400" height="400">
      <div style="display:grid;gap:10px">
        <p class="owner-role">Enterprise experience, small-firm attention.</p>
        <p>Patrik is a software engineer with over five years of experience at IBM, Infor and Accenture, building and supporting enterprise applications for ERP, finance, banking, insurance and reporting systems. He specializes in ETL and data pipelines, and his work spans C#/.NET and Java backends, React interfaces, SQL databases, cloud platforms and AI-assisted development. He founded Jurgen Software Solutions to bring that enterprise-grade discipline to businesses of every size.</p>
        <div class="profile-links">
          <a href="https://www.linkedin.com/in/patrik-jurgen-santiago" target="_blank" rel="noopener">LinkedIn ↗</a>
          <a href="https://github.com/gameovercheeseburger" target="_blank" rel="noopener">GitHub ↗</a>
        </div>
      </div>
    </div>

    <div class="stats reveal">
      <div class="stat"><b>5+</b><span>Years in enterprise software</span></div>
      <div class="stat"><b>3</b><span>Global firms: IBM, Infor, Accenture</span></div>
      <div class="stat"><b>9</b><span>Industry certifications</span></div>
      <div class="stat"><b>2</b><span>Degrees in software &amp; engineering</span></div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap two">
    <div class="stack reveal">
      <h3>Career</h3>
      <ol class="career">
        <li><span class="when">2025 – 2026</span><div><strong>Application Developer, IBM</strong><p>Java Spring Boot microservices and REST APIs on Red Hat OpenShift; production incident resolution with Splunk; secure coding and validation of AI-generated code.</p></div></li>
        <li><span class="when">2020 – 2023</span><div><strong>Software Engineer, Infor</strong><p>C# and Java APIs for ERP, finance and reporting; React dashboards; ETL pipelines with SSIS, PowerShell and Python, and data warehousing on AWS; CI/CD with Jenkins and Docker.</p></div></li>
        <li><span class="when">2019 – 2020</span><div><strong>Associate Software Engineer, Accenture</strong><p>Oracle Sales Cloud integrations with Java, Groovy, SOAP and REST for banking and insurance clients; ETL with Oracle Data Integrator; cut testing errors by 45%.</p></div></li>
        <li><span class="when">2018</span><div><strong>Project &amp; Automation Intern, Accenture</strong><p>Reporting and scheduling tools in C#, VBA and SQL Server; reduced manual reporting time by 40%.</p></div></li>
      </ol>
    </div>
    <div class="stack reveal" style="gap:28px">
      <div class="stack" style="gap:14px">
        <h3>Education</h3>
        <ul class="side-list">
          <li>Diploma in Software Development, Southern Alberta Institute of Technology (SAIT), 2025</li>
          <li>B.S. Computer Engineering, Adamson University, 2018</li>
        </ul>
      </div>
      <div class="stack" style="gap:14px">
        <h3>Certifications</h3>
        <ul class="side-list">
          <li>IBM Generative &amp; Agentic AI Foundation</li>
          <li>AWS Partner: Generative AI Essentials</li>
          <li>Oracle Cloud Infrastructure 2025 Certified AI Foundations Associate</li>
          <li>IBM Cloud Computing Fundamentals</li>
          <li>IBM Web Development Fundamentals</li>
          <li>IBM Enterprise Design Thinking Practitioner</li>
          <li>IBM Garage Essentials</li>
          <li>ServiceNow Micro-Certification: Flow Designer</li>
          <li>HackerRank Python &amp; Java (Basic)</li>
        </ul>
      </div>
    </div>
  </div>
</section>

{CTA_BAND}''')

PAGES["contact.html"] = ("Contact · Jurgen Software Solutions", "Request a quote or email Jurgen Software Solutions.", f'''{page_hero("Contact", "Let's talk about your project", "Tell us what you need and we will reply with a clear plan and an honest estimate. No obligation and no sales pitch.")}
<section class="block">
  <div class="wrap contact-grid">
    <div class="stack reveal">
      <div class="email-box">
        <span class="eyebrow">Email</span>
        <a id="email" href="mailto:patrik.j.santiago@gmail.com">patrik.j.santiago@gmail.com</a>
        <button type="button" id="copy-email" class="btn ghost-dark">Copy email</button>
      </div>
      <p class="muted">We reply to every request within one business day.</p>
    </div>
    <div class="form-card reveal">
      <div class="head"><span class="eyebrow">Request a quote</span><h2>Tell us about your project</h2></div>
      <div data-quote-form></div>
    </div>
  </div>
</section>
''')

for name, (title, desc, body) in PAGES.items():
    active = name
    html = head(title, desc) + header(active) + "\n<main>\n" + body + "</main>\n\n" + FOOTER()
    with open(os.path.join(SITE, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("wrote", name)
