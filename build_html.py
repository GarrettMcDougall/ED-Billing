#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ED Billing Guide — HTML generator.

Rebuilt 2026-08-07 by reverse-engineering the then-current live index.html,
after the original generator was lost to an environment reset. This is the
authoritative source going forward — edit SECTIONS below and re-run this
script rather than hand-editing index.html directly.

Usage:
    python3 build_html.py
Writes to /mnt/user-data/outputs/index.html (or change OUT_PATH below).

Row entry types within a section's list:
    ("SUB", "text")                — small uppercase sub-header
    ("NOTE", "text")               — small red italic note
    ("SECINFO", "text")            — section-level info box (rare; prefer per-row info=)
    ("CALC",)                      — inserts the sedation calculator widget here
    row(desc, code, price, ...)    — a normal billing-code row; see kwargs below

row() kwargs (all optional):
    added=True      — show a green "NEW" tag next to the description
    hidden=True      — search-only row (hidden until the user searches for it)
    badge="g35"|"gno"|"g3only"  — G3/G5 critical-care billing compatibility badge
    syn="keyword keyword"        — extra search synonyms (lay terms etc.)
    info="explanation text"      — adds a tappable (i) info-bubble with this text
    expand=True      — special: marks this row as the ISS-calculator trigger
                        (currently only meaningful for E420; the ISS widget is
                        hard-coded to attach there in render_row()).

