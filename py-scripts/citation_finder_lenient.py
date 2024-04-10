import re
import pandas as pd
import dhlab as dh
import datetime


#### Bygge korpus

#### subject = 'lingvistikk'
#### corp_limit = 1000
#### from_year = 1950

#### corpus = dh.Corpus(doctype='digibok', subject=subject, limit=corp_limit, from_year=from_year)



def findone(regx, s):
    res = re.findall(regx, s)
    try:
        r = res[0]
    except:
        r = "itj no"
    return r


curr_year = datetime.datetime.today().year


def citation_finder_lenient(corpus, yearspan=(1000,curr_year), conc_limit=4000):
    
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

    
    regex1 = r"(?:[A-ZÀ-Ž](?:[A-zÀ-ž-]+|\s*\.)\s*,?\s*)+(?:\s*(?:et\s*al\.?|m(?:ed|\s*\.?)\s*fl(?:ei?re?|\s*\.?))\s*)?,?\s*\[?\s*\d{4}\s*[a-zæøå]?\s*\.?\s*\]?(?:\s*[,;:/)\s–-]\s*(?:[PpSs]\s*\.?)?\[?\s*\d{1,4}\s*[a-zæøå]?\s*\.?\s*\]?(?:\s*[,–-]\s*\d{1,4}\s*[a-zæøå]?\s*\.?)?)*\s*[);]"
    regex2 = r"(?<=[(;])[^(;\d]*?[A-zÀ-ž][^(;]*?\d{4}[^);]*?(?=[);])"
    regex3 = r"(?:(?:[A-ZÀ-Ž](?:[A-zÀ-ž-]+|\s*\.)\s*,?\s*)+(?:og|and|&)\s*)?(?:[A-ZÀ-Ž](?:[A-zÀ-ž-]+|\s*\.)\s*,?\s*)+(?:\s*(?:et\s*al\.?|m(?:ed|\s*\.?)\s*fl(?:ei?re?|\s*\.?))\s*)?\s*\(\s*\d{4}\D[^)]*?\)"
    
    concs1['parentes'] = concs1.concordance.apply(lambda x: findone(regex1, x))
    concs2 = concs1[concs1['parentes'] != 'itj no']
    concs2 = concs2[['urn', 'concordance']]
    
    i_parentes = match_and_explode(concs2, regex2)
    u_parentes = match_and_explode(concs1, regex3)
    
    match_concat = pd.concat([i_parentes, u_parentes], axis=0, ignore_index=True)
    match_sorted = match_concat.sort_values(by=0, ignore_index=True)
    
    return match_sorted
