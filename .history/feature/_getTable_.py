import pandas
import yt_dlp
import gradio
import datetime
import hashlib
import os

def getTable(link: str, query: str) -> tuple:
    option = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'no_warnings': True
    }
    with yt_dlp.YoutubeDL(option) as session:
        response = session.extract_info(link, download=False)
        pass
    information = response['entries']
    title = [item['title'] for item in information]
    name = [item['id'] for item in information]
    duration = [item['duration'] for item in information]
    sheet = pandas.DataFrame(
        {"name": name, 'title': title, 'duration': duration}
    )
    sheet = sheet.dropna().reset_index(drop=True)
    code = str(datetime.datetime.now()).encode()
    tag = hashlib.sha512(code).hexdigest()[:8]
    path = f'.cache/{tag}.csv'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    assert isinstance(sheet, pandas.DataFrame)
    status = gradio.update(visible=True)
    if(query==""): 
        sheet.to_csv(path, index=False)
        response = (sheet, path, status, status)
        return(response)
    sheet = sheet.query(query, engine='python')
    sheet.to_csv(path, index=False)
    table = (sheet, path, status, status)
    return(table)
