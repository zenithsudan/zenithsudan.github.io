#!/usr/bin/env python3
"""Zenith Engineering static site generator.
Every page is written once with both languages side by side: t("English", "العربية").
Run from anywhere:  python3 _src/build.py
Output: / (English) and /ar/ (Arabic), plus sitemap.xml, robots.txt, 404.html.
"""
import os, json, urllib.parse, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://zenithsudan.com"
WA = "249912174908"
WA_DISPLAY = "+249 91 217 4908"
EMAIL = "info@zenithsudan.com"
LI = "https://www.linkedin.com/company/zenithsudan"
LANG = "en"


def t(en, ar):
    return en if LANG == "en" else ar


def url(slug, lang=None):
    lang = lang or LANG
    base = "" if lang == "en" else "/ar"
    return f"{base}/{slug}/" if slug else f"{base}/"


# ---------- components ----------
SYMBOL = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="z" viewBox="0 0 100 100">'
          '<rect x="12" y="14" width="76" height="17" fill="currentColor"/><rect x="12" y="69" width="76" height="17" fill="currentColor"/>'
          '<polygon points="88,31 88,69 12,69" fill="#F2A900"/></symbol></svg>')

WA_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.100L2 22l5-1.300A10 10 0 1 0 12 2zm0 18.200a8.200 8.200 0 0 1-4.200-1.200l-.3-.2-3 .8.8-2.900-.2-.3A8.200 8.200 0 1 1 12 20.200zm4.500-6.100c-.2-.1-1.500-.7-1.700-.8s-.4-.1-.6.100-.6.800-.8 1-.3.200-.6.100a6.700 6.700 0 0 1-3.300-2.900c-.3-.4.200-.4.700-1.300.1-.2 0-.3 0-.4l-.8-1.800c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.300 3 3 0 0 0-.9 2.200 5.200 5.200 0 0 0 1.100 2.800c.1.2 2 3.100 4.900 4.300 1.800.8 2.500.8 3.400.6.600-.1 1.700-.7 1.900-1.400s.2-1.200.2-1.300-.2-.2-.5-.3z"/></svg>')

NAV = [  # (slug, EN, AR)
    ("services", "SERVICES", "الخدمات"),
    ("about", "ABOUT", "من نحن"),
    ("team", "TEAM", "الفريق"),
    ("quality", "QUALITY", "الجودة"),
    ("capabilities", "CAPABILITIES", "القدرات"),
    ("contact", "CONTACT", "تواصل معنا"),
]


def profile_href():
    f = f"/assets/Zenith-Company-Profile-{LANG.upper()}.pdf"
    if os.path.exists(os.path.join(ROOT, f.lstrip("/"))):
        return f, " download"
    q = urllib.parse.quote(t("Please send me the Zenith company profile.", "أرجو إرسال ملف شركة زينث."))
    return f'{url("contact")}?topic={q}#brief', ""


def wa_link(text=None):
    text = text or t("Hello Zenith Engineering, I would like to discuss a project.",
                     "مرحباً زينث الهندسية، أودّ مناقشة مشروع.")
    return f"https://wa.me/{WA}?text=" + urllib.parse.quote(text)


def header(cur, other):
    items = "".join(
        f'<a href="{url(s)}"{" aria-current=page" if s == cur or (cur and cur.startswith(s + "/")) else ""}>{t(e, a)}</a>'
        for s, e, a in NAV)
    lang_a = f'<a class="lang" href="{other}" hreflang="{"ar" if LANG == "en" else "en"}" lang="{"ar" if LANG == "en" else "en"}">{t("العربية", "English")}</a>'
    return (f'<header><div class="wrap"><a class="brand" href="{url("")}" aria-label="Zenith Engineering"><img src="/assets/logo-white.svg" alt="Zenith Engineering" width="161" height="38"></a>'
            f'<input type="checkbox" id="nt" class="nt"><label for="nt" class="burger" aria-label="{t("Menu", "القائمة")}"><i></i><i></i><i></i></label>'
            f'<nav aria-label="{t("Main", "الرئيسية")}">{items}{lang_a}</nav></div></header>')


def footer():
    links = "".join(f'<a href="{url(s)}">{t(e, a).title() if LANG == "en" else a}</a>' for s, e, a in NAV)
    return (f'<footer><div class="wrap"><div class="cols">'
            f'<div><h4>ZENITH ENGINEERING</h4><p>{t("Construction, water infrastructure, solar energy and engineering consultancy across Sudan.", "مقاولات وبنية تحتية للمياه وطاقة شمسية واستشارات هندسية في كل أنحاء السودان.")}</p></div>'
            f'<div><h4>{t("EXPLORE", "استكشف")}</h4>{links}</div>'
            f'<div><h4>{t("CONTACT", "تواصل")}</h4><a href="mailto:{EMAIL}">{EMAIL}</a>'
            f'<a href="{wa_link()}" rel="noopener">{t("WhatsApp", "واتساب")}: <span dir="ltr">{WA_DISPLAY}</span></a>'
            f'<a href="{LI}" rel="noopener">LinkedIn</a><a href="{url("contact")}">{t("Kassala, Sudan", "كسلا، السودان")}</a></div>'
            f'</div><div class="copy"><span>{t("© 2026 Zenith Engineering. All rights reserved.", "© 2026 زينث الهندسية. جميع الحقوق محفوظة.")}</span>'
            f'<span>{t("Kassala, Sudan", "كسلا، السودان")}</span></div></div></footer>'
            f'<a class="wa-float" href="{wa_link()}" rel="noopener" aria-label="WhatsApp">{WA_ICON}<span>WhatsApp</span></a>')


def sec(kicker, h2, lead="", inner="", alt=False, sid=""):
    return (f'<section{" class=alt" if alt else ""}{f" id={sid}" if sid else ""}><div class="wrap">'
            f'<div class="kicker">{kicker}</div><h2>{h2}</h2>{f"<p class=lead>{lead}</p>" if lead else ""}{inner}</div></section>')


