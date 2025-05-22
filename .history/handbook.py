import AudioBucket.tube

link = 'https://www.youtube.com/playlist?list=PLSg6_lakxpXHXJc1lc113qWrbNuxDzK9E'
storage = f'storage/非凡新聞9/'
engine = AudioBucket.tube.Engine(link=link, storage=storage)
engine.pullCatalog()
catalog = engine.catalog.copy()
engine.catalog = catalog[catalog['title'].str.contains('主播葉芷娟')]
engine.catalog
engine.pullArchive()

# import AudioBucket.syndication

# link = 'https://anchor.fm/s/27b2c13c/podcast/rss'
# storage = 'storage/27b2c13c'
# engine = AudioBucket.syndication.Engine(link=link, storage=storage)
# engine.pullCatalog()
# engine.readCatalog(f'{storage}catalog.csv')
# engine.pullArchive()

