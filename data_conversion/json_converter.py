import pandas as pd
import json
import os
from datetime import datetime  

def json2csv(data):
    print("[json_converter] - Salvando os dados recebidos como .json: ", data)
    
    save_path = '/tmp'
    os.makedirs(save_path, exist_ok=True)
    file_name = os.path.join(save_path, 'received_data.json')
    with open(file_name, 'w') as file:
        json.dump(data, file)

    with open('/tmp/received_data.json', 'r') as json_file:
        data = json.load(json_file)

    print("[JSON_converter] - dados do JSON salvo: ", data)
    
    df = pd.DataFrame(data, index=[0])

    csv_file_path = '/tmp/output.csv'
    df.to_csv(csv_file_path, index=False, encoding='utf-8')
    print("[json_converter] - CSV gerado com sucesso.")

    df = pd.read_csv(csv_file_path)
    print("[json_converter] - Conteúdo do CSV em dataframe: ", df)

    return csv_file_path
 
def format_data(data, form_name):
    formatted_data = {'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    if form_name in ["independent_financial_advisor", "familly_office", "wealth_manager"]:
        formatted_data.update({
            "First Name": data.get("First name", ""),
            "Last Name": data.get("Last name", ""),
            "Email": data.get("Email", ""),
            "Company Name": data.get("Company Name", ""),
            "Country of Company": data.get("", ""),
            "AUM": data.get("AUM", ""),
            "Lead Interests": data.get("Lead Interests", ""),
        })

    elif form_name in "contact":
        formatted_data.update({
            "Message Nature": data.get("", ""),
            "First Name": data.get("Firstname", ""),
            "Last Name": data.get("Last name", ""),
            "Email": data.get("email", ""),
            "Message": data.get("Message", "")
        })

    elif form_name in "high_net_worth_individual":
        formatted_data.update({
            "First Name": data.get("First name", ""),
            "Last Name": data.get("Last name", ""),
            "Email": data.get("Email", ""),
            "Investable Assets": data.get("Assets", ""),
            "Country": data.get("Country", ""),
            "Accredited Investor": data.get("Accredited Investor", "")
        })
    
    print("[format_data] - Dados normalizados: ", formatted_data)
    return formatted_data

def format_bulk_data(data, form_name):
    formatted_data = []

    if form_name in ["independent_financial_advisor", "familly_office", "wealth_manager"]:
        for item in data:
            formatted_item = {
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "First name": item.get("first name", ""),
                "Last name": item.get("last name", ""),
                "Email": item.get("email", ""),
                "Company Name": item.get("company name", ""),
                "": item.get("", ""),
                "AUM": item.get("aum", ""),
                "Lead Interests": item.get("lead interests", "")
            }
            formatted_data.append(formatted_item)

    elif form_name in "contact":
        for item in data:
            formatted_item = {
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "": item.get("", ""),
                "Firstname": item.get("firstname", ""),
                "Last name": item.get("last name", ""),
                "email": item.get("email", ""),
                "Message": item.get("message", "")
            }
            formatted_data.append(formatted_item)

    elif form_name in "high_net_worth_individual":
        for item in data:
            formatted_item = {
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "First name": item.get("first name", ""),
                "Last name": item.get("last name", ""),
                "Email": item.get("email", ""),
                "Assets": item.get("assets", ""),
                "Country": item.get("country", ""),
                "Accredited Investor": item.get("accredited investor", "")
            }
            formatted_data.append(formatted_item)
            
    return formatted_data