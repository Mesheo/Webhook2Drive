import pandas as pd
import json
import os

def json2csv(data):
    
    # Salva os dados JSON em um arquivo dentro da pasta 'json_converter'
    save_path = '/tmp'
    os.makedirs(save_path, exist_ok=True)
    file_name = os.path.join(save_path, 'received_data.json')

    with open(file_name, 'w') as file:
        json.dump(data, file)

    # Ler o arquivo JSON
    with open('/tmp/received_data.json', 'r') as json_file:
        data = json.load(json_file)

    print("[JSON_converter] - data: ", data)
    
    # Converter o dicionário para um DataFrame do Pandas
    df = pd.DataFrame(data, index=[0])

    # Escrever o DataFrame para um arquivo CSV
    df.to_csv('/tmp/output.csv', index=False, encoding='utf-8')

    print("CSV gerado com sucesso.")
    csv_file_path = '/tmp/output.csv'
    df = pd.read_csv(csv_file_path)
    # Imprimir o DataFrame
    print("Conteúdo do CSV:")
    print(df)