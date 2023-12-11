from google_play_scraper import (
    app,
    reviews,
    Sort,
)
from pandas import DataFrame
from tqdm import tqdm

#!pip install -qq google-play-scraper


# Target 'Productivity' Apps
app_packages = [
    'com.anydo',
    'com.todoist',
    'com.ticktick.task',
    'com.habitrpg.android.habitica',
    'cc.forestapp',
    'com.oristats.habitbull',
    'com.levor.liferpgtasks',
    'com.habitnow',
    'com.microsoft.todos',
    'prox.lab.calclock',
    'com.gmail.jmartindev.timetune',
    'com.artfulagenda.app',
    'com.tasks.android',
    'com.appgenix.bizcal',
    'com.appxy.planner'
]


app_infos = []

for ap in tqdm(app_packages):
  info = app(ap, lang='en', country='us')
  del info['comments']
  app_infos.append(info)


df_app_info = DataFrame(app_infos)
df_app_info.to_csv('Datasets/apps.csv', index=None, header=True)


app_reviews = []

for ap in tqdm(app_packages):
  for score in range(1, 6):
    for sort_order in [Sort.MOST_RELEVANT, Sort.NEWEST]:
      rvs, a = reviews(
          ap,
          lang='en',
          country='us',
          sort=sort_order,
          count=200 if score == 3 else 100,
          filter_score_with=score
      )

      for r in rvs:
        r['sortOrder'] = 'most_relevant' if sort_order == Sort.MOST_RELEVANT else 'newest'
        r['appId'] = ap
      app_reviews.extend(rvs)

df_app_reviews = DataFrame(app_reviews)
df_app_reviews.to_csv('Datasets/reviews.csv', index=None, header=True)

