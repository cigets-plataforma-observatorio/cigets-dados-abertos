import os
import pathlib
import pyodbc
import pandas as pd
import requests
from requests_toolbelt.multipart import encoder

host = "200.137.215.27"
port = 31010
uid = "admin"
pwd = "*GMLo@HFt2v4"
driver = "Dremio Connector"

ckan_api_url = 'http://localhost:5000/api/3/action'
ckan_username = 'ckan_admin'
ckan_api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJRcXk1UTRJR19VNXZYY0RVcFRJM0EwdWVTTERzd3RlZTVoZ3E5VkFWVC1FIiwiaWF0IjoxNjg4MzMyNzYzfQ.54XHVAwxQlZw4IGCFG3zMQoRUPvN6ut4hfHZEhBMCd8'

cnxn = pyodbc.connect("Driver={};ConnectionType=Direct;HOST={};PORT={};AuthenticationType=Plain;UID={};PWD={}".format(driver, host,port,uid,pwd),autocommit=True)
df = pd.read_sql("select * from INFORMATION_SCHEMA.VIEWS where table_schema = 'Analytics Layer.Educação'", cnxn)

for _, item in df.iterrows():
    caminho = item['TABLE_SCHEMA'].replace('.', os.sep)
    pathlib.Path(caminho).mkdir(parents=True, exist_ok=True)
    nome_arquivo = item['TABLE_NAME'].replace('\\', '-')
    nome_arquivo = item['TABLE_NAME'].replace('/', '-')
    with open(os.path.join(caminho, nome_arquivo), "w") as arquivo:
        print("Gravando ", caminho, nome_arquivo)
        arquivo.write(item['VIEW_DEFINITION'])
    
    # Consultando e escrevendo os resultados
    novoNomeArquivo = ""
    
    with open(os.path.join(caminho, nome_arquivo), "r") as ddl:
        ddlResults = pd.read_sql_query(ddl.read(), cnxn)
        ddlResults = ddlResults.dropna(0)
        csv_data = ddlResults.to_csv(index=False)
        novoNomeArquivo = str(nome_arquivo).replace(' ', '_').replace("-", "").replace(",", "") + ".csv"
        file=open(novoNomeArquivo, "w")
        file.write(str(csv_data))
        file.close()
        
    with open(novoNomeArquivo, "rb") as csv:
        request_data = {
            "id": "4f0c13c9-8fd8-412c-8215-78d290acb7c1", # Deve receber dinamicamente
            "upload": (novoNomeArquivo, csv, "application/octet-stream")
        }
        form = encoder.MultipartEncoder(request_data)
        headers = {'Authorization': ckan_api_key} 
        headers["Content-Type"] = form.content_type
        print('Updating resource: ' + novoNomeArquivo)
        response = requests.post(f'{ckan_api_url}/resource_patch', headers=headers, data=form)    
        print('Response Status Code:', response.status_code)
        #print('Response Text:', response.text)
        if response.status_code == 200:
            print('CSV file updated successfully in CKAN.')
        else:
            print('Failed to update CSV file in CKAN.')
            print('Response:', response.text)