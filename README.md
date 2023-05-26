# QuickLeeg
Crude cli to quickly get builds for League of Legends champions from '[League of Graphs](https://www.leagueofgraphs.com/)' ❤️

Other build sites might be supported in the future

## Features
- Fastest way to get your league build from League of Graphs (< 1s! 🔥)
  - Read more on the [why here](#why)
- Simply pass your desired champion and lane to the app. Your browser will open and snap to your champion's build
- Common champion nicknames supported, with fuzzy matching fallback
- Makes 2 small call to Riot API to make sure champ list is up to date

## Installation
```zsh
pipx install [TBD]
```

## Usage
```zsh
leeg [-h] [-r RANK] champ lane
```
## Why?
League of Graphs is easily the superior league build site. Despite this, getting to your favorite champion's stats is one too many clicks for me. You have to
1) Load the site
2) Click search box
3) Enter champ name
4) Specify lane
5) Specify rank

This script litreally just makes this one step