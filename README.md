# Star Wars Galaxy of Heroes Strike Counter

Being an officer in SWGoH takes time. Keeping track of the performance of your guild members shouldn't drain you more than it already does chasing them to attack the raid and place Maul in Kessel operation 4.

Hotutils already does an amazing job recording statistics from territory battle (tb), territory war (tw), raid, and daily tickets. This repository (specifically the script [collect_strikes.py](collect_strikes.py)), gives you a one-line command to identify who has been underperforming and who is leading your guild across all modes.

This repository collates csv reports from HotUtils to list out who has been underperforming in a guild and who has been leading the way. Metrics are customizable.

## Setting up and Running

### Overview of how this repository runs:
1. Add csv reports to [Reports/](Reports/).
2. Run `uv run collect_strikes.py` from the command line.
3. Read the output list of strike counts with allycode and player names sorted by strike count.

### Detailed Guide
This script runs on python.
1. Clone this repository
2. `uv sync` (pulls from [pyproject.toml](pyproject.toml))
3. Add reports from HotUtils (there may be other ways to gather these csv files but this is what I used) to [Reports/](Reports/).
    - TB: run `/tb stats` with hotbot in Discord. (Don't select excel output as this script currently only accepts csv files.)
      - You will have to rename the file to add "tb" to the start. I.e. so it is named "tbstats" instead of the default "stats".
    - TW: run `/tw stats` with hotbot in Discord. Select however many TW you want to consider. Any active TW are ignored by this script based on time stamp.
    - Raid: run `/raids download` with hotbot in Discord. Select however many raids you want to consider. This file only includes completed raids.
      - You will have to rename the file to add "raid" to the start. I.e. so it is named "raidstats" instead of the default "stats".
    - Tickets: From hotutils.com, go to Guild in the left menu, then Tickets. Export to CSV in the upper right. This always pulls the last 7 days.
4. To run: `uv run collect_strikes.py`. From the root directory of the repository.

If you don't have `uv`, you can set up a python virtual environment and `pip install` the requirements. Currently, that is only `pandas`.

## Customization

The thresholds for the metrics that determine strikes are contained in [GUILD_THRESHOLDS.py](GUILD_THRESHOLDS.py).

Feel free to fork this repository and adjust it to your needs. You can also submit issues for new features (and merge requests if you can implement it yourself).

See the [BACKLOG.md](BACKLOG.md) for a list of future improvements/limitations of the current script. It is highly suggested that you read the code in [collect_strikes.py](collect_strikes.py) to make sure it is striking what you want. Particularly, as each guild can approach TB and TW differently.

## Background
Star Wars Galaxy of Heroes (SWGoH) is a collectible RPG game. The guild aspects of the game include earning tickets to launch raids, participating in those raids, defending and attacking in a territory war, and completing combat missions in a territory battle. Guilds usually work best when everyone is performing roughly near the same level. Each mode has different metrics to track performance.

## Acknowledgements
Thank you to HotUtils for making this script possible with your data scraping and collecting abilities.