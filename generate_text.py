#!/usr/bin/env python3

### --- IMPORT DEPENDENCIES --- ###
import sys
from time import time
import text_stats
import numpy as np

### --- RUN THE PROGRAM FROM COMMAND LINE --- ###
if __name__ == "__main__":
    """(If run from command line): iniatie text generation if given a file name, start word and text length.
    
    The program works by successively building up two dictionaries; word_count, and wordpair_count as they
    are needed, rather than generating them completely in the beginning of the program.

    word_count stores words as keys, and the frequency of that word in the file as the value. This dictionary
    also doubles as a record of which words have been added to both dictionaries so far.
    
    wordpair_count stores keys in the form of 2-tuples (word, successor), with the value being the amount of
    times that successor follows after the word. Such items are stored for every succesor of word."""
    
    print("\nText generation program initiated...\n")

    # Time keeping
    start_time = time()

    # Process INPUT
    try:
        file_name = sys.argv[1]
        current_word = sys.argv[2].lower()
        n_words = int(sys.argv[3])
    except:
        print("An ERROR occured while processing the arguments.")
        print("Make sure that a file name (text),\na start word (text),\nand a number of words to generate (positive integer) is provided.")
        
        print("\nExample input:")
        print("./generate_text.py shakespeare.txt king 100")
        print("./generate_text.py an_abundance_of_katherines.txt math 500")

        quit()

    ## -- GENERATE TEXT -- ##
    
    # Read and format the text from the file into a list of words.
    lines = text_stats.open_file(file_name)
    input_text = text_stats.clean_text(lines)

    # Verify that start word occurs at least once
    if current_word not in input_text:
        print("The word \"", current_word, "\" does not occur in the file.", sep="")
        quit()

    # Setup
    generated_text = [current_word]
    word_count = dict()
    wordpair_count = dict()

    # Iterate until a text of the desired length is achieved
    while len(generated_text) < n_words and time()-start_time < 60:
        # Get frequency of consequents to current word
        if current_word not in word_count:
            # Iterate through each word in the entire text
            for i in range(len(input_text)-1):
                if input_text[i] == current_word:
                    if (current_word, input_text[i+1]) not in wordpair_count:
                        wordpair_count[(current_word, input_text[i+1])] = 1
                    else:
                        wordpair_count[(current_word, input_text[i+1])] += 1
        
        # Get frequency of current word (if not in word_count already)
        if current_word not in word_count:
            word_count[current_word] = input_text.count(current_word)

        # Get successor candidates and their weights, and then randomly select the next word
        candidates = list(filter(lambda x: x[0] == current_word, wordpair_count))
        candidates = [wordpair[1] for wordpair in candidates]
        weights = list(wordpair_count[(current_word, cand)] for cand in candidates)
        current_word = np.random.choice(candidates, 1, weights)[0]

        generated_text.append(current_word)

    if time()-start_time >= 60: print("Program stopped due to exceeding time limit (60 sec).")

    # Print generated text
    print("Generated text (", len(generated_text), " words):", sep="")
    print(" ".join(generated_text))
    
    print("\nProgram run time:", round(time()-start_time, 1), "seconds.")

