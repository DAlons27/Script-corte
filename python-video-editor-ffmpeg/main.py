import os
import cutVideo
import readCSV
import mimetypes
import datetime

csv_path = ''
input_folder = ''
output_folder = ''

def main():
    
    csv_path = input('Ingrese la ruta del archivo CSV: ')
    
    if not os.path.exists(csv_path):
        print('[**************************************************]')
        print('La ruta del archivo no existe')
        print('[**************************************************]')
        return
    
    if not os.path.isfile(csv_path):
        print('[**************************************************]')
        print('La ruta ingresada no es de un archivo')
        print('[**************************************************]')
        return
    
    mime = mimetypes.guess_type(csv_path)
    if not 'csv' in mime[0]:
        print('[**************************************************]')
        print('El archivo ingresado no es un CSV')
        print('[**************************************************]')
        return
    
    input_folder = input('Ingrese la carpeta donde se encuentran los videos sin editar: ')
    
    if not os.path.exists(input_folder):
        print('[**************************************************]')
        print('El directorio no existe')
        print('[**************************************************]')
        return
    
    if not os.path.isdir(input_folder):
        print('[**************************************************]')
        print('La ruta ingresada no es un directorio')
        print('[**************************************************]')
        return
    
    output_folder = input('Ingrese la carpeta donde se guardarán los videos editados: ')
    
    if not os.path.exists(output_folder):
        print('[**************************************************]')
        print('El directorio no existe')
        print('[**************************************************]')
        return
    
    if not os.path.isdir(output_folder):
        print('[**************************************************]')
        print('La ruta ingresada no es un directorio')
        print('[**************************************************]')
        return
    
    if not os.path.exists(os.path.join(os.getcwd(),'logs')):
        os.mkdir(os.path.join(os.getcwd(),'logs'))
    
    now = datetime.datetime.now()
    date_time_str = now.strftime("%Y%m%d-%H%M")
    
    path_log_not_found = os.path.join(os.getcwd(),'logs',f'{date_time_str}-ids_not_found_pruebas.txt') 
    path_log_erros = os.path.join(os.getcwd(),'logs',f'{date_time_str}-erros_pruebas.txt') 
    
    log_not_found = open(path_log_not_found,mode='+a',encoding='utf-8')
    
    log_erros = open(path_log_erros,mode='+a',encoding='utf-8')
    
    items = readCSV.readDataCSV(csv_path)
    
    print(f'[***** {len(items)} PARA EDITAR *****]')
    
    count = 0
    
    for item in items:
        id = item['id']
        cortes = item['cortes']
        
        exist = os.path.join(output_folder,f'{id}.mp4')
        
        if os.path.exists(exist):
            count += 1
            print(f'ID {id} YA FUE EDITADO')
            continue
        
        radis_list = os.listdir(input_folder) 
        radi_founded = False
        input_video_path = ''
        for radi in radis_list:
            if f'{id}.' in radi and '.mp4' in radi:
                radi_founded = True
                input_video_path = os.path.join(input_folder,radi)
                break
        if not radi_founded:
            log_not_found.write(f'{id},\n')
            continue
        try:
            if type(cortes[0]) == str:
                print('CORTE SIMPLE')
                cutVideo.cutSingleVideo(input_video_path,f'{id}','mp4',cortes,output_folder)
                count += 1
            elif type(cortes[0]) == list:
                print('CORTE MULTIPLE')
                cutVideo.cutMultipleVideo(input_video_path,f'{id}','mp4',cortes,output_folder)
                count += 1
        except Exception as e:
            print(f'[!!!!! ERROR AL EDITAR {id} !!!!!]')
            log_erros.write(f'ID {id} ERROR {e}\n')
            continue
    
    print(f'[***** SE EDITARON {count} DE {len(items)} VIDEOS *****]')
main()