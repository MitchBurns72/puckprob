"""Seulement norm() : le reste de cotes.py reste dans le dépôt privé."""
import unicodedata


def norm(nom):
    s = unicodedata.normalize("NFKD", nom or "").encode("ascii", "ignore").decode()
    return " ".join("".join(c if c.isalnum() else " " for c in s.lower()).split())
