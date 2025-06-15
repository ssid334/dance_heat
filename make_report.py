#!/usr/bin/env python3

import requests
import chardet
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from tqdm import tqdm
import numbers


def get_details(soup):

    rv = { }
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 2:
            label = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)

            if label in ["Date & Location", 'Competition', 'Title of Competition', 'Organizer', 'Master of Ceremony', 'Chairman', 'Scrutineer(s)']:
                #print("Date & Location:", value)
                rv[label] = value
    return rv


def add_votes(mdf, url):
    response = requests.get(url)

    detected_encoding = chardet.detect(response.content)['encoding'] or 'utf-8'
    html_text = response.content.decode(detected_encoding, errors='ignore') # or replace
    soup = BeautifulSoup(html_text, 'lxml')
    details = get_details(soup)
    tables = soup.find_all('table')

    #print('url:', url, 'tables:', tables)
    if tables:
        adj_table = tables[2]
        dfd = pd.read_html(StringIO(str(adj_table)))[0]

        dfd_clean = dfd
        result_dict = dict(zip(dfd_clean[0], dfd_clean[1]))

        unwanted_keys = {'Adjudicators', 'ID', 'Name', 'Country'}
        cleaned_adj = {k: v for k, v in result_dict.items() if k not in unwanted_keys }
        cleaned_adj = {k: v for k, v in cleaned_adj.items() if k == k and v == v} # bo tylko NaN != NaN

        #print(cleaned_adj)
        # {'D': 'Fabrega Calderon Jordi', 'E': 'Filippone Federico', 'G': 'Kurgan Pavel', 'I': 'Piskarev Andrey', 'K': 'Suslavicius Remigijus', 'L': 'Svars Aigars', 'Q': 'Longarini Giuseppe'}

        target_table = tables[3]
        df = pd.read_html(StringIO(str(target_table)))[0]
        #print(df)

        '''
                      0                     1                     2                     3                     4                     5   ...                    10                    11                    12                    13                    14                    15
0   Marks of the Couples  Marks of the Couples  Marks of the Couples  Marks of the Couples  Marks of the Couples  Marks of the Couples  ...  Marks of the Couples  Marks of the Couples  Marks of the Couples  Marks of the Couples  Marks of the Couples  Marks of the Couples
1             Couple No.          Adjudicators          Adjudicators          Adjudicators          Adjudicators          Adjudicators  ...           Calculation           Calculation           Calculation           Calculation           Place Dance         Sum of Places
2             Couple No.                     D                     H                     U                     V                     X  ...                   1-3                   1-4                   1-5                   1-6           Place Dance         Sum of Places
3                  WALTZ                 WALTZ                 WALTZ                 WALTZ                 WALTZ                 WALTZ  ...                 WALTZ                 WALTZ                 WALTZ                 WALTZ                     1                     1
4                    321                     5                     6                     3                     5                     5  ...                     1                     1                     5                     -                     5                5 / 5.
5                    325                     6                     4                     6                     4                     6  ...                     -                     2                     3                     7                     6                6 / 6.
6                    328                     3                     5                     5                     2                     3  ...                     5                     -                     -                     -                     3                3 / 3.
7                    330                     4                     2                     4                     6                     4  ...                     1                     6                     -                     -                     4                4 / 4.
8                    331                     1                     1                     1                     1                     2  ...                     -                     -                     -                     -                     1                1 / 1.
9                    336                     2                     3                     2                     3                     1  ...                     -                     -                     -                     -                     2                2 / 2.
10                 TANGO                 TANGO                 TANGO                 TANGO                 TANGO                 TANGO  ...                 TANGO                 TANGO                 TANGO                 TANGO                     2                   1-2
11                   321                     6                     6                     3                     5                     5  ...                     1                     1                     4                     -                     5               10 / 5.
12                   325                     5                     3                     6                     6                     6  ...                     1                     1                     3                     7                     6               12 / 6.
13                   328                     2                     5                     5                     2                     1  ...                     -                     -                     -                     -                     2                5 / 2.
14                   330                     3                     2                     4                     3                     3  ...                     5                     -                     -                     -                     3                7 / 4.
15                   331                     1                     1                     1                     1                     4  ...                     -                     -                     -                     -                     1                2 / 1.
16                   336                     4                     4                     2                     4                     2  ...                     4                     -                     -                     -                     4                6 / 3.
17        VIENNESE WALTZ        VIENNESE WALTZ        VIENNESE WALTZ        VIENNESE WALTZ        VIENNESE WALTZ        VIENNESE WALTZ  ...        VIENNESE WALTZ        VIENNESE WALTZ        VIENNESE WALTZ        VIENNESE WALTZ                     3                   1-3
18                   321                     5                     6                     3                     4                     5  ...                     1                     2                     5                     -                     5               15 / 5.
19                   325                     6                     4                     5                     6                     6  ...                     -                     1                     3                     7                     6               18 / 6.
20                   328                     2                     5                     6                     2                     3  ...                     5                     -                     -                     -                     3                8 / 2.
21                   330                     4                     1                     4                     5                     4  ...                     1                     6                     -                     -                     4               11 / 4.
22                   331                     1                     2                     1                     1                     2  ...                     -                     -                     -                     -                     1                3 / 1.
23                   336                     3                     3                     2                     3                     1  ...                     -                     -                     -                     -                     2                8 / 3.
24             QUICKSTEP             QUICKSTEP             QUICKSTEP             QUICKSTEP             QUICKSTEP             QUICKSTEP  ...             QUICKSTEP             QUICKSTEP             QUICKSTEP             QUICKSTEP                     4                   1-4
25                   321                     6                     6                     3                     5                     6  ...                     1                     1                     3                     7                     6               21 / 5.
26                   325                     5                     4                     4                     6                     5  ...                     -                     2                     5                     -                     5               23 / 6.
27                   328                     2                     5                     6                     2                     4  ...                     3                     5                     -                     -                     4               12 / 3.
28                   330                     3                     2                     5                     3                     3  ...                     6                     -                     -                     -                     3               14 / 4.
29                   331                     1                     3                     1                     1                     2  ...                     -                     -                     -                     -                     1                4 / 1.
30                   336                     4                     1                     2                     4                     1  ...                     -                     -                     -                     -                     2               10 / 2.
31                   NaN                   NaN                   NaN                   NaN                   NaN                   NaN  ...                   NaN                   NaN                   NaN                   NaN                   NaN                   NaN

        '''


        adjudicator_columns = {}

        for col in df.columns:
            if df.at[1, col] == 'Adjudicators':   # wiersz 1 to Adjudicators
                judge_code = df.at[2, col]        # wiersz 2 to np. 'D', 'H' itd.
                if pd.notna(judge_code):
                    adjudicator_columns[col] = cleaned_adj.get(judge_code)

        #print(adjudicator_columns)


        glosowania = { }
        taniec = 'UNDEFINED'
        for row in df.itertuples(index=False):
            if row[0] == row[1] == row[2]:
                taniec = row[0]
            #print( { 'val': row[0]})
            #if isinstance(row[0], numbers.Number):
            if isinstance(row[0], str) and row[0].isdigit():
                for rating in adjudicator_columns:
                    #print('rating:', rating)
                    glosowania[ (row[0], taniec, adjudicator_columns[rating])] = row[rating]

        #print('glosowania:', glosowania)

        #print(mdf)

        rv_df = pd.DataFrame(columns=mdf.columns)
        rv_df['Taniec'] = None
        rv_df['Sedzia'] = None
        rv_df['Ocena'] = None

        ndf = [ ]

        columns = [ ]
        for row in mdf.itertuples(index=False):
            if isinstance(row[1], str) and row[1].isdigit(): # this is pair number

                '''
                 0                1                                     2                             3                Date & Location               Competition Title of Competition    Organizer            Master of Ceremony                     Chairman                  Scrutineer(s)
0  List of Couples  List of Couples                       List of Couples               List of Couples  14.06.2025 Ruscie k./Warszawy  Junior II B  - ST "B" ST     WDSF MAZOVIA CUP  KS K-STUDIO  Danuta Niemczynowicz Przekop  Piotr Czyżyk, Antoni Czyżyk  Jarosław Grunt, Piotr Seliger
1            Place              No.                                Couple                       Country  14.06.2025 Ruscie k./Warszawy  Junior II B  - ST "B" ST     WDSF MAZOVIA CUP  KS K-STUDIO  Danuta Niemczynowicz Przekop  Piotr Czyżyk, Antoni Czyżyk  Jarosław Grunt, Piotr Seliger
2              NaN              NaN                                   NaN                           NaN  14.06.2025 Ruscie k./Warszawy  Junior II B  - ST "B" ST     WDSF MAZOVIA CUP  KS K-STUDIO  Danuta Niemczynowicz Przekop  Piotr Czyżyk, Antoni Czyżyk  Jarosław Grunt, Piotr Seliger
3               1.              356        Meier Antoni & Jajko Marcelina             K-STUDIO - Krosno  14.06.2025 Ruscie k./Warszawy  Junior II B  - ST "B" ST     WDSF MAZOVIA CUP  KS K-STUDIO  Danuta Niemczynowicz Przekop  Piotr Czyżyk, Antoni Czyżyk  Jarosław Grunt, Piotr Seliger
4               2.              359     Szefer Franciszek & Stec Adrianna            SKT PASJA - Kraków  14.06.2025 Ruscie k./Warszawy  Junior II B  - ST "B" ST     WDSF MAZOVIA CUP  KS K-STUDIO  Danuta Niemczynowicz Przekop  Piotr Czyżyk, Antoni Czyżyk  Jarosław Grunt, Piotr Seliger
5               3.              355   Lewandowski Marcel & Chuchla Monika  SKT FABRYKA TAŃCA - Osielsko  14.06.2025 Ruscie k./Warszawy  Junior II B  - ST "B" ST     WDSF MAZOVIA CUP  KS K-STUDIO  Danuta Niemczynowicz Przekop  Piotr Czyżyk, Antoni Czyżyk  Jarosław Grunt, Piotr Seliger
6               4.              358  Petkevicius Emetas & Grabenaite Agne            ŽUVEDRA - Klaipeda  14.06.2025 Ruscie k./Warszawy  Junior II B  - ST "B" ST     WDSF MAZOVIA CUP  KS K-STUDIO  Danuta Niemczynowicz Przekop  Piotr Czyżyk, Antoni Czyżyk  Jarosław Grunt, Piotr Seliger
7              NaN              NaN                                   NaN                           NaN  14.06.2025 Ruscie k./Warszawy  Junior II B  - ST "B" ST     WDSF MAZOVIA CUP  KS K-STUDIO  Danuta Niemczynowicz Przekop  Piotr Czyżyk, Antoni Czyżyk  Jarosław Grunt, Piotr Seliger
                '''

                poz = row[0]
                nr = row[1]
                para = row[2]
                klub = row[3]
                datalokacja = row[4]
                comp = row[5]
                title = row[6]
                org = row[7]
                master = row[8]
                chairman = row[9]
                scru = row[10]

                ne = { }
                for i in glosowania:
                    if i[0] == nr:
                        ne = {
                                'pozycja': poz,
                                'numer': nr,
                                'para': para,
                                'Date & Location': datalokacja,
                                'Competition': comp,
                                'Title of Competition': title,
                                'Organizer': org,
                                'Master of Ceremony': master,
                                'Chairman': chairman,
                                'Scrutineer(s)': scru,
                                'taniec': i[1],
                                'sedzia': i[2],
                                'ocena': glosowania[i]
                                }
                        if not columns:
                            columns = list(ne.keys())
                        ndf.append(ne)

        df_result = pd.DataFrame(ndf, columns=columns)
        return df_result

