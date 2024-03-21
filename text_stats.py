#!/usr/bin/env python3

### --- IMPORT DEPENDENCIES --- ###
import sys
from time import time


### --- READ AND PROCESS FILE --- ###
def open_file(filename):
    """Read the contents of a (text) file

    Arg:
        filename (string): Name of the file to read contents from.
        
    Returns:
        File contents (list): A list of the contents on each line in the file. Not cleaned.
    """

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.readlines()
    except:
        print("The file does not exist!\nSome error occured while trying to read from the input file.")
        quit()


### --- CLEAN TEXT --- ###
def clean_text(text):
    """Clean the contents of one or multiple strings, given in a list.

    Details:
        The cleaning consists of multiple steps:
        Non-alphabetic characters are removed,
        all letters are changed to lowercase,
        the text is split into a list of all the words in the text.

        A word is here implicitly defined as any combination of (at least one) alhapabetic character(s).

    Arg:
        text (string) or (list of strings): String(s) to be cleaned.

    Returns:
        words (list of strings): A list of all the words that were found in the text.
    """

    # Make one long string of all the content
    if type(text) == list: text = " ".join(text)

    # Remove non-letter characters (except for " ") and change to lowercase
    text = "".join(filter(lambda x: x.isalpha() or x == " ", text))
    text = text.lower()

    # Split the string into a list of words
    text = text.split(" ")

    # Remove possible "" word
    text = list(filter(lambda x: x != "", text))

    return(text)


### --- TEXT ANALYSIS --- ###
def get_frequencies(words, look_for = "all", letter_freq = True):
    """Generate dictionaries for the frequencies of individual letters, words, and successor-words respectively.

    Arg:
        words (list of strings): A list of alphabetic strings.
        look_for (string or list): An optional argument specifying which words to get frequencies for.
            if "all", the frequencies for all words are calculated and returned.
        letter_freq (bool): Whether to calculate and return a letter frequency dict in addition to
            the word, and wordpair frequency dicts.

    Returns:
        wordcount (dict): A dict with words as keys, and their frequency as the value.
        lettercount (dict): A dict with alphabetic letters as keys, and their frequency as the value.
        wordpaircount (dict): A dict with tuples (word, successor) as keys, and the frequency of successor immediately following word as the value.
    """

    ## Count occurences of each letter and sort in descending order
    #lettercount = {}
    #for letter in "".join(words):
    #    if letter in lettercount:
    #        lettercount[letter] += 1
    #    else: lettercount[letter] = 1
    #lettercount = dict(sorted(lettercount.items(), key = lambda item: item[1], reverse=True))

    # Count occurences of all words and sort in descending order (old version)
    wordcount = {}
    for word in words:
        # Check if we should look for word
        if look_for == "all" or word in look_for:
            if word in wordcount:
                wordcount[word] += 1
            else: wordcount[word] = 1
    wordcount = dict(sorted(wordcount.items(), key = lambda item: item[1], reverse=True))

    # Count occurences of all words and sort in descending order (new version) (remove: it was worse)
    #wordcount = {}
    #for word in words: wordcount[word] = words.count(word)
    #wordcount = dict(sorted(wordcount.items(), key = lambda item: item[1], reverse=True))
    
    # Count all subsequent occurences and sort in descending order
    wordpaircount = {}
    for i in range(len(words)-1):
        # Check if we should look for main word
        if look_for == "all" or words[i] in look_for:
            # Check if we have already started counting this combination
            if (words[i], words[i+1]) in wordpaircount:
                wordpaircount[(words[i], words[i+1])] += 1
            else: wordpaircount[(words[i], words[i+1])] = 1
    wordpaircount = dict(sorted(wordpaircount.items(), key = lambda item: item[1], reverse=True))
    
    # Should letter freq also be computed?
    if letter_freq:
        # Count occurences of each letter and sort in descending order
        lettercount = {}
        for letter in "".join(words):
            if letter in lettercount:
                lettercount[letter] += 1
            else: lettercount[letter] = 1
        lettercount = dict(sorted(lettercount.items(), key = lambda item: item[1], reverse=True))

        return lettercount, wordcount, wordpaircount
    
    return wordcount, wordpaircount


### --- RUN THE PROGRAM FROM COMMAND LINE --- ###
if __name__ == "__main__":
    """(If run from command line): iniatie text analysis if given a file name."""
    print("\nText analysis program initiated...\n")

    # Time keeping
    start_time = time()

    # Process INPUT file
    if len(sys.argv) > 1:
        in_file_name = sys.argv[1]
    else:
        print("Missing file name.")
        quit()
    
    # Process potential OUTPUT file
    if len(sys.argv) > 2:
        try:
            out_file = open(sys.argv[2], "w") #closed at the end
            print("\nText analysis program initiated...\n", file=out_file)
        except:
            print("An error occured opening/creating the output file.")
            quit()
    else:
        out_file = None

    ### --- ANALYSE TEXT --- ###
    
    # Read the input file, clean the text, and analyse the text
    lines = open_file(filename = in_file_name)
    words = clean_text(lines)
    lettercount, wordcount, wordpaircount = get_frequencies(words)

    ## Format and print a FILE SUMMARY
    print("--- File summary for \"", in_file_name ,"\" ---", sep="", file=out_file)
    print("Total number of words: ", len(words), file=out_file)
    print("Unique number of words:", len(wordcount), file=out_file)

    ## Format and print a LETTER FREQUENCY TABLE
    print("\n--- Letter Frequency Table ---", file=out_file)
    print("{: >4} {: >4}".format(*("Letter", "Frequency")), file=out_file)
    print("{: >4} {: >4}".format(*("------", "---------")), file=out_file)
    for i in zip(lettercount, lettercount.values()):
        #percentage = i[1] / sum(lettercount.values())
        print("{: >4} {: >7}".format(*i), file=out_file)
    
    ## Format and print MOST FREQUENT WORDS and their CONSEQUENTS
    print("\n--- Most frequent words and their consequents ---", file=out_file)
    n_words = 5
    for word in iter(wordcount.items()):
        print(word[0], " (", wordcount[word[0]], " occurrences)", sep="", file=out_file)

        # Print the counts for words following the most common words
        n_subwords = 3
        common_pairs = filter(lambda key: key[0] == word[0], wordpaircount)
        for pair in common_pairs:
            subword_with_count = tuple((pair[1], wordpaircount[pair]))
            print("-- {: <8} {: >2}".format(*subword_with_count), file=out_file)

            # Check if all the first n_subwords subwords have been printed
            n_subwords -= 1
            if n_subwords == 0: break
        
        # Check if all the first n_words words have been printed
        n_words -= 1
        if n_words == 0: break
        else: print("\n", end="", file=out_file)
    
    # Close OUTPUT file
    if out_file != None:
        print("Analysis was successful, output is stored in \"", out_file.name, "\"", sep="")
        print("\nProgram run time:", round(time()-start_time, 1), "seconds.", file=out_file)
        out_file.close()
    
    print("\nProgram run time:", round(time()-start_time, 1), "seconds.")