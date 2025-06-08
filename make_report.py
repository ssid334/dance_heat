#!/usr/bin/env python3

import requests
import chardet
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO


def get_loc(soup):

    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 2:
            label = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)

            if label == "Date & Location":
                print("Date & Location:", value)
                return value

def detailed_data(url):
    url = url.replace(".htm", "R.htm")
    response = requests.get(url)

    detected_encoding = chardet.detect(response.content)['encoding']
    response.encoding = detected_encoding

    html_text = response.content.decode('windows-1250')

    soup = BeautifulSoup(html_text, 'lxml')

    loc = get_loc(soup)

    tables = soup.find_all('table')

    if tables:
        target_table = tables[3]
        df = pd.read_html(StringIO(str(target_table)))[0]

        df["Date & Location"] = loc
        return df
        #print(df)
        #df.to_csv('wyniki_turnieju.csv', index=False, encoding='utf-8-sig')
        #print("Zapisano do 'wyniki_turnieju.csv'")
    else:
        print("Nie znaleziono żadnych tabel na stronie.")


def get_links():
    url = 'https://baza.polskitaniec.org/reg/LIVE/2025/20250510_Pruszcz_Gdanski/index.php'
    response = requests.get(url)

    detected_encoding = chardet.detect(response.content)['encoding']
    html = response.content.decode(detected_encoding)

    soup = BeautifulSoup(html, 'lxml')

    details_links = [
        a['href'] for a in soup.find_all('a')
        if a.text.strip().lower() == 'details' and a.has_attr('href')
    ]

    base_url = 'https://baza.polskitaniec.org/reg/LIVE/2025/20250510_Pruszcz_Gdanski/'
    full_links = [base_url + href for href in details_links]


    return full_links



if __name__ == "__main__":
    links = get_links()
    print('Found %s link(s)' % len(links))

    all_dfs = [ ]
    for i in links:
        all_dfs.append(detailed_data(i))


    combined_df = pd.concat(all_dfs, ignore_index=True)

    df = combined_df.replace('', pd.NA).dropna()
    df = df[df.iloc[:, 0] != 'Result of the Final']
    df = df[df.iloc[:, 0] != 'Place']

    #print(df)
    #df.to_csv("wyniki_polaczone.csv", index=False, encoding="utf-8-sig")

    import sweetviz as sv
    report = sv.analyze(df)
    report.show_html('sweetviz_report.html')


    from ydata_profiling import ProfileReport
    profile = ProfileReport(df, title="Raport", explorative=True)
    profile.to_file("raport.html")

    import dtale
    dtale.show(df)
