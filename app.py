import gradio as gr
from main import getResponse, enhanceResponse


def stream_video(start_time, end_time, video_id):
    html_code = f"""
    <video id="myVideo" width="640" height="360" controls autoplay muted playsinline>
        <source src="https://huggingface.co/datasets/pleyva2004/Video_RAG_Model_Dataset/resolve/main/{video_id}.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <script>
        const video = document.getElementById('myVideo');
        const startTime = {start_time};
        const endTime = {end_time};

        video.addEventListener('loadedmetadata', function() {{
            function trySeek() {{
                if (video.seekable.length > 0) {{
                    video.currentTime = 50;
                    video.play();
                }} else {{
                    setTimeout(trySeek, 200); // Try again in 200ms
                }}
            }}
            trySeek();
        }});

        video.addEventListener('timeupdate', function() {{
            if (video.currentTime >= endTime) {{
                video.pause();
            }}
        }});
    </script>
    """
    return html_code


def combined_interface(question):
    response = getResponse(question)
    text = response.get("chunk_text")
    start_time = (response.get("timestamp")[0])
    end_time = (response.get("timestamp")[1])
    print(start_time, end_time)
    video_id = response.get("video_id")
    print(video_id)
    enhanced_text = enhanceResponse(text, question) + " " + "Please view segment of the video from " + str(start_time) + " to " + str(end_time)
    video_html = stream_video(start_time, end_time, video_id)
    return enhanced_text, video_html

iface = gr.Interface(
    fn=combined_interface,
    inputs=[
        gr.Textbox(lines=3, placeholder="Enter your question...", label="Question"),
        ],
    outputs=[
        gr.Textbox(label="Answer"),
        gr.HTML(label="Video Player")
    ],
    title="Video RAG Search Assistant",
    description="Ask questions about the video and watch relevant segments!"
)

if __name__ == "__main__":
    iface.launch()
