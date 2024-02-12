import nltk
import string
from nltk.corpus import brown
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# Downloading brown and reuters corpus from NLTK 
nltk.download('brown')
nltk.download('stopwords')

# Get the list of stopwords and punctuation and store it in their respective variables
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

#1. Removing stopwords and punctuation and storing remaining words in filtered_words
filtered_corpus = [word.lower() for word in brown.words() if word.lower() not in stop_words and word not in punctuation]

#2. Creating frequency distribution of bigrams for developing 2-gram language model
brown_bigram_frequency_distribution = nltk.FreqDist(nltk.bigrams(filtered_corpus))
brown_unigram_frequency_distribution = nltk.FreqDist(filtered_corpus)

#Function to calculate probabilty of bigram : P(w2 | w1) = Count(w1, w2)/Count(w1)
def bigram_probability(bigram):
    word1, word2 = bigram
    bigrams_count = brown_bigram_frequency_distribution.get(bigram,1)
    word1_unigram_count = brown_unigram_frequency_distribution.get(word1, 1)
    probability = bigrams_count / word1_unigram_count
    return  probability;


"""
    This function finds the top 'n' words that are most likely to follow the given word.
    
    It takes the Parameters as follows:
        word (str): The input word.
        bigram_freq_dist (FreqDist): Frequency distribution of bigrams.
        top_n (int): The number of top words to return.
    
    Returns:
        list: It returns a A list of tuples containing the top 'n'(n=3 in this case) words and their frequencies.
    """
def get_top_next_words(word, brown_bigram_frequency_distribution, top_n=3):
    
    # Fetching all the bigrams that start with the given word and adding the frequency to each bigram.
    bigrams_start_with_w1 = [(w2, freq) for (w1, w2), freq in brown_bigram_frequency_distribution.items() if w1 == word]
    
    # Sort by frequency in descending order to find the top 3 
    #lambda function defines how the elements are compared during the sorting : 
    #which takes an element x(which is tuple(bigram, frequency)) and returns x[1], which is the second element of the tuple.
    #so sorting is based on the frequency count of each bigram
    # tuples with higher values of the second element (frequencies) will appear first in the sorted list
    bigrams_start_with_w1.sort(key=lambda x: x[1], reverse=True)
    # Return the top 'n' words
    return bigrams_start_with_w1[:top_n]

# Task 1:*************** Ask the user for initial word/token W1
while True:
    initial_word = input("Enter initial word/token (W1): ").lower()
    if initial_word in filtered_corpus:
        break
    else:
        print("The word is not in the corpus.")
        choice = input("Would you like to try again? (yes/no): ").lower()
        if choice != 'yes':
            exit()

# Task 2:**************** Get the top 3 most likely words to follow W1
new_sentence = [initial_word]
while True:
    print(f"Current sentence: {' '.join(new_sentence)}")
    print(f"Which word should follow '{initial_word}'.......:")
    top_next_words = get_top_next_words(initial_word, brown_bigram_frequency_distribution)

    for i, (word, freq) in enumerate(top_next_words, start=1):
        #for each word we find construct the bigram and find the the probability of bigram
        print(f"{i}) {word} P({initial_word} {word}) = {bigram_probability((initial_word, word))}")
    print("4) QUIT")
    
    # Ask the user for the next word choice
    choice = input("\nWhich word should follow? Enter the number or QUIT: ").lower()
    
    # Handle user choices
    if choice == '4' or choice.lower() == 'quit':
        break
    elif choice in ['1', '2', '3']:
        word_choice = top_next_words[int(choice) - 1][0]
        new_sentence.append(word_choice)
        initial_word = word_choice    
    else:
        print("Assuming user choice is (1).")
        word_choice = top_next_words[0][0]
        new_sentence.append(word_choice)
        initial_word = word_choice

print("\nFinal sentence is:", ' '.join(new_sentence))
