# -*- coding: utf-8 -*-
"""Génère le CV de Farid Slimani (PDF) — usage : python cv/generate_cv.py
Le PDF de sortie est écrit à la racine du repo (le site le référence)."""
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "CV_Farid_SLIMANI_DZ.pdf")

INDIGO = colors.HexColor("#4F46E5")
DARK = colors.HexColor("#0B1220")
GREY = colors.HexColor("#475569")
LIGHT = colors.HexColor("#64748B")

styles = {}
styles["h1"] = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=24,
                              leading=28, textColor=colors.white,
                              alignment=TA_CENTER)
styles["role"] = ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=12.5,
                                leading=16, textColor=colors.HexColor("#C7D2FE"),
                                alignment=TA_CENTER)
styles["contact"] = ParagraphStyle("contact", fontName="Helvetica", fontSize=9,
                                   leading=13, textColor=colors.HexColor("#E2E8F0"),
                                   alignment=TA_CENTER)
styles["sec"] = ParagraphStyle("sec", fontName="Helvetica-Bold", fontSize=12,
                               leading=15, textColor=INDIGO, spaceBefore=6,
                               spaceAfter=3)
styles["job"] = ParagraphStyle("job", fontName="Helvetica-Bold", fontSize=10.5,
                               leading=14, textColor=DARK, spaceBefore=5)
styles["meta"] = ParagraphStyle("meta", fontName="Helvetica-Oblique", fontSize=8.5,
                                leading=12, textColor=LIGHT)
styles["body"] = ParagraphStyle("body", fontName="Helvetica", fontSize=9,
                                leading=12.6, textColor=GREY)
styles["bullet"] = ParagraphStyle("bullet", parent=styles["body"], leftIndent=10,
                                  bulletIndent=2, spaceAfter=1)


def bullets(items):
    return [Paragraph(t, styles["bullet"], bulletText="\u2022") for t in items]


def sub(list_, title=None):
    """Bloc de sous-projets."""
    out = []
    if title:
        out.append(Paragraph(title, ParagraphStyle(
            "sub", parent=styles["body"], fontName="Helvetica-Bold",
            textColor=DARK, spaceBefore=3)))
    out += bullets(list_)
    return out


doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=15 * mm, rightMargin=15 * mm,
                        topMargin=12 * mm, bottomMargin=12 * mm)
story = []

header = [
    Paragraph("Farid SLIMANI", styles["h1"]),
    Spacer(1, 2),
    Paragraph("Développeur Sénior &amp; Consultant ERP ODOO", styles["role"]),
    Spacer(1, 4),
    Paragraph("\U0001F4CD Bordj El Kiffan, Alger, Algérie&nbsp;&nbsp;|&nbsp;&nbsp;"
              "\U0001F4DE +213 673 697 772&nbsp;&nbsp;|&nbsp;&nbsp;\u2709 tech5262@gmail.com",
              styles["contact"]),
    Paragraph("LinkedIn : linkedin.com/in/farid-slimani&nbsp;&nbsp;|&nbsp;&nbsp;Odoo Apps : "
              "apps.odoo.com (34 modules publiés)&nbsp;&nbsp;|&nbsp;&nbsp;FR · AR · KAB · EN (notions)",
              styles["contact"]),
]
htable = Table([[r] for r in header], colWidths=[180 * mm])
htable.setStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DARK),
    ("BOX", (0, 0), (-1, -1), 1, colors.white),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
])
story.append(htable)
story.append(Spacer(1, 8))

# ---------- PROFIL ----------
story.append(Paragraph("PROFIL", styles["sec"]))
story.append(Paragraph(
    "Consultant et Développeur ERP Odoo avec plus de 10 ans d'expérience dans le développement, "
    "la gestion et l'optimisation de solutions ERP. Fort d'une expérience significative en tant que "
    "Chef de Département et Chef de Division, je combine expertise technique en développement Odoo "
    "avec des compétences avérées en gestion de projets et leadership. Passionné par la transformation "
    "numérique et la résolution de problèmes complexes.", styles["body"]))

