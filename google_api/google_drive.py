from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pandas as pd
import gspread

    
    
def authentication_sheets_process():
    creds = None

    SCOPES = ["https://www.googleapis.com/auth/drive"]
       
    if os.path.exists("google_api/token.json"):
        creds = Credentials.from_authorized_user_file("google_api/token.json", SCOPES)
    if not creds or not creds.valid:
        print("Os creds nao tao validos")
        if creds and creds.expired and creds.refresh_token:
            print("[authentication_sheets] - Requesting refresh token")

            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "google_api/credentials.json", 
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("/tmp/token.json", "w") as token:
            token.write(creds.to_json())
      
    return creds


def spread_sheet_operations(formatted_data, form_name):
    dataframe = pd.DataFrame([formatted_data])

    creds = authentication_sheets_process()
    client = gspread.authorize(creds)

    valvet_forms_sheet_id = "1mQmoCsZViLMNqTuHZEAub0wawW67VlaJkk2ocAc88yQ"
    sheet = client.open_by_key(valvet_forms_sheet_id)

    form_worksheet = sheet.worksheet(form_name)
    print("[spread_sheet_operations] - Succesfuly get form worksheet: ", form_worksheet)

    form_worksheet.append_row(dataframe.values.tolist()[0])

    return form_worksheet.get_all_records()
