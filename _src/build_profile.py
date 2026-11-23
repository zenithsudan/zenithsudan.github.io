#!/usr/bin/env python3
"""Builds assets/Zenith-Company-Profile-EN.pdf and -AR.pdf (A4) from one bilingual source.
Run:  python3 _src/build_profile.py   (needs playwright + chrome)"""
import os, asyncio
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = "file://" + os.path.join(ROOT, "assets")
LANG = "en"
EMAIL, WEB, WA_D, LI = "info@zenithsudan.com", "zenithsudan.com", "+249 91 217 4908", "linkedin.com/company/zenithsudan"


def t(en, ar):
    return en if LANG == "en" else ar


CSS = """
@font-face{font-family:Cairo;font-weight:400;src:url(@@A@@/cairo-arabic-400.woff2) format('woff2');unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF,U+200C-200F}
@font-face{font-family:Cairo;font-weight:700;src:url(@@A@@/cairo-arabic-700.woff2) format('woff2');unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF,U+200C-200F}
@page{size:A4;margin:0}
:root{--navy:#0F2A43;--amber:#F2A900;--steel:#5B6B7B;--light:#F2F4F6;--line:#dde2e8;--ink:#14212d}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,Helvetica,sans-serif;color:var(--ink);font-size:10.4pt;line-height:1.6;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html[lang=ar] body{font-family:Cairo,Arial,sans-serif;font-size:10.8pt;line-height:1.75}
html[lang=ar] *{letter-spacing:0!important}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;background:#fff}
.page:last-child{page-break-after:auto}
.hd{height:19mm;display:flex;align-items:center;justify-content:space-between;padding:0 16mm;border-bottom:2px solid var(--amber)}
.hd img{height:8.5mm}.hd span{font-size:8pt;color:var(--steel)}
.ft{position:absolute;bottom:0;left:0;right:0;height:11mm;background:var(--navy);color:#cbd5df;display:flex;align-items:center;justify-content:space-between;padding:0 16mm;font-size:7.5pt}
.ft b{color:var(--amber)}
.body{padding:13mm 16mm 0}
.kicker{font-size:7.5pt;letter-spacing:.28em;color:var(--amber);font-weight:700}
h1{font-size:24pt;color:var(--navy);line-height:1.18;margin:2mm 0 3mm}
h2{font-size:14pt;color:var(--navy);margin:7mm 0 3mm}
h3{font-size:11.2pt;color:var(--navy);margin-bottom:1mm}
p{color:#33414f;margin-bottom:2.2mm}
.lead{font-size:11pt;margin-bottom:6mm}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:5mm}.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm}
.box{border-top:3px solid var(--navy);background:var(--light);padding:5mm 5mm}
.box.a{border-top-color:var(--amber)}
.box p,.box li{font-size:9.8pt;margin-bottom:1.2mm}
.box ul{list-style:none}.box li{padding:1.7mm 0;border-bottom:1px solid var(--line)}.box li:last-child{border:0}
.tag{display:inline-block;margin-top:1.5mm;font-size:7pt;color:var(--steel);border:1px solid #b9c3cd;padding:.3mm 2mm;background:#fff}
.mission{background:var(--navy);color:#fff;padding:7mm 8mm;margin-top:8mm}
.mission .kicker{color:var(--amber);margin-bottom:1.5mm}.mission p{color:#e3e9ef;margin:0;font-size:10pt}
.stats{display:flex;gap:5mm;margin:6mm 0}.stat{background:var(--light);padding:3.5mm 5mm;min-width:38mm}
.stat b{display:block;font-size:20pt;color:var(--navy);line-height:1}.stat span{font-size:8pt;color:var(--steel)}
.steps{display:flex;margin-top:8mm}
.step{flex:1;background:var(--navy);color:#fff;padding:3.6mm 3.4mm;border-inline-end:1.5px solid var(--amber)}
.step i{font-style:normal;color:var(--amber);font-weight:700;font-size:8pt}.step b{display:block;font-size:8.8pt}.step span{font-size:7.4pt;color:#aeb9c5}
.note{border-inline-start:4px solid var(--amber);background:var(--light);padding:4mm 5mm;margin-top:6mm;font-size:9.8pt;color:#33414f}
.tools{background:var(--light);padding:4mm 5mm;margin-top:6mm;font-size:9.8pt}.tools b{color:var(--navy);font-size:7.5pt;letter-spacing:.2em;display:block}
.cover{background:var(--navy);color:#fff;display:flex;flex-direction:column;justify-content:center;padding:0 22mm}
.cover:before{content:"";position:absolute;right:-60mm;top:-20mm;width:170mm;height:170mm;background:linear-gradient(135deg,transparent 50%,rgba(242,169,0,.12) 50%)}
html[dir=rtl] .cover:before{right:auto;left:-60mm;transform:scaleX(-1)}
.cover img{width:112mm;position:relative}
.cover .t{font-size:17pt;margin-top:12mm;position:relative}
.cover .s{font-size:8pt;letter-spacing:.22em;color:var(--amber);margin-top:9mm;position:relative}
.cover .b{position:absolute;bottom:14mm;left:22mm;right:22mm;display:flex;justify-content:space-between;font-size:8.5pt;color:#9fb0c0}
.person{display:flex;gap:4mm;background:var(--light);padding:4mm;border-top:3px solid var(--amber)}
.person img{width:24mm;height:24mm;object-fit:cover;flex:none}
.person h3{font-size:11.2pt}.role{font-size:7pt;letter-spacing:.2em;color:var(--steel);font-weight:700;margin:.5mm 0 1.5mm}
.person p{font-size:8.6pt;margin:0;line-height:1.5}
.core .box p{font-size:8.6pt}.core .box{padding:4mm}
.owned{display:flex;gap:3mm;align-items:flex-start;padding:2mm 0;border-bottom:1px solid var(--line)}
.owned b.n{color:var(--amber);font-size:14pt;min-width:7mm;line-height:1}
table{width:100%;border-collapse:collapse;margin-top:3mm}td{padding:3.6mm 3mm;border-bottom:1px solid var(--line);font-size:10.4pt}td:first-child{color:var(--steel);width:44%}td:last-child{font-weight:700;color:var(--navy)}
.ltr{direction:ltr;unicode-bidi:isolate;display:inline-block}
""".replace("@@A@@", A)

