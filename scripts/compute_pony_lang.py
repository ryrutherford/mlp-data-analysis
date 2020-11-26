import argparse
import json
import math

#helper function to count the total number of words spoken in the script
#returns the total number of words spoken by all ponies, the word count for each word by pony, the number of ponies that mention each word
def find_totals(pony_counts):
    total = 0
    total_word_counts = {}
    pony_word_counts = {}
    for _, words in pony_counts.items():
        for word, count in words.items():
            total_word_counts[word] = count if word not in total_word_counts else total_word_counts[word] + count
            total += count
            pony_word_counts[word] = 1 if word not in pony_word_counts else pony_word_counts[word] + 1
    return total, total_word_counts, pony_word_counts

#compute the tfidf for each word
def compute_tfidf(pony_counts, use_new_method):
    total_words, total_word_counts, pony_word_counts = find_totals(pony_counts)
    for pony, words in pony_counts.items():
        for word, tf in words.items():
            if(use_new_method):
                idf = math.log(6/pony_word_counts[word])
            else:
                idf = math.log(total_words/total_word_counts[word])
            pony_counts[pony][word] = tf*idf

#finds the num_words words with the highest tfidf count for each pony
def find_highest_tfidfs(tfidf_counts, num_words):
    for pony, words in tfidf_counts.items():
        sorted_tfidfs = sorted(words.items(), key=lambda x: x[1], reverse=True)[:num_words]
        sorted_tfidfs = list(map(lambda tup: tup[0], sorted_tfidfs))
        tfidf_counts[pony] = sorted_tfidfs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="Use improved version of tfidf", action="store_true")
    parser.add_argument("pony_counts", help="the name of the json file which contains the pony word counts")
    parser.add_argument("num_words", help="the number of words to find the highest tfidf score for each pony", type=int)
    args = parser.parse_args()

    p = args.p
    pony_counts = args.pony_counts
    num_words = args.num_words

    with open(pony_counts, "r") as fp:
        pony_counts = json.load(fp)
    
    compute_tfidf(pony_counts, p)
    find_highest_tfidfs(pony_counts, num_words)

    print(json.dumps(pony_counts, indent=2))

if __name__ == "__main__":
    main()