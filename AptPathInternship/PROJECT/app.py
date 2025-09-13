import streamlit as st
import os
import tempfile
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips
import ffmpeg

# UI config
st.set_page_config(page_title="🎬 Reelify", layout="centered")
st.title("🎬 Reelify: Create Smart Vertical Reels")

input_path = None
video_ready = False

# Choose input method
input_method = st.radio("📥 Select input method", ["Upload File", "YouTube URL"])

# 📂 File Upload
if input_method == "Upload File":
    file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])
    if file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
            temp.write(file.read())
            input_path = temp.name
            video_ready = True

# 🔗 YouTube Link
elif input_method == "YouTube URL":
    url = st.text_input("Paste YouTube video link")
    if url and st.button("Download Video"):
        try:
            # Clean and format the URL
            if "youtu.be/" in url:
                url = url.replace("https://youtu.be/", "https://www.youtube.com/watch?v=")
            url = url.split("?")[0]  # remove extra params like ?feature=shared

            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True, file_extension="mp4").first()

            if not stream:
                st.error("❌ No downloadable MP4 stream found.")
            else:
                temp_dir = tempfile.mkdtemp()
                input_path = stream.download(output_path=temp_dir)
                st.success("✅ Video downloaded successfully!")
                video_ready = True
        except Exception as e:
            st.error(f"❌ Download failed: {e}")

# 🧪 Proceed with processing
if video_ready and input_path:
    st.video(input_path)

    # Step 1: Audio Extraction
    st.subheader("🎧 Audio Extraction")
    os.makedirs("output", exist_ok=True)
    audio_path = os.path.join("output", "audio.wav")

    try:
        ffmpeg.input(input_path).output(audio_path, **{"q:a": 0, "map": "a"}).run(overwrite_output=True)
        st.audio(audio_path)
        st.success("✅ Audio extracted successfully!")
    except Exception as e:
        st.error(f"❌ Error extracting audio: {e}")

    # Step 2: Create vertical short reel
    st.subheader("📱 Create 15-sec Smart Vertical Reel")

    try:
        clip = VideoFileClip(input_path)
        duration = clip.duration

        # Choose 3 parts: start, middle, end
        clips = []
        if duration >= 15:
            clips.append(clip.subclip(0, 5))
            clips.append(clip.subclip(duration / 2 - 2.5, duration / 2 + 2.5))
            clips.append(clip.subclip(duration - 5, duration))
        else:
            clips.append(clip.subclip(0, duration))

        final_clip = concatenate_videoclips(clips)

        temp_output = os.path.join("output", "temp_summary.mp4")
        vertical_output = os.path.join("output", "smart_vertical_reel.mp4")

        final_clip.write_videofile(temp_output, codec="libx264", audio_codec="aac")

        # Resize to vertical format using FFmpeg
        ffmpeg.input(temp_output).output(
            vertical_output,
            vf="scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
            vcodec="libx264", acodec="aac", format="mp4"
        ).run(overwrite_output=True)

        st.video(vertical_output)
        st.success("✅ Smart vertical reel created!")

        with open(vertical_output, "rb") as f:
            st.download_button("⬇️ Download Smart Reel", data=f, file_name="smart_reel.mp4", mime="video/mp4")

    except Exception as e:
        st.error(f"❌ Error generating reel: {e}")






