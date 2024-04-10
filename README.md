# Citation-finder

Citation-finder finds in-text citations in a text corpus using regular expressions. The expressions find citations that follow the author name-publication year format of the [APA](https://i.ntnu.no/academic-writing/apa-7), [Harvard](https://i.ntnu.no/academic-writing/harvard) and [Chicago B](https://i.ntnu.no/academic-writing/chicago-b) styles.

### How to use
Citation-finder takes a corpus created with the [dhlab package](https://dhlab.readthedocs.io/en/stable/) from The National Library of Norway.

Install and import dhlab, and [create a corpus](https://dhlab.readthedocs.io/en/stable/library/generated/dhlab.Corpus.html#dhlab.Corpus).

```
pip install -U dhlab

import dhlab as dh

corpus = dh.Corpus(doctype='digibok')
```

Import citation-finder and call the function on the corpus.

```
import citaton_finder as cf

cf.citation_finder(corpus, yearspan=(1900,1965), limit=500)
```

The additional, optional arguments are yearspan and limit. The function searches for concordances using a range of four digit numbers that represent publication years. The range from year to year can be defined with yearspan. The default is from 1000 to the current year. Limit refers to the concordance limit. The default is 4000.

The function returns a Pandas DataFrame with the individual citation matches and their associated URN from the dhlab corpus.

### What will match
Citation-finder will match both citations where the author name and publication year is inside parentheses (e.g. (Smith, 1991)), as well as citations where the author name is outside parentheses and the publication year is inside parentheses (e.g. Smith (1991)).

In order for the regular expressions to distinguish citation-like strings from other text, they assume at least one word beginning with an upper case letter (author name), a four digit number (publication year) and parentheses (or semicolons, which can also surround citations if several are listed in a row.

Additionally the patterns allow for several optional elements:
 * multiple authors can be listed
   * (Lee, Singh and Smith, 1991)
   * Lee, Singh and Smith (1991)
 * author names can include initials
   * (P. W. Smith, 1991)
   * P. W. Smith (1991)
 * author names can be followed by "et al." or "m.fl." in Norwegian
   * (Smith et al., 1991)
   * Smith et al. (1991)
 * publication year can be followed by a page reference
   * (Smith, 1991, p. 123-125)
   * Smith (1991, p. 123-125)
 * publication year can be followed by a single letter to differentiate multiple works by the same author in the same year
   * (Smith, 1991a)
   * Smith (1991a)
 * the author name inside parentheses can be preceded by other text
   * (see for instance Smith, 1991)


Since the regular expressions simply search for patterns in raw text, citation-finder will return all the matching strings regardless of whether they are true citations or not, and will not return citations that do not match the pattern.
