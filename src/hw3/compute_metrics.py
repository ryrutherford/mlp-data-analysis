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
import json

def begin_computations(df, output_file):
    names = { 
            "Twilight Sparkle": "twilight",
            "Applejack": "applejack",
            "Rarity": "rarity",
            "Pinkie Pie": "pinkie",
            "Rainbow Dash": "rainbow",
            "Fluttershy": "fluttershy"
            }
    verbosity = calculate_verbosity(df, names)
    mentions = calculate_mentions(df, names)
    follow_on = calculate_follow_on_comments(df, names)
    non_dict = find_non_dict_words(df, names)
    all_stats = {
                "verbosity": verbosity,
                "mentions": mentions,
                "follow_on_comments": follow_on,
                "non_dictionary_words": non_dict
            }
    if(output_file != None):
        with open(output_file, "w") as out:
            json.dump(all_stats, out, indent = 2, separators=(',', ': '))
    else:
        print(json.dumps(all_stats, indent = 2, separators=(',', ': ')))


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
    #prev_{var} indicates the value of the previous instance of that variable
    prev_speaker = None
    prev_title = None
    for index, row in df.iterrows():
        speaker = row["pony"]
        title = row["title"]
        other_speaking = True
        for dialog_name, data_name in names.items():
            #if the current speaker is equal to the pony (and only the pony) and the prev_speaker was not the pony or the previous line was from a diff episode
            #we increment the dialog event count for that pony
            if(dialog_name == speaker):
                if(prev_speaker != speaker or prev_title != title):
                    #we set other_speaking to False because it means "others" were not speaking
                    other_speaking = False
                    pony_dialog_events[data_name] += 1
                    num_dialog_events += 1
                    break
        #if other_speaking is True then a pony wasn't speaking on its own and if prev_speaker != speaker then this is new dialog for the other character
        if(other_speaking == True and prev_speaker != speaker):
            num_dialog_events += 1
        prev_speaker = speaker
        prev_title = title
    for data_name in names.values():
        pony_dialog_events[data_name] = 0 if num_dialog_events == 0 else float(pony_dialog_events[data_name])/num_dialog_events
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
            #checking if the current_pony is speaking (we only care about when teh pony is the sole speaker)
            if(current_pony == speaker):
                #we will now check for mentions of the other ponies in the dialog
                for pony, pony_shorthand in names.items():
                    #if current_pony == pony then we are looking at when a pony mentions itself which we don't care about
                    if(current_pony != pony):
                        #since mentions of one part of a Pony's name count as a mention we need to count all occurences of any mention of part of the pony's name
                        #and then subtract the number of mentions of the full Pony's name * the number of words in the pony's name to account for the differences
                        split_name = pony.split(" ")

                        #counting all mentions of any part of the pony's name
                        for part_of_name in split_name:
                            mentions_of_pony = len(re.findall(r"\b"+part_of_name+r"\b", dialog))
                            pony_mention_events[current_pony_shorthand][pony_shorthand] += mentions_of_pony
                            num_mentions_by_pony[current_pony_shorthand] += mentions_of_pony
                        
                        #subtracting the amount that we overcounted
                        split_name_len = len(split_name)
                        if(split_name_len > 1):
                            mentions_of_full_name = (split_name_len -1)*len(re.findall(r"\b"+pony+r"\b", dialog))
                            pony_mention_events[current_pony_shorthand][pony_shorthand] -= mentions_of_full_name
                            num_mentions_by_pony[current_pony_shorthand] -= mentions_of_full_name

    #computing the fraction instead of the count of mentions that we currently have
    for pony, other_ponies in pony_mention_events.items():
        for other_pony in other_ponies.keys():
            pony_mention_events[pony][other_pony] = 0 if num_mentions_by_pony[pony] == 0 else float(pony_mention_events[pony][other_pony])/num_mentions_by_pony[pony]
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

    prev_title = None
    prev_speaker = None
    for index, row in df.iterrows():
        speaker = row["pony"]
        title = row["title"]
        
        #if the current title and previous title are different then we set prev_speaker to None so that no follow ons are counted crossing over episodes
        if(title != prev_title and prev_speaker != None):
            prev_speaker = None

        #other_speaking variable indicates whether a non pony char is speaking
        other_speaking = True
        
        #iterating over each pony's full name and shorthand name and checking if they are the speaker
        for current_pony, current_pony_shorthand in names.items():
        
            #if the previous speaker is None then we don't care about who's speaking now because they're not following anyone
            if(prev_speaker == None):
                break

            #if the current pony is speaking we check if this dialog followed another pony's line
            if(current_pony == speaker):
                
                #checking all the other ponies to see if they were the previous speaker
                for pony, pony_shorthand in names.items():
                
                    if(current_pony != pony and pony == prev_speaker):
                        pony_follow_on_events[current_pony_shorthand][pony_shorthand] += 1
                        num_follow_on_by_pony[current_pony_shorthand] += 1
                        other_speaking = False
                        break
                    #if the current pony was also the previous speaker then we set other_speaking to false since another char wasn't speaking and neither was another pony
                    elif(current_pony == pony and current_pony == prev_speaker):
                        other_speaking = False
                        break
                
                #checking if the current_pony was speaking after a non top 6 pony
                if(other_speaking == True):
                    pony_follow_on_events[current_pony_shorthand]["other"] += 1
                    num_follow_on_by_pony[current_pony_shorthand] += 1
                #if other_speaking = False then we've already determined that this line follows another pony's line so we don't need to continue looping
                else:
                    break
        prev_speaker = speaker
        prev_title = title

    #calculating the fraction of follow on events
    for pony, other_ponies in pony_follow_on_events.items():
        for other_pony in other_ponies.keys():
            pony_follow_on_events[pony][other_pony] = 0 if num_follow_on_by_pony[pony] == 0 else float(pony_follow_on_events[pony][other_pony])/num_follow_on_by_pony[pony]
    
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
            if(pony == speaker):
                words_in_dialog = re.sub("\\s*U\\+\\w+>\\s*", " ", dialog)
                #removing all non alphanumeric and space characters and replacing them with a space character
                words_in_dialog = re.sub(r'[^A-Za-z0-9 ]+', " ", words_in_dialog)
                #removing mutliple spaces
                words_in_dialog = re.sub(" +", " ", words_in_dialog)
                #splitting the sentence into individual words
                words_in_dialog = words_in_dialog.split();

                #for each non dictionary word used by this pony we will update its count in the pony_non_dict_words dictionary
                #at the end we will find the top 5 words
                for word in words_in_dialog:
                    if(word.lower() not in words_set):
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
        #taking the top 5 values
        sorted_non_dict_words = sorted_non_dict_words[0:5]
        #function used to select only the word in list comprehension
        f = lambda val: val[0]
        sorted_non_dict_words = [f(i) for i in sorted_non_dict_words]
        #setting the value to be the list
        pony_non_dict_words_final[pony] = sorted_non_dict_words
    return pony_non_dict_words_final
