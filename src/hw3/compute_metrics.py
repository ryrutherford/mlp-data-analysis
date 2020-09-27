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
import os.path as osp
import pandas
import operator

def begin_computations(df, output_file):
    names = { 
            "Twilight Sparkle": "twilight",
            "Applejack": "applejack",
            "Rarity": "rarity",
            "Pinkie Pie": "pinkie",
            "Rainbow Dash": "rainbow",
            "Fluttershy": "fluttershy"
            }
    #calculate_verbosity(df, names)
    #calculate_mentions(df, names)
    #calculate_follow_on_comments(df, names)
    find_non_dict_words(df, names)

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
    return pony_mention_events

"""
this function will calculate the fraction of times a pony has a line that directly follows a character (ponies are treated individually, non ponies are treated as a group
"""
def calculate_follow_on_comments(df, names):
    pony_follow_on_events = {
            "twilight": {
                    "applejack": 0,
                    "rarity": 0,
                    "pinkie": 0,
                    "rainbow": 0,
                    "fluttershy": 0,
                    "other": 0,
                },
            "applejack": {
                    "twilight": 0,
                    "rarity": 0,
                    "pinkie": 0,
                    "rainbow": 0,
                    "fluttershy": 0,
                    "other": 0
                },
            "rarity": {
                    "applejack": 0,
                    "twilight": 0,
                    "pinkie": 0,
                    "rainbow": 0,
                    "fluttershy": 0,
                    "other": 0
                },
            "pinkie": {
                    "applejack": 0,
                    "rarity": 0,
                    "twilight": 0,
                    "rainbow": 0,
                    "fluttershy": 0,
                    "other": 0
                },
            "rainbow": {
                    "applejack": 0,
                    "rarity": 0,
                    "pinkie": 0,
                    "twilight": 0,
                    "fluttershy": 0,
                    "other": 0
                },
            "fluttershy": {
                    "applejack": 0,
                    "rarity": 0,
                    "pinkie": 0,
                    "rainbow": 0,
                    "twilight": 0,
                    "other": 0
                }
            }
    
    #will keep track of the total number of follow on comments a pony has made after other characters to help compute the fraction at the end
    num_follow_on_by_pony = {
            "twilight": 0,
            "applejack": 0,
            "rarity": 0,
            "pinkie": 0,
            "rainbow": 0,
            "fluttershy": 0
            }

    prev_speaker = None
    for speaker in df["pony"]:
        #iterating over each pony's full name and shorthand name and checking if they are the speaker
        for current_pony, current_pony_shorthand in names.items():
            if(current_pony in speaker):
                #prev_speaker_trimmed will remove pony names and things like "and" from the prev_speaker value
                #if prev_speaker_trimmed is empty after all the trimming has been done then the pony didn't speak after an "other" character
                prev_speaker_trimmed = prev_speaker
                #we are ignoring the case where the current pony was also speaking in the previous line as part of a group
                for pony, pony_shorthand in names.items():
                    if(current_pony != pony):
                        if(pony in prev_speaker):
                            pony_follow_on_events[current_pony_shorthand][pony_shorthand] += 1
                            num_follow_on_by_pony[current_pony_shorthand] += 1
                            prev_speaker_trimmed = re.sub(r"\bpony\b", "", prev_speaker_trimmed)
                
                if(prev_speaker != None):
                    prev_speaker_trimmed = re.sub(r"\band\b", "", prev_speaker_trimmed)
                    prev_speaker_trimmed = "".join(prev_speaker_trimmed.split())
                    if(prev_speaker_trimmed != ""):
                        pony_follow_on_events[current_pony_shorthand]["other"] += 1
                        num_follow_on_by_pony[current_pony_shorthand] += 1
        prev_speaker = speaker  
    for pony, other_ponies in pony_follow_on_events.items():
        #sum = 0
        for other_pony in other_ponies.keys():
            pony_follow_on_events[pony][other_pony] = float(pony_follow_on_events[pony][other_pony])/num_follow_on_by_pony[pony]
            #sum += pony_follow_on_events[pony][other_pony]
        #print(sum)
    print(pony_follow_on_events)
    return pony_follow_on_events

def find_non_dict_words(df, names):
    pony_non_dict_words = {
                "twilight": {
                    },
                "applejack": {
                    },
                "rarity": {
                    },
                "pinkie": {
                    },
                "rainbow": {
                    },
                "fluttershy": {
                    }
            }

    #finding the path to the file which contains valid english words
    project_dir = osp.dirname(osp.dirname(osp.dirname(__file__)))
    path_to_words_file = osp.join(project_dir, "data", "words_alpha.txt")
    #extracting the file into a data frame
    words_file = pandas.read_csv(path_to_words_file, header=None, names=["word"], dtype=str)
    #converting the file to a set (to facilitate looking up words)
    words_set = set(words_file["word"])
    
    #iterating over all rows in the datafram which holds the script data
    for index, row in df.iterrows():
        speaker = row["pony"]
        dialog = row["dialog"]
        #in this loop we check if a pony is speaking and if they are we look for non dictionary words
        for pony, pony_shorthand in names.items():
            if(pony in speaker):
                words_in_dialog = re.sub("\\s*u\\+\\w+>\\s*", " ", dialog.lower())
                #removing all non alphanumeric and space characters and replacing them with a space character
                words_in_dialog = re.sub(r'[^A-Za-z0-9 ]+', " ", words_in_dialog)
                #removing mutliple spaces
                words_in_dialog = re.sub(" +", " ", words_in_dialog)
                #splitting the sentence into individual words
                words_in_dialog = words_in_dialog.split();

                #for each non dictionary word used by this pony we will update its count in the pony_non_dict_words dictionary
                #at the end we will find the top 5 words
                for word in words_in_dialog:
                    if(word not in words_set):
                        if(word in pony_non_dict_words[pony_shorthand]):
                            pony_non_dict_words[pony_shorthand][word] += 1
                        else:
                            pony_non_dict_words[pony_shorthand][word] = 1
    #print(pony_non_dict_words)
    #we need to find the list of top 5 used words
    pony_non_dict_words_final = {
                "twilight": [
                    ],
                "applejack": [
                    ],
                "rarity": [
                    ],
                "pinkie": [
                    ],
                "rainbow": [
                    ],
                "fluttershy": [
                    ]
            }
    #we will iterate over each pony, sort their dictionary of non dictionary words and then make a list of the top 5 and add it to our new pony_non_dict_words_final dict
    for pony, non_dict_words in pony_non_dict_words.items():
        #converting the dict to a list
        sorted_non_dict_words = list(non_dict_words.items())
        #sorting the list
        sorted_non_dict_words.sort(key=operator.itemgetter(1), reverse=True)
        #print(sorted_non_dict_words)
        #taking the top 5 values
        sorted_non_dict_words = sorted_non_dict_words[0:5]
        #function used to select only the word in list comprehension
        f = lambda val: val[0]
        sorted_non_dict_words = [f(i) for i in sorted_non_dict_words]
        #setting the value to be the list
        pony_non_dict_words_final[pony] = sorted_non_dict_words
    print(pony_non_dict_words_final)
    return pony_non_dict_words_final
