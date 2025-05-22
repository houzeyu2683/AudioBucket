import gradio
import pandas
import feature

secret = feature.getSecret("secret.yaml")
version = '1.0.0'
title = 'AudioBucket'
theme = gradio.themes.Ocean()
archive = {}
figure = {}
with gradio.Blocks(title=title, theme=theme) as interface:
    gradio.HTML(f"<h1 style='text-align: center;'>{title}</h1>")
    variant = "default"
    with gradio.Row(variant=variant):
        variant = "default"
        with gradio.Column(variant=variant):
            source = gradio.Textbox(label="Enter Source")
            query = gradio.Textbox(label="Enter Query")
            getTable = gradio.Button(value="Get Table")
            archive['table'] = gradio.File(
                label="Download Table", 
                interactive=False, 
                visible=False
            )
            getAudio = gradio.Button(value='Get Audio', visible=False)
            archive['audio'] = gradio.File(
                label="Download Audio", 
                interactive=False, 
                visible=False
            )
            pass
        value = pandas.DataFrame(
            {"name": [], "title": [], "duration": []}
        )
        figure['table'] = gradio.Dataframe(value, max_height=500, wrap=True, show_row_numbers=True)
        getTable.click(
            fn=feature.getTable, 
            inputs=[source, query], 
            outputs=[figure['table'], archive['table'], archive['table'], getAudio]
        )
        pass
    progress = gradio.HTML("<br><br>")
    getAudio.click(
        fn=feature.getAudio,
        inputs=[archive['table']],
        outputs=[archive['audio'], archive['audio']],
        show_progress_on=progress
    )
    pass

interface.launch(
    server_name='0.0.0.0',
    server_port=8000, 
    share=False, 
    favicon_path='./metiral/logo.png', 
    debug=True,
    auth=(secret['user'], secret['password'])
)
