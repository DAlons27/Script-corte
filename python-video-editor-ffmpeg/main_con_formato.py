import os
import cutVideo
import readCSV
import datetime
from typing import TextIO, List, Dict, Any, Tuple
import time
from multiprocessing import Pool, cpu_count
import psutil
import logging
#import wmi 

# Constantes
LOG_DIR = 'logs'
TEMP_LIMIT = 80  # Límite de temperatura en grados Celsius

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def write_to_log(file: TextIO, message: str) -> None:
    """
    Escribe un mensaje en el archivo de log.
    
    Args:
        file (TextIO): Archivo de log.
        message (str): Mensaje a escribir en el log.
    """
    file.write(f"{message}\n")

def verify_directory(path: str, message: str) -> bool:
    """
    Verifica si un directorio existe y es válido.
    
    Args:
        path (str): Ruta del directorio a verificar.
        message (str): Mensaje a mostrar en caso de error.
    
    Returns:
        bool: True si el directorio es válido, False en caso contrario.
    """
    if not os.path.exists(path):
        logging.error(f'❌ ¡Ups! No encuentro {message}')
        return False
    
    if not os.path.isdir(path):
        logging.error(f'❌ La ruta de {message} no parece ser una carpeta válida')
        return False
    
    return True

def create_log_files() -> Tuple[str, str]:
    """
    Crea los archivos de log y retorna las rutas.
    
    Returns:
        Tuple[str, str]: Rutas de los archivos de log creados.
    """
    log_dir = os.path.join(os.getcwd(), LOG_DIR)
    os.makedirs(log_dir, exist_ok=True)
    
    date_time_str = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    path_log_not_found = os.path.join(log_dir, f'{date_time_str}-ids_not_found_pruebas.txt')
    path_log_errors = os.path.join(log_dir, f'{date_time_str}-erros_pruebas.txt')
    
    # Crear archivos con manejo de contexto
    with open(path_log_not_found, 'a') as f:
        write_to_log(f, "#Log de IDs no encontrados")
    
    with open(path_log_errors, 'a') as f:
        write_to_log(f, "# Log de errores durante el procesamiento")
    
    return path_log_not_found, path_log_errors

def process_video(args: Tuple[Dict[str, Any], str, str, str, str]) -> bool:
    """
    Procesa un video individual y retorna True si fue exitoso.
    
    Args:
        args (Tuple[Dict[str, Any], str, str, str, str]): Argumentos necesarios para procesar el video.
    
    Returns:
        bool: True si el video fue procesado exitosamente, False en caso contrario.
    """
    item, input_folder, output_folder, path_log_not_found, path_log_errors = args
    id = item['id']
    cortes = item['cortes']
    
    # Verificar si el video ya fue procesado
    exist = os.path.join(output_folder, f'{id}.mp4')
    if os.path.exists(exist):
        logging.info(f'✅ El video {id} ya está listo')
        return True
    
    # Buscar el archivo de video
    input_video_path = ''
    for radi in os.listdir(input_folder):
        if f'{id}.' in radi and '.mp4' in radi:
            input_video_path = os.path.join(input_folder, radi)
            break
    
    if not input_video_path:
        with open(path_log_not_found, 'a') as f:
            write_to_log(f, f'{id},')
        return False
    
    try:
        if isinstance(cortes[0], str):
            logging.info(f'✂️  Realizando corte simple para el video {id}')
            cutVideo.cutSingleVideo(input_video_path, f'{id}', 'mp4', cortes, output_folder)
        elif isinstance(cortes[0], list):
            logging.info(f'✂️✂️ Realizando cortes múltiples para el video {id}')
            cutVideo.cutMultipleVideo(input_video_path, f'{id}', 'mp4', cortes, output_folder)
        return True
    except Exception as e:
        logging.error(f'❌ Error al editar {id}: {str(e)}')
        with open(path_log_errors, 'a') as f:
            write_to_log(f, f'ID {id} ERROR {str(e)}')
        return False

# def get_cpu_temperature() -> float:
#     """
#     Obtiene la temperatura de la CPU usando OpenHardwareMonitor a través de wmi.
    
#     Returns:
#         float: Temperatura de la CPU en grados Celsius, o None si no se puede obtener la temperatura.
#     """
#     try:
#         w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
#         temperature_info = w.Sensor()
#         for sensor in temperature_info:
#             if sensor.SensorType == 'Temperature' and 'CPU' in sensor.Name:
#                 return sensor.Value
#     except Exception as e:
#         logging.warning(f'No se pudo obtener la temperatura de la CPU: {str(e)}')
#     return None

def calculate_optimal_batch_size(total_items: int) -> int:
    """
    Calcula el tamaño óptimo del lote basado en el número total de items.
    
    Args:
        total_items (int): Número total de items a procesar.
    
    Returns:
        int: Tamaño óptimo del lote.
    """
    if total_items <= 10:
        return total_items
    elif total_items <= 30:
        return 10
    else:
        return 20

def get_processor_info() -> Tuple[int, int]:
    """
    Obtiene información sobre el procesador.
    
    Returns:
        Tuple[int, int]: Número de núcleos físicos y lógicos del procesador.
    """
    physical_cores = psutil.cpu_count(logical=False)
    logical_cores = cpu_count()  # Usando cpu_count de multiprocessing
    return physical_cores, logical_cores

