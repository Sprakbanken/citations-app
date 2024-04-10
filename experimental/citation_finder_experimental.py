#!/usr/bin/env python
# coding: utf-8

import re
import pandas as pd
import dhlab as dh
import datetime


#### Bygge korpus

#### subject = 'lingvistikk'
#### corp_limit = 1000
#### from_year = 1950

#### corpus = dh.Corpus(doctype='digibok', subject=subject, limit=corp_limit, from_year=from_year)


    
curr_year = datetime.datetime.today().year


def citation_finder(corpus, strictness='moderate', yearspan=(1000,curr_year), conc_limit=4000):
    """Finds citations in text using regular expressions"""
    
    
    tall = list(range(yearspan[0],yearspan[1]))

    tallOR = ' OR '.join([str(x) for x in tall])

    tallconc = dh.Concordance(corpus, tallOR, limit=conc_limit)

    concs = tallconc.frame
    concs.concordance = concs.concordance.apply(lambda x:x.replace('<b>', '').replace('</b>', '').replace('...', ''))
    concs1 = concs[['urn', 'concordance']]
    
    
    
    #### Strict
    regex_s1 = r"(?<=[(;]\s)(?:[A-ZÀ-Ž][A-zÀ-ž-]+\s*(?:,|og|and|&)\s*)*[A-ZÀ-Ž][A-zÀ-ž-]+\s*(?:et\s*al\.|mfl\.)?\s*,?\s*\d{4}(?:\s*[a-zæøå])?(?:\s*[,:]\s*(?:[ps]\s*\.\s*)?\d{1,4}(?:\s*[,–-]\s*\d{1,4})*)?(?=\s[);])"
    regex_s2 = r"(?:[A-ZÀ-Ž][A-zÀ-ž-]+\s*(?:,|og|and|&)\s*)*[A-ZÀ-Ž][A-zÀ-ž-]+\s*(?:et\s*al\.|mfl\.)?\s*\(\s*\d{4}(?:\s*[a-zæøå])?(?:\s*[,:]\s*(?:[ps]\s*\.\s*)?\d{1,4}(?:\s*[,–-]\s*\d{1,4})*)?\s*\)"

    #### Moderate
    regex_m1 = r"(?<=[(;])\s*[^(;\d]*?[A-ZÀ-Ž][A-zÀ-ž-]+\s*(?:et\s*al\.?|m(?:ed|\s*\.?)\s*fl(?:ei?re?|\s*\.?))?\s*,?\s*\d{4}\s*[a-zæøå]?(?:\s*\[\s*\d{4}\s*\]\s*[a-zæøå]?)?(?:\s*[,:]\s*(?:[PpSs]\s*\.\s*)?\d{1,4}(?:\s*[,–-]\s*\d{1,4})*)?(?=\s[);])"
    regex_m2 = r"(?:[A-ZÀ-Ž][A-zÀ-ž-]+\s*(?:,|og|and|&)\s*)*[A-ZÀ-Ž][A-zÀ-ž-]+\s*(?:et\s*al\.?|m(?:ed|\s*\.?)\s*fl(?:ei?re?|\s*\.?))?\s*\(\s*\d{4}\s*[a-zæøå]?(?:\s*\[\s*\d{4}\s*\]\s*[a-zæøå]?)?(?:\s*[,:]\s*(?:[PpSs]\s*\.\s*)?\d{1,4}(?:\s*[,–-]\s*\d{1,4})*)?\s*\)"

    #### Lenient
    regex_l1 = r"(?:[A-ZÀ-Ž](?:[A-zÀ-ž-]+|\s*\.)\s*,?\s*)+(?:\s*(?:et\s*al\.?|m(?:ed|\s*\.?)\s*fl(?:ei?re?|\s*\.?))\s*)?,?\s*\[?\s*\d{4}\s*[a-zæøå]?\s*\.?\s*\]?(?:\s*[,;:/)\s–-]\s*(?:[PpSs]\s*\.?)?\[?\s*\d{1,4}\s*[a-zæøå]?\s*\.?\s*\]?(?:\s*[,–-]\s*\d{1,4}\s*[a-zæøå]?\s*\.?)?)*\s*[);]"
    regex_l2 = r"(?<=[(;])[^(;\d]*?[A-zÀ-ž][^(;]*?\d{4}[^);]*?(?=[);])"
    regex_l3 = r"(?:(?:[A-ZÀ-Ž](?:[A-zÀ-ž-]+|\s*\.)\s*,?\s*)+(?:og|and|&)\s*)?(?:[A-ZÀ-Ž](?:[A-zÀ-ž-]+|\s*\.)\s*,?\s*)+(?:\s*(?:et\s*al\.?|m(?:ed|\s*\.?)\s*fl(?:ei?re?|\s*\.?))\s*)?\s*\(\s*\d{4}\D[^)]*?\)"

    #### Open
    regex_o1 = r"(?<=[(;])[^(;\d]*?[A-zÀ-ž][^(;]*?\d{4}[^);]*?(?=[);])"
    regex_o2 = r"(?:[^()\s]+\s+){1,5}\(\s*\d{4}[^)]*?\)"

    #### NOU, StMeld, Prop
    regex_nou = r"(?:(?:NOU|nou)\s*\(?\s*\d{4}\s*:\s*\d{1,4}|(?:St\s*\.?\s*)?Meld\s*\.?\s*(?:St\s*\.?\s*)?(?:nr\s*\.?\s*)?\d{1,3}\s*\(?\s*\d{4}\s*-\s*\d{4}\s*\)?|Prop\s*\.?\s*\d{1,3}\s*[A-ZÆØÅ]\s*\(?\s*\d{4}\s*-\s*\d{4}\s*\)?)(?:\s*[,(]?\s*[PpSs]\s*\.?\s*\d{1,4})?"
    
    
    
    def findone(regx, s):
        res = re.findall(regx, s)
        try:
            r = res[0]
        except:
            r = "itj no"
        return r
    
    
        
    def match_and_explode(c, regex):
        match = []
    
        for i in c.values:
            m = re.findall(regex, i[1])
            if m != []:
                match.append((i[0], m))

        match_df = pd.DataFrame(match)
        match_explode = match_df.explode(column=1)
    
        return match_explode
    
    
    
    if strictness == 'strict':
        i_parentes = match_and_explode(concs1, regex_s1)
        u_parentes = match_and_explode(concs1, regex_s2)
        
    elif strictness == 'moderate':
        i_parentes = match_and_explode(concs1, regex_m1)
        u_parentes = match_and_explode(concs1, regex_m2)
            
    elif strictness == 'lenient':
        concs1['parentes'] = concs1.concordance.apply(lambda x: findone(regex_l1, x))
        concs2 = concs1[concs1['parentes'] != 'itj no']
        concs2 = concs2[['urn', 'concordance']]
        
        i_parentes = match_and_explode(concs_l, regex_l2)
        u_parentes = match_and_explode(concs1, regex_l3)
                
    elif strictness == 'open':
        i_parentes = match_and_explode(concs1, regex_o1)
        u_parentes = match_and_explode(concs1, regex_o2)
                    
    else:
        print("Strictness argument is not valid")
    
    
    
    noustp = match_and_explode(concs1, regex_nou)
    
    match_concat = pd.concat([i_parentes, u_parentes, noustp], axis=0, ignore_index=True)
    match_sorted = match_concat.sort_values(by=0, ignore_index=True)
    
    
    return match_sorted