_pn = [0]


def page(kicker, h1, inner, lead=""):
    _pn[0] += 1
    return (f'<div class="page"><div class="hd"><img src="{A}/logo.svg"><span>{t("Company Profile", "ملف الشركة")}</span></div>'
            f'<div class="body"><div class="kicker">{kicker}</div><h1>{h1}</h1>{f"<p class=lead>{lead}</p>" if lead else ""}{inner}</div>'
            f'<div class="ft"><span><b>ZENITH ENGINEERING</b> · {WEB}</span><span>{_pn[0]:02d}</span></div></div>')


def box(h, p="", items=None, amber=False, tag=None):
    inner = f"<h3>{h}</h3>" + (f"<p>{p}</p>" if p else "") + (("<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>") if items else "") + (f'<span class="tag">{tag}</span>' if tag else "")
    return f'<div class="box{" a" if amber else ""}">{inner}</div>'


def steps(*s):
    return '<div class="steps">' + "".join(f'<div class="step"><i>{i + 1:02d}</i><b>{a}</b><span>{b}</span></div>' for i, (a, b) in enumerate(s)) + "</div>"


def cover():
    return (f'<div class="page cover"><img src="{A}/logo-white.svg"><div class="t">{t("Company Profile", "ملف الشركة")}</div>'
            f'<div class="s">{t("CONSTRUCTION · WATER · SOLAR · CONSULTANCY", "المقاولات · المياه · الطاقة الشمسية · الاستشارات")}</div>'
            f'<div class="b"><span>{t("KASSALA, SUDAN", "كسلا، السودان")}</span><span dir="ltr">{WEB}</span></div></div>')


