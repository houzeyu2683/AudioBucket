import gradio
import pandas
import shutil
import os
import yt_dlp
import datetime
import hashlib
import feedparser
import requests
import time

class Audio:
    """
    音訊處理類別，負責 Gradio 介面渲染、音訊來源搜尋與下載。
    """

    # 初始化使用者名稱
    def __init__(self, user: str) -> None:
        self.user = user
        return

    # 渲染 Gradio 互動式元件
    def renderComponent(self) -> None:
        gradio.HTML(f"<h1 style='text-align: center;'>Audio</h1>")
        variant = "default"
        with gradio.Row(variant=variant):
            variant = "default"
            with gradio.Column(variant=variant):
                # 來源輸入框
                source = gradio.Textbox(label="Enter Source")
                # 條件查詢輸入框
                condition = gradio.Textbox(label="Enter Condition")
                # 搜尋按鈕
                search = gradio.Button(value="Search")
                # 下載表格檔案
                # 預設隱藏
                self.archive['table'] = gradio.File(
                    label="Download Table", 
                    interactive=False, 
                    visible=False
                )
                # 收集音訊按鈕
                # 預設隱藏
                collect = gradio.Button(value='Collect', visible=False)
                # 下載音訊壓縮包
                # 預設隱藏
                self.archive['package'] = gradio.File(
                    label="Download Audio", 
                    interactive=False, 
                    visible=False
                )
                pass
            # 建立空的 DataFrame 作為表格初始值
            column = {"title": [], "duration": [], "name": [], "link": []}
            value = pandas.DataFrame(column)
            # 顯示搜尋結果的表格
            self.view['table'] = gradio.Dataframe(
                value, 
                max_height=500, 
                wrap=True, 
                show_row_numbers=True
            )
            pass
        # 進度顯示區塊
        self.view['progress'] = gradio.HTML("<br><br>")
        # 綁定搜尋按鈕事件
        search.click(
            fn=self.search, 
            inputs=[source, condition], 
            # 顯示表格
            # 顯示表格下載區域
            # 顯示表格檔案
            # 顯示收集按鈕
            # 隱藏音檔下載區域
            outputs=[
                self.view['table'], 
                self.archive['table'], 
                self.archive['table'], 
                collect,
                self.archive['package']
            ]
        )
        # 綁定收集音訊按鈕事件
        collect.click(
            fn=self.collect,
            inputs=[self.archive['table']],
            # 顯示音檔下載區域
            # 顯示音檔檔案
            outputs=[
                self.archive['package'], 
                self.archive['package']
            ],
            show_progress_on=self.view['progress']
        )
        return

    # 搜尋音訊來源
    def search(self, link: str, query: str) -> tuple:
        # 若來源為 YouTube 播放清單
        if('youtube' in link and 'playlist' in link):
            option = {
                'quiet': True,
                'extract_flat': True,
                'force_generic_extractor': True,
                'no_warnings': True
            }
            with yt_dlp.YoutubeDL(option) as session:
                response = session.extract_info(link, download=False)
                information = response['entries']
                # 取得標題、ID、時長
                title = [item['title'] for item in information]
                name = [item['id'] for item in information]
                duration = [item['duration'] for item in information]
                pass
            host = 'https://www.youtube.com/watch?v='
            link = [f'{host}{item}' for item in name]
            # 建立 DataFrame
            table = pandas.DataFrame({
                "name": name, 
                'title': title, 
                'duration': duration, 
                'link': link
            })
            pass
        # 若來源為 Firstory 播放清單
        elif('firstory.me' in link):
            channel = getattr(feedparser.parse(link), 'entries')
            queue = []
            for episode in channel:
                assert isinstance(episode, dict)
                existence = episode.get('enclosures', None)
                if(existence==[]): continue
                duration = episode.get('itunes_duration', None)
                title = episode.get("title", None)
                item = dict(episode.get('enclosures')[0])
                # 以 hash 產生唯一檔名
                name = hashlib.sha256(str(item.get("href")).encode()).hexdigest()[:8]
                link = item.get('href')
                value = {
                    'title': title,
                    'duration': duration,
                    'name': name,
                    'link': link
                }
                queue += [value]
                continue
            table = pandas.DataFrame(queue)
            pass
        # 移除缺漏值並重設索引
        table = table.dropna().reset_index(drop=True)
        if(True):
            # 建立暫存資料夾
            history = os.path.join(".cache", self.user)
            _ = shutil.rmtree(history, ignore_errors=True)
            os.makedirs(history, exist_ok=True)
            # 產生唯一標籤
            code = str(datetime.datetime.now()).encode()
            tag = hashlib.sha512(code).hexdigest()[:8]
            path = os.path.join(history, f'{tag}.csv')
            # 若有查詢條件則進行過濾
            if(query!=""): 
                table = table.query(query, engine='python')
                table = table.reset_index(drop=True)
                pass
            # 儲存查詢結果
            table.to_csv(path, index=False)
            pass
        # 設定元件顯示狀態
        visible = gradio.update(visible=True)
        invisible = gradio.update(visible=False)
        response = (table, path, visible, visible, invisible)
        return(response)

    # 收集音訊檔案並打包
    def collect(self, path: str) -> tuple:
        # 取得標籤與目錄
        tag = str(os.path.basename(path)).replace(".csv", "")
        folder = os.path.join('.cache', self.user, tag)
        os.makedirs(folder, exist_ok=True)
        # 讀取表格
        table = pandas.read_csv(path)
        length = len(table)
        progress = gradio.Progress()
        # 逐筆下載音訊
        for index, item in progress.tqdm(table.iterrows(), total=length):
            # 若來源為 YouTube 播放清單
            if('youtube' in item['link']):
                memory = os.path.join(folder, item['name'])
                option = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(folder, f"{item['name']}.%(ext)s"),
                    'quiet': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'wav'
                    }],
                    'postprocessor_args': [
                        '-ar', '16000'
                    ],
                    'paths': {
                        'temp': memory
                    }
                }
                session = yt_dlp.YoutubeDL(option)
                try:
                    session.download([item['link']])
                    pass
                except:
                    session.close()
                    shutil.rmtree(memory, ignore_errors=True)
                    print(f"Progress: [{index+1}|{length}]", end='\r')
                    continue
                session.close()
                shutil.rmtree(memory, ignore_errors=True)
                if(index%5==0): time.sleep(5)
                pass
            # 若來源為 Firstory 播放清單
            elif('firstory.me' in item['link']):
                response = requests.get(item['link'], stream=True)
                if(response.status_code!=200):
                    print(f"Progress: [{index+1}|{length}]", end='\r')
                    continue
                target = os.path.join(folder, f"{item['name']}.wav")
                stream = open(target, 'wb')
                for chunk in response.iter_content(chunk_size=8192):
                    _ = stream.write(chunk)
                    continue
                stream.close()
                pass
            print(f"Progress: [{index+1}|{length}]", end='\r')
            continue
        print(f"Progress: [{length}|{length}]")
        total = len(os.listdir(folder))
        print(f"Total: [{total}|{length}]")
        if(True):
            # 壓縮所有音訊檔案
            shutil.make_archive(
                base_name='package', 
                format='zip', 
                root_dir=folder
            )
            path = os.path.join(folder, "package.zip")
            shutil.move('./package.zip', path)
            pass
        visible = gradio.update(visible=True)
        response = (path, visible)
        return(response)

    # 靜態屬性：存放檔案元件
    archive = {'table': None, 'package': None}
    # 靜態屬性：存放顯示元件
    view = {'table': None, 'progress': None}
    pass
