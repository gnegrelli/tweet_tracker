from nltk.corpus import stopwords as nltk_stopwords


stopwords = nltk_stopwords.words('portuguese')

# Add punctuation to list of stopwords
stopwords.extend([
    '.', ',', ':', ';', '!', '?', '\'', '’', '\"', '(', ')', '[', ']', '{', '}', '\\', '|', '/', '&', '*', '<', '>',
    '…', '-', '–', '$', '%', '@', ');', '+', '°',
])

stopwords.extend([
    'para', 'pra', 'pro', 'tá', 'q', 'lá', 'aí', 'aqui', 'vc', 'nóiz', 'nóis',
    'esse', 'essa', 'este', 'esta', 'nesse', 'nessa', 'neste', 'nesta', 'desse', 'dessa', 'deste', 'desta',
    'todo', 'toda', 'tudo', 'todos', 'todas',
    'link', 'mil', '2021', 'dia', '19', 'sobre', 'bilhões', 'semana', '1', '2', 'hoje', 'detalhes', 'anos', 'bom',
    '🇧', '🇷', '🤝', '👍', 'grande', '2020', '🏻', 'ano', '5', '2019', '10', '4', 'cerca', '100', '20', 'bem',
    'ainda', 'parte', 'agora', 'quinta-feira', 'sendo', 'ontem', 'boa', 'sempre', 'toneladas', 'casa', 'cada', 'fio',
    'após', 'saiba', 'km', 'novos', 'kg', 'novas', 'novo', 'abraço', '7', 'vai', 'noite', '1.1-', 'c', '12', '21',
    '1.2-', '15', 'a1', '30', 'quase', 'milhões', 'bilhäo', 'milhäo', 'r'
])
