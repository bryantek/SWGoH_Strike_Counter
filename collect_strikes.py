import pandas as pd
import os
import glob
from GUILD_THRESHOLDS import MINIMUM_CM_WAVES, MINIMUM_CM_WAVES_DOUBLE_STRIKE, MINIMUM_DEPLOY_THRESHOLD, MINIMUM_RAID_SCORE, MINIMUM_TICKET_COUNT, MINIMUM_TW_ATTACK_BANNERS, MINIMUM_TW_ATTACK_COUNT, MINIMUM_TW_BANNERS, MINIMUM_TW_DEFENSE_BANNERS
from member_profile import GuildMember
import time


def gather_strikes(reports_dir: str="Reports"):
    guild_member_strikes: dict[int,int] = {}  # ally code as key. strike count as value.
    allycode_to_name: dict[int,str] = {}

    # Load CSV files (Territory War/General stats/TB Stats/Raid Stats)
    csv_files = glob.glob(os.path.join(reports_dir, "*.csv"))
    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        print(f"Reading file: {file_name}")
        try:
            data = pd.read_csv(file_path, encoding='utf-8')
        except:  # This appears to catch the tickets file that hotutils exports.
            data = pd.read_csv(file_path, sep='\t', encoding='utf-16')
        match file_name[:7]:
            case "tickets":  # Daily Tickets
                strike_counts, new_allycode_to_name = collect_ticket_strikes(data)
            case "twstats":  # TW
                strike_counts, new_allycode_to_name = collect_tw_strikes(data)
            case "raidsta":  # Raid
                strike_counts, new_allycode_to_name = collect_raid_strikes(data)
            case "tbstats":  # TB
                strike_counts, new_allycode_to_name = collect_tb_strikes(data)
            case _:  # Ignore anything else. Skip to the next file in the loop.
                continue
        allycode_to_name.update(new_allycode_to_name)
        for key, val in strike_counts.items():  # There is probably a more efficient way.
            guild_member_strikes[key] = guild_member_strikes.get(key, 0) + val
    return guild_member_strikes, allycode_to_name

def parse_ticket_count(x: str):
    if x=='-':
        return 600
    return int(x)

def collect_ticket_strikes(data: pd.DataFrame):
    # Loop through the ticket tracking file and collect daily strikes.
    daily_strike = data.iloc[:,5:].map(lambda x: parse_ticket_count(x)<MINIMUM_TICKET_COUNT)
    total_strikes = daily_strike.apply(lambda row: sum(row), axis=1)
    return dict(zip(data["AllyCode"], total_strikes)), dict(zip(data["AllyCode"],data["Name"]))

def collect_tw_strikes(data: pd.DataFrame):
    # Loop through the file and collect strikes based on the TW.
    total_tw_strikes = dict.fromkeys(set(data["AllyCode"]).difference([0]), 0)
    for row in data.itertuples():
        # The time recorded by hotutils has the decimal removed: a factor of 10000 greater.
        if row.CurrentRoundEndTime > 10000*time.time():  # Skip active TW information
            continue
        match row.MapStatId:
            case "stars":
                if row.Score < MINIMUM_TW_BANNERS:
                    total_tw_strikes[row.AllyCode] += 1
            case "set_defense_stars":
                if row.Score < MINIMUM_TW_DEFENSE_BANNERS:
                    total_tw_strikes[row.AllyCode] += 1
            case "attack_stars":
                if row.Score < MINIMUM_TW_ATTACK_BANNERS:
                    total_tw_strikes[row.AllyCode] += 1
            case "disobey":
                if row.Score < MINIMUM_TW_ATTACK_COUNT:
                    total_tw_strikes[row.AllyCode] += 1
            case _:  # Ignore values I don't know about. Maybe print an error message.
                continue
    return total_tw_strikes, dict(zip(data["AllyCode"],data["Name"]))

