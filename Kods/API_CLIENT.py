import requests
from requests.auth import HTTPBasicAuth

# API URL sagatavošana
url = "https://horizonweb-cloud.visma.lv/REST_H34764033/rest/TDdmKlPamatDat/query?orderby=K.PK_KLIENTS&columns=K.NOSAUK,K.KODS"

# Autentifikācijas dati
user = "restdemo_davis"
password = "uZKWVM#p8kUvN!"  

# Veicam GET pieprasījumu
response = requests.get(url, auth=HTTPBasicAuth(user, password))

# Pārbaudām atbildi
if response.status_code == 200:
    print("Pieprasījums veiksmīgs!")
    print(response.text)  
else:
    print("Pieprasījums neizdevās!")
    print("Statusa kods:", response.status_code)
    print("Atbilde:", response.text)