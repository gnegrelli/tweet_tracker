from nltk.corpus import stopwords as nltk_stopwords


stopwords = nltk_stopwords.words('portuguese')

# Add punctuation to list of stopwords
stopwords.extend([
    '.', ',', ':', ';', '!', '?', '\'', '’', '\"', '(', ')', '[', ']', '{', '}', '\\', '|', '/', '&', '*', '<', '>',
    '…', '-', '–',
])
