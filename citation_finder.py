#!/usr/bin/env python
# coding: utf-8

import re
import pandas as pd
import dhlab as dh

def findone(regex, s):
    res = re.findall(regex,s)
    try:
        r = res[0]
    except:
        r = "itj no"
    return r

#### Bygge korpus
# corpus = dh.Corpus(doctype="digibok", subject = "språkvitenskap", limit = 1000,from_year=1950)

#### Finne konkordanser med årstall mellom 1900 og 2020

def citation_finder(corpus, yearspan = (1900,2020), get_concs: bool = False):

    tall = list(range(yearspan[0],yearspan[1]))

    tallOR = ' OR '.join([str(x) for x in tall])

    tallconc = dh.Concordance(corpus, tallOR, limit=4000)

    concs = tallconc.frame
    concs.concordance = concs.concordance.apply(lambda x:x.replace('<b>', '').replace('</b>', '').replace('...', ''))

    books1 = concs[['urn', 'concordance']]

    #### Regex1
    #### finner alle konkordanser med parentes (eller semikolon) med årstall.

    regex1 = r'[\(;].*?\D\d{4}\D.*?[\);]'

    books1['parentes'] = books1.concordance.apply(lambda x: findone(regex1, x))

    books2 = books1[books1['parentes'] != 'itj no']
    books2 = books2[['urn', 'concordance']]

    #### Regex2
    #### finner alle konkordanser som har tallkonstruksjoner med årstall og potensielt sidetall før sluttparentes (eller semikolon).
    #### books3 er en dataramme med disse resultatene. Den er grunnlaget for å finne de to forskjellige typene siteringer med navn og
    #### årstall inne i parentes, og med navn utenfor parentes.

    regex2 = r'\[?\s*\d{4}\s*[a-zæøå]?\s*\.?\s*\]?(?:\s*[,-;:/\)\s]\s*(?:[ps]\s*\.?)?\[?\s*\d{1,4}\s*[a-zæøå]?\s*\.?\s*\]?)*\s*[\);]'

    books2['årstall + sidetall'] = books2.concordance.apply(lambda x: findone(regex2, x))

    books3 = books2[books2['årstall + sidetall'] != 'itj no']
    books3 = books3[['urn', 'concordance']]

    #### Navn i parentes
    #### Regex3
    #### finner alle konkordanser med navn, årstall og potensielt sidetall før sluttparentes (eller semikolon). Navnet kan følge "og/and/&"
    #### eller følges av "et al.".

    regex3 = r'(?:og|and|&)?(?:[A-ZÆØÅ](?:[A-ZÆØÅa-zæøå-]+|\s*\.)\s*,?\s*)+(?:\s*et\sal\.\s*)?,?\s*\[?\s*\d{4}\s*[a-zæøå]?\s*\.?\s*\]?(?:\s*[,-;:/\)\s]\s*(?:[ps]\s*\.?)?\[?\s*\d{1,4}\s*[a-zæøå]?\s*\.?\s*\]?)*\s*[\);]'

    books3['navn i parentes'] = books3.concordance.apply(lambda x: findone(regex3, x))

    if get_concs:
        return books3

    books4 = books3[books3['navn i parentes'] != 'itj no']
    books4 = books4[['urn', 'concordance']]

    #### Regex4
    #### finner alle treff i alle konkordanser som macther parenteser (eller semikolon) som består av minst én bokstav, årstall og hva som
    #### helst annet. Antakelsen er at vi allerede har filtrert ut parentes-konstruksjoner som ligner på siteringer med navn, årstall og
    #### sidetall og at alle parenteser med minimum én bokstav og et årstall derfor er siteringer.

    regex4 = r'(?<=[\(;])[^(;\d]*?[A-ZÆØÅa-zæøå][^(;]*?\d{4}[^);]*?(?=[\);])'

    match = []

    for i in books4.values:
        m = re.findall(regex4, i[1])
        if m != []:
            match.append((i[0],m))

    match_df = pd.DataFrame(match)
    match_explode = match_df.explode(column=1)

    #### Navn utenfor parentes
    #### Regex5
    #### tar utgangspunkt i books3 og finner alle konkordanser med navn utenfor parentes (eller semikolon) med årstall inni.

    regex5 = '(?:[A-ZÆØÅ](?:[A-ZÆØÅa-zæøå-]+|\s*\.)\s*,?\s*)+[\(;]\s*\d{4}\D'

    books3['navn u/parentes'] = books3.concordance.apply(lambda x: findone(regex5, x))

    books5 = books3[books3['navn u/parentes'] != 'itj no']
    books5 = books5[['urn', 'concordance']]

    #### Regex6
    #### finner alle treff i alle konkordanser som macther navn utenfor parentes (eller semikolon) som består av et årstall og hva som helst
    #### annet. Navnekonstruksjonene kan bestå av flere navn etter hverandre, potensielt skilt av komma eller "og/and/&", eller etterfulgt
    #### av "et al.".

    regex6 = r'(?:(?:[A-ZÆØÅ](?:[A-ZÆØÅa-zæøå-]+|\s*\.)\s*,?\s*)+(?:og|and|&)\s*)?(?:[A-ZÆØÅ](?:[A-ZÆØÅa-zæøå-]+|\s*\.)\s*,?\s*)+(?:\s*et\sal\.)?\s*\(\s*\d{4}\D[^)]*?\)'

    matchu = []

    for i in books5.values:
        mu = re.findall(regex6, i[1])
        if mu != []:
            matchu.append((i[0],mu))

    matchu_df = pd.DataFrame(matchu)
    matchu_explode = matchu_df.explode(column=1)

    ### match_sorted
    # setter sammen datarammene med siteringer for navn i og utenfor parentes, og sorterer på URN.

    match_concat = pd.concat([match_explode, matchu_explode], ignore_index=True)
    match_sorted = match_concat.sort_values(by=0, ignore_index=True)

    return match_sorted







