import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import os
import numpy as np
import matplotlib.pyplot as plt

URL = 'https://www.mohfw.gov.in/'

# make a GET request to fetch the raw HTML content
# web_content = requests.get(URL).content
response = requests.get(URL).content

# parse the html content
# soup = BeautifulSoup(web_content, "html.parser")
soup = BeautifulSoup(response, 'html.parser')

SHORT_HEADERS = ['SNo', 'State', 'Total Confirmed Cases*',
                 'Recovered/Cured', 'Deaths**']

# remove any newlines and extra spaces from left and right


def extract_contents(row): return [x.text.replace('\n', '') for x in row]


header = extract_contents(soup.tr.find_all('th'))


# find all table rows and data cells within
stats = []
all_rows = soup.find_all('tr')

for row in all_rows:
    stat = extract_contents(row.find_all('td'))
# notice that the data that we require is now a list of length 5
    if len(stat) == 5:
        stats.append(stat)

objects = []
for row in stats:
    objects.append(row[1])

y_pos = np.arange(len(objects))

performance = []

for row in stats:
    performance.append(int(row[2]) + int(row[3]))

table = tabulate(stats, headers=SHORT_HEADERS)
print(table)

# Chart: 1 Bar chart

plt.barh(y_pos, performance, align='center', alpha=0.5,
         color='red', edgecolor='black')
plt.yticks(y_pos, objects)
plt.xlim(1, 100000)
plt.xlabel('Number Of Cases')
plt.title('COVID-19 cases')
plt.show()
