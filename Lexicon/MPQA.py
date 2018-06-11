import sys
import re
from collections import namedtuple

import nltk.stem
_stemmer = nltk.stem.PorterStemmer()

_mpqa_lookup_dict = dict()
MPQA_Entry = namedtuple('MPQA_Entry', ['word', 'pos', 'polarity', 'strength', 'stemmed'])

_word_re = re.compile(r'^[a-zA-Z\-]+$')  # all words are of this form
def lookup(word:str, original_pos:str, cache_entry=False)->('polarity', 'strength'):
    """Returns polarity of word and the strength or (None, None) if no entries
             polarity in {'positive', 'negative', 'neutral', 'both'}
             strength in {'strong', 'weak'}
    """
    if not _mpqa_lookup_dict:
        print('MPQA query but data not loaded! Load data first!', file=sys.stderr)
        print('    hint: mpqa.load_data(filename=\'/path/to/mpqa/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff\')', file=sys.stderr)

    if not _word_re.match(word):  # TODO: not sure if "if not word.isalpha() and not _word_re.match(word):" would be faster
        return None, None
    word = word.lower()
    pos = _convert_pos(original_pos)

    for entry_pos in [pos, 'anypos']:
        entry = _mpqa_lookup_dict.get((word, entry_pos))
        if entry:
            return entry.polarity, entry.strength

    return _stem_lookup(word, pos, cache_entry)


#TODO: Test, possibly expand
def _stem_lookup(word: str, pos: str, cache_entry=False)->('polarity', 'strength'):
    stemmed_word = _stemmer.stem(word)
    if stemmed_word != word:
        for entry_pos in [pos, 'anypos']:
            entry = _mpqa_lookup_dict.get((stemmed_word, entry_pos))
            if entry:
                return entry.polarity, entry.strength
    return None, None


def load_data(filename: str):
    """filename should be the full path to: subjclueslen1-HLTEMNLP05.tff  """
    if _mpqa_lookup_dict:  # if already loaded (to reload just wipe out _mpqa_lookup_dict)
        return

    # The odd bits in this re are due to errors in the data
    line_re = re.compile(r'type=(?P<strength>strong|weak)subj len=1 (len=1 )?word1=(?P<word>[a-zA-Z\-]+) pos1=(?P<pos>anypos|adj|adverb|noun|verb) stemmed1=(?P<stemmed>y|n|1)( m)? priorpolarity=(?P<polarity>positive|negative|neutral|both)')
    for line in open(filename):
        line = line.strip()
        if line=='':
            continue
        # error in the data...
        if line == 'type=weaksubj len=1 word1=impassive pos1=adj stemmed1=n polarity=negative priorpolarity=weakneg':
            line = 'type=weaksubj len=1 word1=impassive pos1=adj stemmed1=n priorpolarity=negative'

        match = line_re.match(line)
        if not match:
            print(line)

        #MPQA_Entry = namedtuple('MPQA_Entry', ['word', 'pos', 'polarity', 'strength', 'stemmed'])
        pos = _convert_pos(match.group('pos')) if match.group('pos') != 'anypos' else match.group('pos')
        entry = MPQA_Entry(match.group('word').lower(),
                           pos,
                           match.group('polarity'),
                           match.group('strength'),
                           (match.group('stemmed') == 'y' or match.group('stemmed') == '1'))
        _mpqa_lookup_dict[(entry.word, entry.pos)] = entry

        if entry.stemmed:
            stemmed_entry = MPQA_Entry(_stemmer.stem(entry.word), entry.pos, entry.polarity, entry.strength, entry.stemmed)
            if stemmed_entry.word != entry.word:
                _mpqa_lookup_dict[(stemmed_entry.word, stemmed_entry.pos)] = stemmed_entry



_pos_lookup = {'adverb': 'adverb', 'verb': 'verb', 'noun': 'noun', 'adjective': 'adjective', 'adj': 'adjective'}
# TODO: test!!!!! (hits what it should hit, skips what it should skip)
def _convert_pos(original_pos: str) -> str:
    original_pos = original_pos.lower()

    # already discovered:
    if original_pos in _pos_lookup:
        return _pos_lookup[original_pos]

    # starts with... (not complete!, see Brown Corpus)
    for pos_type, keys in [('noun', ['nn', 'np', 'nr', 'pn']),
                           ('verb', ['vb', 'hv', 'md']),  # 'hv' = helping verb, 'md'=modal
                           ('adverb', ['rb', 'wrb', 'rn']),
                           ('adjective', ['jj'])]:
        for key in keys:
            if original_pos.startswith(key):
                _pos_lookup[original_pos] = pos_type
                return _pos_lookup[original_pos]

    # foreign word... etc.
    if original_pos.startswith('fw-') or original_pos.startswith('at+') or original_pos.startswith('in+'):
        pos_type = _convert_pos(original_pos[3:])
        _pos_lookup[original_pos] = pos_type
        return _pos_lookup[original_pos]

    # unknown
    _pos_lookup[original_pos] = None
    return _pos_lookup[original_pos]