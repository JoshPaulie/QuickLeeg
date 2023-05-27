# QuickLeeg
Crude cli to quickly get builds for League of Legends champions from [League of Graphs](https://www.leagueofgraphs.com/) ❤️

## Features
- Fastest way to get your league build from League of Graphs (< 1s! 🔥)
  - Read more on the [why here](#why)
- Simply pass your desired champion and lane to the app. Your browser will open and snap to your champion's build
- Common champion nicknames supported, with fuzzy matching fallback

## Installation
```zsh
pipx install [TBD]
```

## Usage
```zsh
leeg [-h] [-r RANK] champ lane
leeg aatrox top --rank gold
leeg fizz aram
```

## Why?
League of Graphs is easily the superior league build site. Despite this, getting to your favorite champion's stats is one too many clicks for me. You have to
1) Navigate to League of Graphs
2) Click search box
3) Enter champ name
4) Specify lane
5) Specify rank

This script litreally just makes this one step