def card(h, p="", amber=False, href=None, items=None):
    cls = "card amber" if amber else "card"
    body = f"<h3>{h}</h3>" + (f"<p>{p}</p>" if p else "") + (("<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>") if items else "")
    if href:
        return f'<a class="{cls}" href="{href}">{body}<span class="more">{t("Learn more", "اعرف المزيد")}</span></a>'
    return f'<div class="{cls}">{body}</div>'


def grid(cols, cards):
    return f'<div class="grid g{cols}">{"".join(cards)}</div>'


def hero(tag, h1, p, btns="", page=False, crumbs=""):
    return (f'<div class="hero{" page-hero" if page else ""}"><div class="wrap">{crumbs}<div class="tag">{tag}</div><h1>{h1}</h1>'
            f'{f"<p>{p}</p>" if p else ""}{f"<div class=btns>{btns}</div>" if btns else ""}</div></div>')


def crumbs(*parts):
    out = [f'<a href="{url("")}">{t("Home", "الرئيسية")}</a>'] + list(parts)
    return '<div class="crumbs">' + " / ".join(out) + "</div>"


def process():
    steps = [("01", t("Survey", "المسح"), t("Site and demand", "الموقع والطلب")),
             ("02", t("Design", "التصميم"), t("Drawings and BoQ", "الرسومات وحصر الكميات")),
             ("03", t("Build", "التنفيذ"), t("Supervised works", "أعمال تحت الإشراف")),
             ("04", t("Test", "الاختبار"), t("Checks and records", "فحوص وسجلات")),
             ("05", t("Handover", "التسليم"), t("Training and records", "التدريب والسجلات"))]
    return '<div class="steps">' + "".join(f'<div class="step"><i>{n}</i><b>{a}</b><span>{b}</span></div>' for n, a, b in steps) + "</div>"


def cta(h, label=None, href=None):
    return (f'<div class="cta"><div class="wrap"><h2>{h}</h2>'
            f'<a class="btn" href="{href or url("contact")}">{label or t("START A CONVERSATION", "ابدأ المحادثة")}</a></div></div>')


# ---------- page bodies ----------
SERVICES = [  # slug, EN name, AR name, EN blurb, AR blurb
    ("services/construction", "Construction & Finishing", "المقاولات والتشطيبات",
     "Buildings, fit-outs and rehabilitation delivered by our own civil team.",
     "مبانٍ وأعمال تجهيز وتأهيل ينفذها فريقنا المدني."),
    ("services/water", "Water & Infrastructure", "المياه والبنية التحتية",
     "Water stations, pipelines, tanks and pumping systems, from source to tap.",
     "محطات مياه وخطوط أنابيب وخزانات ومنظومات ضخ، من المصدر إلى الصنبور."),
    ("services/solar", "Solar Energy", "الطاقة الشمسية",
     "Systems sized to the real load for homes, offices, stations and farms.",
     "منظومات مصممة بحسب الحمل الفعلي للمنازل والمكاتب والمحطات والمزارع."),
    ("services/consultancy", "Engineering Consultancy", "الاستشارات الهندسية",
     "Drawings, designs, quantity take-offs and building assessments.",
     "مخططات وتصاميم وحصر كميات وتقييم مباني."),
    ("services/design", "Interior Design & Landscape", "التصميم الداخلي والحدائق",
     "Interiors and gardens designed to be used, and built to last.",
     "تصميم داخلي وحدائق صُممت للاستخدام وبُنيت لتدوم."),
]


def svc_cards():
    return grid(3, [card(t(e, a), t(be, ba), amber=True, href=url(s)) for s, e, a, be, ba in SERVICES])


def page_home():
    wa_btn = f'<a class="btn ghost" href="{wa_link()}" rel="noopener">{t("WHATSAPP US", "تواصل عبر واتساب")}</a>'
    ph, dl = profile_href()
    prof = f'<a class="btn" href="{ph}"{dl}>{t("DOWNLOAD COMPANY PROFILE", "حمّل ملف الشركة") if dl else t("REQUEST OUR COMPANY PROFILE", "اطلب ملف الشركة")}</a>'
    values = grid(4, [
        card(t("Consistent quality", "جودة ثابتة"), t("The same standard on every site, every time.", "المعيار نفسه في كل موقع وفي كل مرة.")),
        card(t("Reliable commitment", "التزام موثوق"), t("Agreed scope, agreed schedule, delivered.", "نطاق متفق عليه، وجدول متفق عليه، وتسليم في موعده.")),
        card(t("Specialized teams", "فرق متخصصة"), t("Engineers and technicians matched to the task.", "مهندسون وفنيون مختارون لطبيعة العمل.")),
        card(t("Modern practice", "ممارسة حديثة"), t("BIM and digital design, with quality never traded for speed.", "نمذجة BIM وتصميم رقمي، دون أن تكون السرعة على حساب الجودة.")),
    ])
    return (hero(t("CONSTRUCTION · WATER · SOLAR · CONSULTANCY", "المقاولات · المياه · الطاقة الشمسية · الاستشارات"),
                 t("Engineering that delivers across Sudan", "هندسة تُنجز، في كل أنحاء السودان"),
                 t("Construction, water infrastructure, solar energy and engineering consultancy, delivered by one accountable team.",
                   "مقاولات وبنية تحتية للمياه وطاقة شمسية واستشارات هندسية، يقدّمها فريق واحد مسؤول عن النتيجة."),
                 prof + wa_btn)
            + sec(t("WHAT WE DO", "ما نقدّمه"), t("One team for the full scope", "فريق واحد للنطاق كاملاً"),
                  t("Clients should not have to coordinate separate contractors for building, water, energy and design. Zenith covers all four.",
                    "لا ينبغي أن يضطر العميل إلى التنسيق بين مقاولين منفصلين للبناء والمياه والطاقة والتصميم. تغطي زينث ذلك كله."),
                  svc_cards())
            + sec(t("WHY ZENITH", "لماذا زينث"), t("The same standard on every site", "المعيار نفسه في كل موقع"), "", values, alt=True)
            + sec(t("HOW WE WORK", "كيف نعمل"), t("Five steps, every project", "خمس خطوات، لكل مشروع"),
                  t("Every project follows the same sequence, with quality checks at each step.", "يمر كل مشروع بالتسلسل نفسه، مع فحوص جودة عند كل خطوة."), process())
            + cta(t("Planning a project? Tell us the scope and we will respond with a clear plan.",
                    "لديك مشروع؟ أخبرنا بنطاق العمل وسنردّ عليك بخطة واضحة.")))


