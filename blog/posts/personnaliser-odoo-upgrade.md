---
title: "Personnaliser Odoo sans casser l'upgrade : 5 bonnes pratiques"
date: "2026-07-22"
tags: ["Odoo", "Développement", "Bonnes pratiques"]
excerpt: "Le premier réflexe d'un consultant Odoo est de créer un module. Encore faut-il le faire dans les règles pour que les mises à jour de l'ERP ne deviennent pas un calvaire."
---

Un des plus gros freins à l'adoption d'Odoo dans les entreprises est la peur de la mise à jour. Elle est légitime : une personnalisation mal écrite peut bloquer l'upgrade. Voici cinq pratiques que j'applique systématiquement.

## 1. Toujours un module, jamais du code dans les fichiers de base

Modifier le code du cœur d'Odoo, c'est la garantie de le perdre à chaque update. Je développe toujours des modules séparés, avec des préfixes clairs (`im_`, `vdm_`, etc.) pour identifier facilement leur origine.

## 2. Utiliser l'héritage plutôt que le copier-coller

Quand il faut changer un formulaire, j'hérite de la vue d'origine (`inherit_id`) au lieu de la dupliquer. Le code reste maintenable et compatible avec les évolutions du standard.

## 3. Versionner tout, dès le premier jour

Git n'est pas optionnel : chaque module doit avoir son historique. En cas de régression, on identifie la cause en quelques minutes au lieu de tout défaire.

## 4. Documenter les points d'extension

Un commentaire ne coûte rien au moment du codage, mais il fait gagner des heures lors de la maintenance. Je documente systématiquement les points d'extension : quelles fonctions sont surchargées, pourquoi, et dans quel module.

## 5. Tester avant de déployer

Un environnement de test isolé et un jeu de tests automatisés minimal (même quelques cas) vous éviteront des surprises coûteuses en production.

> En résumé : **code propre + héritage + Git + documentation + tests** = un Odoo personnalisé qui se met à jour sereinement.

Et si vous avez besoin d'un regard extérieur sur votre projet Odoo, mon profil LinkedIn est toujours ouvert : <https://www.linkedin.com/in/farid-slimani/>