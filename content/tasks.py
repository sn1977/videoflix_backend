from pathlib import Path
import subprocess

# def convert_480p(source):
#   target = source + '_480p.mp4'
#   cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
#   subprocess.run(cmd, shell=True)

def convert_360p(source):
    # Konvertiere den Quellpfad in ein Path-Objekt
    source_path = Path(source)
    # Neues Ziel mit angehängter Auflösung und neuer Endung
    target = str(source_path.with_suffix('')) + '_360p.mp4'
    # ffmpeg-Befehl
    cmd = 'ffmpeg -i "{}" -s hd360 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd, shell=True)
    
def convert_720p(source):
    # Konvertiere den Quellpfad in ein Path-Objekt
    source_path = Path(source)
    # Neues Ziel mit angehängter Auflösung und neuer Endung
    target = str(source_path.with_suffix('')) + '_720p.mp4'
    # ffmpeg-Befehl
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd, shell=True)
    
def convert_1080p(source):
    # Konvertiere den Quellpfad in ein Path-Objekt
    source_path = Path(source)
    # Neues Ziel mit angehängter Auflösung und neuer Endung
    target = str(source_path.with_suffix('')) + '_1080p.mp4'
    # ffmpeg-Befehl
    cmd = 'ffmpeg -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd, shell=True)
    
    # TODO - add a task to delete the original video file after all conversions are done
    # TODO - add HLS conversion