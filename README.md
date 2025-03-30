# AudioBucket

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

Last updated: 2025-03-30

This is a tool for downloading audio files, primarily supporting **RSS feeds** and **YouTube playlists**.  
By providing an **RSS link** or a **YouTube playlist link**, the tool will attempt to download all corresponding audio files.  

This tool is based on [`yt-dlp`][1] for downloading YouTube audio and has been modified to better fit specific needs.  

Install the package using the following `pip` command:  
```bash
pip install git+https://github.com/houzeyu2683/AudioBucket.git
```

1. Provide an RSS link or a YouTube playlist link  
2. Run the tool to start downloading the corresponding audio files  
3. Once the download is complete, the audio files will be stored in the designated folder  

For usage example, please refer to `handbook.py`.

```python
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
```

I hope this helps you. If you find it helpful, please give me a star.

---

[1]: https://github.com/yt-dlp/yt-dlp
