import gradio as gr
from main import getResponse


iface = gr.Interface(
    fn=getResponse,
    inputs=gr.Textbox(lines=3, placeholder="Enter a sentence..."),
    outputs="text",
    title="Video RAG Search Assistant",
    description="Enter your question to see the answer!"
)

if __name__ == "__main__":
    iface.launch()
