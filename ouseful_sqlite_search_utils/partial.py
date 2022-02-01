
from vtfunc import TableFunction
#https://charlesleifer.com/blog/sqlite-table-valued-functions-with-python/
#https://github.com/coleifer/sqlite-vtfunc
#%pip install git+https://github.com/coleifer/sqlite-vtfunc.git

import spacy
import re
import regex
import fuzzysearch
#from spacy.matcher import PhraseMatcher
from spaczz.matcher import FuzzyMatcher

nlp = spacy.blank("en")

class ReSearch(TableFunction):
    params = ['pattern', 'search_string']
    columns = ['match']
    name = 're_search'

    def initialize(self, pattern=None, search_string=None):
        self._iter = re.finditer(pattern, search_string)

    def iterate(self, idx):
        # We do not need `idx`, so just ignore it.
        return (next(self._iter).group(0),)

class RegexSearch(TableFunction):
    params = ['pattern', 'search_string']
    columns = ['match', 'start', 'end']
    name = 'regex_search'

    def initialize(self, pattern=None, search_string=None):
        self._iter = regex.finditer(pattern, search_string)

    def iterate(self, idx):
        item = next(self._iter)
        return (item.group(0), item.start(), item.end(),)

def find_near_matches(pattern, search_string, max_l_dist=3):
    response = fuzzysearch.find_near_matches(pattern, search_string, max_l_dist=max_l_dist)
    if response:
        return response[0].matched
    return ''

class FindNearMatches(TableFunction):
    params = ['target_string', 'search_string', 'max_l_dist']
    columns = ['matched', 'start', 'end', 'dist']
    name = 'find_near_matches_all'

    def initialize(self, target_string=None, search_string=None, max_l_dist=None):
        if max_l_dist is None:
            max_l_dist = 0
        self._iter = iter(fuzzysearch.find_near_matches(target_string, search_string, max_l_dist=max_l_dist))

    def iterate(self, idx):
        r = next(self._iter)
        return (r.matched, r.start, r.end, r.dist,)

class SQLite_FuzzyMatcher(TableFunction):
    params = ['target_string', 'search_string']
    columns = ['matched', 'start', 'end', 'fragment', 'ratio']
    name = 'find_fuzzy_matches'
    
    def initialize(self, target_string=None, search_string=None):
        doc = nlp( search_string )
        matcher = FuzzyMatcher(nlp.vocab)
        # We can tune the sensitivity for the match; default is 75
        matcher.add(search_string, [nlp(target_string)], kwargs=[{"min_r2": 73}])
        self._iter = iter(matcher(doc))

    def iterate(self, idx):
        matched, start, end, ratio = next(self._iter)
        fragment = nlp(matched)[start:end].text
        return (matched, start, end, fragment, ratio,)


# Register the functions
def register_partials(CONN):
    CONN.create_function('find_near_matches', -1, find_near_matches)
    ReSearch.register(CONN) #re_search
    RegexSearch.register(CONN) #regex_search
    FindNearMatches.register(CONN) #find_near_matches_all
    SQLite_FuzzyMatcher.register(CONN) #find_fuzzy_matches