def detailed_data(url):
    url = url.replace(".htm", "L.htm")
    response = requests.get(url)

    detected_encoding = chardet.detect(response.content)['encoding'] or 'utf-8'
    html_text = response.content.decode(detected_encoding, errors='ignore') # or replace
    soup = BeautifulSoup(html_text, 'lxml')
    details = get_details(soup)
    tables = soup.find_all('table')

    if tables:
        target_table = tables[3]
        df = pd.read_html(StringIO(str(target_table)))[0]

        #df["Date & Location"] = loc
        for i in details:
            df[i] = details[i]

        df = add_votes(df, url.replace("L.htm", "S.htm"))

        return df
        #print(df)
        #df.to_csv('wyniki_turnieju.csv', index=False, encoding='utf-8-sig')
        #print("Zapisano do 'wyniki_turnieju.csv'")
    #else:
    #    print("Nie znaleziono żadnych tabel na stronie.")



URLs2p = [
     'https://baza.polskitaniec.org/reg/LIVE/2025/20250118_Szczecin/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250222_Konin/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250223_Warszawa/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250301_Gdansk/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250301_Gdansk_1/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250308_Elblag/index.php'
    ,'https://baza.taniec-nowoczesny.pl/reg/LIVE/2025/20250308_Elblag_ZTN/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250308_Lubawa/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250308_Szczecinek/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250315_Elblag/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250316_Szczecin/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250323_Makow_Podhalanski/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250329_Grajewo/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250329_Sroda_Wielkopolska/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250329_Warszawa/Liga/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250329_Warszawa/Strefa/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250329_Zawiercie/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250405_Kamien_Pomorski/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250412_Lowicz/Liga/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250412_Lowicz/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250412_Nowogard/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250412_Rumia/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250413_Krakow/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250413_Osielsko/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250426_Wroclaw/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250427_Wroclaw/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250427_Zuromin/Liga/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250427_Zuromin/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250510_Pruszcz_Gdanski/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250510_Pruszcz_Gdanski/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250511_Krakow/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250511_Wikielec/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250516_Elblag/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250517_Nowy_Targ/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250524_Brodnica/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250518_Kobierzyce/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250524_Warszawa/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250525_Elblag/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250525_Pila/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250531_Gdansk/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250531_Miedzyzdroje/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250601_Augustow/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250607_Koszalin/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250607_Sochaczew_1/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250607_Sochaczew/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250608_Walbrzych/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250614_Kobylnica/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250614_Rusiec/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250614_Rusiec_1/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250615_Morag/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250615_Olecko/index.php'
    ,'https://baza.polskitaniec.org/reg/LIVE/2025/20250615_Szczecinek/index.php'
    ]

