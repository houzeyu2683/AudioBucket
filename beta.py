import feedparser
import pandas

# link = "https://feed.firstory.me/rss/user/cky2t3wib0v6t0948wnzgqscd"
link = 'https://feeds.soundon.fm/podcasts/adf29720-e93b-4856-a09e-b73544147ec4.xml'
channel = getattr(feedparser.parse(link), 'entries')
queue = []
for episode in channel:
    assert isinstance(episode, dict)
    existence = episode.get('enclosures', None)
    if(existence==[]): continue
    duration = episode.get('itunes_duration', None)
    title = episode.get("title", None)
    item = dict(episode.get('enclosures')[0])
    name = str(item.get("href")).split("?v=")[-1]
    link = item.get('href')
    value = {
        'name': name,
        'title': title,
        'duration': duration,
        'link': link
    }
    queue += [value]
    continue
queue = pandas.DataFrame(queue)
queue.iloc[0]['link']

'https://file.cdn.firstory.me/Record/cky2t3wib0v6t0948wnzgqscd/cmakk5cww089701tz6vsta0sk.mp3?v=1747022635817'

import requests

# 音訊檔案的連結
url = 'https://file.cdn.firstory.me/Record/cky2t3wib0v6t0948wnzgqscd/cmakk5cww089701tz6vsta0sk.mp3?v=1747022635817'

# 下載後儲存的檔案名稱（可自行更改）
filename = 'episode.mp3'

# 發送 GET 請求並寫入檔案
response = requests.get(url, stream=True)
if response.status_code == 200:
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"✅ 檔案已成功下載為：{filename}")
else:
    print(f"❌ 下載失敗，狀態碼：{response.status_code}")