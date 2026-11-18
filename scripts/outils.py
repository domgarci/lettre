"""Liste des abonnés, détection des lettres déjà envoyées, connexion SMTP."""
import os
import re
import smtplib
import ssl
import subprocess

import yaml

from courriel import RACINE


def liste_abonnes():
    brut = os.environ.get("ABONNES", "")
    adresses = [a.strip() for a in re.split(r"[\s,;]+", brut) if "@" in a]
    return sorted(set(a.lower() for a in adresses))


def deja_envoyee(chemin, commit):
    """Vrai si la lettre existait déjà au commit donné avec « envoyer: true »."""
    try:
        ancien = subprocess.run(
            ["git", "show", f"{commit}:{chemin}"], cwd=RACINE,
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    if not ancien.startswith("---"):
        return False
    entete = yaml.safe_load(ancien.split("---", 2)[1]) or {}
    return entete.get("envoyer") is True


def connexion():
    hote = os.environ["SMTP_HOTE"]
    port = int(os.environ.get("SMTP_PORT", "587"))
    securite = os.environ.get("SMTP_SECURITE") or ("ssl" if port == 465 else "starttls")
    contexte = ssl.create_default_context()
    if securite == "ssl":
        serveur = smtplib.SMTP_SSL(hote, port, context=contexte, timeout=60)
    else:
        serveur = smtplib.SMTP(hote, port, timeout=60)
        if securite == "starttls":
            serveur.starttls(context=contexte)
    utilisateur = os.environ.get("SMTP_UTILISATEUR")
    if utilisateur:
        serveur.login(utilisateur, os.environ["SMTP_MOT_DE_PASSE"])
    return serveur
