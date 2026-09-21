from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os

app = FastAPI()

@app.post("/render-video")
async def render_video(
    images: list[UploadFile] = File(...),
    audios: list[UploadFile] = File(...)
):
    os.makedirs("temp", exist_ok=True)
    clips = []
    
    for i in range(len(images)):
        img_path = f"temp/image_{i}.png"
        aud_path = f"temp/audio_{i}.mp3"
        
        with open(img_path, "wb") as f:
            f.write(await images[i].read())
        with open(aud_path, "wb") as f:
            f.write(await audios[i].read())
            
        audio_clip = AudioFileClip(aud_path)
        video_clip = ImageClip(img_path).set_duration(audio_clip.duration).set_audio(audio_clip)
        clips.append(video_clip)

    final_video = concatenate_videoclips(clips, method="compose")
    output_path = "temp/final_video.mp4"
    final_video.write_videofile(output_path, fps=24, preset="ultrafast", audio_codec="aac")
    
    return FileResponse(output_path, media_type="video/mp4", filename="video_final.mp4")
