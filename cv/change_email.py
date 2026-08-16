# -*- coding: utf-8 -*-
"""Remplace slimani.farid.cv@gmail.com par tech5262@gmail.com dans le CV,
en conservant le design original (masquage + insertion au meme emplacement).
Usage : python cv/change_email.py   (ecrase CV_Farid_SLIMANI_DZ.pdf)"""
import os
import statistics

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "CV_Farid_SLIMANI_DZ.pdf")
OLD = "slimani.farid.cv@gmail.com"
NEW = "tech5262@gmail.com"


def sample_bg(page, rect, dpi=300):
    """Couleur moyenne des pixels autour du rect (fond de la bande d'en-tete)."""
    clip = pymupdf.Rect(rect.x0 - 4, rect.y0 + 1, rect.x1 + 4, rect.y0 + 3)
    pix = page.get_pixmap(clip=clip, dpi=dpi)
    n = pix.width * pix.height
    if n == 0:
        return (0.07, 0.08, 0.15)
    rs, gs, bs = [], [], []
    for y in range(pix.height):
        for x in range(pix.width):
            idx = (y * pix.width + x) * pix.n
            rs.append(pix.samples[idx])
            gs.append(pix.samples[idx + 1])
            bs.append(pix.samples[idx + 2])
    r = statistics.median(rs) / 255.0
    g = statistics.median(gs) / 255.0
    b = statistics.median(bs) / 255.0
    return (r, g, b)


def main():
    doc = pymupdf.open(PDF)
    targets = []
    for pno, page in enumerate(doc):
        for r in page.search_for(OLD):
            targets.append((pno, r))

    if not targets:
        print("Aucune occurrence de", OLD)
        return 1

    # Recupere le style du texte original (taille + couleur + baseline)
    styles = {}
    for pno, _ in targets:
        page = doc[pno]
        td = page.get_text("dict")
        for block in td["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    if "slimani" in span["text"].lower():
                        c = span["color"]
                        styles[pno] = (
                            span["size"],
                            ((c >> 16) & 255) / 255.0,
                            ((c >> 8) & 255) / 255.0,
                            (c & 255) / 255.0,
                            span.get("origin", (span["bbox"][0], span["bbox"][3])),
                        )

    for pno, r in targets:
        page = doc[pno]
        bg = sample_bg(page, r)
        page.add_redact_annot(r, fill=bg)
        page.apply_redactions()

    for pno, r in targets:
        page = doc[pno]
        size, cr, cg, cb, origin = styles.get(
            pno, (9.5, 0.784, 0.808, 0.941, (r.x0, r.y1 - 3))
        )
        page.insert_text(
            pymupdf.Point(origin[0], origin[1]),
            NEW,
            fontsize=size,
            fontname="helv",
            color=(cr, cg, cb),
            overlay=True,
        )

    tmp = PDF + ".tmp"
    doc.save(tmp, incremental=False, deflate=True, garbage=4)
    doc.close()
    os.replace(tmp, PDF)
    print("Email remplace :", OLD, "->", NEW, "| style:", styles)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())