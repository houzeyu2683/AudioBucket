import AudioBucket.tube

link = 'https://www.youtube.com/playlist?list=PLu_yoBy_pbO3pR1OGnVruMEJQT4jVDn6X'
storage = f'storage/PLu_yoBy_pbO3pR1OGnVruMEJQT4jVDn6X/'
engine = AudioBucket.tube.Engine(link=None, storage=storage)
engine.pullCatalog()
engine.readCatalog(f'{storage}catalog.csv')
engine.pullArchive()

import AudioBucket.syndication

link = 'https://anchor.fm/s/27b2c13c/podcast/rss'
storage = 'storage/27b2c13c'
engine = AudioBucket.syndication.Engine(link=link, storage=storage)
engine.pullCatalog()
engine.readCatalog(f'{storage}catalog.csv')
engine.pullArchive()

