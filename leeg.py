#! .venv/bin/python
import argparse
import sys
import time
import webbrowser

import requests
import rich
from thefuzz import process

DESCRIPTION = "Crude cli to quickly get champion stats for League, from 'League of Graphs' ❤️"


# Data fetchers
def get_latest_patch() -> str:
    all_patches_url = "http://ddragon.leagueoflegends.com/api/versions.json"
    try:
        response = requests.get(all_patches_url)
        response.raise_for_status()
        all_patches = response.json()
        return all_patches[0]
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(f"There was an error getting the latest patch: {e}")
        sys.exit()


def get_latest_champions() -> list[str]:
    latest_patch = get_latest_patch()
    latest_champions_url = f"http://ddragon.leagueoflegends.com/cdn/{latest_patch}/data/en_US/champion.json"
    try:
        response = requests.get(latest_champions_url)
        response.raise_for_status()
        all_champions = response.json()
        champion_names = [champ for champ in all_champions["data"]]
        return champion_names
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(f"There was an error getting the latest champions: {e}")
        sys.exit()


# Input validators
champ_aliases = {
    "ww": "warwick",
    "vik": "viktor",
}


def validate_champ(champ: str):
    """Validates champion name by either: matching an alias and returning the predefined name OR fuzzy match against the latest champs"""
    champ = champ.lower()
    if champ in champ_aliases.keys():
        return champ_aliases[champ]

    start_time = time.perf_counter()
    fuzzy_champ: str = process.extractOne(champ, get_latest_champions())[0]  # type: ignore 🤮
    end_time = time.perf_counter()

    elapsed_time = f"{end_time - start_time:.3f}"
    rich.print(f"Fuzzy matched [red]{champ}[/] -> [red]{fuzzy_champ.lower()}[/] ([green]{elapsed_time}s[/])")
    return fuzzy_champ.lower()


def validate_lane(lane: str):
    class UnknownLane(Exception):
        pass

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
    raise UnknownLane(f"Unknown role/lane: {lane}. Must be top, jungle, middle, adc, support, or aram")


def validate_rank(rank: str):
    class UnknownRank(Exception):
        pass

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
        case "d" | "diamond":
            return "diamond"
        case "m" | "master":
            return "master"
    raise UnknownRank(f"Unknown rank: {rank}. Must be Iron - Master")


# Main
def main():
    start_time = time.perf_counter()
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("champ", type=validate_champ, help="Champion name")
    parser.add_argument("lane", type=validate_lane, help="Lane name, can also specify 'ARAM' here")
    parser.add_argument("-r", "--rank", type=validate_rank, help="Specify rank")

    args = parser.parse_args()

    champ = args.champ
    lane = args.lane
    rank = args.rank

    log_link = f"https://www.leagueofgraphs.com/champions/builds/{champ}/{lane}"

    if rank:
        log_link += f"/{rank}"

    log_link += "#mainContent"

    rich.print(f"Loading your [blue]{champ}[/] build for [blue]{lane}[/]...")
    rich.print(f"Link: [yellow]{log_link}[/]")
    webbrowser.open(log_link)
    end_time = time.perf_counter()

    elapsed_time = f"{end_time - start_time:.3f}"
    rich.print(f"Build loaded, glhf 💪 ([green]{elapsed_time}s[/])")


if __name__ == "__main__":
    main()
