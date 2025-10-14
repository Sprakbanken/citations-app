# %%
import pandas as pd

import dhlab as dh
from dhlab.api.dhlab_api import word_concordance


import re
import datetime

import citation_finder as df
# %%

# Build corpus

# %%
subject = "lingvistikk"
corp_limit = 1000
from_year = 1950


corpus = dh.Corpus(
    #doctype="digibok",
    subject = subject,
    limit = corp_limit,
    from_year=from_year)

#%%%

corpus.to_excel("korpus.xlsx")

# %%
# Bygg konkordanser

year = datetime.datetime.today().year
tall = list(range(1900, year))
tallOR = " OR ".join([str(x) for x in tall])

conc_limit = 1000



## workaround: use the concordance app instead of the dhlab api
# search for the concordances in the uploaded excel corpus with the tallOR


concs = pd.read_excel("./concordances.xlsx")

concs

# %%st