import argparse
import pandas
import re
import json

names = { 
            "Twilight Sparkle": "twilight",
            "Applejack": "applejack",
            "Rarity": "rarity",
            "Pinkie Pie": "pinkie",
            "Rainbow Dash": "rainbow",
            "Fluttershy": "fluttershy"
            }

def compile_word_counts(df):
    pony_words = { "twilight": {}, "applejack": {}, "rarity": {}, "pinkie": {}, "rainbow": {}, "fluttershy": {} }
    
    #iterating over all rows in the dataframe which holds the script data
    for _, row in df.iterrows():
        speaker = row["pony"]
        dialog = row["dialog"]
        #in this loop we check if a pony is speaking and if they are we look for non dictionary words
        for pony, pony_shorthand in names.items():
            if(pony == speaker):
                #removing unicode characters
                words_in_dialog = re.sub("\\s*U\\+\\w+>\\s*", " ", dialog)
                #removing all punctuation and space characters and replacing them with a space character
                words_in_dialog = re.sub(r'[\(\)\[\]\,\-\.\?\!\:\;\#\& ]+', " ", words_in_dialog)
                #removing mutliple spaces
                words_in_dialog = re.sub(" +", " ", words_in_dialog)
                #splitting the sentence into individual words
                words_in_dialog = words_in_dialog.split()

                #for each used by this pony we will update its count in the dictionary
                for word in words_in_dialog:
                    #finding if the word contains a non alpha character
                    word_contains_non_alpha = re.search(r"[^a-zA-z]", word)
                    #if there was a non alpha character in the word then it will be != None and we ignore this word
                    if(word_contains_non_alpha != None):
                        continue
                    #otherwise we update the count
                    else:
                        word = word.lower()
                        pony_words[pony_shorthand][word] = 1 if word not in pony_words[pony_shorthand] else pony_words[pony_shorthand][word] + 1
    return pony_words

#helper method to remove words that appear < limit times
def remove_infrequent_words(pony_words, limit):
    for pony_name, words in list(pony_words.items()):
        for word, count in list(words.items()):
            if(count < limit):
                del pony_words[pony_name][word]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help="the name of the file to write the json output to")
    parser.add_argument("dialog_file", help="the path to clean_dialog.csv")
    args = parser.parse_args()

    output_location = args.o
    csv_path = args.dialog_file

    df = pandas.read_csv(csv_path)
    pony_words = compile_word_counts(df)
    remove_infrequent_words(pony_words, 5)

    with open(output_location, "w") as fp:
        json.dump(pony_words, fp, indent=2)

if __name__ == "__main__":
    main()