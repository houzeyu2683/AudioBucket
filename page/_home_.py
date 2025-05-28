import gradio

class Home:

    def __init__(self, user: str) -> None:
        self.user = user
        return

    def renderComponent(self) -> None:
        gradio.HTML(f"<h1 style='text-align: center;'>PELA</h1>")
        gradio.HTML(f"<p style='text-align: center;'>Hi, {self.user}</p>")
        return

    pass