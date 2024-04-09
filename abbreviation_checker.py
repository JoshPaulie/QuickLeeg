"""
Quick script for determining abbreviations
"""

from thefuzz import process

from quick_leeg.leeg import get_latest_champions

champs = get_latest_champions()

abbreviations = []

for champ in champs:
    while True:
        abbrv = input(f"Enter abbrv. for {champ}: ")
        if abbrv in ["", "q"]:
            break
        fuzzy_name, fuzzy_match_percent = process.extractOne(abbrv, champs)  # type: ignore
        print(fuzzy_name, fuzzy_match_percent)