def page_about():
    prose = ('<div class="prose">' + "".join(f"<p>{x}</p>" for x in [
        t("Zenith Engineering was founded on a simple observation from inside humanitarian and development projects: the quality and timing of delivery depend on the strength of the technical team on the ground. Clients also lose time coordinating separate contractors for building, water, energy and design.",
          "تأسست زينث الهندسية انطلاقاً من ملاحظة بسيطة من داخل المشاريع الإنسانية والتنموية: جودة التنفيذ وسرعته تعتمدان على قوة الفريق الفني في الميدان. كما يخسر العملاء وقتاً في التنسيق بين مقاولين منفصلين للبناء والمياه والطاقة والتصميم."),
        t("We built Zenith to answer both problems: one trusted Sudanese engineering team, covering the full scope, accountable for the result.",
          "أنشأنا زينث لمعالجة الأمرين معاً: فريق هندسي سوداني موثوق واحد، يغطي النطاق كاملاً ويتحمل مسؤولية النتيجة."),
        t("Sudan's recovery needs reliable infrastructure delivered at scale. We aim to contribute to it with disciplined engineering, modern tools and respect for every client's standards.",
          "يحتاج التعافي في السودان إلى بنية تحتية موثوقة تُنفَّذ على نطاق واسع. ونسعى إلى المساهمة فيه بهندسة منضبطة وأدوات حديثة واحترام لمعايير كل عميل."),
    ]) + "</div>")
    facts = grid(3, [
        card(t("Base", "المقر"), t("Kassala, Sudan", "كسلا، السودان")),
        card(t("Coverage", "التغطية"), t("Projects across Sudan", "مشاريع في كل أنحاء السودان")),
        card(t("Clients", "العملاء"), t("UN agencies, international and local NGOs, and private clients", "وكالات الأمم المتحدة والمنظمات الدولية والمحلية والعملاء من القطاع الخاص")),
    ])
    return (hero(t("ABOUT US", "من نحن"), t("Why Zenith exists", "لماذا وُجدت زينث"), "", page=True, crumbs=crumbs(t("About", "من نحن")))
            + sec(t("OUR STORY", "قصتنا"), t("One accountable engineering team", "فريق هندسي واحد مسؤول"), "", prose + facts)
            + sec(t("HOW WE WORK", "كيف نعمل"), t("Survey, design, build, test, handover", "مسح، تصميم، تنفيذ، اختبار، تسليم"),
                  t("Every project follows the same five steps, with quality checks at each one.", "يمر كل مشروع بالخطوات الخمس نفسها، مع فحوص جودة عند كل خطوة."), process(), alt=True)
            + cta(t("Let us talk about your project.", "لنتحدث عن مشروعك.")))


def page_services():
    return (hero(t("SERVICES", "الخدمات"), t("Five services, one standard", "خمس خدمات، ومعيار واحد"),
                 t("Each service has its own specialists. All share the same management and quality controls.", "لكل خدمة متخصصوها، وتجمعها إدارة واحدة وضوابط جودة واحدة."),
                 page=True, crumbs=crumbs(t("Services", "الخدمات")))
            + sec(t("OUR SERVICES", "خدماتنا"), t("Choose a service", "اختر الخدمة"), "", svc_cards())
            + cta(t("Not sure which service you need? Describe the project.", "لست متأكداً أي خدمة تحتاج؟ صِف لنا المشروع.")))


def service_page(slug, tag, h1, intro, items_title, items, extra="", note=None):
    name = [(e, a) for s, e, a, _, _ in SERVICES if s == slug][0]
    cards = grid(2, [card(t(*i[0]), t(*i[1])) for i in items])
    inner = cards + (f'<div class="note">{note}</div>' if note else "")
    body = (hero(tag, h1, intro, page=True, crumbs=crumbs(f'<a href="{url("services")}">{t("Services", "الخدمات")}</a>', t(*name)))
            + sec(items_title[0], items_title[1], "", inner)
            + extra
            + sec(t("HOW WE WORK", "كيف نعمل"), t("Five steps, every project", "خمس خطوات، لكل مشروع"), "", process(), alt=True)
            + cta(t("Have a project in mind? Send us the scope.", "لديك مشروع؟ أرسل لنا نطاق العمل.")))
    return body


def page_construction():
    return service_page("services/construction", t("CONSTRUCTION & FINISHING", "المقاولات والتشطيبات"),
        t("Buildings built right, finished properly", "مبانٍ تُبنى بإتقان وتُسلَّم مكتملة"),
        t("Our own civil team builds and finishes the project, from foundations to handover.", "يبني فريقنا المدني المشروع ويُنهيه، من الأساسات حتى التسليم."),
        (t("WHAT WE BUILD", "ما نبنيه"), t("Buildings and fit-outs", "المباني والتجهيزات")),
        [(("Health, education and office buildings", "مبانٍ صحية وتعليمية ومكتبية"), ("New construction to agreed drawings, specifications and bills of quantities.", "إنشاء جديد وفق مخططات ومواصفات وجداول كميات متفق عليها.")),
         (("Finishing works", "أعمال التشطيبات"), ("Plastering, flooring, painting, joinery and fittings, completed to a consistent standard.", "لياسة وأرضيات ودهان ونجارة وتجهيزات، بمعيار ثابت.")),
         (("Office fit-out", "تجهيز المكاتب"), ("Partitions, services and finishes for offices and facilities, planned to minimise downtime.", "قواطع وخدمات وتشطيبات للمكاتب والمرافق، بتخطيط يقلل التوقف عن العمل.")),
         (("Rehabilitation", "إعادة التأهيل"), ("Assessment and repair of existing and damaged buildings, scoped before money is spent.", "تقييم المباني القائمة والمتضررة وإصلاحها، بعد تحديد النطاق قبل إنفاق المال."))])