_URLs2p = [ #'https://baza.polskitaniec.org/reg/LIVE/2025/20250615_Szczecinek/index.php'
    'https://baza.polskitaniec.org/reg/LIVE/2025/20250614_Rusiec/index.php'
    #,'https://baza.polskitaniec.org/reg/LIVE/2025/20250614_Rusiec_1/index.php'
          ]

def get_links(url):
    #url = 'https://baza.polskitaniec.org/reg/LIVE/2025/20250510_Pruszcz_Gdanski/index.php'
    response = requests.get(url)

    detected_encoding = chardet.detect(response.content)['encoding']
    html = response.content.decode(detected_encoding)

    soup = BeautifulSoup(html, 'lxml')

    details_links = [
        a['href'] for a in soup.find_all('a')
        if a.text.strip().lower() == 'details' and a.has_attr('href')
    ]

    #base_url = 'https://baza.polskitaniec.org/reg/LIVE/2025/20250510_Pruszcz_Gdanski/'
    base_url = url.rstrip('index.php')
    full_links = [base_url + href for href in details_links]


    return full_links



if __name__ == "__main__":

    all_dfs = [ ]


    for miesiac in tqdm(URLs2p, desc='Miesiac', position=0):
        links = get_links(miesiac)

        for zawody in tqdm(links, desc='Zawody ', position=1, leave=False):
            all_dfs.append(detailed_data(zawody))



    combined_df = pd.concat(all_dfs, ignore_index=True)
    df = combined_df.replace('', pd.NA).dropna()

    for i in [ 'List of Couples', 'Result of the Final', 'Place']:
        df = df[df.iloc[:, 0] != i]

    df = df.rename(columns={0: 'Pozycja', 1: 'Nr. pary', 2: 'Para', 3: 'Klub'})

    #print(df)
    df.to_csv("wyniki_polaczone.csv", index=False, encoding="utf-8-sig")

    #import sweetviz as sv
    #report = sv.analyze(df)
    #report.show_html('sweetviz_report.html')

    from ydata_profiling import ProfileReport
    profile = ProfileReport(df, title="Raport", explorative=True)
    profile.to_file("raport.html")

    #import dtale
    #dtale.show(df)
