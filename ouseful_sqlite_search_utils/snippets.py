from difflib import SequenceMatcher 
#https://docs.python.org/3/library/difflib.html#sequencematcher-objects

from vtfunc import TableFunction
#https://charlesleifer.com/blog/sqlite-table-valued-functions-with-python/
#https://github.com/coleifer/sqlite-vtfunc
#%pip install git+https://github.com/coleifer/sqlite-vtfunc.git

# #import spacy
import en_core_web_sm

nlp = en_core_web_sm.load()
sentencizer = nlp.add_pipe("sentencizer")

class SQLite_Sentenciser(TableFunction):
    params = ['start', 'end', 'text']
    columns = ['sentence', 'sent_idx']
    name = 'get_sentences'

    def initialize(self, start=None, end=None, text=None):
        doc = nlp( text )
        # Use inclusive bounds; start index as provided: 1
        # Reset to Python zero-index
        # If we are passed a start of 0, go with it
        # but tweak the end fence-post too...
        if start == 0:
            end = end - 1
        # If we index from the end, go with it.
        start = start if start <= 0 else start - 1
        sents = list(doc.sents)
        if end is None:
            end = len(sents)
        if len(sents) > start:
            self._iter = zip(sents[start:end], range(start, end))
        else:
            self._iter = iter([])

    def iterate(self, idx):
        sentence, sent_idx = next(self._iter)
        return (sentence.text, sent_idx, )

class SentenceJoin:
    """Join sentences by group."""

    def __init__(self):
        self.sentences = []

    # Define action to be take for each row
    def step(self, item):
        self.sentences.append(item)

    # Return final aggregated value
    def finalize(self):        
        return ' '.join(self.sentences)
    
#https://gist.github.com/wpm/bf1f2301b98a883b50e903bc3cc86439
def paragraphs(document):
    start = 0
    for token in document:
        if token.is_space and token.text.count("\n") > 1:
            yield document[start:token.i]
            start = token.i
    yield document[start:]

class SQLite_Paragraphiser(TableFunction):
    params = ['start', 'end', 'text']
    columns = ['paragraph', 'para_idx']
    name = 'get_paragraphs'

    def initialize(self, start=None, end=None, text=None):
        doc = nlp( text )
        paras = list(paragraphs(doc))
        if start == 0:
            end = end - 1
        # If we index from the end, go with it.
        start = start if start <= 0 else start - 1
        if len(paras) > start:
            # Use inclusive bounds; start index: 1
            self._iter = zip(paras[start:end], range(start,end))
        else:
            self._iter = iter([])
        
    def iterate(self, idx):
        (paragraph, idx) = next(self._iter)
        return (paragraph.text.strip(), idx,)

# To begin with lets assume that the start and end substring are guaranteed unique
# in the searched text
def get_fragment(text, startend):
    """Return substring from a text based on start and end substrings delimited by ::."""
    startend = startend.split("::")
    if startend[0] not in text or startend[1] not in text:
        return

    start_idx = text.index(startend[0])
    end_idx = text.index(startend[1])
    
    if end_idx < start_idx:
        return

    return text[start_idx: end_idx+len(startend[1])]

from difflib import SequenceMatcher 
#https://docs.python.org/3/library/difflib.html#sequencematcher-objects

def get_longest_common_substring(text_a, text_b):
    """Find longest common subtring."""
    # isjunk=None, a='', b='', autojunk=True
    seqMatch = SequenceMatcher(None, text_a, text_b, autojunk=False)
    #Also: 
    # autojunk = True (default)
    # isjunk = None (deafult), same as: lambda x: False;
    # or return True for junk (ignored) using: isjunk = lambda x: x in " \t"
    
    # find_longest_match(alo=0, ahi=None, blo=0, bhi=None)
    # Find longest matching block in a[alo:ahi] and b[blo:bhi].
    match = seqMatch.find_longest_match(0, len(text_a), 0, len(text_b))
    
    if (match.size):
        return text_a[match.a: match.a + match.size]

# Register the functions
def register_snippets(CONN):
    SQLite_Sentenciser.register(CONN) #get_sentences
    CONN.create_aggregate('sentence_join', 1, SentenceJoin)
    CONN.create_function("get_longest_common_substring", 2, get_longest_common_substring)

    SQLite_Paragraphiser.register(CONN) #get_paragraphs

    CONN.create_function("get_fragment", 2, get_fragment)

