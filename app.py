import gradio as gr
from main import getResponse


# 2. Build the Gradio 
iface = gr.Interface(
    fn=getResponse,
    inputs=gr.Textbox(lines=3, placeholder="Enter a sentence..."),
    outputs="text",
    title="Video RAG Search Assistant",
    description="Enter your question to see the answer!"
)

# 3. Launch the app
if __name__ == "__main__":
    iface.launch()
