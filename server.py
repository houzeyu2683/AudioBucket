import gradio
import yaml
import page

def getSecret(path: str) -> dict:
    paper = open(path, 'r')
    secret = yaml.load(paper, yaml.SafeLoader)
    paper.close()
    return(secret)

secret = getSecret(path='./secret.yaml')
title = 'VOMA'
with gradio.Blocks(title=title) as service:
    page.Home(user=secret['user']).renderComponent()
    pass
topic = 'Audio'
with service.route(f"{topic}", f"/{topic}"):
    page.Audio(user=secret['user']).renderComponent()
    pass
service.launch(
    server_name='0.0.0.0',
    server_port=8000, 
    share=False, 
    favicon_path='./metiral/logo.png', 
    debug=True,
    auth=(secret['user'], secret['password'])
)
