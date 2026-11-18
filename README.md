# Lettre d'information hors réseaux sociaux

Site d'archives : https://domgarci.github.io/lettre/

Outil gratuit, sans serveur : un fichier Markdown déposé dans `_posts/` s'affiche sur le site (GitHub Pages) et part par courriel aux abonnés (GitHub Actions). Chaque abonné reçoit un courriel individuel, avec lien de désinscription et sans traceur.

## Écrire une lettre

1. Dans `_posts/`, créez `AAAA-MM-JJ-titre-court.md` (bouton **Add file > Create new file**).
2. Commencez par cet en-tête, puis rédigez en Markdown :

```
---
title: "Titre de la lettre (objet du courriel)"
chapo: "Phrase d'accroche facultative."
numero: 2
envoyer: false
---
```

3. Avec `envoyer: false`, la lettre paraît sur le site sans être envoyée.
4. Test : **Actions > Envoi de la lettre > Run workflow**, chemin du fichier, mode `test`. Vous seul la recevez.
5. Envoi : passez à `envoyer: true` et enregistrez. Une correction ultérieure ne la renvoie pas.

## Gérer les abonnés

**Settings > Secrets and variables > Actions**, secret `ABONNES` : une adresse par ligne. GitHub ne réaffiche pas un secret ; gardez la liste de référence sur votre ordinateur et recollez-la entière à chaque modification.

## Secrets nécessaires

`SMTP_HOTE`, `SMTP_PORT`, `SMTP_UTILISATEUR`, `SMTP_MOT_DE_PASSE`, `EXPEDITEUR`, `NOM_EXPEDITEUR`, `ABONNES`.

## Markdown

`## Intertitre` · `**gras**` · `*italique*` · `[lien](https://...)` · `- puce` · `> citation` · `![image](/assets/photo.jpg)`