def p_about():
    why = t("Zenith was founded on a simple observation from inside humanitarian and development projects: the quality and timing of delivery depend on the strength of the technical team on the ground. Clients also lose time coordinating separate contractors for building, water, energy and design. We built Zenith to answer both problems: one trusted Sudanese engineering team, covering the full scope, accountable for the result.",
            "تأسست زينث انطلاقاً من ملاحظة بسيطة من داخل المشاريع الإنسانية والتنموية: جودة التنفيذ وسرعته تعتمدان على قوة الفريق الفني في الميدان. كما يخسر العملاء وقتاً في التنسيق بين مقاولين منفصلين للبناء والمياه والطاقة والتصميم. أنشأنا زينث لمعالجة الأمرين معاً: فريق هندسي سوداني موثوق واحد، يغطي النطاق كاملاً ويتحمل مسؤولية النتيجة.")
    inner = (f'<div class="stats"><div class="stat"><b>2025</b><span>{t("Established in Kassala", "تأسست في كسلا")}</span></div><div class="stat"><b>5</b><span>{t("Services, one standard", "خدمات، ومعيار واحد")}</span></div></div>'
             f'<h2>{t("Why Zenith exists", "لماذا وُجدت زينث")}</h2><p>{why}</p>'
             f'<h2>{t("What we stand for", "ما نؤمن به")}</h2><div class="g2">'
             + box(t("Consistent quality", "جودة ثابتة"), t("The same standard on every site, checked at each stage of the work.", "المعيار نفسه في كل موقع، مع فحص في كل مرحلة من العمل."))
             + box(t("Reliable commitment", "التزام موثوق"), t("Agreed scope, schedule and cost, honoured and communicated clearly.", "نطاق وجدول وتكلفة متفق عليها، نلتزم بها ونوضحها بشفافية."))
             + box(t("Specialized teams", "فرق متخصصة"), t("Dedicated crews for civil, water, solar and design work.", "فرق مخصصة لأعمال المدني والمياه والطاقة الشمسية والتصميم."))
             + box(t("Modern practice", "ممارسة حديثة"), t("BIM, CAD, hydraulic modelling and GIS applied to reduce errors before work reaches site.", "نطبّق BIM والرسم بالحاسوب والنمذجة الهيدروليكية ونظم المعلومات الجغرافية لتقليل الأخطاء قبل وصول العمل إلى الموقع."))
             + f'</div><div class="mission"><div class="kicker">{t("OUR MISSION", "رسالتنا")}</div><p>{t("To deliver dependable engineering and construction across Sudan, built on consistent quality, reliable commitment and specialized teams, using modern methods and technology.", "تقديم هندسة ومقاولات يُعتمد عليها في كل أنحاء السودان، قائمة على جودة ثابتة والتزام موثوق وفرق متخصصة، باستخدام أساليب وتقنيات حديثة.")}</p></div>')
    return page(t("ABOUT US", "من نحن"), t("Engineering that delivers across Sudan", "هندسة تُنجز في كل أنحاء السودان"), inner,
                t("Zenith Engineering is a Sudanese engineering company based in Kassala, ready to deploy teams across Sudan.", "زينث الهندسية شركة هندسية سودانية مقرها كسلا، وجاهزة لإرسال فرقها إلى كل أنحاء السودان."))


def p_services():
    inner = ('<div class="g2">'
             + box(t("Construction & Finishing", "المقاولات والتشطيبات"), items=[t("Buildings for health, education and offices", "مبانٍ للصحة والتعليم والمكاتب"), t("Finishing works and office fit-out", "أعمال التشطيبات وتجهيز المكاتب"), t("Rehabilitation of existing and damaged buildings", "إعادة تأهيل المباني القائمة والمتضررة")], amber=True)
             + box(t("Water & Infrastructure", "المياه والبنية التحتية"), items=[t("Water stations and pipeline works", "محطات المياه وأعمال الأنابيب"), t("Tank fabrication and installation", "تصنيع الخزانات وتركيبها"), t("Pump supply and installation", "توريد المضخات وتركيبها"), t("Borehole drilling managed by Zenith", "حفر الآبار بإدارة زينث")], amber=True)
             + box(t("Solar Energy", "الطاقة الشمسية"), items=[t("Solar systems for homes and offices", "أنظمة شمسية للمنازل والمكاتب"), t("Solar pumping for water stations", "الضخ بالطاقة الشمسية لمحطات المياه"), t("Power for agricultural projects and facilities", "طاقة للمشاريع والمنشآت الزراعية")], amber=True)
             + box(t("Engineering Consultancy", "الاستشارات الهندسية"), items=[t("Architectural and civil drawings", "رسومات معمارية ومدنية"), t("Designs", "التصاميم"), t("Quantity estimation and BoQs", "حصر الكميات وجداول الكميات (BoQ)"), t("Assessment of damaged buildings", "تقييم المباني المتضررة")], amber=True)
             + box(t("Interior Design & Landscape", "التصميم الداخلي والحدائق"), items=[t("Interiors for offices, homes and commercial spaces", "تصميم داخلي للمكاتب والمنازل والمساحات التجارية"), t("Landscape and gardens", "تنسيق الحدائق"), t("3D visualisation before work starts", "تصور ثلاثي الأبعاد قبل البدء")], amber=True)
             + '</div>' + steps((t("Survey", "المسح"), t("Site and demand", "الموقع والطلب")), (t("Design", "التصميم"), t("Drawings and BoQ", "الرسومات وحصر الكميات")), (t("Build", "التنفيذ"), t("Supervised works", "أعمال تحت الإشراف")), (t("Test", "الاختبار"), t("Checks and records", "فحوص وسجلات")), (t("Handover", "التسليم"), t("Training and records", "التدريب والسجلات"))))
    return page(t("OUR SERVICES", "خدماتنا"), t("Five services, one standard", "خمس خدمات، ومعيار واحد"), inner,
                t("Each service has its own specialists. All share the same management, quality controls and commitment to clients.", "لكل خدمة متخصصوها، وتجمعها إدارة واحدة وضوابط جودة واحدة والتزام واحد تجاه العملاء."))


