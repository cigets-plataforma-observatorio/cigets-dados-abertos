import pyodbc
import requests
import pandas as pd
from requests_toolbelt.multipart import encoder

# Dremio connection details
dremio_host = "200.137.215.27"
dremio_port = 31010
dremio_username = "admin"
dremio_password = "*GMLo@HFt2v4"

# CKAN API endpoint and credentials
ckan_api_url = 'http://localhost:5000/api/3/action'
ckan_username = 'ckan_admin'
ckan_api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJRcXk1UTRJR19VNXZYY0RVcFRJM0EwdWVTTERzd3RlZTVoZ3E5VkFWVC1FIiwiaWF0IjoxNjg4MzMyNzYzfQ.54XHVAwxQlZw4IGCFG3zMQoRUPvN6ut4hfHZEhBMCd8'

# Dremio query
dremio_query = "SELECT * FROM \"Analytics Layer\".\"SIMAPES_SAUDE_MEDICINA\".\"Consulta_Saude_Medicina\" limit 10"

# Dremio ODBC connection string
dremio_connection_string = f"Driver={{Dremio Connector}};ConnectionType=Direct;HOST={dremio_host};PORT={dremio_port};AuthenticationType=Plain;UID={dremio_username};PWD={dremio_password}"

# Create Dremio connection
dremio_conn = pyodbc.connect(dremio_connection_string, autocommit=True)

# Execute the Dremio query
df = pd.read_sql(dremio_query, dremio_conn)

# Export DataFrame to CSV
csv_data = df.to_csv(index=False)

# Writing file to ensure the results query is filled
file=open("arquivo.csv", "w")
file.write(str(csv_data))
file.close()

# Upload CSV to CKAN
request_data = {"id": "4f0c13c9-8fd8-412c-8215-78d290acb7c1"}

with open("arquivo.csv", "rb") as f:
    request_data["upload"] = ("arquivoOutro.csv", f, "application/octet-stream")
    form = encoder.MultipartEncoder(request_data)
    headers = {'Authorization': ckan_api_key} 
    headers["Content-Type"] = form.content_type
    print('Updating resource')
    response = requests.post(f'{ckan_api_url}/resource_patch', headers=headers, data=form)    

print('Response Status Code:', response.status_code)
print('Response Text:', response.text)
if response.status_code == 200:
    print('CSV file updated successfully in CKAN.')
else:
    print('Failed to update CSV file in CKAN.')
    print('Response:', response.text)
