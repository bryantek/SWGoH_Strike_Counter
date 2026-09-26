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

def highlight_tb_performers(data: pd.DataFrame) -> pd.DataFrame:
    """
    From a tb report from hotutils, highlight
        the player who achieved the most CM waves
        the player who won the CM wave "lottery"
            To encourage everyone to increase wave count,
            a CM wave (above the minimum) counts as a ticket to a raffle for a negative strike
        the player who donated the most toons/ships to operations
        the player who won the operations "lottery"
            similar as CM waves.
        the player with the most waves in each phase

    Args:
        data (pd.DataFrame): DataFrame containing Territory Battle data.
                            Format is assumed to be that of running the hotbot command "/tb stats"

    Returns:
        dataframe: A dataframe with allycode as the index and strike counts and allyname in respective columns.
    """
    return pd.DataFrame()

def highlight_tw_performers(data: pd.DataFrame) -> pd.DataFrame:
    """
    From a tw report from hotutils, highlight
        the player who achieved the most attack banners
        the player who achieved the most defense banners
        the player who achieved the most overall banners (minimum 100 banners of each)
        the player with the most holds

    Args:
        data (pd.DataFrame): DataFrame containing Territory Wars data.
                            Format is assumed to be that of running the hotbot command "/tw stats"

    Returns:
        dataframe: A dataframe with allycode as the index and strike counts and allyname in respective columns.
    """
    return pd.DataFrame()

def highlight_raid_performers(data: pd.DataFrame) -> pd.DataFrame:
    """
    From a raid report from hotutils, highlight
        the player who achieved the highest score
        the player who won the raid "lottery" (see highlight_tb_performers)

    Args:
        data (pd.DataFrame): DataFrame containing Raid data.
                            Format is assumed to be that of running the hotbot command "/raids download"

    Returns:
        dataframe: A dataframe with allycode as the index and strike counts and allyname in respective columns.
    """
    return pd.DataFrame()

def print_report_to_csv(strike_counts: pd.DataFrame, file_name: str) -> None:
    """
    Takes the strike_counts (usually created by highlight_X_performers) and prints to a csv for later use in collect_strikes.py.

    Args:
        strike_counts (pd.DataFrame): A dataframe with allycode as the index and strike counts and allyname in respective columns.
        file_name (str): where to save the file to

    Returns:
        None.
    """
    return None

def main():
    parser = argparse.ArgumentParser(description="A basic script to extract top performers from tw or tb reports by HotUtils.")
    parser.add_argument("-file", type=str, default=None, help="The path to the reference file of which guild members to include.")
    parser.add_argument("-type", type=str, default=None, help="The path to the reference file of which guild members to include.")
    args = parser.parse_args()

    missing_arguments = False
    if args.file is None:
        print("This function requires a file to parse top performers from.")
        return
    try:
        data = pd.read_csv(args.file, encoding='utf-8')
    except:  # This appears to catch the tickets file that hotutils exports.
        data = pd.read_csv(args.file, sep='\t', encoding='utf-16')
    match args.type:
        case "tb":
            strike_counts = highlight_tb_performers(data)
        case "tw":
            strike_counts = highlight_tw_performers(data)
        case "raid":
            strike_counts = highlight_raid_performers(data)
        case _:
            print("This function requires you to specify if 'tw' or 'tb' or 'raid' (no other option).")
            return
    print_report_to_csv(strike_counts)
    print("Saved top performer information to ...")

if __name__ == "__main__":
    main()