def page_water():
    return service_page("services/water", t("WATER & INFRASTRUCTURE", "المياه والبنية التحتية"),
        t("From source to tap, built to last", "من المصدر إلى الصنبور، منفذة لتدوم"),
        t("Complete water systems for communities, health facilities, schools and agricultural sites.", "أنظمة مياه متكاملة للمجتمعات والمرافق الصحية والمدارس والمواقع الزراعية."),
        (t("WHAT WE DELIVER", "ما ننفذه"), t("Complete water systems", "أنظمة مياه متكاملة")),
        [(("Pump supply and installation", "توريد المضخات وتركيبها"), ("Selection, supply and installation of submersible and surface pumps, with testing and operator handover.", "اختيار المضخات الغاطسة والسطحية وتوريدها وتركيبها، مع الاختبار وتسليمها للمشغّلين.")),
         (("Tank fabrication and installation", "تصنيع الخزانات وتركيبها"), ("Steel and elevated tanks fabricated and erected, with stands, fittings and leak testing.", "تصنيع الخزانات الحديدية والعلوية ونصبها، مع القواعد والتجهيزات واختبار التسرب.")),
         (("Pipeline works", "أعمال خطوط الأنابيب"), ("Trenching, laying, jointing and pressure testing of distribution and transmission lines.", "الحفر والمد والوصل واختبار الضغط لخطوط التوزيع والنقل.")),
         (("Water stations", "محطات المياه"), ("New construction and rehabilitation of water stations, from civil works to commissioning.", "إنشاء محطات المياه الجديدة وإعادة تأهيلها، من الأعمال المدنية حتى التشغيل."))],
        note=t("<b>Borehole drilling.</b> Carried out by qualified drilling contractors under Zenith's management. We set the technical requirements, supervise the work and verify test results before handover.",
               "<b>حفر الآبار.</b> ينفذها مقاولو حفر مؤهلون تحت إدارة زينث. نحدد المتطلبات الفنية ونشرف على العمل ونتحقق من نتائج الاختبار قبل التسليم."))


def page_solar():
    return service_page("services/solar", t("SOLAR ENERGY", "الطاقة الشمسية"),
        t("Reliable power, sized to the real load", "طاقة موثوقة، بحسب الحمل الفعلي"),
        t("We design, supply and install solar systems so facilities keep running through outages and fuel shortages.", "نصمم أنظمة الطاقة الشمسية ونوردها ونركبها لتواصل المنشآت عملها أثناء انقطاع الكهرباء ونقص الوقود."),
        (t("WHAT WE INSTALL", "ما نركّبه"), t("Solar systems for every setting", "أنظمة شمسية لكل بيئة")),
        [(("Homes and offices", "المنازل والمكاتب"), ("Systems with battery storage, sized to the loads that matter most.", "أنظمة مع تخزين بالبطاريات، بحجم يخدم الأحمال الأهم.")),
         (("Solar water pumping", "الضخ بالطاقة الشمسية"), ("Pumping for water stations without dependence on fuel supply.", "ضخ لمحطات المياه دون الاعتماد على إمداد الوقود.")),
         (("Irrigation and farms", "الري والمزارع"), ("Power for irrigation and farm facilities.", "طاقة للري والمنشآت الزراعية.")),
         (("Design, supply, installation", "تصميم وتوريد وتركيب"), ("One team from load assessment to commissioning, using our own technicians.", "فريق واحد من تقدير الأحمال حتى التشغيل، بفنيين من شركتنا."))])


def page_consultancy():
    return service_page("services/consultancy", t("ENGINEERING CONSULTANCY", "الاستشارات الهندسية"),
        t("Clear drawings, firm numbers", "مخططات واضحة، وأرقام محكمة"),
        t("We prepare the drawings, designs and cost estimates that tender, budget and build decisions depend on.", "نعدّ المخططات والتصاميم وتقديرات التكلفة التي تعتمد عليها قرارات العطاءات والميزانيات والتنفيذ."),
        (t("WHAT WE PREPARE", "ما نعدّه"), t("Design and estimation", "التصميم والتقدير")),
        [(("Architectural and civil drawings", "مخططات معمارية ومدنية"), ("Drawings produced in AutoCAD, Civil 3D and BIM (Revit).", "مخططات منتجة ببرامج AutoCAD وCivil 3D وBIM (Revit).")),
         (("Designs", "التصاميم"), ("Structural, civil and water-system designs, including hydraulic modelling in EPANET.", "تصاميم إنشائية ومدنية وتصاميم أنظمة المياه، بما فيها النمذجة الهيدروليكية في EPANET.")),
         (("Quantity estimation and BoQs", "حصر الكميات وجداول الكميات (BoQ)"), ("Bills of quantities and cost estimates ready for tendering.", "جداول كميات وتقديرات تكلفة جاهزة للطرح.")),
         (("Assessment of damaged buildings", "تقييم المباني المتضررة"), ("Condition assessment before money is spent on repairs.", "تقييم الحالة قبل إنفاق المال على الإصلاح."))])


