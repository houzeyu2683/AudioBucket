import AudioBucket.tube
link = 'https://www.youtube.com/playlist?list=PLHludR7A__g5YkL-MsxBzgO3K7ckydobE'
storage = 'storage/PLHludR7A__g5YkL-MsxBzgO3K7ckydobE'
engine = AudioBucket.tube.Engine(link=link, storage=storage)
engine.pullCatalog()
engine.pullArchive()

import AudioBucket.syndication
link = 'https://anchor.fm/s/27b2c13c/podcast/rss'
storage = 'storage/27b2c13c'
engine = AudioBucket.syndication.Engine(link=link, storage=storage)
engine.pullCatalog()
engine.pullArchive()

