import utils

def test_word_count():
    '''test normal'''
    text = ['папа папа мама', 'дядя бабушка']
    count = utils.word_count(text)
    
    assert count == {'папа': 2, 'мама': 1, 'дядя': 1, 'бабушка': 1}

def test_word_count_tricky():
    '''test tricky'''
    text = ['папа папа мама', 'дядя бабушка']
    count = utils.word_count(text)
    count = utils.word_count(text)

    assert count == {'папа': 2, 'мама': 1, 'дядя': 1, 'бабушка': 1}
