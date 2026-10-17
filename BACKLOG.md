# Backlog

This is a list of improvements to be made.
 - A feature to provide a single ally code and automatically extract information from the files in Reports/
   - Either all pieces of information related to that ally code or
   - Just the (increasing/decreasing) strike count actions.
 - Include an optional file to import that manually adjusts players strike counts up or down. (To address things not captured by this script.)
 - Active TW are ignored based on timestamp. It may be useful to also automatically ignore any TW in tw files that were collected during its sign-up phase.
 - Currently all of every file in [Reports/](Reports/) is included in strike collection. Add a time cutoff that automatically ignores anything before a given timestamp.
 - Adjust ticket strike tracking to have the option to count by average. Or give partial strikes (e.g. 300/600 tickets is 1/2 strike). And an *option* for negative strikes. E.g. if a guild has a minimum of 500 tickets/day, then a member who always gets 600 tickets/day will get -1/6 strikes per day (*if* the guild turns on negative ticket strikes).
 - Add TW checks to highlight the best performer defender (most defensive teams, most single hold, most total holds), and best attacker (most attacking banners, most attacks), and best overall. Some of these may not be possible.
 - Add scripts to parse the TW and TB for top performers and the "lottery" winners and post those to a manual strike adjustment file.
 - Currently checking if someone didn't deploy in TB (and thus gets a strike) works by pre-assigning strikes to everyone, then removing strikes if they did deploy. It is done this way because a deploy of 0 doesn't show up in the csv output by Hotbot. But this assumes that there is a spot to deploy each phase (which for some guilds there may not be).
 - Specific special mission checks are currently by round. E.g. if your guild attempts the Zeffo Unlock SM in phase 3, this script incorrectly checks for the attempt in phase 2.
 - Add unit tests
 - Add a better tracking of allycode->Name logic. Maybe make a "Member" class that contains allycode (unique id), name, and strike count. Potentially a full list of actions for each member.

 # Implemented

This is a list of improvements formerly in the backlog, and how it was addressed.
 - If someone goes *all defense* in TW, there isn't a way to separately check that they 1. placed enough defense and 2. don't strike them for not attacking. This could be done manually once that feature is enabled.
   - Instead of not striking them for not attacking, or adjusting manually, we added an *all defense* banners threshold that provides a negative strike, thus counteracting the positive strike from not attacking.
 - Add a reference file to know which members are still in this guild and thus to exclude everyone else (use the ticket file?). This may trim down the allycode to name logic.
   - This didn't trim down the allycode to name logic because the reference file is optional. It works by trimming only what gets returned at the final step. The information is still collected on everyone, but ignored for those not in the reference file. Yes, not the most efficient.