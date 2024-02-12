import nltk
from nltk.util import ngrams
from nltk.probability import FreqDist 
from nltk.corpus import brown 
from nltk.corpus import stopwords
from nltk.probability import LidstoneProbDist, FreqDist

# Download the Brown Corpus if not already downloaded
nltk.download('brown')
nltk.download('stopwords')
# Get the English stopwords
stop_words = set(stopwords.words('english'))

# Finding the brown corpus bigrams from the brown cropus words
brown_corpus_bigrams = list(nltk.bigrams(brown.words()))

#Finding the frequency distribution for the bigrams and the for the unigrams
brown_bigram_frequency_distribution = FreqDist(brown_corpus_bigrams)
brown_unigram_frequency_distribution = FreqDist(brown.words())

#print(f"\n printing brown unigram count : {brown_unigram_frequency_distribution.items()}")
#print(f"total brown corpus bigrams : {sum(brown_bigram_frequency_distribution.values())} ")


#1.****************** Asking the user to enter the input sentence
sentence = input("Please Enter a sentence of your choice and wait for the magic to happen: ")


#2.******************* print(Converting the sentence into lowercase***********************************)

#processing the input sentence
sentence = sentence.lower()
words_of_sentence = sentence.split()
#Appending the start and end to the initial sentence
words_of_sentence = ['<s>'] + words_of_sentence + ['</s>']


#3.****************** Since we are developing 2-gram language model, first we Tokenize the sentence into bigrams
sentence_bigrams = list(nltk.bigrams(words_of_sentence))

bigram_probabilities = {}


def bigram_probability(bigram):
    word1, word2 = bigram
    bigrams_count = brown_bigram_frequency_distribution.get(bigram,1)
    first_word_unigram_count = brown_unigram_frequency_distribution.get(word1, 1)
    probability = bigrams_count / first_word_unigram_count
    if first_word == '<s>':
        probability = 0.25
    if second_word == '</s>':
        probability = 0.25
    return  probability;   

def unigram_probability(word):
    word_count = brown_unigram_frequency_distribution.get(first_word, 1)
    total_words_count = sum(brown_unigram_frequency_distribution.values())
    probabilty = first_word_unigram_count / total_words_count
    return probabilty


#calculating the probabilties for each bigram
for bigram in sentence_bigrams:
    first_word, second_word = bigram
    #counting the number of bigrams(w1, w2) from frequency distribution dictionary
    bigrams_count = brown_bigram_frequency_distribution.get(bigram,1)
    #finding the total count of w1
    first_word_unigram_count = brown_unigram_frequency_distribution.get(first_word, 1)
    #finding the probabilty of each bigram i.e : P(w1,w2) = count(w1,w2)/count(w1)
    probability = bigrams_count / first_word_unigram_count

    if first_word == '<s>':
        probability = 0.25
    if second_word == '</s>':
        probability = 0.25

    #saving the bigram probabilties in a dictonary for calculating the total probability of the sentence and printing in the next part      
    bigram_probabilities[bigram] = probability


print(f"\nCalculating the porbability for the sentence: '{sentence}' ")
print("\nProbablities of each bigram\n")

#Calculating the probability of the sentence : P(S) => P(w1,w2,w3...) = P(w1) * P(w2|w1) * P(w3|w2).......
sentence_probability = 1
for bigram, bigram_probability in bigram_probabilities.items():
    print(f"{bigram} and its probability: {bigram_probability}")
    sentence_probability = sentence_probability * bigram_probability
    
print(f"\nProbabilty of sentence : {sentence_probability}")    
