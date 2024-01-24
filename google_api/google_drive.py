from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import os

def drive_uploader(form_name):
    print("[drive_uploder] - Iniciando comunicação com drive")
    SCOPES = ["https://www.googleapis.com/auth/drive"]

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

    try:
        service = build("drive", "v3", credentials=creds)

        #Listando as pastas
        response = service.files().list(
            q="name='Forms' and mimeType='application/vnd.google-apps.folder'",
            spaces='drive'
        ).execute()

        #Criando a pasta se não existe
        if not response['files']:
            file_metadata = {
                "name": "Forms",
                "mimeType": "application/vnd/google-apps.folder"
            }

            file = service.files().create(
                body=file_metadata,
                fields="id"
            ).execute()

            folder_id = file.get('id')
        else:
            folder_id = response['files'][0]['id']

        #populando a pasta
        file_metadata = {
            "name": form_name,
            "parents": [folder_id] #adikcionando o file dentro da pasta
        }

        media = MediaFileUpload(f'/tmp/output.csv')
        upload_file = service.files().create(body=file_metadata,
                                            media_body=media,
                                                fields="id").execute()

    except HttpError as e:
        print("Error: ", str(e))