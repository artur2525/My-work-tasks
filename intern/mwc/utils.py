def word_count(batches, count=None):
    '''create right func'''

    if count is not None:
        pass
    else:
        count = {}

    for texts in batches:
        for text in texts:
            for words in text:
                for word in words:
                    if word != ' ':
                        count[word] = count.get(word, 0) + 1
    return count