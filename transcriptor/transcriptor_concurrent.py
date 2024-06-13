from pymongo import MongoClient
from moviepy.editor import VideoFileClip
import requests
import os
from tqdm import tqdm
import concurrent.futures
import logging
import colorlog

def setup_logger():
    log_colors = {
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }

    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
        log_colors=log_colors
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger

logger = setup_logger()

def convert_video_to_audio(video_file_path, audio_file_path):
    try:
        video = VideoFileClip(video_file_path)
        audio = video.audio
        audio.write_audiofile(audio_file_path)
        audio.close()
        video.close()
    except Exception as e:
        logging.error(f"Error converting video to audio: {e}")

def download_video(url, file_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            with open(file_path, 'wb') as file, tqdm(
                desc=file_path,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        bar.update(len(chunk))
            logging.info(f"Download completed: {file_path}")
        else:
            logging.error(f"Failed to download video. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error downloading video: {e}")

def process_document(document):
    video_file_path = f'D:/webir/{document["_id"]}.mp4'
    audio_file_path = f'D:/webir/{document["_id"]}.mp3'
    
    try:
        download_video(document['video'], video_file_path)
        convert_video_to_audio(video_file_path, audio_file_path)
        os.remove(video_file_path)
    except Exception as e:
        logging.error(f"Error processing document {document['_id']}: {e}")

def main():
    uri='mongodb+srv://spoturno:AJFY2oSTelEuFT66@webirdatabase.slyw0m4.mongodb.net/?retryWrites=true&w=majority&appName=WebirDatabase'
    client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=False)
    db = client['webir']
    collection = db['lessons']

    all_documents = collection.find()
    documents_list = list(all_documents)

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(process_document, document) for document in documents_list[100:124]]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error in future: {e}")

if __name__ == "__main__":
    main()
