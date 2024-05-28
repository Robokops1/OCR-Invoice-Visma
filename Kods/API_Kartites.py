import requests
from requests.auth import HTTPBasicAuth

# API URL 
url = "https://horizonweb-cloud.visma.lv/REST_H34764033/rest/TDdmCustomer/template/2"

# Autentifikācijas dati
user = "restdemo_davis"
password = "uZKWVM#p8kUvN!"  

xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<resource>
    <docType>CRM</docType>
    <entity>
        <TIPS>3</TIPS>
        <NOSAUK>Jauns klients</NOSAUK>
        <REG_NR>123456789</REG_NR>
    </entity>
</resource>
"""
# Veicam pieprasījumu
response = requests.post(url, data=xml.strip().encode('utf-8'), headers={'Content-Type': 'application/xml'}, auth=HTTPBasicAuth(user, password))

# Pārbaudām atbildi
if response.status_code == 200:
    print("Pieprasījums veiksmīgs!")
    print(response.text)  
else:
    print("Pieprasījums neizdevās!")
    print("Statusa kods:", response.status_code)
    print("Atbilde:", response.text)