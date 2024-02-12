import nltk
import matplotlib.pyplot as plt
from nltk.corpus import brown, reuters
from nltk.corpus import stopwords
import string
from nltk.probability import FreqDist

# Download stopwords and corpora if not already downloaded
nltk.download('stopwords')
nltk.download('brown')
nltk.download('reuters')

# Storing the stop words in a set
stop_words = set(stopwords.words('english'))

#adding punctuation words to stop words. 
stop_words.update(string.punctuation)


#This function will remove stop words from the corpus. It takes the words as the input and filters out the stop words from it.
def remove_stopwords(words):
    return [word for word in words if word.lower() not in stop_words]

# This function finds the freq_distribution and stores the key value pairs in a dictionary
def get_unigram_frequency_distribution(corpus):
    if corpus.words()!='':
        words = corpus.words()
        words_filtered = remove_stopwords(words)
        frequency_distribution = FreqDist(words_filtered)
        return frequency_distribution
    else:
        return {}


brown_unigram_frequency_distribution = get_unigram_frequency_distribution(brown)
reuters_unigram_frequency_distribution = get_unigram_frequency_distribution(reuters)

# for word, count in brown_freq_dist.items():
#    print(f"{word}: {count}\n")

# *************************   Part 2 ***********************************************************

# Shjowing the top ten words for both corpora
print("Top ten words in Brown Corpus:")
print(brown_unigram_frequency_distribution.most_common(10))

print("\nTop ten words in Reuters Corpus:")
print(reuters_unigram_frequency_distribution.most_common(10))


# ********************************************   Part 3   *******************************************
#Analysing the top 1000 words from the corpus. We use graphs to visualize the ranks and frequencies.

# Finding ranks and frequencies for the first 1000 words in both corpora
brown_ranks, brown_freqs = zip(*enumerate([freq for word, freq in brown_unigram_frequency_distribution.most_common(1000)], 1))
reuters_ranks, reuters_freqs = zip(*enumerate([freq for word, freq in reuters_unigram_frequency_distribution.most_common(1000)], 1))



# Plot log-log graphs for both corpora
#Python Matplotliv is used for plotting the graphs. plt is a object of matplotlib
plt.figure(figsize=(10, 6))
plt.plot(brown_ranks, brown_freqs, label='Brown Corpus')
plt.plot(reuters_ranks, reuters_freqs, label='Reuters Corpus')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Log(Rank)')
plt.ylabel('Log(Frequency)')
plt.title('Log(Rank) vs Log(Frequency) for the First 1000 Words')
plt.legend()
plt.show()

#***************************      Part 4 *************************************************

brown_technical_words = ["algorithm", "protocol"]
brown_non_technical_words = ["house","tree"]

reuters_technical_words = ["stock", "inflation"]
reuters_non_technical_words = ["chair", "banana"]

#This function finds the ptobability for each word in the corpus
def find_unigram_probability(words, total):
    for word in words:
        word_count = brown_unigram_frequency_distribution[word]
        print(f"unigram proababilty of {word}: {word_count/total}\n")

print("\nfinding probabilities for technical and non technical words in brown coprus")
find_unigram_probability(brown_technical_words, brown_unigram_frequency_distribution.N())
find_unigram_probability(brown_non_technical_words, brown_unigram_frequency_distribution.N())


print("finding probabilities for technical and non technical words in reuters coprus")
find_unigram_probability(reuters_technical_words, reuters_unigram_frequency_distribution.N())
find_unigram_probability(reuters_non_technical_words, reuters_unigram_frequency_distribution.N())