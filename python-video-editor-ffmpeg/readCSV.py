import pandas as pd

def convert_string_to_list_of_pairs(string:str):
    # Separa la cadena de texto en una lista de pares
    array = string.split("|")
    
    if len(array) == 2:
        return array

    resultado = [array[i:i+2] for i in range(0, len(array), 2)]
    return resultado
        
#string = "00:00:00|00:01:00|00:01:08|00:07:26|00:08:25|00:09:26"
#string = "00:00:00|00:01:00|00:01:08|00:07:26|00:08:25|00:09:26"

# array = convert_string_to_list_of_pairs(string)

# print(array)

def readDataCSV(csvPath:str):
    df = pd.read_csv(csvPath)
    data = df.iterrows()
    items = []
    for row in data:
        item = row[1]
        id = item['ID']
        cortes = item['CORTES']
        
        if item['TYPE'] != 'Video':
            continue
        if not isinstance(cortes,str):
            continue
        cortes = convert_string_to_list_of_pairs(cortes)
        items.append({
            'id':id,
            'cortes':cortes
        })
    
    return items

# print(readDataCSV('videos-editar-paquete-mayo.csv'))
    