import gradio
import yaml
import page

def getSecret(path: str) -> dict:
    paper = open(path, 'r')
    secret = yaml.load(paper, yaml.SafeLoader)
    paper.close()
    return(secret)

# 讀取密鑰檔案
# 取得使用者帳號與密碼
secret = getSecret(path='./secret.yaml')

# 設定 Gradio 服務的標題
title = 'PELA'

# 註冊首頁
with gradio.Blocks(title=title) as service:
    # 渲染首頁元件
    page.Home(user=secret['user']).renderComponent()
    pass

# 設定 Audio 主題頁面的路由
topic = 'Audio'
with service.route(f"{topic}", f"/{topic}"):
    # 渲染 Audio 頁面元件
    page.Audio(user=secret['user']).renderComponent()
    pass

# 啟動 Gradio 服務
service.launch(
    server_name='0.0.0.0',           # 監聽所有網路介面
    server_port=8000,                # 伺服器埠號
    share=False,                     # 不啟用 Gradio 公開分享
    favicon_path='./metiral/logo.png', # 設定網站 favicon
    debug=True,                      # 啟用除錯模式
    auth=(secret['user'], secret['password']) # 設定登入驗證
)
