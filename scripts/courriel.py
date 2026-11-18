"""Construction des courriels de la lettre (texte + HTML), à partir du Markdown."""
import html
import os
import re
import sys
from email.message import EmailMessage
from email.utils import formataddr, formatdate, make_msgid
from pathlib import Path
from urllib.parse import quote

import markdown
import yaml

RACINE = Path(__file__).resolve().parent.parent
GABARIT = Path(__file__).resolve().parent / "gabarit_courriel.html"
NOM_FICHIER = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.(md|markdown)$")


def lire_config():
    with open(RACINE / "_config.yml", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def lire_lettre(chemin):
    texte = Path(chemin).read_text(encoding="utf-8")
    entete, corps = {}, texte
    if texte.startswith("---"):
        _, bloc, corps = texte.split("---", 2)
        entete = yaml.safe_load(bloc) or {}
    return entete, corps.strip()


def url_publique(chemin, config):
    """Reconstruit l'adresse de la lettre selon le permalien /lettres/:year/:month/:title/."""
    m = NOM_FICHIER.match(Path(chemin).name)
    if not m:
        sys.exit(f"Nom de fichier invalide : {chemin} (attendu AAAA-MM-JJ-titre.md)")
    annee, mois, _, titre, _ = m.groups()
    base = (config.get("url", "") + config.get("baseurl", "")).rstrip("/")
    return base, f"{base}/lettres/{annee}/{mois}/{titre}/"


def absolutiser(html_corps, base):
    """Rend absolus les liens et images relatifs, illisibles dans un courriel."""
    return re.sub(r'(src|href)="/(?!/)', rf'\1="{base}/', html_corps)


def lien_desinscription(contact, adresse):
    sujet = quote("Désinscription de la lettre")
    corps = quote(f"Merci de retirer l'adresse {adresse} de la liste de diffusion.")
    return f"mailto:{contact}?subject={sujet}&body={corps}"


def construire(entete, corps_md, config, destinataire, expediteur):
    base, url_lettre = url_publique(entete["_chemin"], config)
    contact = config.get("email_contact") or expediteur
    titre_lettre = config.get("title", "Lettre d'information")
    sujet = entete.get("title", "Lettre d'information")
    desinscription = lien_desinscription(contact, destinataire)

    corps_html = markdown.markdown(corps_md, extensions=["extra", "sane_lists"])
    corps_html = absolutiser(corps_html, base)
    chapo = entete.get("chapo", "")

    page = GABARIT.read_text(encoding="utf-8")
    remplacements = {
        "{{TITRE_LETTRE}}": html.escape(titre_lettre),
        "{{SUJET}}": html.escape(sujet),
        "{{CHAPO}}": f'<p style="font-style:italic;color:#5f5f5f;">{html.escape(chapo)}</p>' if chapo else "",
        "{{CORPS}}": corps_html,
        "{{URL_LETTRE}}": url_lettre,
        "{{URL_SITE}}": base + "/",
        "{{DESINSCRIPTION}}": html.escape(desinscription),
        "{{AUTEUR}}": html.escape(config.get("author", "")),
    }
    for cle, valeur in remplacements.items():
        page = page.replace(cle, valeur)

    texte = (
        f"{titre_lettre}\n{sujet}\n\n"
        + (f"{chapo}\n\n" if chapo else "")
        + f"{corps_md}\n\n"
        + f"Version en ligne : {url_lettre}\n"
        + f"Se désinscrire : écrire à {contact} (objet : Désinscription)\n"
    )

    msg = EmailMessage()
    msg["Subject"] = sujet
    msg["From"] = formataddr((os.environ.get("NOM_EXPEDITEUR") or config.get("author", ""), expediteur))
    msg["To"] = destinataire
    msg["Reply-To"] = contact
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=expediteur.split("@")[-1])
    # En-tête court et purement ASCII, lu par Gmail, Outlook, etc. pour afficher « Se désabonner ».
    msg["List-Unsubscribe"] = f"<mailto:{contact}?subject=Desinscription>"
    msg.set_content(texte)
    msg.add_alternative(page, subtype="html")
    return msg