def p_water():
    inner = ('<div class="g2">'
             + box(t("Pump supply and installation", "توريد المضخات وتركيبها"), t("Selection, supply and installation of submersible and surface pumps, with testing and operator handover.", "اختيار المضخات الغاطسة والسطحية وتوريدها وتركيبها، مع الاختبار وتسليمها للمشغّلين."), tag=t("Zenith team", "فريق زينث"))
             + box(t("Tank fabrication and installation", "تصنيع الخزانات وتركيبها"), t("Steel and elevated tanks fabricated and erected, with stands, fittings and leak testing.", "تصنيع الخزانات الحديدية والعلوية ونصبها، مع القواعد والتجهيزات واختبار التسرب."), tag=t("Zenith team", "فريق زينث"))
             + box(t("Pipeline works", "أعمال خطوط الأنابيب"), t("Trenching, laying, jointing and pressure testing of distribution and transmission lines.", "الحفر والمد والوصل واختبار الضغط لخطوط التوزيع والنقل."), tag=t("Zenith team", "فريق زينث"))
             + box(t("Water stations", "محطات المياه"), t("New construction and rehabilitation of water stations, from civil works to commissioning.", "إنشاء محطات المياه الجديدة وإعادة تأهيلها، من الأعمال المدنية حتى التشغيل."), tag=t("Zenith team", "فريق زينث"))
             + '</div>'
             + f'<div class="note"><b>{t("Borehole drilling.", "حفر الآبار.")}</b> {t("Carried out by qualified drilling contractors under Zenith management. We set the technical requirements, supervise the work and verify test results before handover.", "ينفذها مقاولو حفر مؤهلون تحت إدارة زينث. نحدد المتطلبات الفنية ونشرف على العمل ونتحقق من نتائج الاختبار قبل التسليم.")}</div>'
             + steps((t("Survey", "المسح"), t("Site and demand", "الموقع والطلب")), (t("Design", "التصميم"), t("Drawings and hydraulics", "الرسومات والهيدروليكا")), (t("Build", "التنفيذ"), t("Supervised works", "أعمال تحت الإشراف")), (t("Test", "الاختبار"), t("Pressure and flow", "الضغط والتدفق")), (t("Handover", "التسليم"), t("Training and records", "التدريب والسجلات"))))
    return page(t("WATER & INFRASTRUCTURE", "المياه والبنية التحتية"), t("From source to tap, built to last", "من المصدر إلى الصنبور، منفذة لتدوم"), inner,
                t("We deliver complete water systems for communities, health facilities, schools and agricultural sites. Our own teams handle supply, fabrication and installation, and we manage drilling through specialist contractors.", "ننفذ أنظمة مياه متكاملة للمجتمعات والمرافق الصحية والمدارس والمواقع الزراعية. تتولى فرقنا التوريد والتصنيع والتركيب، وندير أعمال الحفر عبر مقاولين متخصصين."))


def p_solar():
    inner = ('<div class="g2" style="grid-template-columns:1fr">'
             + box(t("Homes and offices", "المنازل والمكاتب"), t("Solar systems with battery storage for lighting, cooling, equipment and communications, sized to the building's daily use.", "أنظمة شمسية مع تخزين بالبطاريات للإنارة والتبريد والمعدات والاتصالات، بحجم يناسب الاستخدام اليومي للمبنى."), tag=t("Zenith team", "فريق زينث"))
             + box(t("Solar water pumping", "الضخ بالطاقة الشمسية"), t("Solar-powered pumping for water stations and boreholes, cutting fuel dependence and running costs.", "ضخ بالطاقة الشمسية لمحطات المياه والآبار، يقلل الاعتماد على الوقود وتكاليف التشغيل."), tag=t("Zenith team", "فريق زينث"))
             + box(t("Agricultural projects and facilities", "المشاريع والمنشآت الزراعية"), t("Power for irrigation, cold storage and farm facilities, designed around the site's seasonal demand.", "طاقة للري والتبريد والمنشآت الزراعية، مصممة بحسب الطلب الموسمي للموقع."), tag=t("Zenith team", "فريق زينث"))
             + '</div>' + steps((t("Assess", "التقييم"), t("Load and site", "الحمل والموقع")), (t("Size", "التحجيم"), t("Panels, battery, inverter", "الألواح والبطارية والمحوّل")), (t("Install", "التركيب"), t("Safe, supervised works", "أعمال آمنة تحت الإشراف")), (t("Test", "الاختبار"), t("Output and protection", "الإنتاج والحماية")), (t("Handover", "التسليم"), t("User training", "تدريب المستخدمين"))))
    return page(t("SOLAR ENERGY", "الطاقة الشمسية"), t("Reliable power where the grid is not", "طاقة موثوقة حيث لا توجد الشبكة"), inner,
                t("We design, supply and install solar systems sized to the real load, so facilities keep running through outages and fuel shortages. Our own team carries the work from assessment to handover.", "نصمم أنظمة الطاقة الشمسية ونوردها ونركبها بحسب الحمل الفعلي، لتواصل المنشآت عملها أثناء انقطاع الكهرباء ونقص الوقود. يتولى فريقنا العمل من التقييم حتى التسليم."))


