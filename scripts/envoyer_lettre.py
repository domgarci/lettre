#!/usr/bin/env python3
"""Envoi d'une lettre d'information rédigée en Markdown.

Chaque abonné reçoit un courriel individuel (aucune adresse n'est visible
des autres destinataires), au format texte et HTML, avec un lien de
désinscription. Les réglages publics viennent de _config.yml ; les
identifiants SMTP et la liste des abonnés viennent des variables
d'environnement (secrets GitHub).

Usage :
  python scripts/envoyer_lettre.py _posts/2026-11-18-premiere-lettre.md [--test] [--brouillon DOSSIER] [--forcer]

  --test        envoie uniquement à l'adresse de l'expéditeur
  --brouillon   n'envoie rien ; écrit les courriels (.eml) dans DOSSIER
  --forcer      ignore la mention « envoyer: false » de l'en-tête
"""
import argparse
import os
import smtplib
import sys
import time
from pathlib import Path

from courriel import construire, lire_config, lire_lettre
from outils import connexion, deja_envoyee, liste_abonnes


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("fichiers", nargs="+")
    p.add_argument("--test", action="store_true")
    p.add_argument("--brouillon", metavar="DOSSIER")
    p.add_argument("--forcer", action="store_true")
    p.add_argument("--avant", metavar="COMMIT",
                   help="commit de référence : une lettre déjà marquée envoyer: true à ce commit n'est pas renvoyée")
    p.add_argument("--pause", type=float, default=float(os.environ.get("PAUSE_ENTRE_ENVOIS", "2")))
    args = p.parse_args()

    config = lire_config()
    expediteur = os.environ.get("EXPEDITEUR") or config.get("email_contact")
    if not expediteur:
        sys.exit("Aucune adresse d'expéditeur : renseignez le secret EXPEDITEUR.")

    for chemin in args.fichiers:
        entete, corps = lire_lettre(chemin)
        entete["_chemin"] = chemin
        if not (args.forcer or args.test) and entete.get("envoyer") is not True:
            print(f"· {chemin} : « envoyer: true » absent de l'en-tête, aucun envoi.")
            continue
        if args.avant and not (args.forcer or args.test) and deja_envoyee(chemin, args.avant):
            print(f"· {chemin} : déjà marquée « envoyer: true » avant cette modification, aucun nouvel envoi.")
            continue
        destinataires = [expediteur] if args.test else liste_abonnes()
        if not destinataires:
            sys.exit("La liste des abonnés est vide : renseignez le secret ABONNES.")

        print(f"· {chemin} : {len(destinataires)} destinataire(s){' [TEST]' if args.test else ''}")
        if args.brouillon:
            dossier = Path(args.brouillon)
            dossier.mkdir(parents=True, exist_ok=True)
            for i, d in enumerate(destinataires, 1):
                msg = construire(entete, corps, config, d, expediteur)
                (dossier / f"{Path(chemin).stem}-{i:04d}.eml").write_bytes(bytes(msg))
            print(f"  Brouillons écrits dans {dossier}/")
            continue

        serveur = connexion()
        envoyes, echecs = 0, []
        try:
            for d in destinataires:
                try:
                    serveur.send_message(construire(entete, corps, config, d, expediteur))
                    envoyes += 1
                except smtplib.SMTPServerDisconnected:
                    serveur = connexion()
                    serveur.send_message(construire(entete, corps, config, d, expediteur))
                    envoyes += 1
                except smtplib.SMTPException as e:
                    echecs.append((d, str(e)))
                time.sleep(args.pause)
        finally:
            try:
                serveur.quit()
            except smtplib.SMTPException:
                pass
        print(f"  Envoyés : {envoyes} · Échecs : {len(echecs)}")
        for d, e in echecs:
            # On masque la partie locale de l'adresse dans les journaux publics.
            print(f"  échec pour ***@{d.split('@')[-1]} : {e}")
        if echecs:
            sys.exit(1)


if __name__ == "__main__":
    main()
