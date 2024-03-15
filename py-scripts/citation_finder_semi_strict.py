import re
import pandas as pd
import dhlab as dh


#### Bygge korpus

#### subject = 'lingvistikk'
#### corp_limit = 1000
#### from_year = 1950

#### corpus = dh.Corpus(doctype='digibok', subject=subject, limit=corp_limit, from_year=from_year)

# To do:
# add current year with datetime


def citation_finder_semi_strict(corpus, yearspan=(1000,2024), conc_limit=4000):
    
    tall = list(range(yearspan[0],yearspan[1]))

    tallOR = ' OR '.join([str(x) for x in tall])

    tallconc = dh.Concordance(corpus, tallOR, limit=conc_limit)


    concs = tallconc.frame
    concs.concordance = concs.concordance.apply(lambda x:x.replace('<b>', '').replace('</b>', '').replace('...', ''))
    concs1 = concs[['urn', 'concordance']]


    def match_and_explode(c, regex):
        match = []
    
        for i in c.values:
            m = re.findall(regex, i[1])
            if m != []:
                match.append((i[0], m))

        match_df = pd.DataFrame(match)
        match_explode = match_df.explode(column=1)
    
        return match_explode
    
    
    regex1 = r"(?<=[(;])\s*[^(;\d]*?[A-ZÀ-Ž][A-zÀ-ž-]+\s*(?:et\s*al\.?|m(?:ed|\s*\.?)\s*fl(?:ei?re?|\s*\.?))?\s*,?\s*\d{4}\s*[a-zæøå]?(?:\s*\[\s*\d{4}\s*\]\s*[a-zæøå]?)?(?:\s*[,:]\s*(?:[PpSs]\s*\.\s*)?\d{1,4}(?:\s*[,–-]\s*\d{1,4})*)?\s*(?=[);])"
    regex2 = r"(?:[A-ZÀ-Ž][A-zÀ-ž-]+\s*(?:,|og|and|&)\s*)*[A-ZÀ-Ž][A-zÀ-ž-]+\s*(?:et\s*al\.?|m(?:ed|\s*\.?)\s*fl(?:ei?re?|\s*\.?))?\s*\(\s*\d{4}\s*[a-zæøå]?(?:\s*\[\s*\d{4}\s*\]\s*[a-zæøå]?)?(?:\s*[,:]\s*(?:[PpSs]\s*\.\s*)?\d{1,4}(?:\s*[,–-]\s*\d{1,4})*)?\s*[);]"
    
    i_parentes = match_and_explode(concs1, regex1)
    u_parentes = match_and_explode(concs1, regex2)
    
    match_concat = pd.concat([i_parentes, u_parentes], axis=0, ignore_index=True)
    match_sorted = match_concat.sort_values(by=0, ignore_index=True)
    
    return match_sorted
