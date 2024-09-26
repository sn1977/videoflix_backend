# from pathlib import Path
# import subprocess

# import logging
# from venv import logger

# # def convert_480p(source):
# #   target = source + '_480p.mp4'
# #   cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
# #   subprocess.run(cmd, shell=True)

# def convert_360p(source):
#     # Konvertiere den Quellpfad in ein Path-Objekt
#     source_path = Path(source)
#     # Neues Ziel mit angehängter Auflösung und neuer Endung
#     target = str(source_path.with_suffix('')) + '_360p.mp4'
#     # ffmpeg-Befehl
#     # cmd = 'ffmpeg -i "{}" -s 640x360 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
#     cmd = f'ffmpeg -i "{source}" -s 640x360 -c:v libx264 -crf 23 -c:a aac "{target}"'
#     subprocess.run(cmd, shell=True)
    
# def convert_720p(source):
#     # Konvertiere den Quellpfad in ein Path-Objekt
#     source_path = Path(source)
#     # Neues Ziel mit angehängter Auflösung und neuer Endung
#     target = str(source_path.with_suffix('')) + '_720p.mp4'
#     # ffmpeg-Befehl
#     cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
#     subprocess.run(cmd, shell=True)
    
# def convert_1080p(source):
#     # Konvertiere den Quellpfad in ein Path-Objekt
#     source_path = Path(source)
#     # Neues Ziel mit angehängter Auflösung und neuer Endung
#     target = str(source_path.with_suffix('')) + '_1080p.mp4'
#     # ffmpeg-Befehl
#     cmd = 'ffmpeg -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
#     subprocess.run(cmd, shell=True)
    
#     # TODO - add a task to delete the original video file after all conversions are done
#     # TODO - add HLS conversion
    
#     logger = logging.getLogger(__name__)

# def convert_hls(source):
#     source_path = Path(source)
#     base = source_path.stem  # Name ohne Erweiterung
#     target_dir = source_path.parent / f"{base}_hls"
#     target_dir.mkdir(parents=True, exist_ok=True)
#     playlist = target_dir / "index.m3u8"

#     cmd = [
#         'ffmpeg',
#         '-i', str(source_path),
#         '-codec: copy',
#         '-start_number', '0',
#         '-hls_time', '10',
#         '-hls_list_size', '0',
#         '-f', 'hls',
#         str(playlist)
#     ]
#     try:
#         logger.info(f'Starte HLS-Konvertierung: {" ".join(cmd)}')
#         subprocess.run(cmd, check=True)
#         logger.info(f'HLS erfolgreich erstellt: {playlist}')
#     except subprocess.CalledProcessError as e:
#         logger.error(f'Fehler bei der HLS-Konvertierung: {e}')

from pathlib import Path
import subprocess
import logging

logger = logging.getLogger(__name__)  # Korrekte Logger-Initialisierung

def convert_360p(source):
    source_path = Path(source)
    target = str(source_path.with_suffix('')) + '_360p.mp4'
    cmd = f'ffmpeg -i "{source}" -s 640x360 -c:v libx264 -crf 23 -c:a aac "{target}"'
    subprocess.run(cmd, shell=True)
    logger.info(f'Video erfolgreich in 360p konvertiert: {target}')

def convert_720p(source):
    source_path = Path(source)
    target = str(source_path.with_suffix('')) + '_720p.mp4'
    cmd = f'ffmpeg -i "{source}" -s hd720 -c:v libx264 -crf 23 -c:a aac "{target}"'
    subprocess.run(cmd, shell=True)
    logger.info(f'Video erfolgreich in 720p konvertiert: {target}')

def convert_1080p(source):
    source_path = Path(source)
    target = str(source_path.with_suffix('')) + '_1080p.mp4'
    cmd = f'ffmpeg -i "{source}" -s hd1080 -c:v libx264 -crf 23 -c:a aac "{target}"'
    subprocess.run(cmd, shell=True)
    logger.info(f'Video erfolgreich in 1080p konvertiert: {target}')

def convert_hls(source):
    source_path = Path(source)
    base = source_path.stem  # Name ohne Erweiterung
    target_dir = source_path.parent / f"{base}_hls"
    target_dir.mkdir(parents=True, exist_ok=True)
    playlist = target_dir / "index.m3u8"

    cmd = [
        'ffmpeg',
        '-i', str(source_path),
        '-c', 'copy',
        '-start_number', '0',
        '-hls_time', '10',
        '-hls_list_size', '0',
        '-hls_segment_filename', f"{target_dir}/segment%03d.ts",  # Hinzugefügt für Segmentbenennung
        '-f', 'hls',
        str(playlist)
    ]
    try:
        logger.info(f'Starte HLS-Konvertierung: {" ".join(cmd)}')
        subprocess.run(cmd, check=True)
        logger.info(f'HLS erfolgreich erstellt: {playlist}')
    except subprocess.CalledProcessError as e:
        logger.error(f'Fehler bei der HLS-Konvertierung: {e}')