def page_design():
    return service_page("services/design", t("INTERIOR DESIGN & LANDSCAPE", "التصميم الداخلي والحدائق"),
        t("Spaces and gardens designed for use", "مساحات وحدائق صُممت للاستخدام"),
        t("We design interiors and outdoor spaces, then build them with the same team and the same standard.", "نصمم المساحات الداخلية والخارجية ثم ننفذها بالفريق نفسه وبالمعيار نفسه."),
        (t("WHAT WE DESIGN", "ما نصمّمه"), t("Interiors and outdoor spaces", "مساحات داخلية وخارجية")),
        [(("Interior design", "التصميم الداخلي"), ("Layouts, finishes and fittings for offices, homes and commercial spaces.", "توزيعات وتشطيبات وتجهيزات للمكاتب والمنازل والمساحات التجارية.")),
         (("Landscape and gardens", "تنسيق الحدائق"), ("Gardens and outdoor areas planned for the local climate and low maintenance.", "حدائق ومساحات خارجية مخططة بحسب المناخ المحلي وبصيانة منخفضة.")),
         (("Design to build", "من التصميم إلى التنفيذ"), ("The same team that designs the space builds it, so the result matches the drawings.", "الفريق الذي يصمم المساحة هو من ينفذها، فتطابق النتيجة المخططات.")),
         (("Visualisation", "التصور ثلاثي الأبعاد"), ("3D views before work starts, so decisions are made on paper rather than on site.", "تصورات ثلاثية الأبعاد قبل البدء، لتُتخذ القرارات على الورق لا في الموقع."))])


def leader(img, name_en, name_ar, role_en, role_ar, alt_en, alt_ar, bio_en, bio_ar):
    return (f'<div class="lead-card"><img src="/assets/{img}" alt="{t(alt_en, alt_ar)}" width="130" height="130" loading="lazy">'
            f'<div><h3>{t(name_en, name_ar)}</h3><div class="role">{t(role_en, role_ar)}</div><p>{t(bio_en, bio_ar)}</p></div></div>')


def page_team():
    leaders = '<div class="lead-grid">' + leader(
        "albraa.jpg", "Albraa Ibrahim Khamis Mohamed", "البراء إبراهيم خميس محمد", "FOUNDER &amp; GENERAL MANAGER", "المؤسس والمدير العام",
        "Albraa Ibrahim Khamis Mohamed, Founder and General Manager of Zenith Engineering", "البراء إبراهيم خميس محمد، المؤسس والمدير العام لزينث الهندسية",
        "Civil engineer experienced in managing construction and infrastructure projects in complex field conditions, from planning and design through to handover. Albraa founded Zenith to give clients one accountable company and one consistent standard of delivery, instead of coordinating separate contractors for each need. He leads Zenith's strategy, its administrative and technical standards, and its relationships with clients, across contracting, solar energy and engineering consultancy, with quality and integrity at the centre of how the company works.",
        "مهندس مدني ذو خبرة في إدارة مشاريع الإنشاءات والبنية التحتية في ظروف ميدانية معقدة، من التخطيط والتصميم حتى التسليم. أسس البراء زينث ليمنح العملاء شركة واحدة مسؤولة ومعيارًا واحدًا في التنفيذ، بدلًا من التنسيق بين مقاولين منفصلين لكل احتياج. ويقود استراتيجية زينث ومعاييرها الإدارية والفنية وعلاقاتها مع العملاء، في المقاولات والطاقة الشمسية والاستشارات الهندسية، وتقوم طريقة عمل الشركة على الجودة والنزاهة.") + leader(
        "mohamed.jpg", "Mohamed Mamoun Mohamed Khider", "محمد مأمون محمد خضر", "EXECUTIVE OPERATIONS MANAGER", "المدير التنفيذي للعمليات",
        "Mohamed Mamoun Mohamed Khider, Executive Operations Manager of Zenith Engineering", "محمد مأمون محمد خضر، المدير التنفيذي للعمليات لزينث الهندسية",
        "Civil engineer (building and construction) with 10+ years of experience leading work teams, supervising sites and managing material supply chains. He builds execution systems that protect efficiency and quality, and previously managed a company importing and delivering pumps and solar energy equipment. Mohamed runs Zenith's operations.",
        "مهندس مدني (بناء وتشييد) بخبرة تزيد على 10 سنوات في قيادة فرق العمل والإشراف الميداني وإدارة سلاسل توريد المواد. يضع أنظمة تنفيذ تضمن الكفاءة والجودة، وسبق له إدارة شركة تعمل في استيراد وتوصيل المضخات ومعدات الطاقة الشمسية. يتولى محمد إدارة عمليات زينث.") + "</div>"
    core = grid(3, [
        card(t("Mossab Hassan Ali Mohammed", "مصعب حسن علي محمد"), t("Civil engineer. Construction, finishing and supply chain, with NGO site experience.", "مهندس مدني. الإنشاء والتشطيب وسلاسل التوريد، بخبرة في مواقع المنظمات.")),
        card(t("Asim Seddig Mohamed Alhassan", "عاصم صديق محمد الحسن"), t("Mechanical engineer. Solar systems, plumbing and electrical works.", "مهندس ميكانيكي. الأنظمة الشمسية وأعمال السباكة والكهرباء.")),
        card(t("Yasser Abdeaziz Alkay", "ياسر عبد العزيز الكي"), t("Geological engineer. Boreholes, pumps, tanks and water stations.", "مهندس جيولوجي. الآبار والمضخات والخزانات ومحطات المياه.")),
    ])
    tech = f'<p class="lead">{t("Skilled technicians with more than ten years in the trade join each project, with specialist subcontractors brought in under Zenith management when the work calls for it.", "ينضم إلى كل مشروع فنيون مهرة بخبرة تتجاوز عشر سنوات في المهنة، مع مقاولين متخصصين من الباطن تحت إدارة زينث عندما يتطلب العمل ذلك.")}</p>'
    return (hero(t("TEAM", "الفريق"), t("Led by engineers who have built it before", "بقيادة مهندسين سبق لهم التنفيذ"), "", page=True, crumbs=crumbs(t("Team", "الفريق")))
            + sec(t("LEADERSHIP", "القيادة"), t("The people accountable for your project", "المسؤولون عن مشروعك"), "", leaders)
            + sec(t("TECHNICAL CORE", "النواة الفنية"), t("Specialist engineers in every discipline", "مهندسون متخصصون في كل تخصص"), "", core + tech, alt=True)
            + cta(t("Meet the team on your next project.", "تعرّف على الفريق في مشروعك القادم.")))


