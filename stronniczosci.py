

from ydata_profiling import ProfileReport
import sweetviz as sv
import pandas as pd
import sys

df = pd.read_csv('wyniki_polaczone.csv')


'''
# zakładam, że już masz DataFrame `df`
df['data_konkursu'] = pd.to_datetime(df['Date & Location'].str.extract(r'(\d{4}-\d{2}-\d{2})')[0], errors='coerce')

# Dodajemy unikalny identyfikator konkursu
df['konkurs_id'] = df['data_konkursu'].astype(str) + '_' + df['Title of Competition'].str.replace(r'\s+', '_', regex=True)

# Dodajemy identyfikator pary (na podstawie numeru lub imienia)
df['para_id'] = df['numer'].astype(str) + '_' + df['para']

# Dla przejrzystości ograniczamy do potrzebnych kolumn
df_oceny = df[['konkurs_id', 'para_id', 'taniec', 'sedzia', 'ocena']]


# Liczymy średnią ocenę wszystkich sędziów dla danej pary w danym tańcu
df_oceny['srednia_dla_pary'] = df_oceny.groupby(['konkurs_id', 'para_id', 'taniec'])['ocena'].transform('mean')

# Liczymy odchylenie konkretnego sędziego od średniej
df_oceny['odchylenie_sedziego'] = df_oceny['ocena'] - df_oceny['srednia_dla_pary']

# Średnie odchylenie sędziego od reszty
df_bias = df_oceny.groupby('sedzia')['odchylenie_sedziego'].mean().sort_values()

print(df_bias)
df_pair_bias = df_oceny.groupby(['sedzia', 'para_id'])['odchylenie_sedziego'].mean().unstack()

# Przykład: zobaczmy tylko silne pozytywne odchylenia
df_pair_bias[df_pair_bias > 0.5].dropna(how='all')
'''

print(df)

df['konkurs_id'] = df['Date & Location'] + '-' + df['Title of Competition']

df['srednia_dla_pary'] = df.groupby(['konkurs_id', 'numer', 'taniec'])['ocena'].transform('mean')
df['odchylenie_sedziego'] = df['ocena'] - df['srednia_dla_pary']

#report = sv.analyze(df)
#report.show_html('sweetviz_report.html')

profile = ProfileReport(df, title="Raport", explorative=True)
profile.to_file("raport.html")


