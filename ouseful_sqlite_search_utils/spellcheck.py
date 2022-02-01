from vtfunc import TableFunction

# Spell checking and grammar checking using:
#
# - https://github.com/jxmorris12/language_tool_python/
# - https://languagetool.org/
# Note that this will download the LanguageTool Java package (~200MB) on first run
 
# %pip install --upgrade language_tool_python
import language_tool_python

# Loading the languagetool is slow, so it makes sense to only do it once.
# So put it in a class and refer to it from a persistent object context

class TypoHighlighter:
    """Find typographical errors in a text and highlight them.
        Note that this class make be slow to instantiate as the
        LanguageTool http server started.
    """
    # Shared instance
    tool = language_tool_python.LanguageTool('en-UK')
    
    def __init__(self, style='html', #lang='en-UK',
                 html_color='red', md_style='__'):
        self.style = style
        #self.lang = lang
        self.html_color = html_color
        self.md_style = md_style
        
    def typo_styler(self, error):
        """Highlight error term."""
        typo = error.context
        from_ = error.offsetInContext
        to_ = from_ + error.errorLength
        txt = typo[from_:to_]
        if self.style=='html':
            typo =  typo[:from_] + f'<span style="color:{self.html_color}">{txt}</span>{typo[to_:]}'
        elif not None:
            typo =  f"{typo[:from_]}{self.md_style}{txt}{self.md_style}{typo[to_:]}"
        #print(f"**{html}")
        return typo

    def highlight_typos(self, text, highlight=True):
        """Highlight spelling errors in text."""
        matches = TypoHighlighter.tool.check(text)
        if not highlight:
            return matches
        else:
            return [self.typo_styler(m) for m in matches]

class DBTypoHighlighter(TableFunction):
    """Return a virtual table containing highlighted typos in the presented text."""
    # Input parameter - the text we want to check for typos
    params = ['text']
    # A single output column containing highlighted errors in context
    columns = ['highlight']
    # The name of the function we can call in SQLite
    name = 'typo_highlighter'
    
    # A class global spellchecker object
    typo_highlighter = TypoHighlighter()
    
    def initialize(self, text=None):
        """Return an iterator to generate output virtual table rows."""
        self._iter = iter(DBTypoHighlighter.typo_highlighter.highlight_typos(text))

    def iterate(self, idx):
        """Return the next row for the virtual table."""
        # We don't need to make us of the idx value
        # but it is required in the methof signature 
        item = next(self._iter)
        # The final , is required.
        return (item,)

# Register the functions
def register_partials(CONN):
    DBTypoHighlighter.register(CONN) #typo_highlighter