# ---------- COMPÉTENCES ----------
story.append(Paragraph("COMPÉTENCES TECHNIQUES", styles["sec"]))
comps = [
    ("ERP Odoo (versions 8 à 19)",
     ["Développement & personnalisation de modules", "CRM, Vente, Achat, Stock, Comptabilité, RH, Paie",
      "Déploiement, formation, support"]),
    ("Développement Backend & Web",
     ["Python, XML, QWeb, OWL, SQL", "HTML, CSS, JavaScript",
      "Django, Symfony, Flutter, PHP, Java, C++"]),
    ("Intégration & API",
     ["Conception et développement d'APIs REST", "Intégration avec applications tierces",
      "Bibliothèques Python : flask, FastAPI"]),
    ("Bases de données & DevOps",
     ["PostgreSQL, MySQL", "Ubuntu, Debian", "GIT — contrôle de version & collaboration"]),
    ("Gestion de projets",
     ["Gestion du cycle de vie ERP (planification → déploiement)", "Méthodes Agiles (Scrum)",
      "Pilotage de KPIs & amélioration continue"]),
    ("Leadership & management",
     ["Management d'équipes de développement", "Conduite du changement & digitalisation",
      "Formation et accompagnement utilisateurs"]),
]
for title, items in comps:
    story.append(Paragraph("<b>%s</b>&nbsp;: %s" % (title, " · ".join(items)), styles["body"]))
    story.append(Spacer(1, 2.5))

# ---------- EXPÉRIENCE ----------
story.append(Paragraph("EXPÉRIENCE PROFESSIONNELLE", styles["sec"]))

story.append(Paragraph("Chef de Département — Développement des Systèmes d'Information", styles["job"]))
story.append(Paragraph("SNTF (Société Nationale des Transports Ferroviaires) · Alger, Algérie — "
                       "fév. 2023 → Aujourd'hui", styles["meta"]))
story += bullets([
    "Piloter la digitalisation de l'entreprise, notamment la mise en œuvre et l'optimisation de l'ERP Odoo.",
    "Superviser une équipe de 20 personnes (siège + 4 directions régionales SNTF).",
    "Assurer la gestion complète du cycle de vie des projets (planification → déploiement → amélioration).",
    "Collaborer avec les parties prenantes pour identifier les besoins métier et proposer des solutions innovantes.",
    "Mesurer les résultats via des KPIs et proposer des axes d'amélioration continue.",
])

story.append(Paragraph("Chef de Division Web &amp; ERP", styles["job"]))
story.append(Paragraph("SNTF (Société Nationale des Transports Ferroviaires) · Alger, Algérie — "
                       "déc. 2019 → fév. 2023", styles["meta"]))
story += bullets([
    "Diriger une équipe de 5 à 6 développeurs spécialisés Odoo et superviser les projets web.",
    "Développer et intégrer des solutions personnalisées aux besoins de l'entreprise.",
])
story.append(Paragraph("Projets clés livrés :", ParagraphStyle(
    "pkey", parent=styles["body"], fontName="Helvetica-Bold", textColor=DARK, spaceBefore=2)))
story += sub([
    "Référentiel produits (catalogue marchandises, contraintes, type de wagon adapté), déclarations d'expédition, "
    "conventions tarifaires clients, facturation automatisée en fin de cycle, transfert instantané des documents "
    "entre gares via Odoo web (remplace l'échange physique).",
], "◆ Solution de Gestion du Transport de Marchandises")
story += sub([
    "Référentiel ferroviaire (trains, gares, relations, calendriers), tarification différenciée (étudiant, retraité…), "
    "vente en gare avec synchronisation bidirectionnelle national ↔ gares, tableaux de bord analytiques multi-niveaux "
    "(ventes par gare, région, relation).",
], "◆ Solution de Gestion des Billets Voyageurs")
story += sub([
    "Système d'archivage et gestion des documents internes.",
], "◆ Solution d'Archivage des Documents")
story += sub([
    "Remplacement du suivi Excel par des tableaux de bord Odoo interactifs : meilleure visibilité, priorisation des "
    "incidents et aide à la décision en temps réel.",
], "◆ Outil de Synthèse des Incidents Ferroviaires")

