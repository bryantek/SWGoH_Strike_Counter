# Backlog

This is a list of improvements to be made.
 - A feature to provide a single ally code and automatically extract information from the files in Reports/
   - Either all pieces of information related to that ally code or
   - Just the (increasing/decreasing) strike count actions.
 - Include an optional file to import that manually adjusts players strike counts up or down. (To address things not captured by this script.)
 - Active TW are ignored based on timestamp. It may be useful to also automatically ignore any TW in tw files that were collected during its sign-up phase.
 - Currently all of every file in [Reports/](Reports/) is included in strike collection. Add a time cutoff that automatically ignores anything before a given timestamp.
 - Adjust ticket strike tracking to have the option to count by average. Or give partial strikes (e.g. 300/600 tickets is 1/2 strike). And an *option* for negative strikes. E.g. if a guild has a minimum of 500 tickets/day, then a member who always gets 600 tickets/day will get -1/6 strikes per day (*if* the guild turns on negative ticket strikes).
 - If someone goes *all defense* in TW, there isn't a way to separately check that they 1. placed enough defense and 2. don't strike them for not attacking. This could be done manually once that feature is enabled.
 - Currently checking if someone didn't deploy in TB (and thus gets a strike) works by pre-assigning strikes to everyone, then removing strikes if they did deploy. It is done this way because a deploy of 0 doesn't show up in the csv output by Hotbot. But this assumes that there is a spot to deploy each phase (which for some guilds there may not be).
 - Specific special mission checks are currently by round. E.g. if your guild attempts the Zeffo Unlock SM in phase 3, this script incorrectly checks for the attempt in phase 2.