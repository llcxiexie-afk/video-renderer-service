from fastapi import FastAPI
from fastapi.responses import FileResponse
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from pydantic import BaseModel
import os
import base64
import shutil

app = FastAPI()

class FileData(BaseModel):
    filename: str
    mimeType: str
    data: str

class RenderRequest(BaseModel):
    images: list[FileData]
    audios: list[FileData]

@app.post("/render-video")
async def render_video(request: RenderRequest):
    os.makedirs("temp", exist_ok=True)
    
    # Decodificar y guardar imágenes
    image_paths = []
    for i, img in enumerate(request.images):
        img_path = f"temp/image_{i}.png"
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(img.data))
        image_paths.append(img_path)
    
    # Decodificar y guardar audios
    audio_paths = []
    for i, aud in enumerate(request.audios):
        aud_path = f"temp/audio_{i}.mp3"
        with open(aud_path, "wb") as f:
            f.write(base64.b64decode(aud.data))
        audio_paths.append(aud_path)
    
    # Crear clips de video
    clips = []
    min_count = min(len(image_paths), len(audio_paths))
    for i in range(min_count):
        audio_clip = AudioFileClip(audio_paths[i])
        video_clip = ImageClip(image_paths[i]).set_duration(audio_clip.duration).set_audio(audio_clip)
        clips.append(video_clip)
    
    # Concatenar y exportar
    final_video = concatenate_videoclips(clips, method="compose")
    output_path = "temp/final_video.mp4"
    final_video.write_videofile(output_path, fps=24, preset="ultrafast", audio_codec="aac")
    
    # Limpiar archivos temporales
    for path in image_paths + audio_paths:
        if os.path.exists(path):
            os.remove(path)
    
    return FileResponse(output_path, media_type="video/mp4", filename="video_final.mp4")