def p_consult():
    inner = ('<div class="g2">'
             + box(t("Architectural and civil drawings", "مخططات معمارية ومدنية"), t("Plans, sections, details and site layouts, produced to a consistent standard and ready for tender or construction.", "مساقط وقطاعات وتفاصيل ومخططات مواقع، بمعيار ثابت وجاهزة للطرح أو التنفيذ."), tag=t("Zenith team", "فريق زينث"))
             + box(t("Designs", "التصاميم"), t("Structural and civil designs for buildings, water facilities and supporting works, with the basis of design recorded.", "تصاميم إنشائية ومدنية للمباني ومرافق المياه والأعمال المساندة، مع توثيق أساس التصميم."), tag=t("Zenith team", "فريق زينث"))
             + box(t("Quantity estimation and BoQs", "حصر الكميات وجداول الكميات"), t("Itemised quantities and priced bills of quantities that match the drawings, supporting clear tender evaluation.", "كميات مفصلة وجداول كميات مسعّرة تطابق المخططات، تدعم تقييماً واضحاً للعطاءات."), tag=t("Zenith team", "فريق زينث"))
             + box(t("Damaged building assessment", "تقييم المباني المتضررة"), t("Condition surveys that record damage, set repair priorities and cost the works needed to restore safe use.", "مسوح للحالة توثّق الضرر وتحدد أولويات الإصلاح وتقدّر كلفة الأعمال اللازمة لاستعادة الاستخدام الآمن."), tag=t("Zenith team", "فريق زينث"))
             + f'</div><div class="tools"><b>{t("TOOLS", "الأدوات")}</b>{t("AutoCAD and Civil 3D for drawings, EPANET for water networks, GIS for site mapping, and BIM (Revit) for coordinating architectural, structural and services drawings.", "AutoCAD وCivil 3D للمخططات، وEPANET لشبكات المياه، ونظم المعلومات الجغرافية لرسم المواقع، وBIM (Revit) لتنسيق المخططات المعمارية والإنشائية والخدمات.")}</div>'
             + steps((t("Brief", "الموجز"), t("Scope and needs", "النطاق والاحتياجات")), (t("Survey", "المسح"), t("Site and condition", "الموقع والحالة")), (t("Design", "التصميم"), t("Drawings and BoQ", "المخططات وجداول الكميات")), (t("Review", "المراجعة"), t("Internal check", "فحص داخلي")), (t("Deliver", "التسليم"), t("Final package", "الحزمة النهائية"))))
    return page(t("ENGINEERING CONSULTANCY", "الاستشارات الهندسية"), t("Clear designs, accurate numbers", "تصاميم واضحة، وأرقام دقيقة"), inner,
                t("Good projects start with good documents. We prepare the drawings, designs and cost estimates that tender, budget and build decisions depend on, and we assess existing buildings before money is spent on repairs.", "المشاريع الجيدة تبدأ بوثائق جيدة. نعدّ المخططات والتصاميم وتقديرات التكلفة التي تعتمد عليها قرارات العطاءات والميزانيات والتنفيذ، ونقيّم المباني القائمة قبل إنفاق المال على إصلاحها."))


