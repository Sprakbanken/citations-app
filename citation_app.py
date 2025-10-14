import dhlab as dh
import streamlit as st
import pandas as pd
import datetime
import citation_finder as cf

st.set_page_config(layout="wide")

st.title('Citation-finder')

st.subheader('Lag korpus')

subject=st.text_input('Søk på temaord', 'Søk', help='Skriv ønsket søkeord for tema. Du kan bruke * som wildcard før eller etter søkeordet, f.eks. "språk*"')

corp_limit=st.number_input('Antall verk', value=500, help='Sett maksgrense for antall verk i korpuset')

st.subheader('Konkordansevalg')
st.markdown('Citation-finder henter tekst fra konkordanser. Velg årsspennet som skal brukes for å søke etter konkordanser og hvor mange konkordanser som skal hentes ut.')

curr_year=datetime.datetime.today().year
from_year=st.number_input('Fra år', value=1000, help='Velg startår for årsspennet som skal brukes i konkordansesøket')
to_year=st.number_input('Til år', value=curr_year, help='Velg sluttår for årsspennet som skal brukes i konkordansesøket')
yearspan=(from_year,to_year)

conc_limit=st.number_input('Antall konkordanser', value=4000, help='Sett maksgrense for antall konkordanser som skal hentes ut')


st.write(subject, corp_limit, from_year, to_year, conc_limit)



corpus = dh.Corpus(doctype='digibok', subject=subject, limit=corp_limit)


df = cf.citation_finder(corpus, yearspan=yearspan, conc_limit=conc_limit)
df.columns = ["urn","citation"]

res = df.merge(corpus.frame, left_on='urn', right_on='urn')['urn title authors year citation'.split()]

st.markdown('Corpus + citations')

st.dataframe(res)
