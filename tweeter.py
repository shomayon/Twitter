import nltk
from nltk.tokenize import word_tokenize

tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'

tokens = word_tokenize(tweet)
print(tokens)
#print(word_tokenize(tweet))
# ['RT', '@', 'marcobonzanini', ':', 'just', 'an', 'example', '