def collect_raid_strikes(data: pd.DataFrame):
    # Loop through the file and collect strikes based on the raid.
    total_raid_strikes = dict.fromkeys(set(data["AllyCode"]).difference([0]), 0)
    for row in data.itertuples():
        # print(row)
        # All raids captured have already been completed.
        if row.AllyCode == 0:  # The player is no longer in the guild.
            continue
        if row.Score < MINIMUM_RAID_SCORE:
            # print(f"{row.AllyCode} ------ {row.Score}")
            total_raid_strikes[row.AllyCode] += 1
    return total_raid_strikes, dict(zip(data["AllyCode"],data["Name"]))

def collect_tb_strikes(data: pd.DataFrame):
    # Loop through the file and collect strikes based on the TB.
    # Everyone starts with 10 strikes. Each time they deploy in phases 2-6, they remove 2 strikes.
    total_tb_strikes = dict.fromkeys(set(data["AllyCode"]).difference([0]), 10)
    for row in data.itertuples():
        match row.MapStatId:
            case "strike_encounter":
                if row.Score < MINIMUM_CM_WAVES_DOUBLE_STRIKE:
                    total_tb_strikes[row.AllyCode] += 2
                elif MINIMUM_CM_WAVES:
                    total_tb_strikes[row.AllyCode] += 1
            case "covert_results_round_1":
                total_tb_strikes[row.AllyCode] -= row.SpecialResults.count("Succeeded")
            case "covert_results_round_2":
                if "Cere/Cal Kestis:Unattempted" in row.SpecialResults:
                    total_tb_strikes[row.AllyCode] += 1
                total_tb_strikes[row.AllyCode] -= row.SpecialResults.count("Succeeded")
            case "covert_results_round_3":
                if "Bo/BAM Mandalore Unlock:Unattempted" in row.SpecialResults:
                    total_tb_strikes[row.AllyCode] += 1
                total_tb_strikes[row.AllyCode] -= row.SpecialResults.count("Succeeded")
            case "covert_results_round_4":
                total_tb_strikes[row.AllyCode] -= row.SpecialResults.count("Succeeded")
            case "covert_results_round_5":
                total_tb_strikes[row.AllyCode] -= row.SpecialResults.count("Succeeded")
            case "covert_results_round_6":
                total_tb_strikes[row.AllyCode] -= row.SpecialResults.count("Succeeded")
            case "power_round_2":  # I would love to combine this with the other power_round_#
                if row.Score >= MINIMUM_DEPLOY_THRESHOLD:
                    total_tb_strikes[row.AllyCode] -= 2
            case "power_round_3":
                if row.Score >= MINIMUM_DEPLOY_THRESHOLD:
                    total_tb_strikes[row.AllyCode] -= 2
            case "power_round_4":
                if row.Score >= MINIMUM_DEPLOY_THRESHOLD:
                    total_tb_strikes[row.AllyCode] -= 2
            case "power_round_5":
                if row.Score >= MINIMUM_DEPLOY_THRESHOLD:
                    total_tb_strikes[row.AllyCode] -= 2
            case "power_round_6":
                if row.Score >= MINIMUM_DEPLOY_THRESHOLD:
                    total_tb_strikes[row.AllyCode] -= 2
            case _:  # Ignore values we don't care about.
                continue
    return total_tb_strikes, dict(zip(data["AllyCode"],data["Name"]))

def print_for_discord(strike_counts, allycode_to_name_decoder):
    sorted_dict = dict(sorted(strike_counts.items(), key=lambda item: -item[1]))
    for allycode, strike_count in sorted_dict.items():
        print(f"{strike_count} --- {allycode_to_name_decoder[allycode]} : {allycode}")

def main():
    strike_counts, allycode_to_name_decoder = gather_strikes()
    print("Printing strike counts:")
    print_for_discord(strike_counts, allycode_to_name_decoder)

if __name__ == "__main__":
    main()
