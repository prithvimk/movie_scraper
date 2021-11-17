from bs4 import BeautifulSoup
import requests
import string

movie_list = []

with open('movies.txt') as file:
    for movie in file:
        movie = movie.strip()

        url = 'https://en.wikipedia.org/wiki/' + string.capwords(movie)
        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'html5lib')

        table = soup.find('table', attrs={'class': 'infobox vevent'})

        content_dict = {}

        # getting name of the movie

        movie_name = table.find(
            'th', attrs={'class': 'infobox-above summary'}).text
        #print('Movie: ', movie_name)
        content_dict['Movie'] = movie_name

        # getting name of director

        director_name = table.find(
            'th', attrs={'class': 'infobox-label'}, text='Directed by').find_next().text
        #print('Director: ', director_name)
        content_dict['Director'] = director_name

        # getting year of release

        release_date = table.find(
            'th', attrs={'class': 'infobox-label'}, text='Release date').find_next_sibling().text.strip()
        #print('Release Date: ', release_date)
        content_dict['Release Date'] = release_date

        # overall gross earnings

        overall_gross_earnings = table.find(
            'th', attrs={'class': 'infobox-label'}, text='Box office').find_next().text
        #print('Overall Gross Earnings: ', overall_gross_earnings)
        content_dict['Overall Gross Earnings'] = overall_gross_earnings

        # names of the cast

        label = table.find(
            'th', attrs={'class': 'infobox-label'}, text='Starring').find_next_sibling()
        cast = []
        #print('Cast:')

        for s in label.strings:
            if str(s.strip()):
                cast.append(s.strip())
        #print(cast)
        content_dict['Cast'] = cast

        movie_list.append(content_dict)

print(movie_list)

import csv

fields = ['Movie', 'Director', 'Release Date', 'Overall Gross Earnings', 'Cast']

with open('output.csv', 'w', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fields)

    writer.writeheader()

    writer.writerows(movie_list)