def p_build_design():
    inner = (f'<h2>{t("Construction & Finishing", "المقاولات والتشطيبات")}</h2><div class="g2">'
             + box(t("Health, education and office buildings", "مبانٍ صحية وتعليمية ومكتبية"), t("New construction to agreed drawings, specifications and bills of quantities.", "إنشاء جديد وفق مخططات ومواصفات وجداول كميات متفق عليها."))
             + box(t("Finishing and office fit-out", "التشطيبات وتجهيز المكاتب"), t("Plastering, flooring, painting, joinery and fittings, with works planned to minimise downtime.", "لياسة وأرضيات ودهان ونجارة وتجهيزات، بتخطيط يقلل التوقف عن العمل."))
             + box(t("Rehabilitation", "إعادة التأهيل"), t("Assessment and repair of existing and damaged buildings, scoped before money is spent.", "تقييم المباني القائمة والمتضررة وإصلاحها، بعد تحديد النطاق قبل إنفاق المال."))
             + box(t("Supply and site logistics", "التوريد ولوجستيات الموقع"), t("Material supply managed by our own team, with our vehicle for hauling to site.", "توريد المواد بإدارة فريقنا، ومركبتنا الخاصة لنقلها إلى الموقع."))
             + f'</div><h2>{t("Interior Design & Landscape", "التصميم الداخلي والحدائق")}</h2><div class="g2">'
             + box(t("Interior design", "التصميم الداخلي"), t("Layouts, finishes and fittings for offices, homes and commercial spaces.", "توزيعات وتشطيبات وتجهيزات للمكاتب والمنازل والمساحات التجارية."))
             + box(t("Landscape and gardens", "تنسيق الحدائق"), t("Gardens and outdoor areas planned for the local climate and low maintenance.", "حدائق ومساحات خارجية مخططة بحسب المناخ المحلي وبصيانة منخفضة."))
             + box(t("Design to build", "من التصميم إلى التنفيذ"), t("The same team that designs the space builds it, so the result matches the drawings.", "الفريق الذي يصمم المساحة هو من ينفذها، فتطابق النتيجة المخططات."))
             + box(t("3D visualisation", "التصور ثلاثي الأبعاد"), t("3D views before work starts, so decisions are made on paper rather than on site.", "تصورات ثلاثية الأبعاد قبل البدء، لتُتخذ القرارات على الورق لا في الموقع."))
             + '</div>')
    return page(t("CONSTRUCTION & DESIGN", "الإنشاء والتصميم"), t("Built right, designed for use", "مبنية بإتقان، ومصممة للاستخدام"), inner)


def person(img, name, role, bio):
    return f'<div class="person"><img src="{A}/{img}"><div><h3>{name}</h3><div class="role">{role}</div><p>{bio}</p></div></div>'


def p_team():
    inner = ('<div class="g2">'
             + person("albraa.jpg", t("Albraa Ibrahim Khamis Mohamed", "البراء إبراهيم خميس محمد"), t("FOUNDER &amp; GENERAL MANAGER", "المؤسس والمدير العام"),
                      t("Civil engineer experienced in managing construction and infrastructure projects in complex field conditions, from planning and design through to handover. He founded Zenith to give clients one accountable company and one consistent standard of delivery, and leads its strategy, administrative and technical standards, and client relationships.",
                        "مهندس مدني ذو خبرة في إدارة مشاريع الإنشاءات والبنية التحتية في ظروف ميدانية معقدة، من التخطيط والتصميم حتى التسليم. أسس زينث ليمنح العملاء شركة واحدة مسؤولة ومعيارًا واحدًا في التنفيذ، ويقود استراتيجيتها ومعاييرها الإدارية والفنية وعلاقاتها مع العملاء."))
             + person("mohamed.jpg", t("Mohamed Mamoun Mohamed Khider", "محمد مأمون محمد خضر"), t("EXECUTIVE OPERATIONS MANAGER", "المدير التنفيذي للعمليات"),
                      t("Civil engineer (building and construction) with 10+ years of experience leading work teams, supervising sites and managing material supply chains. He builds execution systems that protect efficiency and quality, and previously managed a company importing and delivering pumps and solar energy equipment. He runs Zenith's operations.",
                        "مهندس مدني (بناء وتشييد) بخبرة تزيد على 10 سنوات في قيادة فرق العمل والإشراف الميداني وإدارة سلاسل توريد المواد. يضع أنظمة تنفيذ تضمن الكفاءة والجودة، وسبق له إدارة شركة تعمل في استيراد وتوصيل المضخات ومعدات الطاقة الشمسية. يتولى إدارة عمليات زينث."))
             + '</div><h2>' + t("Technical core", "النواة الفنية") + '</h2><div class="g3 core">'
             + box(t("Mossab Hassan Ali Mohammed", "مصعب حسن علي محمد"), t("Civil engineer. 7 years in construction and finishing works, team management, supply chain management and damaged building assessment. Experience delivering projects and sites for humanitarian organizations.", "مهندس مدني. 7 سنوات في أعمال الإنشاء والتشطيب وإدارة الفرق وإدارة سلاسل التوريد وتقييم المباني المتضررة. خبرة في تنفيذ المشاريع والمواقع لصالح منظمات إنسانية."), amber=True)
             + box(t("Asim Seddig Mohamed Alhassan", "عاصم صديق محمد الحسن"), t("Mechanical engineer. Specialist in building services modelling, with 7 years in solar energy, plumbing and electrical works, and in field supervision.", "مهندس ميكانيكي. متخصص في نمذجة خدمات المباني، بخبرة 7 سنوات في الطاقة الشمسية وأعمال السباكة والكهرباء والإشراف الميداني."), amber=True)
             + box(t("Yasser Abdeaziz Alkay", "ياسر عبد العزيز الكي"), t("Geological engineer. 9 years in borehole drilling, pump installation, tanks and water stations. Four full years in water programs with an international humanitarian organization.", "مهندس جيولوجي. 9 سنوات في حفر الآبار وتركيب المضخات والخزانات ومحطات المياه، منها أربع سنوات كاملة في برامج المياه مع منظمة إنسانية دولية."), amber=True)
             + '</div><h2>' + t("How we deliver", "كيف ننفذ") + '</h2><div class="g2">'
             + box(t("Skilled technicians", "فنيون مهرة"), t("Technicians with 10+ years of experience in masonry, steel, carpentry and finishing.", "فنيون بخبرة تزيد على 10 سنوات في البناء والحديد والنجارة والتشطيب."))
             + box(t("Specialist subcontractors", "مقاولون متخصصون من الباطن"), t("Brought in where the work calls for them, under Zenith's supervision.", "يُستعان بهم عندما يتطلب العمل ذلك، وتحت إشراف زينث."))
             + '</div>')
    return page(t("OUR TEAM", "فريقنا"), t("People who have built it before", "أناس سبق لهم التنفيذ"), inner,
                t("Zenith is led by two civil engineers who manage its strategy and operations, supported by a technical team and skilled tradespeople.", "يقود زينث مهندسان مدنيان يديران استراتيجيتها وعملياتها، ويدعمهما فريق فني وحرفيون مهرة."))


