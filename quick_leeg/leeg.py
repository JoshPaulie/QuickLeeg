#! .venv/bin/python
import argparse
import os
import sys
import time
import webbrowser

import requests
import rich
from thefuzz import process

from .__about__ import description, version


# Data fetchers
def get_latest_patch() -> str:
    """Pull the latest LoL SemVar patch, needed for get_latest_champions()"""
    all_patches_url = "http://ddragon.leagueoflegends.com/api/versions.json"
    try:
        response = requests.get(all_patches_url)
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(f"There was an error getting the latest patch: {e}")
        sys.exit()
    all_patches = response.json()
    return all_patches[0]


def get_latest_champions() -> list[str]:
    latest_patch = get_latest_patch()
    latest_champions_url = f"http://ddragon.leagueoflegends.com/cdn/{latest_patch}/data/en_US/champion.json"

    try:
        start_time = time.perf_counter()
        response = requests.get(latest_champions_url)
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(f"There was an error getting the latest champions: {e}")
        sys.exit()

    all_champions = response.json()
    champion_names = [champ for champ in all_champions["data"]]

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    rich.print(f"Latest champions downloaded... ([green]{elapsed_time:.3f}s[/])")
    return champion_names


# Common (to me) Champion Aliases
# "Why aliases if fuzzy matching?"
# League has many colloquial champ names and abbreviations,
# most of which don't fuzzy match to their respective champ name
champ_aliases = {
    "ww": "warwick",
    "vik": "viktor",
    "yi": "masteryi",
    "tf": "twistedfate",
    "rg": "renata",
    "j4": "jarvaniv",
    "mf": "missfortune",
    "sol": "aurelionsol",
    "ali": "alistar",
    "gp": "gangplank",
    "wu": "monkeyking",
    "wukong": "monkeyking",
    "tk": "tahmkench",
    "vel": "velkoz",
}


# Input validators
def validate_champ(champ: str):
    """Validates champion name by either: matching an alias and returning the predefined name OR fuzzy match against the latest champs"""
    champ = champ.lower()

    if champ in champ_aliases.keys():
        matched_alias = champ_aliases[champ]
        rich.print(f"Alias matched [green]{champ}[/] -> [blue]{matched_alias}[/]")
        return matched_alias

    latest_champs = get_latest_champions()
    if champ in [champ.lower() for champ in latest_champs]:
        return champ

    fuzzy_champ, fuzzy_match_percent = process.extractOne(champ, latest_champs)  # type: ignore 🤮
    fuzzy_champ = fuzzy_champ.lower()
    rich.print(f"Fuzzy matched [red]{champ}[/] -> [blue]{fuzzy_champ}[/] ({fuzzy_match_percent}% match)")
    return fuzzy_champ


class UnknownLane(Exception):
    pass


def validate_lane(lane: str):
    lane = lane.lower()
    match lane:
        case "t" | "top":
            return "top"
        case "j" | "jg" | "jungle":
            return "jungle"
        case "m" | "mid" | "middle":
            return "middle"
        case "a" | "adc" | "ad" | "bot" | "bottom":
            return "adc"
        case "s" | "sup" | "supp" | "support":
            return "support"
        case "aram":
            return lane
    raise UnknownLane(
        f"Unknown role/lane: [red]{lane}[/]. Must be top, jungle, middle, adc, support, or aram"
    )


class UnknownRank(Exception):
    pass


def validate_rank(rank: str):
    rank = rank.lower()
    match rank:
        case "i" | "iron":
            # lol, imagine
            return "iron"
        case "b" | "br" | "bronze":
            return "bronze"
        case "s" | "sil" | "silver":
            return "silver"
        case "g" | "gold":
            return "gold"
        case "p" | "plat" | "platinum":
            # Plat is the default rank and can't be set, so by returning None
            # a rank won't be appended to the link
            return None
        case "e" | "em" | "emerald":
            return "emerald"
        case "d" | "diamond":
            return "diamond"
        case "m" | "master":
            return "master"
    raise UnknownRank(f"Unknown rank: [red]{rank}[/]. Must be Iron - Master")


# Main
def main():
    # Performance timer
    start_time = time.perf_counter()

    # CLI handling
    parser = argparse.ArgumentParser(prog="leeg", description=description)
    parser.add_argument("champ", type=validate_champ, help="Champion name")
    parser.add_argument("lane", type=validate_lane, help="Lane name or 'ARAM'")
    parser.add_argument("-r", "--rank", type=validate_rank, help="Specify rank")
    parser.add_argument("-v", "--version", action="version", version=f"leeg v{version}")

    try:
        args = parser.parse_args()
    except (UnknownLane, UnknownRank) as e:
        rich.print(f"Error occurred: {e}")
        sys.exit()

    champ = args.champ
    lane = args.lane
    rank = args.rank

    # Base link
    log_link = f"https://www.leagueofgraphs.com/champions/builds/{champ}/{lane}"

    # Get rank from envvar, validate if present
    environment_rank = os.getenv("DEFAULT_RANK")
    try:
        if environment_rank:
            rank = validate_rank(environment_rank)
    except UnknownRank as e:
        rich.print(f"Error occurred: {e}")
        sys.exit()

    # Add rank if provided
    if rank:
        log_link += f"/{rank}"

    # Add element tag to URL, providing "snapping" to main content
    log_link += "#mainContent"

    # Open link in default browser, provide link incase that fails
    rich.print(f"Opening your [green]{champ}[/] [blue]{lane}[/] build...")
    rich.print(f"Link: [yellow]{log_link}[/]")
    webbrowser.open(log_link)

    # Display performance time, final message
    end_time = time.perf_counter()
    elapsed_time = f"{end_time - start_time:.3f}"
    rich.print(f"Build opened in your browser, glhf 💪 ([green]{elapsed_time}s[/])")


if __name__ == "__main__":
    main()