def page_quality():
    blocks = grid(4, [
        card(t("Quality at every stage", "الجودة في كل مرحلة"), t("Materials checked on delivery, works inspected before they are covered, tests recorded before handover.", "فحص المواد عند التسليم، ومعاينة الأعمال قبل تغطيتها، وتوثيق الاختبارات قبل التسليم.")),
        card(t("Health and safety", "الصحة والسلامة"), t("Hazards identified before work starts, with protective equipment, safe methods and incident reporting.", "تحديد المخاطر قبل بدء العمل، مع معدات الوقاية وطرق العمل الآمنة والإبلاغ عن الحوادث.")),
        card(t("Integrity", "النزاهة"), t("Honest bidding, declared conflicts of interest, and no tolerance for bribery or improper payments.", "تقديم عطاءات نزيهة، والإفصاح عن تضارب المصالح، وعدم التسامح مع الرشوة أو المدفوعات غير المشروعة.")),
        card(t("Safeguarding", "الحماية"), t("A code of conduct for all staff and subcontractors, a named focal point and clear steps for raising concerns.", "مدونة سلوك لجميع الموظفين والمقاولين من الباطن، ونقطة اتصال معروفة، وخطوات واضحة لرفع الشكاوى.")),
    ])
    note = (f'<div class="note">{t("Our water and construction work is planned in line with Sphere standards and the Core Humanitarian Standard, and our safeguarding approach follows IASC principles. We work with community participation, coordinate with partners and design for operation and maintenance after handover.", "نخطط أعمال المياه والإنشاءات وفق معايير سفير والمعيار الإنساني الأساسي (CHS)، ويتبع نهجنا في الحماية مبادئ لجنة الوكالات الدائمة (IASC). نعمل بمشاركة المجتمع، ونتنسق مع الشركاء، ونصمم مع مراعاة التشغيل والصيانة بعد التسليم.")}</div>')
    return (hero(t("METHODOLOGY AND QUALITY", "المنهجية والجودة"), t("The same standard on every site", "المعيار نفسه في كل موقع"), "", page=True, crumbs=crumbs(t("Quality", "الجودة")))
            + sec(t("OUR COMMITMENTS", "التزاماتنا"), t("How we protect the result", "كيف نحمي النتيجة"), "", blocks + note)
            + sec(t("HOW WE WORK", "كيف نعمل"), t("Five steps, every project", "خمس خطوات، لكل مشروع"), "", process(), alt=True)
            + cta(t("Want to see how this applies to your project?", "تريد أن ترى كيف ينطبق ذلك على مشروعك؟")))


def page_capabilities():
    rows = [("AutoCAD", t("Architectural and civil drawings", "رسومات معمارية ومدنية")),
            ("Civil 3D", t("Site, roads and earthworks design", "تصميم المواقع والطرق والأعمال الترابية")),
            ("Revit (BIM)", t("3D building models and coordinated drawings", "نماذج ثلاثية الأبعاد للمباني ومخططات منسقة")),
            ("EPANET", t("Hydraulic modelling of water networks", "النمذجة الهيدروليكية لشبكات المياه")),
            ("GIS", t("Mapping, site selection and spatial analysis", "الخرائط واختيار المواقع والتحليل المكاني"))]
    tbl = (f'<table class="tbl"><thead><tr><th>{t("TOOL", "الأداة")}</th><th>{t("USED FOR", "الاستخدام")}</th></tr></thead><tbody>'
           + "".join(f'<tr><td><b dir="ltr">{a}</b></td><td>{b}</td></tr>' for a, b in rows) + "</tbody></table>")
    equip = grid(3, [
        card(t("Design workstations", "محطات التصميم"), t("High-specification computers for BIM and engineering software.", "حواسيب عالية المواصفات لبرمجيات BIM والبرمجيات الهندسية.")),
        card(t("Site equipment", "معدات الموقع"), t("Welding machines, rebar cutting and concreting equipment.", "ماكينات لحام وقطع حديد التسليح ومعدات صب الخرسانة.")),
        card(t("Transport", "النقل"), t("Our own vehicle for hauling materials, with other equipment rented per project.", "مركبتنا الخاصة لنقل المواد، مع استئجار المعدات الأخرى بحسب المشروع.")),
    ])
    return (hero(t("CAPABILITIES", "القدرات"), t("Modern tools, equipped teams", "أدوات حديثة، وفرق مجهزة"), "", page=True, crumbs=crumbs(t("Capabilities", "القدرات")))
            + sec(t("SOFTWARE", "البرمجيات"), t("Designed digitally before it is built", "تُصمَّم رقمياً قبل أن تُبنى"),
                  t("Digital design reduces errors before work reaches the site.", "يقلل التصميم الرقمي الأخطاء قبل وصول العمل إلى الموقع."), tbl)
            + sec(t("EQUIPMENT", "المعدات"), t("What we bring to site", "ما نحضره إلى الموقع"), "", equip, alt=True)
            + cta(t("Need to know whether we can handle your scope?", "تريد أن تعرف إن كنا نستطيع تنفيذ نطاق عملك؟")))


