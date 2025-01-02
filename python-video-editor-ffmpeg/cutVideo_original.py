# cutVideo.py
import subprocess
import os

def cutMultipleVideo(input_video_path: str, name: str, ext: str, cortes: list[list[str]], outdir: str):
    file_dir = os.path.join(outdir, name)
    file_txt = os.path.join(file_dir, 'files.txt')

    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    if os.path.exists(file_txt):
        os.remove(file_txt)

    with open(file_txt, mode='a+', encoding='utf-8') as filetxt:
        filetxt.write('# primer línea\n')
        
        for index, corte in enumerate(cortes):
            inicio = corte[0]
            fin = corte[1]
            filename = f'{name}part{index}.{ext}'
            filedir = os.path.join(file_dir, filename)

            # Optimización de FFmpeg para cortes más rápidos
            subprocess.run([
                'ffmpeg', 
                '-i', input_video_path, 
                '-ss', inicio, 
                '-to', fin,
                '-c:v', 'copy',  # Copiar el video sin recodificar
                '-c:a', 'copy',  # Copiar el audio sin recodificar
                '-avoid_negative_ts', '1',
                filedir
            ], check=True)

            filetxt.write(f"file '{filedir}'\n")

    out_filename = os.path.join(outdir, f'{name}.mp4')
    
    # Optimización de la concatenación
    subprocess.run([
        'ffmpeg',
        '-fflags', '+genpts',
        '-f', 'concat',
        '-safe', '0',
        '-i', file_txt,
        '-c', 'copy',
        '-movflags', '+faststart',
        out_filename
    ], check=True)

def cutSingleVideo(input_video_path: str, name: str, ext: str, cortes: list[str], outdir: str):
    inicio = cortes[0]
    fin = cortes[1]
    filename = f'{name}.{ext}'
    filedir = os.path.join(outdir, filename)

    # Optimización de FFmpeg para cortes más rápidos
    subprocess.run([
        'ffmpeg',
        '-i', input_video_path,
        '-ss', inicio,
        '-to', fin,
        '-c:v', 'copy',  # Copiar el video sin recodificar
        '-c:a', 'copy',  # Copiar el audio sin recodificar
        '-avoid_negative_ts', '1',
        '-movflags', '+faststart',
        filedir
    ], check=True)
