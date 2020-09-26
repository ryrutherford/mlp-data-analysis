"""
This module contains the code to compute metrics for:
    - verbosity
    - mentions
    - follow on comments
    - non dictionary words spoken
for each pony:
    - Twilight Sparkle (twilight),
    - Applejack (applejack),
    - Rarity (rarity),
    - Pinkie Pie (pinkie),
    - Rainbow Dash (rainbow), and
    - Fluttershy (fluttershy)
"""

import re

def begin_computations(df, output_file):
    names = { 
            "Twilight Sparkle": "twilight",
            "Applejack": "applejack",
            "Rarity": "rarity",
            "Pinkie Pie": "pinkie",
            "Rainbow Dash": "rainbow",
            "Fluttershy": "fluttershy"
            }
    calculate_verbosity(df, names)
    calculate_mentions(df, names)

"""
this function will calculate the verbosity for each pony (the fraction of dialog events that each pony has)
"""
def calculate_verbosity(df, names):
    pony_dialog_events = {
                "twilight": 0,
                "applejack": 0,
                "rarity": 0,
                "pinkie": 0,
                "rainbow": 0,
                "fluttershy": 0
            }
    num_dialog_events = 0
    prev_speaker = None
    for speaker in df["pony"]:
        for dialog_name, data_name in names.items():
            if(dialog_name in speaker):
                #if the pony is part of the current speaker string (either speaking alone or part of a group) and the same group (or pony) isn't speaking consecutively,
                #then we increment the count
                #i.e. we only increment the count when the pony is speaking and the current speaker is not the same as the last speaker
                #e.g. Narrator and Fluttershy are previous speaker and Fluttershy is the current speaker --> increment the count
                #e.g. Narrator and Fluttershy are previous speaker and Narrator and Fluttershy are current speaker --> don't increment the count
                if(prev_speaker != speaker):
                    pony_dialog_events[data_name] += 1
                    num_dialog_events += 1
        prev_speaker = speaker
    sum = 0
    for data_name in names.values():
        pony_dialog_events[data_name] = float(pony_dialog_events[data_name])/num_dialog_events
        sum += pony_dialog_events[data_name]
    print(pony_dialog_events)
    print(sum)
    return pony_dialog_events

"""
this function will calculate the number of times each pony mentions the other as a fraction
"""
def calculate_mentions(df, names):
    pony_mention_events = {
            "twilight": {
                    "applejack": 0,
                    "rarity": 0,
                    "pinkie": 0,
                    "rainbow": 0,
                    "fluttershy": 0
                },
            "applejack": {
                    "twilight": 0,
                    "rarity": 0,
                    "pinkie": 0,
                    "rainbow": 0,
                    "fluttershy": 0
                },
            "rarity": {
                    "applejack": 0,
                    "twilight": 0,
                    "pinkie": 0,
                    "rainbow": 0,
                    "fluttershy": 0
                },
            "pinkie": {
                    "applejack": 0,
                    "rarity": 0,
                    "twilight": 0,
                    "rainbow": 0,
                    "fluttershy": 0
                },
            "rainbow": {
                    "applejack": 0,
                    "rarity": 0,
                    "pinkie": 0,
                    "twilight": 0,
                    "fluttershy": 0
                },
            "fluttershy": {
                    "applejack": 0,
                    "rarity": 0,
                    "pinkie": 0,
                    "rainbow": 0,
                    "twilight": 0
                }
            }
    
    #will keep track of the total number of mentions a pony has made of other ponies to help compute the fraction at the end
    num_mentions_by_pony = {
            "twilight": 0,
            "applejack": 0,
            "rarity": 0,
            "pinkie": 0,
            "rainbow": 0,
            "fluttershy": 0
            }

    for index, row in df.iterrows():
        speaker = row["pony"]
        dialog = row["dialog"]
        #iterating over each pony's full name and shorthand name and checking if they are the speaker
        for current_pony, current_pony_shorthand in names.items():
            #checking if the current_pony is speaking
            if(current_pony in speaker):
                #we will now check for mentions of the other ponies in the dialog
                for pony, pony_shorthand in names.items():
                    #if current_pony == pony then we are looking at when a pony mentions itself which we don't care about
                    if(current_pony != pony):
                        #since mentions of one part of a Pony's name count as a mention we need to count all occurences of any mention of part of the pony's name
                        #and then subtract the number of mentions of the full Pony's name * the number of words in the pony's name to account for the differences
                        split_name = pony.split(" ")

                        #counting all mentions of any part of the pony's name
                        for part_of_name in split_name:
                            mentions_of_pon = len(re.findall(r"\b"+part_of_name+r"\b", dialog))
                            pony_mention_events[current_pony_shorthand][pony_shorthand] += mentions_of_pon
                            num_mentions_by_pony[current_pony_shorthand] += mentions_of_pon
                        
                        #subtracting the amount that we overcounted
                        split_name_len = len(split_name)
                        if(split_name_len > 1):
                            mentions_of_full_name = (split_name_len -1)*len(re.findall(r"\b"+pony+r"\b", dialog))
                            pony_mention_events[current_pony_shorthand][pony_shorthand] -= mentions_of_full_name
                            num_mentions_by_pony[current_pony_shorthand] -= mentions_of_full_name
    for pony, other_ponies in pony_mention_events.items():
        #sum = 0
        for other_pony in other_ponies.keys():
            pony_mention_events[pony][other_pony] = float(pony_mention_events[pony][other_pony])/num_mentions_by_pony[pony]
            #sum += pony_mention_events[pony][other_pony]
        #print(sum)
    print(pony_mention_events)

def calculate_follow_on_comments(df):
    pass

def find_non_dict_words(df):
    pass


