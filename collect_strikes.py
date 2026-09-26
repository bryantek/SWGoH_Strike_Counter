import argparse
import glob
import os
import pandas as pd
import time
from GUILD_THRESHOLDS import (
    MINIMUM_CM_WAVES, 
    MINIMUM_CM_WAVES_DOUBLE_STRIKE, 
    MINIMUM_CM_WAVES_NEGATIVE_STRIKE,
    NEGATIVE_STRIKE_FOR_SM_SUCCESS,
    MINIMUM_DEPLOY_THRESHOLD, 
    MINIMUM_RAID_SCORE, 
    MINIMUM_RAID_SCORE_DOUBLE_STRIKE, 
    MINIMUM_TICKET_COUNT, 
    MINIMUM_TW_ATTACK_BANNERS, 
    MINIMUM_TW_ATTACK_COUNT, 
    MINIMUM_TW_BANNERS, 
    MINIMUM_TW_DEFENSE_BANNERS,
    MINIMUM_TW_ALL_DEFENSE_BANNERS
)


def gather_strikes(reports_dir: str="Reports", reference_file: str = None):
    """
    Gathers strike counts for guild members from various reports.

    Args:
        reports_dir (str): Directory containing the reports. Default: "Reports".
        reference_file (str): if None, collects information on all members in all reports.
                                If specified, only those members listed in the reference file. Usually the most recent tickets file.
                                    Technically the information is collected on everyone, but only the specified ones are returned.
                                Assumes that the reference file lives within the reports_dir.
                                If the reference file doesn't exist, then it is the same as reference_file=None.

    Returns:
        tuple: A tuple containing a dictionary of strike counts and a dictionary of ally code to name mappings.
    """
    guild_member_strikes: dict[int,int] = {}  # ally code as key. strike count as value.
    allycode_to_name: dict[int,str] = {}

    # Load CSV files (Territory War/Tickets/Territory Battle/Raid)
    guild_members_set: set[int] = None
    csv_files = glob.glob(os.path.join(reports_dir, "*.csv"))
    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        print(f"Reading file: {file_name}")
        try:
            data = pd.read_csv(file_path, encoding='utf-8')
        except:  # This appears to catch the tickets file that hotutils exports.
            data = pd.read_csv(file_path, sep='\t', encoding='utf-16')
        if file_name == reference_file:  # To avoid loading it again later.
            guild_members_set: set[int] = set(data["AllyCode"])
        match file_name:
            case str() if file_name.startswith("tickets"):  # Daily Tickets
                strike_counts, new_allycode_to_name = collect_ticket_strikes(data)
            case str() if file_name.startswith("tw"):  # TW
                strike_counts, new_allycode_to_name = collect_tw_strikes(data)
            case str() if file_name.startswith("raid"):  # Raid
                strike_counts, new_allycode_to_name = collect_raid_strikes(data)
            case str() if file_name.startswith("tb"):  # TB
                strike_counts, new_allycode_to_name = collect_tb_strikes(data)
            case str() if file_name.startswith("manual"):  # Manual
                strike_counts, new_allycode_to_name = collect_manual_strikes(data)
            case _:  # Ignore anything else. Skip to the next file in the loop.
                continue
        allycode_to_name.update(new_allycode_to_name)
        for key, val in strike_counts.items():  # There is probably a more efficient way.
            guild_member_strikes[key] = guild_member_strikes.get(key, 0) + val
    
    if guild_members_set is None:  # Don't need to filter. Either there wasn't a file to filter, or the file doesn't exist.
        return guild_member_strikes, allycode_to_name
    else:
        return {k: guild_member_strikes[k] for k in guild_members_set}, {k: allycode_to_name[k] for k in guild_members_set}

def collect_ticket_strikes(data: pd.DataFrame):
    """
    Collects strike counts from ticket tracking data.

    Args:
        data (pd.DataFrame): DataFrame containing ticket tracking data.
                            Format is assumed to be that of exporting to csv from the Guild->Tickets section of HotUtils' website

    Returns:
        tuple: A tuple containing a dictionary of strike counts and a dictionary of ally code to name mappings.
    """
    def parse_ticket_count(x: str):
        """ A helper function for collect_ticket_strikes.
        If a member was not in the guild for all past days, then their count is "-".
        This gets parsed to 600 so they don't receive a strike.
        """
        if x=='-':
            return 600
        return int(x)
    # Loop through the ticket tracking file and collect daily strikes.
    daily_strike = data.iloc[:,5:].map(lambda x: parse_ticket_count(x)<MINIMUM_TICKET_COUNT)
    total_strikes = daily_strike.apply(lambda row: sum(row), axis=1)
    return dict(zip(data["AllyCode"], total_strikes)), dict(zip(data["AllyCode"],data["Name"]))