def p_quality():
    inner = ('<div class="g2">'
             + box(t("Quality at every stage", "الجودة في كل مرحلة"), t("Materials checked on delivery, works inspected before they are covered, and tests recorded before handover.", "فحص المواد عند التسليم، ومعاينة الأعمال قبل تغطيتها، وتوثيق الاختبارات قبل التسليم."))
             + box(t("Health and safety", "الصحة والسلامة"), t("Hazards identified before work starts, with protective equipment, safe methods and incident reporting on every site.", "تحديد المخاطر قبل بدء العمل، مع معدات الوقاية وطرق العمل الآمنة والإبلاغ عن الحوادث في كل موقع."))
             + box(t("Integrity", "النزاهة"), t("Honest bidding, declared conflicts of interest, and no tolerance for bribery or improper payments.", "تقديم عطاءات نزيهة، والإفصاح عن تضارب المصالح، وعدم التسامح مع الرشوة أو المدفوعات غير المشروعة."))
             + box(t("Safeguarding", "الحماية"), t("A code of conduct for all staff and subcontractors, a named focal point and clear steps for raising concerns.", "مدونة سلوك لجميع الموظفين والمقاولين من الباطن، ونقطة اتصال معروفة، وخطوات واضحة لرفع الشكاوى."))
             + f'</div><h2>{t("Aligned with humanitarian standards", "متوافق مع المعايير الإنسانية")}</h2><p>{t("Our water and construction work is planned in line with Sphere standards and the Core Humanitarian Standard, and our safeguarding approach follows IASC principles. We work with community participation, coordinate with partners and design for operation and maintenance after handover.", "نخطط أعمال المياه والإنشاءات وفق معايير سفير والمعيار الإنساني الأساسي (CHS)، ويتبع نهجنا في الحماية مبادئ لجنة الوكالات الدائمة (IASC). نعمل بمشاركة المجتمع، ونتنسق مع الشركاء، ونصمم مع مراعاة التشغيل والصيانة بعد التسليم.")}</p>'
             + steps((t("Plan", "التخطيط"), t("Scope, risks, resources", "النطاق والمخاطر والموارد")), (t("Build", "التنفيذ"), t("Supervised, inspected", "تحت الإشراف والمعاينة")), (t("Verify", "التحقق"), t("Tests and records", "الاختبارات والسجلات")), (t("Handover", "التسليم"), t("Training, defects period", "التدريب وفترة العيوب"))))
    return page(t("METHODOLOGY AND QUALITY", "المنهجية والجودة"), t("The same standard on every site", "المعيار نفسه في كل موقع"), inner,
                t("Our approach is built on four commitments that apply to every project, whatever its size.", "يقوم نهجنا على أربعة التزامات تنطبق على كل مشروع مهما كان حجمه."))


