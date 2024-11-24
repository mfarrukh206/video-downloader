from flask import Flask, render_template, request, redirect, url_for, flash, Response
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Directory to save temporary video/audio
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('video_url')
    download_format = request.form.get('format')  # Get the selected format (audio/video)

    if not video_url:
        flash("Please enter a valid YouTube URL.")
        return redirect(url_for('index'))

    try:
        # If the user selects 'audio', we set up the ydl_opts for audio-only download.
        if download_format == 'audio':
            ydl_opts = {
                'format': 'bestaudio/best',  # Best audio format only
                'postprocessors': [{
                    'key': 'FFmpegAudioConvertor',  # Convert audio
                    'preferredcodec': 'mp3',  # Convert to mp3
                    'preferredquality': '192',  # Audio quality
                }],
                'noplaylist': True  # Disable playlist downloads
            }
        else:
            # Default to video download if 'audio' is not selected
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',  # Download best video and audio combined
                'merge_output_format': 'mp4',  # Ensure video and audio are merged into MP4
            }

        # Use yt-dlp to download the video/audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            filename = f"{info_dict['title']}.mp4"

            # Stream the video directly to the browser
            def generate():
                # Open the file as a stream and yield it in chunks to the browser
                with ydl.temp_files[0].open('rb') as f:
                    while chunk := f.read(1024 * 1024):  # Read 1MB at a time
                        yield chunk

            # Return the stream as a response with appropriate headers
            return Response(generate(),
                            content_type='video/mp4',
                            headers={"Content-Disposition": f"attachment; filename={filename}"})

        flash("Download completed successfully!")
    except yt_dlp.utils.DownloadError as e:
        flash(f"An error occurred: {str(e)}")
    except Exception as e:
        flash(f"An error occurred: {str(e)}")

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