def page_contact():
    ways = (f'<div class="ways">'
            f'<a class="way" href="{wa_link()}" rel="noopener"><div><b>WHATSAPP</b><span dir="ltr">{WA_DISPLAY}</span><small>{t("Mohamed Mamoun, Executive Operations Manager", "محمد مأمون، المدير التنفيذي للعمليات")}</small></div></a>'
            f'<a class="way" href="mailto:{EMAIL}"><div><b>{t("EMAIL", "البريد")}</b><span dir="ltr">{EMAIL}</span></div></a>'
            f'<a class="way" href="{LI}" rel="noopener"><div><b>LINKEDIN</b><span dir="ltr">linkedin.com/company/zenithsudan</span></div></a>'
            f'<div class="way"><div><b>{t("BASE", "المقر")}</b><span>{t("Kassala, Sudan", "كسلا، السودان")}</span><small>{t("Projects across Sudan", "مشاريع في كل أنحاء السودان")}</small></div></div>'
            f'</div>')
    intro = t("Hello Zenith Engineering, I would like to discuss a project.", "مرحباً زينث الهندسية، أودّ مناقشة مشروع.")
    form = (f'<form class="brief" id="brief" onsubmit="return false" data-wa="{WA}" data-mail="{EMAIL}" data-intro="{intro}" data-subject="{t("Project enquiry", "استفسار عن مشروع")}">'
            f'<h3 style="color:var(--navy)">{t("Send a project brief", "أرسل موجزاً عن مشروعك")}</h3>'
            f'<label for="f1">{t("Your name", "الاسم")}</label><input id="f1" name="name" data-label="{t("Name", "الاسم")}" required autocomplete="name">'
            f'<label for="f2">{t("Organization (optional)", "الجهة (اختياري)")}</label><input id="f2" name="org" data-label="{t("Organization", "الجهة")}" autocomplete="organization">'
            f'<label for="f3">{t("Project location", "موقع المشروع")}</label><input id="f3" name="loc" data-label="{t("Location", "الموقع")}">'
            f'<label for="f4">{t("Service", "الخدمة")}</label><select id="f4" name="svc" data-label="{t("Service", "الخدمة")}"><option value=""></option>'
            + "".join(f'<option>{t(e, a)}</option>' for s, e, a, _, _ in SERVICES) + '</select>'
            f'<label for="f5">{t("Scope and timeline", "النطاق والجدول الزمني")}</label><textarea id="f5" name="message" data-label="{t("Details", "التفاصيل")}"></textarea>'
            f'<div class="btns"><button type="button" class="btn" data-send="wa">{t("SEND VIA WHATSAPP", "أرسل عبر واتساب")}</button>'
            f'<button type="button" class="btn alt2" data-send="mail">{t("SEND BY EMAIL", "أرسل بالبريد")}</button></div>'
            f'<p class="hint">{t("Your message opens in WhatsApp or your email app for you to review and send. Nothing is sent until you press send there.", "تُفتح رسالتك في واتساب أو تطبيق البريد لتراجعها وترسلها. لا يُرسل شيء قبل أن تضغط إرسال هناك.")}</p></form>')
    inner = f'<div class="contact-grid" id="brief-wrap">{ways}{form}</div><script src="/assets/site.js" defer></script>'
    return (hero(t("CONTACT", "تواصل معنا"), t("Tell us about your project", "حدثنا عن مشروعك"),
                 t("Send us your scope, location and timeline. We will reply with questions or a proposal, and share our company profile on request.",
                   "أرسل لنا نطاق العمل والموقع والجدول الزمني. سنرد عليك بأسئلة أو بعرض، ونشارك ملف الشركة عند الطلب."), page=True, crumbs=crumbs(t("Contact", "تواصل معنا")))
            + sec(t("GET IN TOUCH", "تواصل معنا"), t("Choose the way that suits you", "اختر الطريقة المناسبة لك"), "", inner, sid="contact-us"))


PAGES = [  # slug, title EN, title AR, desc EN, desc AR, body fn
    ("", "Zenith Engineering — Construction, Water, Solar & Engineering Consultancy in Sudan", "زينث الهندسية — مقاولات ومياه وطاقة شمسية واستشارات هندسية في السودان",
     "Zenith Engineering is a Sudanese engineering company in Kassala delivering construction, water infrastructure, solar energy and engineering consultancy across Sudan.",
     "زينث الهندسية شركة هندسية سودانية في كسلا تنفذ المقاولات والبنية التحتية للمياه والطاقة الشمسية والاستشارات الهندسية في كل أنحاء السودان.", page_home),
    ("about", "About Zenith Engineering — Why we exist", "من نحن — زينث الهندسية",
     "Zenith was founded to give clients one accountable engineering team for building, water, energy and design in Sudan.",
     "تأسست زينث لتمنح العملاء فريقاً هندسياً واحداً مسؤولاً عن البناء والمياه والطاقة والتصميم في السودان.", page_about),
    ("services", "Services — Zenith Engineering", "الخدمات — زينث الهندسية",
     "Construction and finishing, water infrastructure, solar energy, engineering consultancy, and interior design and landscape in Sudan.",
     "المقاولات والتشطيبات، والبنية التحتية للمياه، والطاقة الشمسية، والاستشارات الهندسية، والتصميم الداخلي والحدائق في السودان.", page_services),
    ("services/construction", "Construction & Finishing in Sudan — Zenith Engineering", "المقاولات والتشطيبات في السودان — زينث الهندسية",
     "Buildings, finishing, office fit-outs and rehabilitation delivered by Zenith's own civil team.", "مبانٍ وتشطيبات وتجهيز مكاتب وإعادة تأهيل ينفذها فريق زينث المدني.", page_construction),
    ("services/water", "Water & Infrastructure in Sudan — Zenith Engineering", "المياه والبنية التحتية في السودان — زينث الهندسية",
     "Water stations, pipelines, tanks, pump supply and installation, with drilling managed through specialist contractors.", "محطات مياه وخطوط أنابيب وخزانات وتوريد المضخات وتركيبها، مع إدارة الحفر عبر مقاولين متخصصين.", page_water),
    ("services/solar", "Solar Energy in Sudan — Zenith Engineering", "الطاقة الشمسية في السودان — زينث الهندسية",
     "Solar systems for homes, offices, water pumping, irrigation and farms, designed to the real load.", "أنظمة شمسية للمنازل والمكاتب وضخ المياه والري والمزارع، مصممة بحسب الحمل الفعلي.", page_solar),
    ("services/consultancy", "Engineering Consultancy in Sudan — Zenith Engineering", "الاستشارات الهندسية في السودان — زينث الهندسية",
     "Drawings, designs, BoQs and building assessments using AutoCAD, Civil 3D, Revit (BIM), EPANET and GIS.", "مخططات وتصاميم وجداول كميات وتقييم مباني ببرامج AutoCAD وCivil 3D وRevit وEPANET وGIS.", page_consultancy),
    ("services/design", "Interior Design & Landscape in Sudan — Zenith Engineering", "التصميم الداخلي والحدائق في السودان — زينث الهندسية",
     "Interior design and landscape for offices, homes and commercial spaces, built by the team that designs them.", "تصميم داخلي وتنسيق حدائق للمكاتب والمنازل والمساحات التجارية، ينفذه الفريق الذي يصممها.", page_design),
    ("team", "Team — Zenith Engineering", "الفريق — زينث الهندسية",
     "Meet the founder, the operations manager and the specialist engineers behind Zenith Engineering in Kassala, Sudan.", "تعرّف على المؤسس والمدير التنفيذي للعمليات والمهندسين المتخصصين في زينث الهندسية في كسلا، السودان.", page_team),
    ("quality", "Methodology & Quality — Zenith Engineering", "المنهجية والجودة — زينث الهندسية",
     "Quality, health and safety, integrity and safeguarding commitments on every Zenith project.", "التزامات الجودة والصحة والسلامة والنزاهة والحماية في كل مشروع لزينث.", page_quality),
    ("capabilities", "Capabilities — Zenith Engineering", "القدرات — زينث الهندسية",
     "Engineering software and site equipment behind Zenith's delivery.", "البرمجيات الهندسية ومعدات الموقع التي يقوم عليها تنفيذ زينث.", page_capabilities),
    ("contact", "Contact Zenith Engineering — Kassala, Sudan", "تواصل مع زينث الهندسية — كسلا، السودان",
     "Contact Zenith Engineering by WhatsApp, email or LinkedIn, or send a project brief.", "تواصل مع زينث الهندسية عبر واتساب أو البريد أو LinkedIn، أو أرسل موجزاً عن مشروعك.", page_contact),
]