def collect_tw_strikes(data: pd.DataFrame):
    """
    Collects strike counts from Territory War data.

    Args:
        data (pd.DataFrame): DataFrame containing Territory War data.
                            Format is assumed to be that of running the hotbot command "/tw stats"

    Returns:
        tuple: A tuple containing a dictionary of strike counts and a dictionary of ally code to name mappings.
    """
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
                if row.Score >= MINIMUM_TW_ALL_DEFENSE_BANNERS:
                    total_tw_strikes[row.AllyCode] -= 1
                elif row.Score < MINIMUM_TW_DEFENSE_BANNERS:
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
    """
    Collects strike counts from Raid data.

    Args:
        data (pd.DataFrame): DataFrame containing Raid data.
                            Format is assumed to be that of running the hotbot command "/raids download"

    Returns:
        tuple: A tuple containing a dictionary of strike counts and a dictionary of ally code to name mappings.
    """
    # Loop through the file and collect strikes based on the raid.
    total_raid_strikes = dict.fromkeys(set(data["AllyCode"]).difference([0]), 0)
    for row in data.itertuples():
        # All raids captured have already been completed.
        if row.AllyCode == 0:  # The player is no longer in the guild.
            continue
        if row.Score < MINIMUM_RAID_SCORE_DOUBLE_STRIKE:
            total_raid_strikes[row.AllyCode] += 2
        elif row.Score < MINIMUM_RAID_SCORE:
            total_raid_strikes[row.AllyCode] += 1
    return total_raid_strikes, dict(zip(data["AllyCode"],data["Name"]))

def collect_tb_strikes(data: pd.DataFrame):
    """
    Collects strike counts from Territory Battle data.

    Args:
        data (pd.DataFrame): DataFrame containing Territory Battle data.
                            Format is assumed to be that of running the hotbot command "/tb stats"

    Returns:
        tuple: A tuple containing a dictionary of strike counts and a dictionary of ally code to name mappings.
    """
    # Loop through the file and collect strikes based on the TB.
    # This uses the csv output from HotUtils. Potentially the excel output has more information.
    # Everyone starts with 10 strikes. Each time they deploy in phases 2-6, they remove 2 strikes.
    total_tb_strikes = dict.fromkeys(set(data["AllyCode"]).difference([0]), 10)
    for row in data.itertuples():  # There is likely a more efficient way to apply functions to this dataframe.
        match row.MapStatId:
            case "strike_encounter":
                if row.Score >= MINIMUM_CM_WAVES_NEGATIVE_STRIKE:
                    total_tb_strikes[row.AllyCode] -= 1
                elif row.Score < MINIMUM_CM_WAVES_DOUBLE_STRIKE:
                    total_tb_strikes[row.AllyCode] += 2
                elif row.Score < MINIMUM_CM_WAVES:
                    total_tb_strikes[row.AllyCode] += 1
            
            case "covert_results_round_1":
                total_tb_strikes[row.AllyCode] -= NEGATIVE_STRIKE_FOR_SM_SUCCESS * row.SpecialResults.count("Succeeded")
            case "covert_results_round_2":
                if "Cere/Cal Kestis:Unattempted" in row.SpecialResults:
                    total_tb_strikes[row.AllyCode] += 1
                total_tb_strikes[row.AllyCode] -= NEGATIVE_STRIKE_FOR_SM_SUCCESS * row.SpecialResults.count("Succeeded")
            case "covert_results_round_3":
                if "Bo/BAM Mandalore Unlock:Unattempted" in row.SpecialResults:
                    total_tb_strikes[row.AllyCode] += 1
                total_tb_strikes[row.AllyCode] -= NEGATIVE_STRIKE_FOR_SM_SUCCESS * row.SpecialResults.count("Succeeded")
            case "covert_results_round_4":
                total_tb_strikes[row.AllyCode] -= NEGATIVE_STRIKE_FOR_SM_SUCCESS * row.SpecialResults.count("Succeeded")
            case "covert_results_round_5":
                total_tb_strikes[row.AllyCode] -= NEGATIVE_STRIKE_FOR_SM_SUCCESS * row.SpecialResults.count("Succeeded")
            case "covert_results_round_6":
                total_tb_strikes[row.AllyCode] -= NEGATIVE_STRIKE_FOR_SM_SUCCESS * row.SpecialResults.count("Succeeded")
            
            case "power_round_2":  # I would love to combine this with the other power_round_# cases.
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

def collect_manual_strikes(data: pd.DataFrame):
    """
    Collects strike counts from a csv.
    These files may be outputs of top_performers.py but can be manually created.

    Args:
        data (pd.DataFrame): DataFrame containing manual adjustments to strike counts.
                            Assumes the format is 3 columns: AllyCode, Name, StrikeCount

    Returns:
        tuple: A tuple containing a dictionary of strike counts and a dictionary of ally code to name mappings.
    """
    return dict(zip(data["AllyCode"],data["StrikeCount"])), dict(zip(data["AllyCode"],data["Name"]))

def print_all_strike_counts(strike_counts, allycode_to_name_decoder):
    """
    Prints all strike counts in descending order.

    Args:
        strike_counts (dict): Dictionary containing ally code and strike counts.
        allycode_to_name_decoder (dict): Dictionary containing ally code and names.
    """
    sorted_dict = dict(sorted(strike_counts.items(), key=lambda item: -item[1]))
    for allycode, strike_count in sorted_dict.items():
        print(f"{strike_count} --- {allycode_to_name_decoder[allycode]} : {allycode}")

def main():
    parser = argparse.ArgumentParser(description="A basic script to collate information from HotUtils reports of a SWGoH guild.")
    parser.add_argument("-reference_file", type=str, default=None, help="The path to the reference file of which guild members to include.")
    args = parser.parse_args()

    strike_counts, allycode_to_name_decoder = gather_strikes(reference_file=args.reference_file)
    print("Printing strike counts:")
    print_all_strike_counts(strike_counts, allycode_to_name_decoder)

if __name__ == "__main__":
    main()