def select_processing_intensity(cpu_count_logical: int) -> int:
    """
    Permite al usuario seleccionar la intensidad de procesamiento.
    
    Args:
        cpu_count_logical (int): Número de núcleos lógicos del procesador.
    
    Returns:
        int: Número de núcleos a utilizar para el procesamiento.
    """
    while True:
        print("\n🚀 ¡Elige qué tan rápido quieres que trabaje!")
        print(f"1 - Modo tranquilo (25% - {max(cpu_count_logical // 4, 1)} núcleos)")
        print(f"2 - Modo equilibrado (50% - {max(cpu_count_logical // 2, 1)} núcleos)")
        print(f"3 - Modo turbo ({cpu_count_logical - 1} núcleos)")
        
        try:
            choice = int(input("📝 ¿Qué modo prefieres? (1-3): "))
            if choice == 1:
                return max(cpu_count_logical // 4, 1)
            elif choice == 2:
                return max(cpu_count_logical // 2, 1)
            elif choice == 3:
                return max(cpu_count_logical - 1, 1)
            else:
                logging.warning("😅 Por favor, elige un número del 1 al 3")
        except ValueError:
            logging.warning("😅 Necesito un número válido del 1 al 3")

def process_batch(batch_items: List[Dict[str, Any]], input_folder: str, output_folder: str, 
                 path_log_not_found: str, path_log_errors: str, num_processes: int) -> List[bool]:
    """
    Procesa un lote de videos.
    
    Args:
        batch_items (List[Dict[str, Any]]): Lista de items a procesar.
        input_folder (str): Carpeta de entrada donde se encuentran los videos sin editar.
        output_folder (str): Carpeta de salida donde se guardarán los videos editados.
        path_log_not_found (str): Ruta del archivo de log para IDs no encontrados.
        path_log_errors (str): Ruta del archivo de log para errores.
        num_processes (int): Número de procesos a utilizar.
    
    Returns:
        List[bool]: Lista de resultados de procesamiento para cada video.
    """
    with Pool(processes=num_processes) as pool:
        args = [(item, input_folder, output_folder, path_log_not_found, path_log_errors) 
               for item in batch_items]
        return pool.map(process_video, args)

def main() -> None:
    """
    Función principal que coordina la ejecución del programa.
    """
    csv_path = r'C:\Users\Alons\Desktop\corte-video\python-video-editor-ffmpeg\SUBSANACIONES-KOLIBRI-CORTES.csv'
    
    # Mostrar información del procesador
    cpu_physical, cpu_logical = get_processor_info()
    print("\n💻 Información de tu computadora:")
    logging.info(f"• {cpu_physical} núcleos físicos")
    logging.info(f"• {cpu_logical} núcleos lógicos")
    
    # Seleccionar intensidad de procesamiento
    num_processes = select_processing_intensity(cpu_logical)
    logging.info(f"🚀 ¡Genial! Trabajaremos con {num_processes} núcleos")
    
    input_folder = input('\n📁 ¿Dónde están los videos sin editar?: ').strip()
    if not verify_directory(input_folder, 'la carpeta de videos'):
        return
    
    output_folder = input('📂 ¿Dónde quieres guardar los videos editados?: ').strip()
    if not verify_directory(output_folder, 'la carpeta de destino'):
        return
    
    path_log_not_found, path_log_errors = create_log_files()
    
    try:
        start_time = time.time()
        items = readCSV.readDataCSV(csv_path)
        total_items = len(items)
        logging.info(f'🎬 Encontré {total_items} videos para editar')
        
        batch_size = calculate_optimal_batch_size(total_items)
        total_batches = (total_items + batch_size - 1) // batch_size
        
        successful_edits = 0
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, total_items)
            current_batch = items[start_idx:end_idx]
            
            logging.info(f"✨ Procesando lote {batch_num + 1} de {total_batches}")
            logging.info(f"📊 Videos {start_idx + 1} a {end_idx} de {total_items}")
            
            # Verificar temperatura antes de procesar el lote
            # temp = get_cpu_temperature()
            # if temp and temp > TEMP_LIMIT:
            #     logging.warning(f"¡ADVERTENCIA! Temperatura CPU alta: {temp}°C")
            #     logging.info("Pausando por 2 minutos para enfriamiento...")
            #     time.sleep(120)
            
            # Procesar el lote

            results = process_batch(current_batch, input_folder, output_folder,
                                 path_log_not_found, path_log_errors, num_processes)
            
            successful_edits += sum(1 for result in results if result)
            
            if batch_num < total_batches - 1:
                logging.info("⏳ Pequeña pausa de 10 segundos...")
                time.sleep(1)
        
        end_time = time.time()
        total_process_time = end_time - start_time
        total_process_time_formatted = time.strftime("%H:%M:%S", time.gmtime(total_process_time))
        
        print("\n🎉 ¡Proceso completado!")
        logging.info(f'✅ Se editaron exitosamente {successful_edits} de {total_items} videos')
        logging.info(f'⏱️  Tiempo total: {total_process_time_formatted}')
        
    except Exception as e:
        logging.error(f'❌ Ups, algo salió mal: {str(e)}')
    finally:
        if os.path.exists(path_log_not_found) or os.path.exists(path_log_errors):
            print("\n📝 Los registros quedaron guardados en:")
            logging.info(f"• Videos no encontrados: {path_log_not_found}")
            logging.info(f"• Registro de errores: {path_log_errors}")

if __name__ == "__main__":
    main()