story.append(Paragraph("Ingénieur Informatique — Consultant ERP &amp; SI", styles["job"]))
story.append(Paragraph("AASYS · Alger, Algérie — mars 2019 → déc. 2019", styles["meta"]))
story += bullets([
    "Portage de modules Odoo (RH, Paie) vers l'ERP Open-Prod : analyse/adaptation du code source, mapping des "
    "modèles de données, ajustement des vues et workflows, tests de non-régression.",
    "Parser de factures PDF fournisseurs : moteur d'extraction automatique (références, montants, TVA…), création "
    "automatique des factures dans Odoo — taux de fiabilité de l'extraction supérieur à 99% en production.",
    "ERP médical : RH & paie, parc automobile, vente et location d'équipements médicaux, stocks de médicaments "
    "importés avec traçabilité (lots, péremptions), vente facturation et suivi des encaissements.",
])

story.append(Paragraph("Développeur Odoo", styles["job"]))
story.append(Paragraph("MLMConseil · Bouira, Algérie — juil. 2016 → mars 2019", styles["meta"]))
story += sub([
    "Fournisseurs (hôtels, transporteurs, guides), circuits et voyages organisés, réservations/devis/contrats, "
    "intégration email Bedsonline (confirmations hôtel), parsing Amadeus (devis et réservations de vols), "
    "facturation clients et gestion de la trésorerie.",
], "◆ Solution de Gestion d'Agence de Voyage")
story += sub([
    "Gestion du parc (fiches techniques, disponibilité, kilométrage, maintenance), contrats de location avec état "
    "des lieux, gestion des cautions, amendes et sinistres, facturation clients.",
], "◆ Solution de Gestion de Location de Voiture")
story += sub([
    "Manifests de chargement et connaissements (bill of lading), suivi des expéditions et transitaires, formalités "
    "douanières, facturation en devises et gestion des écarts de change.",
], "◆ Solution Import / Export")
story += sub([
    "Inscriptions, dossiers élèves et enseignants, emplois du temps, présences, examens/notation/bulletins, "
    "facturation des frais de scolarité.",
], "◆ Solution de Gestion d'École Privée")
story += bullets([
    "Personnalisation de modules Odoo standard : CRM, Vente, Achat, Stock, Facturation, Comptabilité, RH & Paie.",
    "APIs REST pour intégration et synchronisation des données Odoo avec des applications tierces.",
])

# ---------- FORMATION ----------
story.append(Paragraph("FORMATION", styles["sec"]))
story.append(Paragraph("Master — Réseaux, Mobilités &amp; Systèmes Embarqués", styles["job"]))
story.append(Paragraph("Université Mouloud Mammeri de Tizi-Ouzou — BAC+5 — 2012 → 2016", styles["meta"]))
story.append(Paragraph("PFE : application Android GPS/JSON pour la gestion de la mobilité.", styles["body"]))
story.append(Spacer(1, 3))
story.append(Paragraph("Licence en Informatique", styles["job"]))
story.append(Paragraph("Université Mouloud Mammeri de Tizi-Ouzou — BAC+3 — 2008 → 2012", styles["meta"]))
story.append(Paragraph("PFE : site web de gestion de librairies (PHP, MySQL, HTML/CSS, JS).", styles["body"]))

story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1")))
story.append(Paragraph(
    "<i>34 modules publiés sur Odoo Apps — disponible à la demande en version Word/PDF sur mesure.</i>",
    ParagraphStyle("foot", parent=styles["meta"], alignment=TA_CENTER, spaceBefore=3)))

doc.build(story)
print("PDF généré :", OUT)