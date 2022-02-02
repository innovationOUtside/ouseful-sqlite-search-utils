# `ouseful-sqlite-search-utils`

Custom application defined search functions for SQLite.

These functions were originally developed to support the searching of a simple text database containing fairy stories and traditional story collections.

Each database record contained a single, complete fairy story, ranging from a few hundered to a few thousand words, the story title, and a source reference.

In its raw form the database allows discovery and retrieval of stories based on *exact matching* of specific words phrases provided in a search query using the SQL query language.

By setting up the database as *full-text searchable* database, a simpler interface could be provided that supported searching from what was effectively a simple search box.

This is okay as far as it goes, but sometimes requiring words to match the words that appear in a document *exactly* is too cosntraining. This is particularly true in the case when searching over texts that are generated from book scans using OCR (optical character recognition), or old texts in which older forms of English are used. Such texts often contain typographical errors arising from an imperfect OCR process, or variant *ye olde* spellings compared to the spellings we might use today. These errors can prevent the matching of search terms with terms that are, or *should be*, in the text, *if* the OCR process had worked perfectly or if we were searching using the appropriate spelling variant.

In addition, we don't always want to return the whole text (which is to say, a complete story). For example, we might want to return just a particular paragraph, or sentence withing a paragraph, or a fragment of text that starts with one phrase and ends with another; or we might weant to find repeating phrases within a text, such as a repeating refrain or chant within a particular story.

Various functions were created to support seaching the collection. They are of two broad types:

- *snippet returning functions* that return fragments or snippets from a document;
- *approximate search functions* that support partial and fuzzy matching.

## Installation

Install as:

`pip install git+https://github.com/innovationOUtside/ouseful-sqlite-search-utils.git`

## Examples

See the example notebook(s) in the `examples` directory.

## Snippet Returning Functions

The package currently includes several snippet returning functions for returning one or more snippets, or fragments, from a particular record:

Scalar returning functions:

- `get_fragment()`
- `get_longest_common_substring()`

Aggregation functions:

- `join_sentences()`

Table returning functions:

- `get_sentences()`
- `get_paragraphs()`

## Approximate Search Functions

The package currently includes several "approximate" search functions that can retrieve a document based on exactly *or almost* matching terms in the search query with terms that appear in the document:

Scalar functions:

- `find_near_matches()`

Table returning functions:

- `re_search()`
- `regex_search()`
- `find_near_matches_all()`
- `find_fuzzy_matches()`

## Other

 - `typo_highlighter()`