VERSION must be bumped (and version.txt updated to match) on every real change
so the auto-update banner fires for people with an older copy already open.
"""
import json as _json

VERSION = "2026-08-07g"

OUT_PATH = "/mnt/user-data/outputs/index.html"

def row(desc, code, price, added=False, hidden=False, badge=None, syn=None, info=None, expand=False, fxbadge=None):
    return ("ROW", desc, code, price, {
        "added": added, "hidden": hidden, "badge": badge,
        "syn": syn, "info": info, "expand": expand, "fxbadge": fxbadge,
    })

SECTIONS = [
    ('assess', 'Assessments', '#0ea5e9', [
        ('SUB', 'Weekday (08:00–17:00)'),
        row('Multi system', 'H103', '$46.65'),
        row('Comprehensive', 'H102', '$56.70'),
        row('Minor', 'H101', '$22.65'),
        row('Re-assessment*', 'H104', '$22.75'),
        ('SUB', 'Evening (17:00–24:00)'),
        row('Multi system', 'H133', '$61.50'),
        row('Comprehensive', 'H132', '$75.40'),
        row('Minor', 'H131', '$30.05'),
        row('Re-assessment*', 'H134', '$30.05'),
        ('SUB', 'Nights (00:00–08:00) incl weekend'),
        row('Multi system', 'H123', '$80.95'),
        row('Comprehensive', 'H122', '$99.60'),
        row('Minor', 'H121', '$39.85'),
        row('Re-assessment*', 'H124', '$39.80'),
        ('SUB', 'Sat/Sun/Holidays (08:00–24:00)'),
        row('Multi system', 'H153', '$69.60'),
        row('Comprehensive', 'H152', '$85.70'),
        row('Minor', 'H151', '$34.15'),
        row('Re-assessment*', 'H154', '$34.15'),
        ('SUB', 'Consultation & admin'),
        row('Consultation (sent by GP)', 'H055', '$125.65'),
        row('Holding orders', 'H105', '$29.05'),
        row('EP admits to other MRP, at their request', 'C004', '$38.35'),
        row('EP admits and is the MRP', 'C933', '$82.00'),
        row('EM consultation (non-FRCPC)', 'H065', '$95.60'),
        ('NOTE', '*R/A: max 3/pt/d & 2/MD/pt/d; document change'),
    ]),
    ('crit', 'Critical Care', '#ef4444', [
        ('SUB', 'Life-threatening resusc (organ failure)'),
        row('First 15 min', 'G521', '$125.10', syn='code blue cardiac arrest crash resuscitation'),
        row('2nd 15 min', 'G523', '$64.50', syn='code blue cardiac arrest crash resuscitation'),
        row('Every 15 min after', 'G522', '$42.50', syn='code blue cardiac arrest crash resuscitation'),
        row('4th doc per 15 min', 'G391', '$34.35', syn='resuscitation code'),
        row('Trauma premium (ISS>15)', 'E420', '50%', expand=True),
        ('SUB', 'Other resusc'),
        row('First 15 min', 'G395', '$64.70', syn='resuscitation code'),
        row('Every 15 min after', 'G391', '$34.35', syn='resuscitation code'),
        row('CritiCall referring out', 'K736', '$37.05'),
        ('SUB', 'Resuscitative Procedures'),
        row('Chest tube', 'Z341', '$76.80', badge='g35', syn='pneumothorax pleural', info='Tube thoracostomy for pneumothorax, haemothorax, or empyema. Billable alongside G3/G5 critical care codes (see badge above). A same-day tube exchange is billed as a single Z341, not as two separate insertions.'),
        row('Chest tube — removal', 'Z363', '$20.00', badge='g35', info="Removal of a chest tube once it's no longer needed. Not payable the same day as a Z341 insertion for the same patient — a same-day tube exchange is billed as Z341 alone."),
        row('Cardioversion (G3 only, not G5)', 'Z437', '$92.45', badge='g3only', syn='shock defibrillation dccv afib arrhythmia'),
        row('Paracentesis diagnostic', 'Z590', '$31.30', badge='g35', syn='ascites fluid belly'),
        row('Paracentesis therapeutic', 'Z591', '$57.65', badge='g35', syn='ascites fluid belly'),
        row('Pericardiocentesis', 'Z401', '$131.70', badge='g35', syn='cardiac tamponade fluid heart'),
        row('Thoracentesis (dx or tx)', 'Z332', '$104.40', badge='g35', syn='pleural effusion fluid lung', info="One code covers both diagnostic and therapeutic aspiration — you don't need to choose between them. Bill Z332 whether you're sampling for diagnosis, draining for symptom relief, or both in the same visit."),
        row('IO (intraosseous line)', 'G270', '$23.90', badge='g35', syn='io line bone access'),
        row('LP (lumbar puncture)', 'Z804', '$150.00', badge='g35', syn='lp spinal tap'),
        row('Endotracheal intubation', 'G211', '$38.35', badge='gno', syn='airway tube intubate'),
        row('Transcutaneous/transthoracic pacemaker insertion', 'G303', '$51.25', badge='g3only', syn='pacing pacer code'),
        row('Arterial puncture for blood gas', 'Z459', '$10.20', badge='gno', syn='abg blood gas'),
        row('Gastric lavage — therapeutic', 'G356', '$33.80', badge='gno', syn='overdose toxic ingestion pump stomach', info='Typical ED use: a significant toxic ingestion within the treatment window, or occasionally a massive upper GI bleed needing lavage before endoscopy. Distinct from routine NG tube placement, which is bundled into critical care codes and not separately billable alongside them.'),
        row('Gastric lavage — diagnostic', 'G355', '$9.60', hidden=True, badge='gno', syn='overdose toxic ingestion pump stomach'),
        ('SUB', 'Advanced Resuscitative Procedures'),
        row('Flexible or rigid bronchoscopy, ± biopsy, suction, or contrast injection', 'Z327', '$124.90', badge='g35', info='Rare in the ED — consider for a retained airway foreign body, significant haemoptysis, or clearing an obstructed airway when direct visualization is needed. The add-on codes E636 (lavage) and E838 (high-risk) only apply on top of this base code, not standalone.'),
        row('Broncho-alveolar lavage, add to Z327', 'E636', '$50.00', badge='g35', info='Add-on to Z327 only — not billable standalone. Use when lavage fluid is sent for infection workup or malignancy diagnosis, not for simple suctioning during the same scope.'),
        row('Bronchoscopy in high-risk resp. failure patient, add to Z327', 'E838', '$79.40', badge='g35', info='Add-on to Z327 for a bronchoscopy in a patient with severe hypoxemia or hypercapnia. Payment condition: you must remain with the patient after the procedure until oxygenation returns to baseline — document this explicitly.'),
        row('Limited bronchoscopy with endobronchial blocker or double-lumen tube placement', 'Z342', '$112.55', badge='g35', info='For lung-isolation procedures — placing a bronchial blocker or positioning a double-lumen tube, e.g. to protect a non-bleeding lung during massive haemoptysis. Uncommon in the ED (more typical in OR/ICU), but billable if you perform it yourself at the bedside.'),
        row('Emergency rigid bronchoscopy for obstructed airway', 'Z360', '$474.65', badge='gno'),
        row('Emergency tracheotomy', 'Z325', '$474.65', badge='g35', info="Reserved for a genuine crash airway in a patient who is NOT already intubated — not for a planned or semi-elective tracheostomy on an already-tubed patient. Document why endotracheal intubation or cricothyrotomy wasn't feasible in the moment."),
        row('Change of tracheostomy tube', 'Z326', '$12.50', badge='g35'),
        row('Insertion of Swan-Ganz (pulmonary artery) catheter', 'Z438', '$162.50', badge='g35'),
        row('Cardiac massage, open (e.g. during resuscitative thoracotomy)', 'R765', '$231.30', badge='g35', syn='open cardiac massage thoracotomy code', info='For open (direct) cardiac massage during a resuscitative thoracotomy \u2014 distinct from closed/external compressions, which are covered under critical care time codes. Related formal cardiac-surgery codes (R712, R748, R749, M137) may also apply depending on what else was done; confirm the combination with your billing office.'),
        row('Thoracotomy, ± biopsy', 'M137', '$390.65', info="A formal thoracotomy code — not routine bedside billing. This is not the same as an ED resuscitative thoracotomy for penetrating arrest, which doesn't have its own distinct code in the schedule. Confirm the procedure genuinely meets this code's surgical requirements before billing; check with your billing office if unsure."),
        row('Pericardiectomy, one side open', 'R748', '$635.45', info="A formal pericardiectomy code (unilateral) \u2014 not routine ED billing. Distinct from pericardiocentesis (Z401) or a bedside pericardial window; confirm the specific surgical procedure was performed before billing."),
        row('Pericardiectomy, both sides open or sternal split', 'R749', '$1097.90', info="A formal pericardiectomy code \u2014 not routine ED billing. Distinct from pericardiocentesis (Z401); confirm the specific surgical procedure was performed before billing."),
        row('Cardiotomy, with exploration', 'R712', '$525.75', info="A formal cardiotomy code for surgical exploration of the heart \u2014 not the same as open cardiac massage (R765) during a resuscitative thoracotomy. Confirm the procedure meets this code's surgical requirements before billing."),
        row('Exploration of major artery', 'R764', '$271.60', info="For surgical exploration of a major artery, e.g. after penetrating vascular trauma. A formal vascular surgery code \u2014 confirm it matches what was actually done before billing in an ED context."),
        row('Hypothermia (therapeutic) induction and management', 'G210', '$190.75', badge='g35', syn='ttm targeted temperature management cooling post-arrest'),
        row('Insertion of oesophageal transducer (for TEE)', 'G580', '$45.00', badge='g35'),
        row('Oesophageal tamponade device insertion (e.g. Blakemore/Minnesota)', 'G349', '$45.30', badge='g35'),
        ('SUB', 'G/K code premium'),
        row('Weekend/Holiday 08–24h', 'H113', '$32.20'),
        row('Nights 00–08h', 'H112', '$50.95'),
        row('Evenings 17–24h Mon–Thu', 'H114', '$23.65'),
        row('Ground ambulance detention (per 15 min)', 'K101', '$60.00'),
        row('Air ambulance detention (per 15 min)', 'K111', '$60.00'),
        row('Return without patient to original location', 'K112', '$21.10'),
    ]),
    ('counsel', 'Counseling & Forms', '#8b5cf6', [
        ('SUB', 'Counseling (30 min = 1 unit, min 20 min)'),
        row('Donor discussion (per unit)', 'K014', '$80.00', info='Time-based discussion with family around organ/tissue donation, billed per 30-minute unit (or major part thereof). Document the duration and content of the discussion.'),
        row('Relatives of dying pt (per unit)', 'K015', '$80.00', info='Time-based counselling of relatives on behalf of a catastrophically or terminally ill patient — for one or more family members. Billed per unit (30 min or major part thereof).'),
        row('Needle stick / STD', 'K028', '$80.00', info='Time-based, all-inclusive assessment and counselling for a suspected STI or blood-borne pathogen exposure (e.g. needle-stick). Not payable alongside another consultation, assessment, or visit by you for the same patient the same day. Capped at 2 units/patient/day and 4 units/patient/year.'),
        row('Mental Health (per unit, 30 min)', 'K005', '$80.00', info='Individual primary mental health care, billed per unit. Not payable alongside another consultation or visit for the same patient the same day unless the diagnoses are clearly distinct.'),
        ('SUB', 'Forms'),
        row('Form 1', 'K623', '$133.60', syn='mental health act involuntary', info='Application for psychiatric assessment under the Mental Health Act (Form 1). Includes the necessary history, exam, notifying the patient/family/relevant authorities, and completing the form itself.'),
        row("Substance abuse assm't", 'K680', '$80.00', info='Time-based extended assessment for a patient receiving substance-abuse therapy. Not payable alongside another consultation, assessment, visit, or time-based service the same day. Not eligible for smoking-cessation management — use E079 for that.'),
        row("Interview with Children's Aid Society", 'K003', '$80.00', info="For a documented interview with Children's Aid Society staff regarding a patient in your care — keep a record of who you spoke with and what was discussed."),
        row('Counselling / education (per 30 min)', 'K013', '$80.00', info='Individual counselling, billed per unit. Covers the first three units per patient per provider per 12-month period before a lower add-on rate applies to further units.'),
        row('Phone reporting of MOH-reportable disease', 'K034', '$36.00', info='Telephone reporting of a reportable disease to the Medical Officer of Health, as required under the Health Protection and Promotion Act.'),
        row('Blood sample collection at request of police', 'K061', '$34.80', info='For collecting a blood sample specifically at the request of police (e.g. an impaired-driving investigation) — distinct from routine clinical venipuncture (G489).'),
        row('Sexual assault examination, female', 'K018', '$358.45', info='For a sexual assault examination and evidence-kit documentation (Ministry of the Attorney General / Solicitor General kit). Covers the exam and documentation itself \u2014 not a general assessment fee.'),
        row('Sexual assault examination, male', 'K021', '$282.75', info='For a sexual assault examination and evidence-kit documentation (Ministry of the Attorney General / Solicitor General kit). Covers the exam and documentation itself \u2014 not a general assessment fee.'),
        row('Phone consult ER to other MD, >10 min, no live consult', 'K734', '$37.05', info='For a documented telephone consultation of more than 10 minutes with another physician, where no live/in-person consult takes place.'),
        row('Consultant ER MD phone recommendations, >10 min', 'K735', '$47.75', info="For the consulting physician's documented telephone recommendations back to the referring physician, more than 10 minutes — the receiving side of a K734-type call."),
        row('CritiCall receiving consult', 'K737', '$47.75', info='For accepting a CritiCall-referred patient and providing recommendations — the receiving-physician counterpart to K736 (referring out).'),
        row('Smoking cessation counselling (initial)', 'E079', '$15.95', syn='quit smoking', info='Initial smoking-cessation counselling visit. Billed separately from, and not interchangeable with, K680 (which explicitly excludes smoking-cessation management).'),
        row('MTO', 'K035', '$36.25', info='For completing a Ministry of Transportation medical report (e.g. a fitness-to-drive assessment).'),
        row('Death cert & pronounce', 'A777', '$44.55', syn='death certificate pronounce', info='Covers both pronouncing death and completing the death certificate for the same patient in one service.'),
        row('Death cert only', 'A771', '$24.20', syn='death certificate pronounce', info='Completing the death certificate only — use when pronouncement was already done by someone else (e.g. a nurse under an existing hospital protocol).'),
        row("Home care appl'n (CCAC)", 'K070', '$34.75', syn='ccac discharge planning', info='For completing and submitting a home care referral form to Ontario Health atHome on behalf of a patient you provide ongoing care for. Billed in addition to the assessment fee, where applicable. Limited to one per home care admission per patient.'),
        row('Acute home care supervision (<8wk)', 'K071', '$21.95', syn='ccac discharge planning', info='Medical advice, direction, or information provided for a patient in the first 8 weeks of a home care program. Must be documented in the chart. Not payable the same day as a consultation or visit for the same patient.'),
        row('Chronic home care supervision (>8wk)', 'K072', '$21.95', syn='ccac discharge planning', info='Same as K071, but for supervision after the 8th week of the home care program — use this once the acute window has passed.'),
    ]),
    ('svp', 'On Call / SVP', '#0891b2', [
        ('SUB', 'SVP assessment codes'),
        row('Minor', 'A001', '$26.80'),
        row('Intermediate', 'A007', '$44.55'),
        row('General assessment', 'A003', '$95.60'),
        row('General re-assessment', 'A004', '$39.35'),
        ('SUB', 'Weekday (07–17) — max 5 pts'),
        row('Travel Premium', 'H960', '$37.40'),
        row('1st pt seen', 'H980', '$20.55'),
        row('Additional pts', 'H981', '$20.55'),
        ('SUB', 'Evening (17–24) — max 5 pts'),
        row('Travel Premium', 'H962', '$37.40'),
        row('1st pt seen', 'H984', '$61.70'),
        row('Additional pts', 'H985', '$61.70'),
        row('Procedure premium', 'E409', '50%'),
        ('SUB', 'Nights (00–07) — no max'),
        row('Travel Premium', 'H964', '$37.40'),
        row('1st pt seen', 'H986', '$102.80'),
        row('Additional pts', 'H987', '$102.80'),
        ('SUB', 'Wknd/holidays (07–24) — max 10 pts'),
        row('Travel Premium', 'H963', '$37.40'),
        row('1st pt seen', 'H988', '$77.10'),
        row('Additional pts', 'H989', '$77.10'),
        row('Procedure premium', 'E410', '75%'),
    ]),
    ('discrep', 'Discrepancies (Phone)', '#7c3aed', [
        ('NOTE', '⚠ Must add + K301 (phone modifier) to each of these codes.'),
        ('SUB', 'Telephone calls'),
        row("Call someone else's patient", 'A102', '$15.00'),
        row('Call your patient, simple', 'A001', '$26.80'),
        row('Call your patient, complex', 'A007', '$44.55'),
    ]),
    ('id', 'I&D', '#14b8a6', [
        ('SUB', 'Local anesthetic'),
        row('SC x1 (incl trephination)', 'Z101', '$28.20'),
        row('SC x2', 'Z173', '$33.25'),
        row('SC x3+', 'Z174', '$44.70'),
        row('perianal', 'Z104', '$33.25'),
        row('ischiorectal / pilonidal', 'Z106', '$48.60'),
        row('palmar / plantar spaces', 'Z103', '$48.60'),
        row('Breast', 'Z140', '$33.00'),
        row('Oral / PTA', 'Z506', '$50.90'),
        row('Vulvar / Bartholin', 'Z714', '$25.40'),
        ('SUB', 'Under sedation'),
        row('SC x1', 'Z102', '$48.60'),
        row('SC x2+', 'Z172', '$72.95'),
        row('perianal', 'Z105', '$72.30'),
        row('ischiorectal / pilonidal', 'Z107', '$118.30'),
        row('palmar / plantar spaces', 'Z108', '$78.90'),
        row('Vulvar / Bartholin', 'Z715', '$102.05'),
        ('SUB', 'Foreign body removal'),
        row('SC/skin, local anaesthetic', 'Z114', '$27.65'),
        row('SC/skin, general anaesthetic', 'Z115', '$97.30'),
        row('Excision of foreign body (muscle/soft tissue)', 'R517', '$107.70', syn='foreign body deep muscle'),
        row('Cornea FB x1', 'Z847', '$33.00', syn='eye foreign body'),
        row('Cornea FB x2 (Z845 if 3+)', 'Z848', '$45.00', syn='eye foreign body'),
        row('Corneal/eye FB, 3 or more', 'Z845', '$50.90', syn='eye foreign body eye foreign body'),
        row('Ear FB, simple', 'Z915', '$10.55'),
        row('Ear FB w sedation', 'Z866', '$50.90'),
        row('Nose, simple', 'Z311', '$10.55'),
        row('Nose, w sedation', 'Z312', '$50.90'),
        row('GI / rectal FB', 'Z541', '$66.50'),
        row('Fecal disimpaction', 'Z756', '$46.00', syn='constipation impaction'),
        row('Vagina FB', 'Z432', '$54.10'),
        row('Nail plate excision', 'Z128', '$36.30'),
        row('Nail excision + cautery', 'Z130', '$68.75'),
        row('Revision of amputated finger tip', 'R629', '$241.55', syn='fingertip amputation traumatic'),
        row('Gastrostomy tube change', 'Z520', '$10.65', syn='g-tube g tube gastric tube feeding tube'),
        row('Eyelid abscess I&D', 'Z854', '$60.00', syn='stye hordeolum boil pus infection'),
        row('Cyst removal, face/neck (1)', 'Z122', '$42.20', syn='lump bump sebaceous cyst'),
        row('Cyst removal, face/neck (2)', 'Z123', '$74.30', syn='lump bump sebaceous cyst'),
        row('Cyst removal, face/neck (3+)', 'Z124', '$85.45', syn='lump bump sebaceous cyst'),
        row('Ingrown nail, multiple', 'Z129', '$39.20', syn='toenail ingrown toe'),
        row('Skin lesion excise/suture (1)', 'Z162', '$21.90', syn='mole growth lump'),
        row('Skin lesion excise/suture (2)', 'Z163', '$29.05', syn='mole growth lump'),
        row('Skin lesion excise/suture (3+)', 'Z164', '$48.50', syn='mole growth lump'),
        row('Secondary wound closure', 'Z783', '$97.35'),
    ]),
    ('lac', 'Lacerations', '#10b981', [
        ('SUB', 'Simple (not face) — 50% if glue'),
        row('< 5 cm', 'Z176', '$21.90', syn='laceration cut wound stitches sutures'),
        row('5–10 cm', 'Z175', '$39.35', syn='laceration cut wound stitches sutures'),
        row('10–15 cm', 'Z179', '$55.20', syn='laceration cut wound stitches sutures'),
        row('> 15 cm', 'Z191', '$84.70', syn='laceration cut wound stitches sutures'),
        row('Earlobe', 'R024', '$110.25'),
        ('SUB', 'Face, bleeder, layers'),
        row('< 5 cm', 'Z154', '$39.35', syn='laceration cut wound stitches sutures face'),
        row('5–10 cm', 'Z177', '$78.15', syn='laceration cut wound stitches sutures face'),
        row('10–15 cm', 'Z190', '$111.20', syn='laceration cut wound stitches sutures face'),
        row('> 15 cm', 'Z192', '$169.75', syn='laceration cut wound stitches sutures face'),
        row('w sedation', 'E530', '$55.20'),
        ('SUB', 'Complex'),
        row('Complex (not face)', 'Z188', '$101.15', syn='laceration cut wound stitches sutures complex'),
        row('Complex face', 'Z187', '$101.15', syn='laceration cut wound stitches sutures complex face'),
        row('Zone 1 digit', 'Z189', '$101.15', syn='laceration cut wound stitches sutures finger'),
        row('Eyelid laceration repair, full thickness', 'E199', '$452.65', syn='cut wound stitches sutures'),
        ('SUB', 'Wound / ulcer debridement (>10 min)'),
        row('To SC tissue — one', 'Z080', '$20.00'),
        row('To SC tissue — two', 'Z081', '$30.00'),
        row('To SC tissue — three', 'Z082', '$45.00'),
        row('To SC tissue — four+', 'Z083', '$60.00'),
        row('Tendon/lig/bursa/bone — one', 'Z084', '$60.00'),
        row('Tendon/lig/bursa/bone — 2+', 'Z085', '$90.00'),
        row('Out-of-hospital premium', 'E542', '$11.15'),
    ]),
    ('sedation', 'Procedural Sedation', '#f43f5e', [
        ("CALC",),
        ('SUB', 'Reference — raw codes'),
        row('BASE: 6u (procedure code + "C")', '6u', '$95.52'),
        row('Add TIME to base; 15 min = 1u', '1u', '$15.92'),
        row('If no code available (6u base)', 'E003C', '$95.52'),
        row('Exam under anesthesia (6u base)', 'E023C', '$95.52'),
        ('SUB', 'Extra units'),
        row('ASA E — Emergency sedation = 4u', 'E020C', '$63.68'),
        row('ASA III: Severe systemic = 2u', 'E022C', '$31.84'),
        row('ASA IV: Incapacitating = 10u', 'E017C', '$159.20'),
        row('ASA V: Moribund = 20u', 'E016C', '$318.40'),
        row('BMI > 40 = 2u', 'E010C', '$31.84'),
        row('Prone position = 4u', 'E011C', '$63.68'),
        row('Semi-sit (>60°) = 4u', 'E024C', '$63.68'),
        row('Age 29d–1yo = 4u', 'E009C', '$63.68'),
        row('Age 1–8yo = 2u', 'E019C', '$31.84'),
        row('Age 70–79 = 1u', 'E007C', '$15.92'),
        row('Age 80+ = 3u', 'E018C', '$47.76'),
        ('SUB', 'Sedation premiums'),
        row('Weekend/Evening (1700–2400)', 'E400C', '50%'),
        row('Night (2400–0800)', 'E401C', '75%'),
    ]),
    ('misc', 'Misc / HEENT / Blocks', '#6366f1', [
        ('SUB', 'Procedure premiums (add to procedure fee)'),
        row('Eve (1700–2400), Wknd, Holiday', 'E412', '+20%'),
        row('Nights (0000–0700)', 'E413', '+40%'),
        ('SUB', 'Misc (HEENT, vertigo, hernia, ECG)'),
        row('Tonometry', 'G435', '$5.10', syn='eye pressure glaucoma'),
        row('Epistaxis packing (per side)', 'Z315', '$15.35', syn='nosebleed nose bleed'),
        row('Epistaxis cautery (per side)', 'Z314', '$11.50', syn='nosebleed nose bleed'),
        row('Epistaxis posterior packing', 'Z316', '$35.50', syn='nosebleed nose bleed'),
        row('Drainage of abscess or haematoma (nasal septum)', 'Z301', '$55.60', syn='septal hematoma nose'),
        row('I&D of extensive pinna haematoma, w/ packing & compression dressing (general anaesthetic)', 'E317', '$139.95', syn='ear hematoma cauliflower ear auricular'),
        row('I&D of extensive pinna haematoma, w/ packing & compression dressing (local)', 'E318', '$92.40', syn='ear hematoma cauliflower ear auricular'),
        row('Ear syringing', 'G420', '$13.15', syn='ear wax cerumen'),
        row('Epley +', 'G403', '$21.70', syn='vertigo dizzy dizziness bppv'),
        row('Hernia/prolapse reduction', 'Z538', '$25.25'),
        row('ECG', 'G313', '$4.55'),
        row('Tetanus by MD', 'G847', '$5.40', syn='tetanus shot immunization'),
        row('Joint/bursa inject-aspirate', 'G370', '$20.25'),
        row('Injection/aspiration bursa or joint, each additional', 'G371', '$19.90'),
        row('IM / SC injection', 'G372', '$4.55'),
        row('IV start, adult', 'G379', '$6.15', badge='gno', syn='iv line intravenous'),
        row('IV start, infant/child', 'G376', '$10.20', badge='gno', syn='iv line intravenous'),
        row('IV cutdown', 'G380', '$27.05', badge='gno', syn='iv access'),
        row('Venipuncture, adult', 'G489', '$3.54', syn='blood draw blood work'),
        row('Venipuncture, child', 'G482', '$7.35', syn='blood draw blood work'),
        row('Venipuncture, infant', 'G480', '$9.90', syn='blood draw blood work'),
        row('Foley catheter insertion', 'Z611', '$9.15', badge='gno', syn='urinary catheter bladder catheter'),
        row('Manual catheter declotting and irrigation of bladder', 'Z608', '$58.65', syn='blocked catheter clogged foley'),
        row('Arterial line', 'G268', '$31.25', badge='gno', syn='a-line line access'),
        row('Central line', 'G269', '$31.25', badge='gno', syn='cvc line access'),
        row('Aspiration of bursa / complex joint ± injection', 'G328', '$39.80'),
        row('Lateral canthotomy', 'E234', '$51.45', syn='eye orbital pressure eye emergency'),
        row('Nasolacrimal irrigation (per eye)', 'Z901', '$27.00', hidden=True, syn='tear duct blocked tear duct'),
        row('Major eye examination', 'A115', '$53.60', hidden=True),
        row('Eye X-ray for foreign body', 'X016', '$9.90', hidden=True),
        row('Ear canal biopsy', 'Z909', '$25.85', hidden=True),
        row('FB larynx / indirect laryngoscopy', 'Z324', '$44.70', syn='airway throat'),
        row('Laryngoscopy, direct, with FB removal', 'Z322', '$106.45', syn='airway throat'),
        row('Transvascular (transvenous) pacemaker', 'Z443', '$154.10', syn='pacing pacer transvenous'),
        row('I&D hemorrhoid', 'Z545', '$25.25', syn='rectal bleeding piles'),
        row('Keloid injection (extensive)', 'G396', '$24.90', hidden=True, syn='scar'),
        ('SUB', 'Ultrasound'),
        row('US-guided aspiration / I&D', 'J149', '$56.45', info="Covers real-time ultrasound guidance for a bedside aspiration, drainage, or biopsy you perform yourself — e.g. an abscess I&D or joint aspiration under direct US visualization. Bill the professional component ($56.45) when using hospital equipment; don't bill this separately for routine diagnostic or procedural POCUS (see H100)."),
        row('POCUS', 'H100', '$19.65'),
        ('SUB', 'Nerve blocks lasting > 4h'),
        row('Peripheral nerve, major', 'G060', '$55.00'),
        row('Peripheral nerve, minor', 'G061', '$30.00'),
        row('Local nerve block for procedure', 'G224', '$15.55'),
        row('Trigger point (single / 1st)', 'G384', '$8.85', syn='muscle knot myofascial'),
        row("Trigger point ea add'l (max 2)", 'G385', '$4.55', syn='muscle knot myofascial'),
        row('Major plexus (>=2 periph)', 'G260', '$80.00'),
        row('Supraorbital', 'G235', '$34.10', syn='forehead block'),
        row('Inferior alveolar (max/mand)', 'G250', '$75.10', syn='dental block tooth block jaw block'),
        row('Infraorbital', 'G219', '$34.20', syn='face block'),
        row('Mental branch', 'G225', '$34.20', syn='chin block'),
        row('Spheno-palatine ganglion', 'G921', '$12.50'),
        row('Femoral unilateral', 'G243', '$54.65'),
        row('Ilioinguinal / iliohypogastric nerve block', 'G218', '$54.65'),
        row('Intercostal nerve block', 'G220', '$34.20'),
        row('Intercostal nerve block, each additional', 'G221', '$16.95'),
        row('Other cranial nerve block', 'G227', '$54.65'),
        row('Intrapleural block (single)', 'G258', '$44.25', hidden=True),
        row('Intrapleural block w/ catheter', 'G067', '$80.00', hidden=True),
        row('Outpatient continuous nerve block infusion', 'G063', '$29.20', hidden=True),
    ]),
    ('gugiob', 'GU / GI / OB', '#0d9488', [
        ('SUB', 'Genitourinary'),
        row('Priapism — aspiration/irrigation + injection', 'Z786', '$250.00', syn='erection penis'),
        row('Priapism — adult or child', 'S569', '$65.30', hidden=True, syn='erection penis'),
        row('Hydrocele aspiration', 'Z708', '$21.20', syn='scrotum testicle swelling'),
        row('Incision and drainage of cyst, abscess or haematoma (vaginal)', 'Z728', '$97.20', syn='vaginal abscess bartholin'),
        row('Repair of laceration (vaginal)', 'P036', '$54.40', syn='perineal tear postpartum laceration'),
        ('SUB', 'Gastrointestinal / rectal'),
        row('Anoscopy / proctoscopy', 'Z543', '$8.70', syn='rectal bleeding hemorrhoids'),
        ('SUB', 'Obstetric / gynecologic'),
        row('ED pelvic exam with speculum', 'H264', '$12.00', syn='gyne vaginal exam speculum'),
        row('Vaginal delivery', 'P006', '$512.65', info='For a vaginal delivery performed by you \u2014 e.g. a precipitous ED delivery. Includes repair of a first- or second-degree tear or episiotomy extension, if performed.'),
        row('Caesarean section', 'P018', '$579.80', info='For a Caesarean section performed by you \u2014 an extremely rare ED scenario (e.g. a perimortem C-section during maternal cardiac arrest). Confirm eligibility criteria with your billing office before submitting.'),
        row('Non-OBGYN attending delivery/C-section, resus newborn', 'P009', '$512.65'),
        row('Intracavitary US (transvaginal/rectal)', 'J138', '$48.75', hidden=True),
    ]),
    ('fx', 'Fractures', '#f59e0b', [
        ('SUB', 'No reduction'),
        row('Phalanx', 'F004', '$49.20', syn='finger toe digit', fxbadge="no"),
        row('Metacarpal', 'F008', '$49.20', syn='hand finger knuckle wrist', fxbadge="no"),
        row('Intra-articular', 'F006', '$119.75', fxbadge="no"),
        row('Carpus', 'F102', '$49.20', syn='wrist', fxbadge="no"),
        row('Scaphoid', 'F018', '$49.20', fxbadge="no"),
        row("Radius distal (Colles', Smith)", 'F027', '$67.75', syn='wrist distal radius wrist distal radius wrist', fxbadge="no"),
        row('Radius & ulnar shaft', 'F024', '$67.75', fxbadge="no"),
        row('Radius & ulna – Monteggia', 'F014', '$67.75', syn='forearm', fxbadge="no"),
        row('Radius or ulna', 'F031', '$81.30', fxbadge="no"),
        row('Epicondyle', 'F029', '$67.75', syn='elbow tennis elbow golfers elbow', fxbadge="no"),
        row('Transcondylar / condylar', 'F039', '$67.75', syn='elbow elbow', fxbadge="no"),
        row('Olecranon', 'F034', '$126.25', syn='elbow', fxbadge="no"),
        row('Humerus tuberosity', 'F047', '$67.80', syn='arm upper arm', fxbadge="no"),
        row('Humerus neck w/o head disl', 'F053', '$67.80', syn='arm upper arm', fxbadge="no"),
        row('Humeral neck w head disl', 'F050', '$67.80', syn='arm upper arm', fxbadge="no"),
        row('Humeral shaft', 'F042', '$67.80', syn='arm upper arm', fxbadge="no"),
        row('Scapula', 'F119', '$67.80', syn='shoulder blade', fxbadge="no"),
        row('Patella', 'F085', '$67.75', syn='kneecap knee', fxbadge="no"),
        row('Tibia +/- fibula', 'F078', '$115.95', syn='leg shin lower leg leg lower leg', fxbadge="no"),
        row('Fibula', 'F082', '$67.75', syn='leg lower leg', fxbadge="no"),
        row('Ankle', 'F074', '$67.75', syn='ankle sprain', fxbadge="no"),
        row('Metatarsus', 'F062', '$67.75', syn='foot toe forefoot foot ankle hindfoot', fxbadge="no"),
        row('Toe', 'F056', '$49.20', fxbadge="no"),
        row('Tarsus excluding os calcis', 'F066', '$98.10', syn='foot ankle hindfoot heel calcaneus', fxbadge="no"),
        ('SUB', 'Closed reduction'),
        row('Phalanx', 'F005', '$99.25', syn='finger toe digit', fxbadge="closed"),
        row('Metacarpal', 'F009', '$99.25', syn='hand finger knuckle wrist', fxbadge="closed"),
        row('Intra-articular', 'F006', '$119.75', fxbadge="closed"),
        row('Carpus', 'F016', '$115.10', syn='wrist', fxbadge="closed"),
        row('Radius distal (hematoma block)', 'F028', '$109.45', syn='wrist', fxbadge="closed"),
        row('Radius distal (under sedation)', 'F046', '$149.35', syn='wrist', fxbadge="closed"),
        row('Epicondyle', 'F037', '$126.25', syn='elbow tennis elbow golfers elbow', fxbadge="closed"),
        row('Transcondylar / condylar', 'F040', '$298.35', syn='elbow elbow', fxbadge="closed"),
        row('Olecranon', 'F035', '$129.00', syn='elbow', fxbadge="closed"),
        row('Radius & ulnar shaft', 'F025', '$148.50', fxbadge="closed"),
        row('Radius & ulna – Monteggia', 'F022', '$144.80', syn='forearm', fxbadge="closed"),
        row('Radius or ulna', 'F032', '$117.85', fxbadge="closed"),
        row('Humerus tuberosity', 'F048', '$117.85', syn='arm upper arm', fxbadge="closed"),
        row('Humerus neck w/o head disl', 'F054', '$133.60', syn='arm upper arm', fxbadge="closed"),
        row('Humeral neck w head disl', 'F051', '$183.80', syn='arm upper arm', fxbadge="closed"),
        row('Humeral shaft', 'F043', '$147.60', syn='arm upper arm', fxbadge="closed"),
        row('Clavicle', 'F110', '$62.20', syn='collarbone', fxbadge="closed"),
        row('Sternum', 'F123', '$115.95', syn='chest breastbone', fxbadge="closed"),
        row('Femur child', 'F094', '$258.00', syn='thigh upper leg', fxbadge="closed"),
        row('Femur adult', 'F095', '$407.35', syn='thigh upper leg', fxbadge="closed"),
        row('Tibia with or without fibula', 'F079', '$180.05', syn='leg shin lower leg leg lower leg', fxbadge="closed"),
        row('Fibula', 'F083', '$101.25', syn='leg lower leg', fxbadge="closed"),
        row('Ankle', 'F075', '$144.80', syn='ankle sprain', fxbadge="closed"),
        row('Ankle w tibial plafond burst', 'F104', '$363.40', syn='leg shin lower leg ankle sprain', fxbadge="closed"),
        row('Toe', 'F058', '$72.35', fxbadge="closed"),
        row('Tarsus excluding os calcis', 'F067', '$165.20', syn='foot ankle hindfoot heel calcaneus', fxbadge="closed"),
        row('Intra-articular fracture – IP joint', 'F057', '$77.95', fxbadge="closed"),
        row('Metatarsus, no reduction', 'F061', '$49.20', syn='foot toe forefoot foot ankle hindfoot', fxbadge="closed"),
        row('Calcaneus, no reduction', 'F070', '$97.35', syn='heel', fxbadge="closed"),
        row('Phalanx (hand), open fracture', 'F007', '$346.50', syn='finger toe digit', fxbadge="closed"),
        row('Phalanx (hand) fracture, each additional', 'E558', '$22.25', syn='finger toe digit', fxbadge="closed"),
        row('Phalanx (foot) fracture, each additional', 'E560', '$12.05', syn='finger toe digit', fxbadge="closed"),
        row('Metacarpal fracture, each additional', 'E577', '$10.25', syn='hand finger knuckle wrist', fxbadge="closed"),
        row('Toe fracture, each additional', 'E578', '$10.25', fxbadge="closed"),
        row('Nasal bone – closed reduction', 'F136', '$102.35', syn='nose broken nose', fxbadge="closed"),
        row('Nasal bone – open reduction', 'F137', '$316.35', hidden=True, syn='nose broken nose', fxbadge="closed"),
    ]),
    ('disloc', 'Dislocations', '#d946ef', [
        row('Finger', 'D001', '$57.50'),
        row('Metacarpal / phalangeal', 'D004', '$57.50', syn='finger toe digit hand finger knuckle wrist'),
        row('Carpal', 'D007', '$128.05', syn='wrist'),
        row('Elbow joint', 'D009', '$84.45', syn='elbow dislocation'),
        row('Radial head (pulled elbow)', 'D012', '$39.00', syn='nursemaid pulled elbow toddler'),
        row('AC / SCJ (no sedation)', 'D014', '$67.80', syn='shoulder collarbone acromioclavicular sternoclavicular'),
        row('AC / SCJ (w sedation), 6u', 'D025', '$134.55', syn='shoulder collarbone acromioclavicular sternoclavicular'),
        row('Glenohumeral (no sedation)', 'D015', '$49.20', syn='shoulder arm upper arm'),
        row('Glenohumeral (w sedation), 6u', 'D016', '$111.40', syn='shoulder arm upper arm'),
        row('Temporomandibular joint', 'D062', '$51.65', syn='jaw tmj'),
        row('Hip', 'D042', '$268.25', syn='femoral head groin'),
        row('Knee', 'D038', '$207.90', syn='knee dislocation'),
        row('Patella (no sedation)', 'D040', '$62.20', syn='kneecap knee'),
        row('Patella (w sedation)', 'D031', '$97.35', syn='kneecap knee'),
        row('Ankle', 'D035', '$111.35', syn='ankle sprain'),
        row('Interphalangeal', 'D027', '$57.50', syn='finger toe digit finger toe digit ip joint'),
        row('Metatarsophalangeal / tarsus', 'D030', '$57.50', syn='finger toe digit foot toe mtp foot ankle hindfoot'),
        row('Tarso-metatarsal', 'D026', '$147.60', syn='foot lisfranc'),
        row('Tarsus', 'D033', '$147.60', syn='foot ankle hindfoot'),
    ]),
    ('burns', 'Burns & Casts', '#fb923c', [
        ('SUB', 'Burn debridement'),
        row('Hand (ea side)', 'R660', '$31.65'),
        row('Each finger', 'R661', '$52.55'),
        row('Face (ea)', 'R662', '$31.65'),
        row('Other', 'R637', '$32.50'),
        ('SUB', 'Casts / splints (no fracture)'),
        row('Arm / forearm / wrist', 'Z203', '$24.10'),
        row('Below knee', 'Z213', '$24.10', syn='knee dislocation'),
        row('Full leg', 'Z211', '$28.20'),
        row('Hand', 'Z202', '$14.90'),
        row('Cast removal (>2wk)', 'Z204', '$10.25'),
        row('Toe cast/splint', 'Z198', '$10.25'),
        row('Foot cast/splint', 'Z199', '$14.90'),
        row('Finger cast/splint', 'Z201', '$10.25'),
        row('Shoulder spica cast', 'Z208', '$97.35'),
        row('Wedging of cast (non-fracture)', 'Z216', '$10.25'),
    ]),
]


# ---------- STATIC TEMPLATE PIECES (verified against the live app; edit with care) ----------
CSS = '\n  :root {\n    --bg:#f4f6f8; --card:#ffffff; --card2:#f7fafc;\n    --ink:#15202b; --ink2:#33404c; --muted:#6b7885;\n    --border:#e3e9ef; --border2:#d5dde4; --rowline:#eef1f4;\n    --staroff:#c7ced6; --fav:#f5a524;\n    --pos:#0b7a4b; --posbg:#d9f7e6;\n    --neg:#c00000; --neg2:#b42318; --negbg:#fdecea; --negborder:#f6c9c4;\n    --accent:#153d64; --accent-ink:#ffffff;\n    --shadow:rgba(0,0,0,.12);\n    --iss-accent:#e97132; --iss-tint:#faf5f2; --iss-border:#f2c9b3;\n    --code-color:inherit;\n  }\n  [data-theme="navy"] {\n    --bg:#0a1522; --card:#122238; --card2:#0f1d30;\n    --ink:#dce6f0; --ink2:#b7c9db; --muted:#7d94ac;\n    --border:#1f3652; --border2:#28496b; --rowline:#1c344f;\n    --staroff:#3f5a78; --fav:#f5a524;\n    --pos:#4fd3a0; --posbg:#123a2c;\n    --neg:#ff8577; --neg2:#ff9c8f; --negbg:#3a1712; --negborder:#5c261c;\n    --accent:#2f6da0; --accent-ink:#ffffff;\n    --shadow:rgba(0,0,0,.45);\n    --iss-accent:#e97132; --iss-tint:#241a12; --iss-border:#4a2f1c;\n    --code-color:#6ec3ff;\n  }\n  [data-theme="oled"] {\n    --bg:#000000; --card:#141210; --card2:#100e0c;\n    --ink:#eae3d6; --ink2:#c9beac; --muted:#8a8072;\n    --border:#2a251f; --border2:#332c24; --rowline:#221d18;\n    --staroff:#4a423a; --fav:#f5a524;\n    --pos:#8fb87a; --posbg:#1c2617;\n    --neg:#e08a7d; --neg2:#e29a8e; --negbg:#2c1712; --negborder:#452720;\n    --accent:#7a5230; --accent-ink:#f0e6d8;\n    --shadow:rgba(0,0,0,.6);\n    --iss-accent:#c2823f; --iss-tint:#1c1611; --iss-border:#3a2c1c;\n    --code-color:#e0a05a;\n  }\n\n  * { box-sizing:border-box; -webkit-tap-highlight-color:transparent; }\n  html { scroll-behavior:smooth; }\n  body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,\n         "Liberation Sans",Arial,sans-serif; background:var(--bg); color:var(--ink);\n         font-size:16px; line-height:1.3; transition:background .15s,color .15s; }\n  .wrap { max-width:760px; margin:0 auto; padding:0 12px 60px; }\n\n  header { position:sticky; top:0; z-index:20; background:var(--bg);\n           padding:12px 12px 8px; margin:0 -12px; }\n  h1 { font-size:18px; margin:0; }\n  .titlerow { display:flex; align-items:center; justify-content:space-between; gap:8px;\n              flex-wrap:wrap; margin:0 0 8px; }\n\n  .theme-toggle { display:flex; gap:4px; background:var(--card2); border:1px solid var(--border);\n                  border-radius:8px; padding:3px; }\n  .theme-btn { border:none; background:none; padding:5px 7px; font-size:11px; font-weight:700;\n               border-radius:6px; cursor:pointer; color:var(--muted); line-height:1; white-space:nowrap; }\n  .theme-btn.on { background:var(--accent); color:var(--accent-ink); }\n\n  .search { width:100%; padding:11px 14px; font-size:16px; border:1.5px solid var(--border2);\n            border-radius:10px; background:var(--card); color:var(--ink); outline:none; }\n  .search:focus { border-color:#0ea5e9; box-shadow:0 0 0 3px #0ea5e922; }\n\n  .nav { display:grid; grid-template-columns:repeat(3,1fr); gap:5px; margin:10px 0 4px; }\n  @media(min-width:560px) { .nav { grid-template-columns:repeat(4,1fr); } }\n  .navchip { display:flex; align-items:center; gap:5px; text-decoration:none;\n             color:var(--ink); background:var(--card); border:1px solid var(--border);\n             border-left:4px solid var(--c); border-radius:7px; padding:6px 7px;\n             font-size:11px; font-weight:600; line-height:1.15; }\n  .navchip:active { background:var(--card2); }\n  .navchip-fav { font-weight:700; }\n  .navchip-upd { font-weight:700; }\n  .navdot { width:7px; height:7px; border-radius:50%; background:var(--c); flex:none; }\n\n  section { margin-top:16px; scroll-margin-top:var(--hoff, 230px); }\n  .secban { display:flex; align-items:center; gap:9px; font-size:15px; font-weight:800;\n            background:var(--card2);\n            background:color-mix(in srgb, var(--c) 14%, var(--card));\n            border:1px solid var(--border);\n            border:1px solid color-mix(in srgb, var(--c) 30%, var(--card));\n            border-left:6px solid var(--c);\n            padding:9px 12px; border-radius:9px; color:var(--ink); }\n  .bandot { width:11px; height:11px; border-radius:50%; background:var(--c); flex:none; }\n  .top { margin-left:auto; font-size:11px; font-weight:600; color:var(--muted); text-decoration:none; }\n  .rows { margin-top:4px; }\n\n  .sub { font-size:11px; font-weight:700; letter-spacing:.4px; text-transform:uppercase;\n         color:var(--muted); padding:9px 6px 3px; }\n  .note { font-size:11.5px; font-style:italic; color:var(--neg); padding:5px 6px; }\n\n  .row { display:flex; align-items:center; gap:9px; background:var(--card);\n         border-bottom:1px solid var(--rowline); border-left:6px solid var(--c);\n         padding:10px 12px 10px 8px; }\n  .code { font-size:16px; font-weight:800; min-width:56px; letter-spacing:.3px; color:var(--code-color); }\n  .desc { flex:1; font-size:13.5px; color:var(--ink2); }\n  .price { font-size:15px; font-weight:800; color:var(--pos); white-space:nowrap; }\n  .new { display:inline-block; font-size:9px; font-weight:800; color:var(--pos);\n         background:var(--posbg); border-radius:4px; padding:1px 5px; margin-left:6px;\n         vertical-align:middle; letter-spacing:.3px; }\n  .gbadge { display:inline-block; font-size:9px; font-weight:800; border-radius:4px;\n            padding:1px 6px; margin-left:6px; vertical-align:middle; letter-spacing:.3px; }\n  .gbadge.g35 { color:#0a5a8a; background:#dceefc; }\n  [data-theme="navy"] .gbadge.g35, [data-theme="oled"] .gbadge.g35 { color:#8fd0ff; background:#0f2e46; }\n  .gbadge.gno { color:var(--neg2); background:var(--negbg); }\n  .gbadge.g3only { color:#8a5a00; background:#fdf0d5; }\n  [data-theme="navy"] .gbadge.g3only, [data-theme="oled"] .gbadge.g3only { color:#f0c060; background:#3a2c0f; }\n  .gbadge.fxno { color:#4b5563; background:#e5e7eb; }\n  [data-theme="navy"] .gbadge.fxno, [data-theme="oled"] .gbadge.fxno { color:#c4cad3; background:#2a333f; }\n  .gbadge.fxclosed { color:#6d28d9; background:#ede9fe; }\n  [data-theme="navy"] .gbadge.fxclosed, [data-theme="oled"] .gbadge.fxclosed { color:#c4b5fd; background:#2f2350; }\n\n  /* ---- Info (i) buttons + collapsible panels ---- */\n  .row.has-info { border-bottom:none; border-radius:0; }\n  .info-btn { border:1.5px solid var(--border2); background:var(--card); color:var(--muted);\n              width:19px; height:19px; border-radius:50%; font-size:11px; font-weight:800;\n              cursor:pointer; flex:none; display:inline-flex; align-items:center;\n              justify-content:center; padding:0; line-height:1; font-style:italic;\n              font-family:Georgia,"Times New Roman",serif; }\n  .info-btn.open { background:var(--c); border-color:var(--c); color:#fff; }\n  .info-panel { display:none; font-size:12px; color:var(--ink2); background:var(--card2);\n                border:1px solid var(--border); border-top:none; border-left:6px solid var(--c);\n                border-radius:0 0 8px 8px; padding:9px 12px 11px; margin:0 0 4px;\n                line-height:1.55; }\n  .info-panel.open { display:block; }\n  .info-panel.hidden { display:none !important; }\n  .sec-info { font-size:11.5px; color:var(--ink2); background:var(--card2); border:1px solid var(--border);\n              border-radius:7px; padding:8px 10px; margin:6px 0; line-height:1.5; }\n\n  .star { border:none; background:none; font-size:20px; line-height:1; cursor:pointer;\n          color:var(--staroff); padding:0 2px; flex:none; width:26px; }\n  .star.on { color:var(--fav); }\n\n  /* search-only rows: hidden by default, shown when filtering or when favourited-clone */\n  .srch { display:none; }\n  body.searching .srch { display:flex; }\n\n  .hidden { display:none !important; }\n  .noresult { text-align:center; color:var(--muted); padding:30px 10px; font-size:14px; }\n  .fav-empty { font-size:13px; color:var(--muted); font-style:italic; padding:12px 8px; }\n\n  /* ---- Sedation calculator ---- */\n  .calc { background:var(--card); border:1px solid var(--border); border-left:6px solid #f43f5e;\n          border-radius:9px; padding:12px 12px 14px; margin-top:4px; }\n  .calc-h { font-size:14px; font-weight:800; margin-bottom:10px; }\n  .calc-row { display:block; margin:10px 0; }\n  .calc-lbl { display:block; font-size:11px; font-weight:700; text-transform:uppercase;\n              letter-spacing:.3px; color:var(--muted); margin-bottom:5px; }\n  .calc-in { width:100%; padding:9px 11px; font-size:16px; border:1.5px solid var(--border2);\n             border-radius:8px; outline:none; background:var(--card); color:var(--ink); }\n  .calc-in:focus { border-color:#f43f5e; box-shadow:0 0 0 3px #f43f5e22; }\n  .ac-wrap { position:relative; }\n  .ac-list { position:absolute; left:0; right:0; top:calc(100% + 4px); z-index:30;\n             background:var(--card); border:1px solid var(--border2); border-radius:8px; overflow:hidden;\n             box-shadow:0 6px 18px var(--shadow); display:none; max-height:230px; overflow-y:auto; }\n  .ac-list.on { display:block; }\n  .ac-item { display:flex; align-items:center; gap:9px; padding:9px 11px; cursor:pointer;\n             border-bottom:1px solid var(--rowline); }\n  .ac-item:last-child { border-bottom:none; }\n  .ac-item.active, .ac-item:active { background:#f43f5e14; }\n  .ac-item .acc { font-weight:800; min-width:52px; color:#f43f5e; }\n  .ac-item .acd { font-size:13px; color:var(--ink2); }\n  .ac-none { padding:9px 11px; color:var(--muted); font-size:13px; }\n  #c-proc-picked.set { color:var(--pos); font-weight:600; }\n  .calc-hint { font-size:11px; color:var(--muted); margin:-4px 0 8px; }\n  .seg, .chips { display:flex; flex-wrap:wrap; gap:6px; }\n  .seg button, .chips button { font-size:13px; font-weight:600; padding:8px 11px;\n             border:1.5px solid var(--border2); background:var(--card); color:var(--ink2); border-radius:8px;\n             cursor:pointer; }\n  .seg button.on { background:#f43f5e; border-color:#f43f5e; color:#fff; }\n  .chips button.on { background:var(--pos); border-color:var(--pos); color:#fff; }\n  .calc-out { margin-top:12px; background:var(--card2); border:1px solid var(--border);\n              border-radius:8px; padding:11px 12px; font-size:14px; min-height:44px; }\n  .calc-out .line { display:flex; justify-content:space-between; gap:10px; padding:3px 0;\n                    border-bottom:1px solid var(--rowline); }\n  .calc-out .line:last-child { border-bottom:none; }\n  .calc-out .cc { font-weight:800; }\n  .calc-out .cu { color:var(--muted); font-size:12px; }\n  .calc-out .tot { font-weight:800; margin-top:6px; }\n  .calc-out .warn { color:var(--neg2); font-size:12px; margin-top:6px; }\n  .calc-copy { margin-top:10px; width:100%; padding:10px; font-size:14px; font-weight:700;\n               border:none; border-radius:8px; background:var(--accent); color:var(--accent-ink); cursor:pointer; }\n  .calc-copy.done { background:var(--pos); color:#fff; }\n  #updbar { position:fixed; left:0; right:0; bottom:0; z-index:50; background:var(--accent);\n            color:var(--accent-ink); font-size:13px; text-align:center; padding:10px 12px; }\n  #updbar button { margin-left:8px; font-size:13px; font-weight:700; padding:6px 12px;\n            border:none; border-radius:7px; background:var(--fav); color:#15202b; cursor:pointer; }\n  #forcerefresh { display:inline-flex; align-items:center; gap:6px; font-size:14px;\n            font-weight:700; color:var(--accent); background:var(--card); border:1.5px solid var(--accent);\n            border-radius:9px; padding:10px 18px; cursor:pointer; margin:4px auto 10px;\n            box-shadow:0 1px 2px var(--shadow); }\n  #forcerefresh:active { background:var(--accent); color:var(--accent-ink); }\n  #forcerefresh.done { background:var(--pos); border-color:var(--pos); color:#fff; }\n  #forcerefresh.checking { opacity:.7; }\n  /* ---- Expandable row + ISS calculator ---- */\n  .row-expand { cursor:pointer; }\n  .exp-hint { display:inline-block; margin-left:8px; font-size:10px; font-weight:700;\n              color:var(--iss-accent); background:var(--iss-tint); border-radius:4px; padding:1px 6px;\n              vertical-align:middle; }\n  .row-expand.open .exp-hint { background:var(--iss-accent); color:#fff; }\n  .expand-panel { display:none; }\n  .expand-panel.open { display:block; }\n  .iss { background:var(--card); border:1px solid var(--iss-border); border-left:6px solid var(--iss-accent);\n         border-radius:0 0 9px 9px; padding:12px; margin:0 0 4px; }\n  .iss-reminder { font-size:11px; color:var(--ink2); background:var(--iss-tint); border-radius:7px;\n                  padding:7px 9px; margin-bottom:11px; line-height:1.5; }\n  .iss-grid { display:flex; flex-direction:column; gap:10px; }\n  .iss-reg { display:flex; flex-direction:column; gap:5px; }\n  .iss-name { font-size:13px; font-weight:700; }\n  .iss-sub { font-weight:400; color:var(--muted); font-size:11px; }\n  .iss-seg { display:flex; gap:5px; flex-wrap:wrap; }\n  .iss-seg button { flex:1; min-width:36px; font-size:14px; font-weight:700; padding:8px 0;\n             border:1.5px solid var(--border2); background:var(--card); color:var(--ink2); border-radius:8px;\n             cursor:pointer; }\n  .iss-seg button.on { background:var(--iss-accent); border-color:var(--iss-accent); color:#fff; }\n  .iss-seg button.on.sev6 { background:var(--neg2); border-color:var(--neg2); }\n  .iss-out { margin-top:13px; background:var(--card2); border:1px solid var(--border); border-radius:9px;\n             padding:12px; text-align:center; }\n  .iss-score { display:flex; align-items:baseline; justify-content:center; gap:10px; }\n  .iss-val { font-size:34px; font-weight:800; line-height:1; }\n  .iss-lbl { font-size:13px; font-weight:700; }\n  .iss-out.major { background:var(--negbg); border-color:var(--negborder); }\n  .iss-out.major .iss-val { color:var(--neg2); }\n  .iss-out.minor .iss-val { color:var(--pos); }\n  .iss-detail { font-size:11.5px; color:var(--muted); margin-top:7px; line-height:1.5; }\n  .iss-flag { display:inline-block; font-weight:800; font-size:12px; padding:3px 9px;\n              border-radius:6px; margin-top:8px; }\n  .iss-flag.yes { background:var(--neg2); color:#fff; }\n  .iss-flag.no { background:var(--posbg); color:var(--pos); }\n  .iss-reset { margin-top:10px; width:100%; padding:9px; font-size:13px; font-weight:700;\n               border:1.5px solid var(--border2); background:var(--card); color:var(--ink2); border-radius:8px;\n               cursor:pointer; }\n  .iss-note { font-size:10.5px; color:var(--muted); font-style:italic; margin-top:9px; line-height:1.45; }\n  .upd-card { background:var(--card); border:1px solid var(--border); border-left:6px solid #0891b2;\n              border-radius:9px; padding:14px 14px 16px; margin-top:4px; text-align:center; }\n  #forcerefresh { margin:0 auto 10px; }\n  .upd-meta { font-size:12px; color:var(--muted); line-height:1.45; }\n  .footmeta { font-size:10.5px; color:var(--muted); font-style:italic; }\n  footer { margin-top:26px; text-align:center; display:flex; flex-direction:column; align-items:center; }\n'

EARLY_THEME_SCRIPT = "<script>(function(){try{var t=localStorage.getItem('edbill_theme_v1');if(t)document.documentElement.setAttribute('data-theme',t);}catch(e){}})();</script>"

CALC_HTML = '<div class="calc" id="sedcalc">\n  <div class="calc-h">Sedation code builder</div>\n\n  <label class="calc-row">\n    <span class="calc-lbl">Procedure (search by name or code)</span>\n    <div class="ac-wrap">\n      <input id="c-proc" class="calc-in" type="text" inputmode="text"\n             placeholder="e.g. shoulder, F046, ankle…" autocomplete="off">\n      <div id="c-proc-list" class="ac-list"></div>\n    </div>\n  </label>\n  <div class="calc-hint" id="c-proc-picked">Search the base procedure you\'re sedating for — its code becomes the "C" code.</div>\n\n  <label class="calc-row">\n    <span class="calc-lbl">Total sedation time (minutes)</span>\n    <input id="c-time" class="calc-in" type="number" inputmode="numeric" min="0" step="1" placeholder="e.g. 40">\n  </label>\n\n  <div class="calc-row">\n    <span class="calc-lbl">ASA class</span>\n    <div class="seg" id="c-asa">\n      <button type="button" data-v="1" class="on">I–II</button>\n      <button type="button" data-v="3">III</button>\n      <button type="button" data-v="4">IV</button>\n      <button type="button" data-v="5">V</button>\n    </div>\n  </div>\n\n  <div class="calc-row">\n    <span class="calc-lbl">Age band</span>\n    <div class="seg" id="c-age">\n      <button type="button" data-v="adult" class="on">Adult &lt;70</button>\n      <button type="button" data-v="29d1">29d–1y</button>\n      <button type="button" data-v="1to8">1–8y</button>\n      <button type="button" data-v="70">70–79</button>\n      <button type="button" data-v="80">80+</button>\n    </div>\n  </div>\n\n  <div class="calc-row">\n    <span class="calc-lbl">Modifiers</span>\n    <div class="chips" id="c-mods">\n      <button type="button" data-v="E020C">ASA-E emergency</button>\n      <button type="button" data-v="E010C">BMI &gt; 40</button>\n      <button type="button" data-v="E011C">Prone</button>\n      <button type="button" data-v="E024C">Sitting &gt;60&deg;</button>\n    </div>\n  </div>\n\n  <div class="calc-row">\n    <span class="calc-lbl">Time premium</span>\n    <div class="seg" id="c-prem">\n      <button type="button" data-v="" class="on">None</button>\n      <button type="button" data-v="E400C">Eve/Wknd</button>\n      <button type="button" data-v="E401C">Night</button>\n    </div>\n  </div>\n\n  <div class="calc-out" id="c-out"></div>\n  <button type="button" class="calc-copy" id="c-copy">Copy codes</button>\n</div>'

ISS_HTML = '<div class="iss" id="isscalc">\n  <div class="iss-reminder">AIS per region: <b>1</b> minor · <b>2</b> moderate · <b>3</b> serious · <b>4</b> severe · <b>5</b> critical · <b>6</b> unsurvivable (auto ISS 75)</div>\n  <div class="iss-grid">\n    <div class="iss-reg" data-reg="head"><span class="iss-name">Head / Neck</span><div class="iss-seg" data-reg="head"></div></div>\n    <div class="iss-reg" data-reg="face"><span class="iss-name">Face</span><div class="iss-seg" data-reg="face"></div></div>\n    <div class="iss-reg" data-reg="chest"><span class="iss-name">Chest</span><div class="iss-seg" data-reg="chest"></div></div>\n    <div class="iss-reg" data-reg="abdo"><span class="iss-name">Abdomen</span><div class="iss-seg" data-reg="abdo"></div></div>\n    <div class="iss-reg" data-reg="extr"><span class="iss-name">Extremities <span class="iss-sub">(incl. pelvis)</span></span><div class="iss-seg" data-reg="extr"></div></div>\n    <div class="iss-reg" data-reg="ext"><span class="iss-name">External</span><div class="iss-seg" data-reg="ext"></div></div>\n  </div>\n  <div class="iss-out" id="iss-out">\n    <div class="iss-score"><span class="iss-val" id="iss-val">0</span><span class="iss-lbl" id="iss-lbl">Select AIS scores above</span></div>\n    <div class="iss-detail" id="iss-detail"></div>\n  </div>\n  <button type="button" class="iss-reset" id="iss-reset">Reset</button>\n  <div class="iss-note">You supply the AIS score per region (your clinical judgment). This tool squares the top three and flags major trauma. Not a substitute for the AIS dictionary.</div>\n</div>'

HEADER_SHELL = '<body>\n<a id="top"></a>\n<div class="wrap">\n  <header>\n    <div class="titlerow"><h1>ED Billing Guide</h1><span class="theme-toggle" id="themeToggle"><button type="button" class="theme-btn" data-theme-val="light">Light</button><button type="button" class="theme-btn" data-theme-val="navy">Navy</button><button type="button" class="theme-btn" data-theme-val="oled">OLED</button></span></div>\n    <input class="search" id="q" type="text" inputmode="search"\n           placeholder="Search code or description…" autocomplete="off">\n    <nav class="nav" id="nav">__NAV__</nav>\n  </header>\n  '

FOOTER_ONLY = '<div class="noresult hidden" id="noresult">No matches.</div>\n  <footer>\n    <div class="footmeta">Ontario SOB Amendment 50 · verify against your latest schedule before billing · <span id="verstamp">v__VERSION__</span></div>\n  </footer>\n</div>\n'

MAIN_JS = '\n(function () {\n  var STORE_KEY = \'edbill_favs_v1\';\n\n  function loadFavs() {\n    try {\n      var raw = window.localStorage.getItem(STORE_KEY);\n      if (raw) return JSON.parse(raw);\n    } catch (e) {}\n    return [];\n  }\n  function saveFavs(list) {\n    try { window.localStorage.setItem(STORE_KEY, JSON.stringify(list)); } catch (e) {}\n  }\n\n  function init() {\n    // ---------- Theme toggle ----------\n    (function initTheme() {\n      var KEY = \'edbill_theme_v1\';\n      var toggle = document.getElementById(\'themeToggle\');\n      if (!toggle) return;\n      var btns = Array.prototype.slice.call(toggle.querySelectorAll(\'.theme-btn\'));\n      function current() {\n        return document.documentElement.getAttribute(\'data-theme\') || \'light\';\n      }\n      function applyActive() {\n        var cur = current();\n        btns.forEach(function (b) {\n          b.classList.toggle(\'on\', b.getAttribute(\'data-theme-val\') === cur);\n        });\n      }\n      function setTheme(val) {\n        if (val === \'light\') document.documentElement.removeAttribute(\'data-theme\');\n        else document.documentElement.setAttribute(\'data-theme\', val);\n        try { localStorage.setItem(KEY, val); } catch (e) {}\n        applyActive();\n      }\n      btns.forEach(function (b) {\n        b.addEventListener(\'click\', function () { setTheme(b.getAttribute(\'data-theme-val\')); });\n      });\n      applyActive();\n    })();\n\n    var q = document.getElementById(\'q\');\n    var sections = Array.prototype.slice.call(document.querySelectorAll(\'#content > section\'));\n    var headerEl = document.querySelector(\'header\');\n    function setHeaderOffset() {\n      if (!headerEl) return;\n      var h = headerEl.getBoundingClientRect().height;\n      document.documentElement.style.setProperty(\'--hoff\', (h + 10) + \'px\');\n    }\n    setHeaderOffset();\n    window.addEventListener(\'resize\', setHeaderOffset);\n    window.addEventListener(\'orientationchange\', setHeaderOffset);\n    // Recompute after tapping a section link (nav can change height when it hides during search)\n    document.querySelectorAll(\'.navchip\').forEach(function(a){\n      a.addEventListener(\'click\', function(){ setTimeout(setHeaderOffset, 0); });\n    });\n    var contentSections = sections.filter(function (s) { return s.id !== \'favourites\'; });\n    var nav = document.getElementById(\'nav\');\n    var noresult = document.getElementById(\'noresult\');\n    var favRows = document.getElementById(\'fav-rows\');\n    var favEmpty = document.getElementById(\'fav-empty\');\n\n    var favs = loadFavs();\n\n    // Build a map code -> source row element (first match in content sections)\n    function sourceRowFor(code) {\n      return document.querySelector(\'#content > section:not(#favourites) .row[data-fk="\' + code + \'"]\');\n    }\n\n    function renderFavs() {\n      // clear existing clones (rows and any info-panels)\n      Array.prototype.slice.call(favRows.querySelectorAll(\'.row, .info-panel\')).forEach(function (r) { r.remove(); });\n      if (!favs.length) { favEmpty.style.display = \'\'; }\n      else { favEmpty.style.display = \'none\'; }\n      favs.forEach(function (code) {\n        var src = sourceRowFor(code);\n        if (!src) return;\n        var clone = src.cloneNode(true);\n        clone.classList.remove(\'srch\'); // always visible in favourites\n        clone.classList.remove(\'hidden\');\n        // clone\'s star should reflect \'on\' and toggle off when tapped\n        var st = clone.querySelector(\'.star\');\n        if (st) { st.classList.add(\'on\'); st.textContent = \'★\'; }\n        favRows.appendChild(clone);\n        // clone the adjacent info-panel too, if this row has one\n        var srcPanel = src.nextElementSibling;\n        if (srcPanel && srcPanel.classList.contains(\'info-panel\')) {\n          var panelClone = srcPanel.cloneNode(true);\n          panelClone.classList.remove(\'open\', \'hidden\');\n          favRows.appendChild(panelClone);\n        }\n      });\n    }\n\n    function isFav(code) { return favs.indexOf(code) !== -1; }\n\n    function setStarState(code, on) {\n      // update every star for this code (original + any fav clone)\n      var stars = document.querySelectorAll(\'.star[data-fav="\' + code + \'"]\');\n      Array.prototype.slice.call(stars).forEach(function (s) {\n        s.classList.toggle(\'on\', on);\n        s.textContent = on ? \'★\' : \'☆\';\n      });\n    }\n\n    function toggleFav(code) {\n      var i = favs.indexOf(code);\n      if (i === -1) favs.push(code); else favs.splice(i, 1);\n      saveFavs(favs);\n      setStarState(code, isFav(code));\n      renderFavs();\n    }\n\n    // Delegate star taps\n    document.addEventListener(\'click\', function (e) {\n      var t = e.target;\n      if (t && t.classList && t.classList.contains(\'star\')) {\n        e.preventDefault();\n        var code = t.getAttribute(\'data-fav\');\n        if (code) toggleFav(code);\n        return;\n      }\n      if (t && t.classList && t.classList.contains(\'info-btn\')) {\n        e.preventDefault();\n        var row = t.closest(\'.row\');\n        var panel = row ? row.nextElementSibling : null;\n        if (panel && panel.classList.contains(\'info-panel\')) {\n          var open = panel.classList.toggle(\'open\');\n          t.classList.toggle(\'open\', open);\n        }\n        return;\n      }\n    });\n\n    // Initialize star states from stored favs\n    favs.forEach(function (code) { setStarState(code, true); });\n    renderFavs();\n\n    // ---- Search ----\n    // ---------- Typo-tolerant matching ----------\n    function levenshtein(a, b) {\n      if (a === b) return 0;\n      if (!a.length) return b.length;\n      if (!b.length) return a.length;\n      var prev = [];\n      for (var j = 0; j <= b.length; j++) prev[j] = j;\n      for (var i = 1; i <= a.length; i++) {\n        var cur = [i];\n        for (var j2 = 1; j2 <= b.length; j2++) {\n          var cost = a[i - 1] === b[j2 - 1] ? 0 : 1;\n          cur[j2] = Math.min(prev[j2] + 1, cur[j2 - 1] + 1, prev[j2 - 1] + cost);\n        }\n        prev = cur;\n      }\n      return prev[b.length];\n    }\n    function fuzzyHit(term, haystack) {\n      // exact substring first (cheap, always correct)\n      if (haystack.indexOf(term) !== -1) return true;\n      if (term.length < 4) return false; // avoid false positives on very short terms\n      var thresh = term.length <= 5 ? 1 : (term.length <= 9 ? 2 : 3);\n      var words = haystack.split(/[^a-z0-9]+/);\n      for (var k = 0; k < words.length; k++) {\n        var w = words[k];\n        if (!w || Math.abs(w.length - term.length) > thresh) continue;\n        if (levenshtein(term, w) <= thresh) return true;\n      }\n      return false;\n    }\n\n    function run() {\n      var t = (q.value || \'\').trim().toLowerCase();\n      if (!t) {\n        document.body.classList.remove(\'searching\');\n        document.querySelectorAll(\'.row\').forEach(function (r) { r.classList.remove(\'hidden\'); });\n        document.querySelectorAll(\'.info-panel\').forEach(function (p) { p.classList.remove(\'hidden\'); });\n        sections.forEach(function (s) { s.classList.remove(\'hidden\'); });\n        document.querySelectorAll(\'.sub, .note, .sec-info\').forEach(function (s) { s.classList.remove(\'hidden\'); });\n        if (nav) nav.classList.remove(\'hidden\');\n        if (noresult) noresult.classList.add(\'hidden\');\n        return;\n      }\n      document.body.classList.add(\'searching\');\n      if (nav) nav.classList.add(\'hidden\');\n      var anyGlobal = false;\n      sections.forEach(function (sec) {\n        var any = false;\n        sec.querySelectorAll(\'.row\').forEach(function (r) {\n          var code = r.getAttribute(\'data-code\') || \'\';\n          var desc = r.getAttribute(\'data-desc\') || \'\';\n          var syn = (r.getAttribute(\'data-syn\') || \'\').toLowerCase();\n          var hit = fuzzyHit(t, code) || fuzzyHit(t, desc) || fuzzyHit(t, syn);\n          r.classList.toggle(\'hidden\', !hit);\n          var panel = r.nextElementSibling;\n          if (panel && panel.classList.contains(\'info-panel\')) {\n            panel.classList.toggle(\'hidden\', !hit);\n          }\n          if (hit) any = true;\n        });\n        sec.querySelectorAll(\'.sub, .note, .sec-info\').forEach(function (s) { s.classList.add(\'hidden\'); });\n        // Hide the favourites section during active search to avoid duplicate hits\n        if (sec.id === \'favourites\') { sec.classList.add(\'hidden\'); return; }\n        sec.classList.toggle(\'hidden\', !any);\n        if (any) anyGlobal = true;\n      });\n      if (noresult) noresult.classList.toggle(\'hidden\', anyGlobal);\n    }\n    q.addEventListener(\'input\', run);\n    q.addEventListener(\'keyup\', run);\n    q.addEventListener(\'search\', run);\n\n    // ---------- Sedation calculator ----------\n    (function initCalc() {\n      var box = document.getElementById(\'sedcalc\');\n      if (!box) return;\n      var UNIT = 15.92;            // $ per unit\n      var BASE_UNITS = 6;          // procedural sedation base\n      var proc = document.getElementById(\'c-proc\');\n      var timeIn = document.getElementById(\'c-time\');\n      var out = document.getElementById(\'c-out\');\n\n      var state = { asa: \'1\', age: \'adult\', mods: {}, prem: \'\' };\n\n      function segWire(id, key) {\n        var seg = document.getElementById(id);\n        seg.querySelectorAll(\'button\').forEach(function (b) {\n          b.addEventListener(\'click\', function () {\n            seg.querySelectorAll(\'button\').forEach(function (x) { x.classList.remove(\'on\'); });\n            b.classList.add(\'on\');\n            state[key] = b.getAttribute(\'data-v\');\n            render();\n          });\n        });\n      }\n      segWire(\'c-asa\', \'asa\');\n      segWire(\'c-age\', \'age\');\n      segWire(\'c-prem\', \'prem\');\n\n      var mods = document.getElementById(\'c-mods\');\n      mods.querySelectorAll(\'button\').forEach(function (b) {\n        b.addEventListener(\'click\', function () {\n          var v = b.getAttribute(\'data-v\');\n          if (state.mods[v]) { delete state.mods[v]; b.classList.remove(\'on\'); }\n          else { state.mods[v] = true; b.classList.add(\'on\'); }\n          render();\n        });\n      });\n\n      // ----- Procedure autocomplete -----\n      var PROC_LIST = __PROCLIST__;\n      var acList = document.getElementById(\'c-proc-list\');\n      var picked = document.getElementById(\'c-proc-picked\');\n      var chosenCode = \'\';\n      var activeIdx = -1;\n      var curMatches = [];\n\n      function normalize(x){ return (x||\'\').toLowerCase(); }\n\n      function renderMatches(q) {\n        q = normalize(q).trim();\n        acList.innerHTML = \'\';\n        activeIdx = -1;\n        if (!q) { acList.classList.remove(\'on\'); curMatches = []; return; }\n        var terms = q.split(/\\s+/);\n        curMatches = PROC_LIST.filter(function (it) {\n          var hay = normalize(it.c) + \' \' + normalize(it.d) + \' \' + normalize(it.k || \'\');\n          return terms.every(function (t) { return hay.indexOf(t) !== -1; });\n        }).slice(0, 12);\n        if (!curMatches.length) {\n          acList.innerHTML = \'<div class="ac-none">No match — you can also type a code directly.</div>\';\n          acList.classList.add(\'on\');\n          return;\n        }\n        curMatches.forEach(function (it, i) {\n          var el = document.createElement(\'div\');\n          el.className = \'ac-item\';\n          el.setAttribute(\'data-i\', i);\n          el.innerHTML = \'<span class="acc">\' + it.c + \'</span><span class="acd">\' + it.d + \'</span>\';\n          el.addEventListener(\'mousedown\', function (e) { e.preventDefault(); choose(i); });\n          acList.appendChild(el);\n        });\n        acList.classList.add(\'on\');\n      }\n\n      function choose(i) {\n        var it = curMatches[i];\n        if (!it) return;\n        chosenCode = it.c;\n        proc.value = it.c + \' — \' + it.d;\n        picked.textContent = \'Using \' + it.c + \' → "\' + it.c + \'C"\';\n        picked.classList.add(\'set\');\n        acList.classList.remove(\'on\');\n        render();\n      }\n\n      function highlight(dir) {\n        var items = acList.querySelectorAll(\'.ac-item\');\n        if (!items.length) return;\n        activeIdx += dir;\n        if (activeIdx < 0) activeIdx = items.length - 1;\n        if (activeIdx >= items.length) activeIdx = 0;\n        items.forEach(function (el, i) { el.classList.toggle(\'active\', i === activeIdx); });\n        items[activeIdx].scrollIntoView({ block: \'nearest\' });\n      }\n\n      proc.addEventListener(\'input\', function () {\n        chosenCode = \'\';                     // typing invalidates a prior pick\n        picked.classList.remove(\'set\');\n        picked.textContent = \'Search the base procedure — its code becomes the "C" code.\';\n        renderMatches(proc.value);\n        render();\n      });\n      proc.addEventListener(\'keydown\', function (e) {\n        if (!acList.classList.contains(\'on\')) return;\n        if (e.key === \'ArrowDown\') { e.preventDefault(); highlight(1); }\n        else if (e.key === \'ArrowUp\') { e.preventDefault(); highlight(-1); }\n        else if (e.key === \'Enter\') { if (activeIdx >= 0) { e.preventDefault(); choose(activeIdx); } }\n        else if (e.key === \'Escape\') { acList.classList.remove(\'on\'); }\n      });\n      proc.addEventListener(\'blur\', function () { setTimeout(function(){ acList.classList.remove(\'on\'); }, 150); });\n      proc.addEventListener(\'focus\', function () { if (proc.value) renderMatches(proc.value); });\n      timeIn.addEventListener(\'input\', render);\n\n      function timeUnits(mins) {\n        // each 15 min or part thereof: 1u first hr, 2u >60-90min, 3u >90min\n        if (!mins || mins <= 0) return 0;\n        var u = 0, blocks = Math.ceil(mins / 15);\n        for (var i = 0; i < blocks; i++) {\n          var mid = i * 15; // start minute of this block\n          if (mid < 60) u += 1;\n          else if (mid < 90) u += 2;\n          else u += 3;\n        }\n        return u;\n      }\n\n      // Extra-unit values\n      var EXTRA = {\n        E020C: 4, E010C: 2, E011C: 4, E024C: 4,\n        E022C: 2, E017C: 10, E016C: 20,\n        E009C: 4, E019C: 2, E007C: 1, E018C: 3\n      };\n      var LABEL = {\n        E020C: \'ASA-E emergency\', E010C: \'BMI > 40\', E011C: \'Prone\', E024C: \'Sitting >60°\',\n        E022C: \'ASA III\', E017C: \'ASA IV\', E016C: \'ASA V\',\n        E009C: \'Age 29d–1y\', E019C: \'Age 1–8y\', E007C: \'Age 70–79\', E018C: \'Age 80+\',\n        E400C: \'Eve/Wknd premium\', E401C: \'Night premium\'\n      };\n\n      function render() {\n        var lines = [];\n        var codes = [];\n        var pcode = \'\';\n        if (chosenCode) { pcode = chosenCode.toUpperCase(); }\n        else {\n          // user typed a raw code directly: take first token (letters+digits)\n          var raw = (proc.value || \'\').trim();\n          var mm = raw.match(/^[A-Za-z]\\d{2,3}/);\n          if (mm) pcode = mm[0].toUpperCase();\n        }\n        var mins = parseInt(timeIn.value, 10) || 0;\n        var tU = timeUnits(mins);\n        var totalUnits = BASE_UNITS + tU;\n\n        // Base line\n        var baseCode = pcode ? (pcode + \'C\') : \'(procedure)C\';\n        lines.push({ c: baseCode, u: BASE_UNITS + \' base\' + (tU ? \' + \' + tU + \' time\' : \'\') + \' units\', hint: true });\n        if (pcode) codes.push(baseCode);\n\n        // ASA extra\n        var asaCode = ({ \'3\':\'E022C\', \'4\':\'E017C\', \'5\':\'E016C\' })[state.asa];\n        if (asaCode) { lines.push({ c: asaCode, u: LABEL[asaCode] + \' (+\' + EXTRA[asaCode] + \'u)\' }); codes.push(asaCode); totalUnits += EXTRA[asaCode]; }\n\n        // Age extra\n        var ageCode = ({ \'29d1\':\'E009C\', \'1to8\':\'E019C\', \'70\':\'E007C\', \'80\':\'E018C\' })[state.age];\n        if (ageCode) { lines.push({ c: ageCode, u: LABEL[ageCode] + \' (+\' + EXTRA[ageCode] + \'u)\' }); codes.push(ageCode); totalUnits += EXTRA[ageCode]; }\n\n        // Modifier extras\n        Object.keys(state.mods).forEach(function (m) {\n          lines.push({ c: m, u: LABEL[m] + \' (+\' + EXTRA[m] + \'u)\' });\n          codes.push(m); totalUnits += EXTRA[m];\n        });\n\n        // Premium (percentage, not units)\n        if (state.prem) { lines.push({ c: state.prem, u: LABEL[state.prem] }); codes.push(state.prem); }\n\n        var html = lines.map(function (l) {\n          return \'<div class="line"><span class="cc">\' + l.c + \'</span><span class="cu">\' + l.u + \'</span></div>\';\n        }).join(\'\');\n\n        var est = (totalUnits * UNIT);\n        html += \'<div class="line tot"><span>Total units</span><span>\' + totalUnits + \'u  ≈  $\' + est.toFixed(2) + \'</span></div>\';\n        if (state.prem) html += \'<div class="warn">+ \' + (state.prem === \'E401C\' ? \'75%\' : \'50%\') + \' premium applies on top.</div>\';\n        if (!pcode) html += \'<div class="warn">Enter the procedure code to complete the "C" code.</div>\';\n\n        out.innerHTML = html;\n        out._codes = codes.join(\'  \');\n      }\n\n      document.getElementById(\'c-copy\').addEventListener(\'click\', function () {\n        var txt = out._codes || \'\';\n        var btn = this;\n        function ok() { btn.textContent = \'Copied ✓\'; btn.classList.add(\'done\');\n                        setTimeout(function(){ btn.textContent=\'Copy codes\'; btn.classList.remove(\'done\'); }, 1500); }\n        if (navigator.clipboard && navigator.clipboard.writeText) {\n          navigator.clipboard.writeText(txt).then(ok, ok);\n        } else { ok(); }\n      });\n\n      render();\n    })();\n\n    // ---------- ISS calculator (inline under E420) ----------\n    (function initISS() {\n      var trigger = document.querySelector(\'.row-expand[data-expand="iss"]\');\n      var panel = document.getElementById(\'iss-panel\');\n      if (!trigger || !panel) return;\n\n      // toggle expand on row tap (but not when tapping the star)\n      trigger.addEventListener(\'click\', function (e) {\n        if (e.target && e.target.classList && e.target.classList.contains(\'star\')) return;\n        var open = panel.classList.toggle(\'open\');\n        trigger.classList.toggle(\'open\', open);\n      });\n\n      var regions = [\'head\',\'face\',\'chest\',\'abdo\',\'extr\',\'ext\'];\n      var scores = { head:null, face:null, chest:null, abdo:null, extr:null, ext:null };\n      var names = { head:\'Head/Neck\', face:\'Face\', chest:\'Chest\', abdo:\'Abdomen\', extr:\'Extremities\', ext:\'External\' };\n\n      // build 0-6 buttons in each segment\n      panel.querySelectorAll(\'.iss-seg\').forEach(function (seg) {\n        var reg = seg.getAttribute(\'data-reg\');\n        for (var n = 0; n <= 6; n++) {\n          (function (val) {\n            var b = document.createElement(\'button\');\n            b.type = \'button\';\n            b.textContent = val;\n            b.addEventListener(\'click\', function () {\n              if (scores[reg] === val) { scores[reg] = null; }\n              else { scores[reg] = val; }\n              // update button states in this segment\n              seg.querySelectorAll(\'button\').forEach(function (x, i) {\n                var on = (scores[reg] === i);\n                x.classList.toggle(\'on\', on);\n                x.classList.toggle(\'sev6\', on && i === 6);\n              });\n              computeISS();\n            });\n            seg.appendChild(b);\n          })(n);\n        }\n      });\n\n      var outEl = document.getElementById(\'iss-out\');\n      var valEl = document.getElementById(\'iss-val\');\n      var lblEl = document.getElementById(\'iss-lbl\');\n      var detEl = document.getElementById(\'iss-detail\');\n\n      function computeISS() {\n        var vals = [];\n        var anySix = false;\n        regions.forEach(function (r) {\n          var v = scores[r];\n          if (v !== null) { vals.push({ r: r, v: v }); if (v === 6) anySix = true; }\n        });\n\n        if (!vals.length) {\n          valEl.textContent = \'0\';\n          lblEl.textContent = \'Select AIS scores above\';\n          detEl.innerHTML = \'\';\n          outEl.className = \'iss-out\';\n          return;\n        }\n\n        var iss, top3;\n        if (anySix) {\n          iss = 75;\n          top3 = [{ r: vals.filter(function(x){return x.v===6;})[0].r, v: 6 }];\n        } else {\n          var sorted = vals.slice().sort(function (a, b) { return b.v - a.v; });\n          top3 = sorted.slice(0, 3);\n          iss = top3.reduce(function (sum, x) { return sum + x.v * x.v; }, 0);\n        }\n\n        valEl.textContent = iss;\n        var major = iss > 15;\n        lblEl.textContent = major ? \'Major trauma\' : \'Not major\';\n        outEl.className = \'iss-out \' + (major ? \'major\' : \'minor\');\n\n        var parts = top3.map(function (x) { return names[x.r] + \' \' + x.v + (anySix ? \'\' : \'² =\' + (x.v*x.v)); });\n        var calc = anySix\n          ? \'AIS 6 in \' + names[top3[0].r] + \' → ISS auto-set to 75 (unsurvivable).\'\n          : \'Top three: \' + parts.join(\'  +  \') + \'  =  \' + iss;\n        var flag = major\n          ? \'<div class="iss-flag yes">ISS &gt; 15 → E420 trauma premium billable</div>\'\n          : \'<div class="iss-flag no">ISS ≤ 15 → E420 not met</div>\';\n        detEl.innerHTML = calc + \'<br>\' + flag;\n      }\n\n      document.getElementById(\'iss-reset\').addEventListener(\'click\', function () {\n        regions.forEach(function (r) { scores[r] = null; });\n        panel.querySelectorAll(\'.iss-seg button\').forEach(function (b) { b.classList.remove(\'on\',\'sev6\'); });\n        computeISS();\n      });\n\n      computeISS();\n    })();\n  }\n\n  // ---------- Auto-update check ----------\n  var LOCAL_VERSION = \'__VERSION__\';\n  function checkForUpdate(force) {\n    try {\n      var url = \'version.txt?ts=\' + Date.now(); // cache-bust the check itself\n      fetch(url, { cache: \'no-store\' }).then(function (r) {\n        if (!r.ok) return; return r.text();\n      }).then(function (txt) {\n        if (!txt) return;\n        var remote = txt.trim();\n        if (remote && remote !== LOCAL_VERSION) {\n          if (force) { hardReload(); return; }\n          showUpdateBar(remote);\n        } else if (force) {\n          var b = document.getElementById(\'forcerefresh\');\n          if (b) { b.classList.remove(\'checking\'); b.classList.add(\'done\');\n                   b.textContent = \'Up to date ✓\';\n                   setTimeout(function(){ b.classList.remove(\'done\'); b.textContent=\'↻ Check for update\'; }, 1600); }\n        }\n      }).catch(function(){});\n    } catch (e) {}\n  }\n  function hardReload() {\n    // append a cache-busting param and reload\n    var u = location.pathname + \'?v=\' + Date.now();\n    location.replace(u);\n  }\n  function showUpdateBar(remote) {\n    if (document.getElementById(\'updbar\')) return;\n    var bar = document.createElement(\'div\');\n    bar.id = \'updbar\';\n    bar.innerHTML = \'A newer version (\' + remote + \') is available. \'\n                  + \'<button type="button" id="updbtn">Update now</button>\';\n    document.body.appendChild(bar);\n    document.getElementById(\'updbtn\').addEventListener(\'click\', hardReload);\n  }\n\n  if (document.readyState === \'loading\') document.addEventListener(\'DOMContentLoaded\', init);\n  else init();\n\n  // run update check shortly after load (needs connectivity; fails silently offline)\n  setTimeout(function(){ checkForUpdate(false); }, 800);\n  document.addEventListener(\'DOMContentLoaded\', function () {\n    var fr = document.getElementById(\'forcerefresh\');\n    if (fr) fr.addEventListener(\'click\', function (e) {\n      e.preventDefault();\n      fr.classList.add(\'checking\'); fr.textContent = \'Checking…\';\n      checkForUpdate(true);\n      // if no newer version (or offline), restore label after a moment\n      setTimeout(function(){\n        if (fr.classList.contains(\'checking\')) { fr.classList.remove(\'checking\'); fr.textContent=\'↻ Check for update\'; }\n      }, 4000);\n    });\n  });\n})();\n'


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render_entry(entry):
    kind = entry[0]
    if kind == "SUB":
        return f'<div class="sub">{esc(entry[1])}</div>'
    if kind == "NOTE":
        return f'<div class="note">{esc(entry[1])}</div>'
    if kind == "SECINFO":
        return f'<div class="sec-info">{esc(entry[1])}</div>'
    if kind == "CALC":
        return CALC_HTML
    if kind == "ROW":
        _, desc, code, price, meta = entry
        d = esc(desc)
        badge_html = ""
        if meta.get("badge") == "g35":
            badge_html = '<span class="gbadge g35" title="Billable with G3/G5 series">G3/G5</span>'
        elif meta.get("badge") == "gno":
            badge_html = '<span class="gbadge gno" title="Not billable with G3/G5 series">\u2298G3/G5</span>'
        elif meta.get("badge") == "g3only":
            badge_html = '<span class="gbadge g3only" title="Billable with G3 series only, not G5">G3 only</span>'
        fx_html = ""
        if meta.get("fxbadge") == "no":
            fx_html = '<span class="gbadge fxno">No reduction</span>'
        elif meta.get("fxbadge") == "closed":
            fx_html = '<span class="gbadge fxclosed">Reduction</span>'
        new_html = '<span class="new">NEW</span>' if meta.get("added") else ""
        has_info = bool(meta.get("info"))
        is_expand = bool(meta.get("expand"))
        cls = "row"
        if is_expand: cls += " row-expand"
        if meta.get("hidden"): cls += " srch"
        if has_info: cls += " has-info"
        extra_attr = ' data-expand="iss"' if is_expand else ""
        syn_attr = f' data-syn="{esc(meta["syn"])}"' if meta.get("syn") else ""
        exp_hint = '<span class="exp-hint" aria-hidden="true">\u25b8 ISS calc</span>' if is_expand else ""
        info_btn = '<button class="info-btn" type="button" aria-label="More info">i</button>' if has_info else ""
        out = (f'<div class="{cls}" data-code="{code.lower()}" data-desc="{d.lower()}" '
               f'data-fk="{code}"{syn_attr}{extra_attr}>'
               f'<button class="star" type="button" aria-label="Toggle favourite" data-fav="{code}">\u2606</button>'
               f'<span class="code">{code}</span>'
               f'<span class="desc">{d}{fx_html}{badge_html}{new_html}{exp_hint}</span>'
               f'<span class="price">{esc(price)}</span>{info_btn}</div>')
        if has_info:
            out += f'<div class="info-panel">{esc(meta["info"])}</div>'
        if is_expand:
            out += f'<div class="expand-panel" id="iss-panel">{ISS_HTML}</div>'
        return out
    raise ValueError(f"unknown entry kind: {kind}")


def render_section(sec_id, title, color, entries):
    body = "".join(render_entry(e) for e in entries)
    return (f'<section id="{sec_id}" style="--c:{color}">'
            f'<div class="secban"><span class="bandot"></span>{esc(title)}'
            f'<a class="top" href="#top">\u2191 top</a></div>'
            f'<div class="rows">{body}</div></section>')


def build_nav_and_favourites(sections):
    nav_cells = ['<a class="navchip navchip-fav" href="#favourites" style="--c:#f5a524">'
                 '<span class="navdot"></span>\u2605 Favourites</a>']
    for sec_id, title, color, _ in sections:
        nav_cells.append(f'<a class="navchip" href="#{sec_id}" style="--c:{color}">'
                          f'<span class="navdot"></span>{esc(title)}</a>')
    nav_cells.append('<a class="navchip navchip-upd" href="#updates" style="--c:#0891b2">'
                      '<span class="navdot"></span>\u21bb Updates</a>')
    fav_section = ('<section id="favourites" style="--c:#f5a524">'
                   '<div class="secban"><span class="bandot"></span>\u2605 Favourites'
                   '<a class="top" href="#top">\u2191 top</a></div>'
                   '<div class="rows" id="fav-rows">'
                   '<div class="fav-empty" id="fav-empty">Tap the \u2606 on any code to add it here.</div>'
                   '</div></section>')
    return "".join(nav_cells), fav_section


def build_proc_list(sections):
    """Sedation-calculator searchable procedure list: every ROW with a real code,
    excluding 'no sedation' variants, percentage rows, and unit-helper pseudo-codes."""
    SYNONYMS = {
        "glenohumeral": "shoulder", "radial head": "pulled elbow nursemaid",
        "colles": "wrist distal radius", "smith": "wrist distal radius",
        "distal radius": "wrist", "radius distal": "wrist",
        "olecranon": "elbow", "epicondyle": "elbow", "transcondylar": "elbow", "condylar": "elbow",
        "patella": "kneecap", "phalanx": "finger toe", "phalangeal": "finger toe",
        "interphalangeal": "finger toe ip", "metacarpal": "hand finger",
        "metatarsal": "foot toe", "metatarsophalangeal": "foot toe",
        "carpal": "wrist", "carpus": "wrist", "tarsus": "foot ankle", "tarso": "foot",
        "calcis": "heel", "clavicle": "collarbone", "humeral": "arm", "humerus": "arm",
        "temporomandibular": "jaw tmj", "cardioversion": "shock defibrillation dccv afib",
        "reduction": "reduce dislocation fracture", "acj": "ac joint shoulder",
        "scj": "sternoclavicular", "hip": "femoral head", "monteggia": "forearm",
        "tibia": "leg shin", "fibula": "leg", "femur": "thigh", "sternum": "chest",
        "scapula": "shoulder blade", "vulvar": "bartholin vagina", "bartholin": "vulva vagina abscess",
    }
    items = []
    seen = set()
    for sec_id, title, color, entries in sections:
        for e in entries:
            if e[0] != "ROW": continue
            _, desc, code, price, meta = e
            if not code or not code[0:1].isalpha(): continue
            dl = desc.lower()
            if "no sedation" in dl or "without sedation" in dl: continue
            if isinstance(price, str) and "%" in price: continue
            if code in ("6u", "1u"): continue
            if code in seen: continue
            seen.add(code)
            kw = [syn for trig, syn in SYNONYMS.items() if trig in dl]
            item = {"c": code, "d": desc}
            if kw: item["k"] = " ".join(kw)
            items.append(item)
    return _json.dumps(items, ensure_ascii=False)


def build():
    sections = SECTIONS
    section_html = "".join(
        render_section(sec_id, title, color, entries)
        for sec_id, title, color, entries in sections
        if sec_id != "updates"
    )
    # Updates section is templated specially below (contains the live version stamp + legend);
    # it is intentionally NOT part of SECTIONS since its content is version-dependent.
    nav_html, fav_html = build_nav_and_favourites(sections)
    proc_list_json = build_proc_list(sections)

    updates_html = (
        '<section id="updates" style="--c:#0891b2"><div class="secban">'
        '<span class="bandot"></span>\u21bb Updates<a class="top" href="#top">\u2191 top</a></div>'
        '<div class="rows"><div class="upd-card">'
        '<button type="button" id="forcerefresh">\u21bb Check for update</button>'
        '<div class="upd-meta">You are viewing <b>v__VERSION__</b>.<br>'
        'When a newer version is published, a prompt appears at the bottom of the screen. '
        'You can also check any time with the button above.</div></div>'
        '<div class="upd-card" style="text-align:left">'
        '<div style="font-weight:800;font-size:13px;margin-bottom:8px;">Critical care badge legend</div>'
        '<div style="font-size:12px;line-height:1.6;">'
        '<span class="gbadge g35">G3/G5</span> Billable alongside critical care (G395/G391 or G521\u2013G523)<br>'
        '<span class="gbadge g3only">G3 only</span> Billable with G395/G391 series only, not G521\u2013G523<br>'
        '<span class="gbadge gno">\u2298G3/G5</span> Bundled into critical care \u2014 not separately billable with either series'
        '</div></div></div></section>'
    )

    content = fav_html + section_html + updates_html

    html = (
        "<!DOCTYPE html>\n<html lang=\"en\"><head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=5\">\n"
        "<title>ED Billing Guide</title>\n"
        + EARLY_THEME_SCRIPT + "\n"
        "<style>" + CSS + "</style></head>\n"
        + HEADER_SHELL
        + f'<div id="content">{content}</div>\n'
        + FOOTER_ONLY
        + "<script>" + MAIN_JS + "</script>\n"
        "</body></html>\n"
    )

    html = html.replace("__NAV__", nav_html)
    html = html.replace("__PROCLIST__", proc_list_json)
    html = html.replace("__VERSION__", VERSION)

    with open(OUT_PATH, "w") as f:
        f.write(html)
    print(f"Wrote {len(html)} bytes to {OUT_PATH}")
    print(f"Sections: {len(sections)}  |  Codes: {len(set(e[2] for _,_,_,ents in sections for e in ents if e[0]=='ROW'))}")


if __name__ == "__main__":
    build()
