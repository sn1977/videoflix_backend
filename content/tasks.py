from pathlib import Path
import subprocess

# def convert_480p(source):
#   target = source + '_480p.mp4'
#   cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
#   subprocess.run(cmd, shell=True)

def convert_480p(source):
    # Konvertiere den Quellpfad in ein Path-Objekt
    source_path = Path(source)
    # Neues Ziel mit angehängter Auflösung und neuer Endung
    target = str(source_path.with_suffix('')) + '_480p.mp4'
    # ffmpeg-Befehl
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd, shell=True)