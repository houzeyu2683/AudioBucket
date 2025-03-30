import AudioBucket.tube
link = 'https://www.youtube.com/playlist?list=PLHludR7A__g5YkL-MsxBzgO3K7ckydobE'
storage = 'storage/PLHludR7A__g5YkL-MsxBzgO3K7ckydobE'
engine = AudioBucket.tube.Engine(link=link, storage=storage)
engine.pullCatalog()
engine.pullArchive()

import AudioBucket.syndication
link = 'https://media.rss.com/sanguoxzhu/feed.xml'
storage = 'storage/sanguoxzhu'
engine = AudioBucket.syndication.Engine(link=link, storage=storage)
engine.pullCatalog()
engine.pullArchive()

