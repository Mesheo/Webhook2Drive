from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os
import pandas as pd
import gspread

def authentication_process():
    print("[google_drive] - Iniciando Autenticação com Google Cloud")

    SCOPES = ["https://www.googleapis.com/auth/drive",
              "https://www.googleapis.com/auth/spreadsheets"]

    creds = None

    if os.path.exists("google_api/token.json"):
        creds = Credentials.from_authorized_user_file("google_api/token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "google_api/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('/tmp/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def download_file(service, file_id, file_name, destination_path):
    request = service.files().get_media(fileId=file_id)

    with open(destination_path, "wb") as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
    print(f"Arquivo '{file_name}' baixado com sucesso como '{destination_path}'.")
  
def merge_csv_files(original_file, new_file, merged_file):
    df_original = pd.read_csv(original_file)
    df_new = pd.read_csv(new_file)

    # Concatenar os DataFrames
    df_merged = pd.concat([df_original, df_new], ignore_index=True)

    # Salvar o DataFrame mesclado em um novo arquivo CSV
    df_merged.to_csv(merged_file, index=False, encoding='utf-8')

    print(f"Arquivos CSV mesclados com sucesso. Arquivo salvo como '{merged_file}'.")

def drive_uploader(form_name, csv_file_path):
    creds = authentication_process()

    target_folder_id = ''
    try:
        service = build("drive", "v3", credentials=creds)

        #Verificando se a pasta já existe
        folder_name = 'VELVET_FORMS';
        response = service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
            spaces='drive'
        ).execute()
        print(f"[google_drive] - AQUI as pastas com nome {folder_name}: ", response['files'])
 
        #Criando a pasta se não existe
        if not response['files']:
            print(f"[google_drive] - Pasta {folder_name} não encontrada, criando agora...")
            file_metadata = {
                "name": folder_name,
                "mimeType": "application/vnd/google-apps.folder"
            }

            file = service.files().create(
                body=file_metadata,
                fields="id"
            ).execute()
            target_folder_id = file.get('id')

        else:
            print(f"[google_drive] - Pasta {folder_name} já existe!")
            target_folder_id = response['files'][0]['id']

        #Verificando se ja tem um csv do formulario dentro pasta
        result = service.files().list(
                q=f"name='{form_name}' and '{target_folder_id}' in parents",
                spaces="drive",
            ).execute()

        form_file = result.get("files", [])

        if form_file:
            print("[goole_drive] - Arquivo csv do formulario encontrado, inciando adição...", form_file)

            form_file_id = form_file[0]["id"]
            download_path = "/tmp/download_form_file.csv"

            download_file(service, form_file_id, f'{form_name}.csv', download_path)
            merge_csv_files(csv_file_path, download_path, "/tmp/merged_output.csv")

             # Upload do novo arquivo mesclado
            media = MediaFileUpload("/tmp/merged_output.csv")
            request = service.files().update(
                fileId=form_file_id,
                media_body=media
            ).execute()

            print("[google_drive] - Arquivo atualizado com sucesso: ", request)
        else:
            print("[google_drive] - Arquivo csv não encontrado na pasta, criando agora...")

            # Arquivo não existe, cria um novo
            file_metadata = {
                "name": form_name,
                "parents": [target_folder_id]
            }
            
            media = MediaFileUpload(f'/tmp/output.csv')
            request = service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            ).execute()

    except HttpError as e:
        print("Error: ", str(e))

def spread_sheet_operations():
    creds =authentication_process()
    client = gspread.authorize(creds)

    sheet_id = "1mQmoCsZViLMNqTuHZEAub0wawW67VlaJkk2ocAc88yQ"
    sheet = client.open_by_key(sheet_id)
    values_list = sheet["High Net-Worth Individual"].row_values(1)
    return values_list