def p_resources():
    def own(n, h, p):
        return f'<div class="owned"><b class="n">{n}</b><div><h3 style="font-size:9.6pt">{h}</h3><p style="margin:0;font-size:8.8pt">{p}</p></div></div>'
    inner = ('<div class="g2"><div class="box a"><div class="kicker" style="color:var(--navy)">' + t("OWNED", "نملكها") + '</div>'
             + own("3", t("Welding machines", "ماكينات لحام"), t("Different capacities, covering light fabrication to heavier steel work.", "بقدرات مختلفة، من التصنيع الخفيف إلى أعمال الحديد الأثقل."))
             + own("2", t("Pickup trucks", "سيارات بيك أب"), t("1-tonne and 1.5-tonne payloads for moving materials to site.", "حمولة 1 طن و1.5 طن لنقل المواد إلى الموقع."))
             + own("2", t("Portable generators", "مولدات متنقلة"), t("Fuel-powered, for tools and works at sites without mains power.", "تعمل بالوقود، للأدوات والأعمال في المواقع بلا كهرباء عامة."))
             + own("+", t("Site and design equipment", "معدات الموقع والتصميم"), t("Rebar cutting and concreting equipment, plus high-specification design workstations.", "معدات قطع حديد التسليح وصب الخرسانة، إضافة إلى محطات تصميم عالية المواصفات."))
             + '</div><div class="box"><div class="kicker" style="color:var(--navy)">' + t("PROVIDED PER PROJECT", "تُوفَّر لكل مشروع") + '</div>'
             + own("", t("Heavy plant", "آليات ثقيلة"), t("Excavators, loaders and compaction equipment, arranged through vetted rental providers.", "حفارات ومحمّلات ومعدات دك، تُرتَّب عبر مزودي تأجير تم التحقق منهم."))
             + own("", t("Drilling rigs", "جهاز الحفر"), t("Supplied by specialist drilling contractors under our management.", "يوفرها مقاولو حفر متخصصون تحت إدارتنا."))
             + own("", t("Additional transport", "نقل إضافي"), t("Trucks and lifting equipment hired to match delivery volumes.", "شاحنات ومعدات رفع تُستأجر بما يناسب حجم التوريد."))
             + '</div></div>'
             + f'<div class="note">{t("Every project starts with a resource plan that names what we use, what we hire and who supplies it, so clients know the capacity behind the schedule.", "يبدأ كل مشروع بخطة موارد تحدد ما نستخدمه وما نستأجره ومن يورده، ليعرف العملاء القدرة التي يقوم عليها الجدول الزمني.")}</div>')
    return page(t("RESOURCES", "الموارد"), t("The right tools for each project", "الأدوات المناسبة لكل مشروع"), inner,
                t("We own the equipment our daily work depends on and bring in specialist plant for each project. This keeps our costs lean and our capacity matched to the job.", "نملك المعدات التي يعتمد عليها عملنا اليومي، ونستقدم الآليات المتخصصة لكل مشروع. وهذا يبقي تكاليفنا منخفضة وقدرتنا متناسبة مع العمل."))


def p_contact():
    rows = [(t("Business name", "الاسم التجاري"), "Zenith Engineering · زينث الهندسية"),
            (t("Founder & General Manager", "المؤسس والمدير العام"), t("Albraa Ibrahim", "البراء إبراهيم")),
            (t("Executive Operations Manager", "المدير التنفيذي للعمليات"), t("Mohamed Mamoun", "محمد مأمون")),
            (t("WhatsApp / Phone", "واتساب / هاتف"), f'<span class="ltr">{WA_D}</span>'),
            (t("Email", "البريد"), f'<span class="ltr">{EMAIL}</span>'),
            (t("Website", "الموقع"), f'<span class="ltr">{WEB}</span>'),
            ("LinkedIn", f'<span class="ltr">{LI}</span>'),
            (t("Base", "المقر"), t("Kassala, Sudan", "كسلا، السودان")),
            (t("Coverage", "التغطية"), t("Projects across Sudan", "مشاريع في كل أنحاء السودان"))]
    inner = "<table>" + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows) + "</table>"
    return page(t("CONTACT", "تواصل معنا"), t("Work with us", "اعمل معنا"), inner,
                t("We welcome tender invitations, site visits and technical discussions.", "نرحب بدعوات العطاءات والزيارات الميدانية والنقاشات الفنية."))


def build(lang):
    global LANG
    LANG = lang
    _pn[0] = 1
    pages = [cover(), p_about(), p_services(), p_water(), p_solar(), p_consult(), p_build_design(), p_team(), p_quality(), p_resources(), p_contact()]
    title = t("Zenith Engineering — Company Profile", "زينث الهندسية — ملف الشركة")
    return (f'<!DOCTYPE html><html lang="{lang}" dir="{"ltr" if lang == "en" else "rtl"}"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>'
            + "".join(pages) + "</body></html>")


async def main():
    os.makedirs("/tmp/zprofile", exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        for lang in ("en", "ar"):
            f = f"/tmp/zprofile/profile-{lang}.html"
            open(f, "w", encoding="utf-8").write(build(lang))
            pg = await b.new_page()
            await pg.goto("file://" + f)
            await pg.wait_for_timeout(600)
            out = os.path.join(ROOT, "assets", f"Zenith-Company-Profile-{lang.upper()}.pdf")
            await pg.pdf(path=out, prefer_css_page_size=True, print_background=True)
            await pg.close()
            print("wrote", out)
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
