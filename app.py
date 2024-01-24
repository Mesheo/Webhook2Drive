from flask import Flask, jsonify, make_response, request
import os
from test_folder import test_folder
import json
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

def json_converter():
    # Ler o arquivo JSON
    with open('/tmp/json_converter/received_data.json', 'r') as json_file:
        data = json.load(json_file)

    print("[JSON_converter] - data: ", data)
    
    # Converter o dicionário para um DataFrame do Pandas
    df = pd.DataFrame(data, index=[0])

    # Reorganizar as colunas e substituir espaços por barras
    # df.columns = ['data/' + col.replace(' ', '/') for col in df.columns]

    # Escrever o DataFrame para um arquivo CSV
    df.to_csv('/tmp/output.csv', index=False, encoding='utf-8')

    print("CSV gerado com sucesso.")
    csv_file_path = '/tmp/output.csv'
    df = pd.read_csv(csv_file_path)
    # Imprimir o DataFrame
    print("Conteúdo do CSV:")
    print(df)

def drive_uploader():
    print("[drive_uploder] - Iniciando comunicação com drive")

    SCOPES = ["https://www.googleapis.com/auth/drive"]

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('/tmp/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        #Listando as pastas
        response = service.files().list(
            q="name='BackupFolder2022' and mimeType='application/vnd.google-apps.folder'",
            spaces='drive'
        ).execute()

        #Criando a pasta se não existe
        if not response['files']:
            file_metadada = {
                "name": "BackupFolder2022",
                "mimeType": "application/vnd/google-apps.folder"
            }

            file = service.files().create(
                body=file_metadada,
                fields="id"
            ).execute()

            folder_id = file.get('id')
        else:
            folder_id = response['files'][0]['id']

        #populando a pasta
        for file in os.listdir('backupfiles'):
            file_metadata = {
                "name": file,
                "parents": [folder_id] #adikcionando o file dentro da pasta
            }

            media = MediaFileUpload(f'backupfiles/{file}')
            upload_file = service.files().create(body=file_metadada,
                                                media_body=media,
                                                fields="id").execute()

    except HttpError as e:
        print("Error: ", str(e))

app = Flask(__name__)

@app.route("/")
def hello_from_root():
    dado = test_folder.funcao_modulo1()
    return jsonify(message=f'Hello from root! -> {dado}')

@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')

@app.route("/webhook", methods=["POST"])
def webhook():
    # Verifica se a requisição contém dados JSON
    if not request.is_json:
        return make_response(jsonify(error='Invalid JSON'), 400)

    # Obtém os dados JSON da requisição
    data = request.get_json()

    # Salva os dados JSON em um arquivo dentro da pasta 'json_converter'
    save_path = '/tmp/json_converter'
    os.makedirs(save_path, exist_ok=True)
    file_name = os.path.join(save_path, 'received_data.json')

    with open(file_name, 'w') as file:
        json.dump(data, file)

    json_converter()
    # Retorna uma resposta ao front-end (você pode personalizar isso conforme necessário)
    drive_uploader()
    return jsonify(message=f'Webhook data received successfully. JSON data saved at GoogleDrive')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == "__main__":
    app.run(debug=True)