def jsonld():
    return json.dumps({
        "@context": "https://schema.org", "@type": "Organization", "name": "Zenith Engineering",
        "alternateName": "زينث الهندسية", "url": SITE, "logo": SITE + "/assets/logo.png", "email": EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": "Kassala", "addressCountry": "SD"},
        "areaServed": "SD", "sameAs": [LI],
        "contactPoint": {"@type": "ContactPoint", "telephone": "+" + WA, "contactType": "sales", "availableLanguage": ["en", "ar"]}},
        ensure_ascii=False)


def render(slug, ti_en, ti_ar, de_en, de_ar, fn):
    global LANG
    en_url, ar_url = SITE + url(slug, "en"), SITE + url(slug, "ar")
    out = {}
    for lang in ("en", "ar"):
        LANG = lang
        title, desc = (ti_en, de_en) if lang == "en" else (ti_ar, de_ar)
        other = url(slug, "ar" if lang == "en" else "en")
        canon = en_url if lang == "en" else ar_url
        body = fn()
        out[lang] = (
            f'<!DOCTYPE html>\n<html lang="{lang}" dir="{"ltr" if lang == "en" else "rtl"}">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>{title}</title>\n<meta name="description" content="{desc}">\n'
            f'<meta name="theme-color" content="#0F2A43">\n<link rel="canonical" href="{canon}">\n'
            f'<link rel="alternate" hreflang="en" href="{en_url}">\n<link rel="alternate" hreflang="ar" href="{ar_url}">\n<link rel="alternate" hreflang="x-default" href="{en_url}">\n'
            f'<link rel="icon" type="image/svg+xml" href="/favicon.svg">\n<link rel="apple-touch-icon" href="/assets/logo.png">\n'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Zenith Engineering"><meta property="og:title" content="{title}">'
            f'<meta property="og:description" content="{desc}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}/assets/og.png">'
            f'<meta property="og:locale" content="{"en_US" if lang == "en" else "ar_AR"}"><meta name="twitter:card" content="summary_large_image">\n'
            f'<link rel="stylesheet" href="/assets/style.css">\n<script type="application/ld+json">{jsonld()}</script>\n</head>\n<body>\n'
            f'<a class="skip" href="#main">{t("Skip to content", "انتقل إلى المحتوى")}</a>\n{SYMBOL}\n{header(slug, other)}\n<main id="main">{body}</main>\n{footer()}\n</body>\n</html>\n')
    return out


def write(path, content):
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    for d in ("ar", "about", "services", "team", "quality", "capabilities", "contact"):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)
    for fn in ("index.html", "404.html", "sitemap.xml", "robots.txt"):
        p = os.path.join(ROOT, fn)
        if os.path.exists(p):
            os.remove(p)
    urls = []
    for slug, te, ta, de, da, fn in PAGES:
        pages = render(slug, te, ta, de, da, fn)
        write(url(slug, "en") + "index.html", pages["en"])
        write(url(slug, "ar") + "index.html", pages["ar"])
        urls.append(slug)
    # 404
    global LANG
    LANG = "en"
    body = (hero("404", "Page not found", "The page you are looking for does not exist or has moved.", f'<a class="btn" href="/">GO TO HOME</a><a class="btn ghost" href="/ar/">الصفحة الرئيسية</a>'))
    write("404.html", f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found — Zenith Engineering</title><meta name="robots" content="noindex"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/assets/style.css"></head><body>{SYMBOL}{header("", "/ar/")}<main id="main">{body}</main>{footer()}</body></html>')
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for slug in urls:
        for lang in ("en", "ar"):
            sm.append(f'<url><loc>{SITE}{url(slug, lang)}</loc>'
                      f'<xhtml:link rel="alternate" hreflang="en" href="{SITE}{url(slug, "en")}"/><xhtml:link rel="alternate" hreflang="ar" href="{SITE}{url(slug, "ar")}"/></url>')
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm))
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print(f"built {len(urls) * 2} pages")


if __name__ == "__main__":
    main()
