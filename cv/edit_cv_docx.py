# -*- coding: utf-8 -*-
"""Modifie CV_Farid_SLIMANI_DZ (1).docx -> CV_Farid_SLIMANI_DZ.docx
- email unifie : tech5262@gmail.com
- ajoute LinkedIn + Odoo Apps (hyperliens) dans l'en-tete
- ajoute les "Valeurs ajoutees" (SNTF, AASYS, MLMConseil)
- ajoute les modules complementaires MLMConseil
Usage : python cv/edit_cv_docx.py"""
import os
import re
import shutil
import zipfile

import xml.etree.ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

ET.register_namespace("w", W)
ET.register_namespace("r", REL)
ET.register_namespace("xml", "http://www.w3.org/XML/1998/namespace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "CV_Farid_SLIMANI_DZ (1).docx")
DST = os.path.join(ROOT, "CV_Farid_SLIMANI_DZ.docx")


def w(tag):
    return f"{{{W}}}{tag}"


def ptext(p):
    return "".join(t.text or "" for t in p.iter(w("t")))


def find_para(root, predicate, label):
    for p in root.iter(w("p")):
        if predicate(ptext(p)):
            return p
    raise RuntimeError("Paragraphe introuvable : " + label)


def clone_el(el):
    return ET.fromstring(ET.tostring(el))


def make_text_of(run, text):
    t = run.find(w("t"))
    if t is None:
        t = ET.SubElement(run, w("t"))
    t.text = text
    t.set(f"{{http://www.w3.org/XML/1998/namespace}}space", "preserve")


def make_bullet(tpl_bullet, text):
    p = clone_el(tpl_bullet)
    for r in list(p.findall(w("r"))):
        p.remove(r)
    r = ET.SubElement(p, w("r"))
    rpr = tpl_bullet.find(w("r")).find(w("rPr"))
    if rpr is not None:
        r.append(clone_el(rpr))
    make_text_of(r, "–  " + text)
    return p


def make_header(tpl_header, text):
    p = clone_el(tpl_header)
    runs = p.findall(w("r"))
    label = runs[-1]
    make_text_of(label, text)
    for r in runs[2:-1]:
        p.remove(r)
    return p


def insert_after(root, anchor, new_paras):
    parent = None
    for cand in root.iter():
        if anchor in list(cand):
            parent = cand
            break
    idx = list(parent).index(anchor)
    for i, el in enumerate(new_paras, start=1):
        parent.insert(idx + i, el)


def main():
    zin = zipfile.ZipFile(SRC)
    doc_data = zin.read("word/document.xml")
    rels_data = zin.read("word/_rels/document.xml.rels")
    rels_path = "word/_rels/document.xml.rels"
    doc_path = "word/document.xml"

    for m in re.finditer(rb'xmlns[:](\w+)="([^"]+)"', doc_data):
        ET.register_namespace(m.group(1).decode(), m.group(2).decode())
    root_start = doc_data.index(b"<w:document")
    root_open_end = doc_data.index(b">", root_start) + 1
    orig_prefix = doc_data[:root_start]
    orig_root_open = doc_data[root_start:root_open_end]

    root = ET.fromstring(doc_data)
    rels = ET.fromstring(rels_data)

    email_p = find_para(root, lambda t: "slimani" in t, "email")
    mlm_last = find_para(
        root, lambda t: t.startswith("–  Accès et synchronisation des données"), "mlm_last"
    )
    mlm_header_tpl = find_para(
        root, lambda t: t.startswith("◆ APIs pour applications"), "mlm_header_tpl"
    )
    sntf_last = find_para(
        root, lambda t: t.startswith("▸  Mesurer les résultats via des KPIs"), "sntf_last"
    )
    aasys_last = find_para(
        root, lambda t: "Vente aux clients" in t and "encaissements" in t, "aasys_last"
    )
    profil_p = find_para(
        root, lambda t: t.startswith("Consultant et Développeur ERP Odoo"), "profil"
    )

    # -- 1) email -----------------------------------------------------------
    done = False
    for r in email_p.findall(w("r")):
        t = r.find(w("t"))
        if t is not None and "slimani" in (t.text or ""):
            t.text = "tech5262@gmail.com "
            done = True
    if not done:
        raise RuntimeError("run email non trouve")

    # -- 2) lien LinkedIn + Odoo Apps dans l'en-tete -------------------------
    rpr_contact = email_p.findall(w("r"))[1].find(w("rPr"))

    def crun(text):
        r = ET.Element(w("r"))
        if rpr_contact is not None:
            r.append(clone_el(rpr_contact))
        make_text_of(r, text)
        return r

    def chyperlink(run, rid):
        h = ET.Element(w("hyperlink"))
        h.set(f"{{{REL}}}id", rid)
        h.append(run)
        return h

    existing = [r.get("Id") for r in rels.findall("{http://schemas.openxmlformats.org/package/2006/relationships}Relationship")]
    nums = [int(x) for x in re.findall(r"rId(\d+)", " ".join(existing))] or [0]
    nid = max(nums)
    rid_li, rid_apps = f"rId{nid+1}", f"rId{nid+2}"
    ET.SubElement(
        rels,
        "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship",
        {
            "Id": rid_li,
            "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
            "Target": "https://www.linkedin.com/in/farid-slimani/",
            "TargetMode": "External",
        },
    )
    ET.SubElement(
        rels,
        "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship",
        {
            "Id": rid_apps,
            "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
            "Target": "https://apps.odoo.com/apps/modules/browse?search=slimani",
            "TargetMode": "External",
        },
    )

    links_p = ET.Element(w("p"))
    links_p.append(crun("LinkedIn : "))
    links_p.append(chyperlink(crun("linkedin.com/in/farid-slimani"), rid_li))
    links_p.append(crun("  |  Odoo Apps : "))
    links_p.append(chyperlink(crun("apps.odoo.com"), rid_apps))
    links_p.append(crun(" — 34 modules publiés"))
    insert_after(root, email_p, [links_p])

    # -- 3) SNTF valeurs ajoutees -------------------------------------------
    insert_after(root, sntf_last, [
        make_header(mlm_header_tpl, "Valeurs ajoutées à la SNTF :"),
        make_bullet(mlm_last, "Réduction des dépenses : développement des solutions en interne plutôt que "
                              "recours à des fournisseurs externes."),
        make_bullet(mlm_last, "Initiation d'une équipe d'ingénieurs au développement Odoo et aux bonnes "
                              "pratiques (code clair et commenté, Git)."),
    ])

    # -- 4) AASYS valeurs ajoutees ------------------------------------------
    insert_after(root, aasys_last, [
        make_header(mlm_header_tpl, "Valeurs ajoutées à AASYS :"),
        make_bullet(mlm_last, "Tableaux de bord de suivi des projets."),
        make_bullet(mlm_last, "Réduction des délais de réalisation : suivi quotidien de l'avancement des "
                              "tâches et déblocage des points bloquants."),
    ])

    # -- 5) MLMConseil modules complementaires + valeurs ajoutees ------------
    insert_after(root, mlm_last, [
        make_header(mlm_header_tpl, "Autres modules développés pour des clients :"),
        make_bullet(mlm_last, "Suivi des chèques : état des chèques générés par les paiements de factures "
                              "(reçu, encaissé, rejeté)."),
        make_bullet(mlm_last, "Calcul du timbre fiscal selon la méthode algérienne (activable ou non par "
                              "facture d'achat / de vente)."),
        make_bullet(mlm_last, "Calcul des frais d'approche pour les produits importés payés en devises."),
        make_bullet(mlm_last, "Authentification par numéro de téléphone avec vérification et validation SMS "
                              "(utilisateurs internes et externes)."),
        make_bullet(mlm_last, "Distribution automatique des fiches de paie des employés selon leur matricule."),
        make_bullet(mlm_last, "Plateforme web de location de véhicules : algeriacarental.com (proposition et "
                              "réalisation)."),
        make_header(mlm_header_tpl, "Valeurs ajoutées à MLMConseil :"),
        make_bullet(mlm_last, "Proposition et mise en place de normes de développement internes."),
        make_bullet(mlm_last, "Formation et accompagnement des nouvelles recrues."),
    ])

    # -- 6) Profil : phrase differenciante -----------------------------------
    texts = [r.find(w("t")).text for r in profil_p.findall(w("r")) if r.find(w("t")) is not None]
    last_run_texts = [r for r in profil_p.findall(w("r")) if r.find(w("t")) is not None]
    last_run = last_run_texts[-1]
    new_sentence = (" Auteur de 34 modules publiés sur la plateforme Odoo Apps, solutions testées, "
                    "documentées et adoptées en production.")
    last_run.find(w("t")).text = (last_run.find(w("t")).text or "") + new_sentence

    # -- ecriture -------------------------------------------------------------
    doc_xml_bytes = ET.tostring(root, encoding="utf-8", xml_declaration=False)
    et_open_end = doc_xml_bytes.index(b">") + 1
    et_root_open = doc_xml_bytes[:et_open_end]
    et_decls = dict(re.findall(rb'xmlns[:](\w+)="([^"]+)"', et_root_open))
    extra = bytearray()
    for m in re.finditer(rb'xmlns[:](\w+)="([^"]+)"', orig_root_open):
        pref, uri = m.group(1), m.group(2)
        if pref not in et_decls:
            extra += b' xmlns:' + pref + b'="' + uri + b'"'
    new_root_open = et_root_open[:-1] + bytes(extra) + b">"
    doc_xml_bytes = orig_prefix + new_root_open + doc_xml_bytes[et_open_end:]
    rels_xml_bytes = ET.tostring(rels, encoding="utf-8", xml_declaration=True)

    with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == doc_path:
                data = doc_xml_bytes
            elif item.filename == rels_path:
                data = rels_xml_bytes
            zout.writestr(item, data)
    zin.close()
    print("DOCX modifie :", DST)


if __name__ == "__main__":
    main()