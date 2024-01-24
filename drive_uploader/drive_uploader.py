import os
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

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

        with open('token.json', 'w') as token:
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