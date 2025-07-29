import requests
import datetime
import zoneinfo
import bs4
import lxml
import string
import os
import json
from flask import Flask, jsonify
from flask import request
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

blob_connection_string = os.getenv('BLOB_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)

def blob_tulemuste_nimekiri():
    container_client = blob_service_client.get_container_client(container= "tulemused")
    blob_client = container_client.get_blob_client("tulemused.json")
    blob_data = blob_client.download_blob().readall()
    return json.loads(blob_data)

def blob_ules_laadimine(data):
    container_client = blob_service_client.get_container_client(container="tulemused")
    blob_client = container_client.get_blob_client("tulemused.json")
    blob_client.upload_blob(data,)

@app.route('/tulemused', methods=['GET'])
def vaata_tulemusi():
    try:
        data = blob_tulemuste_nimekiri()
        print(data)
        return jsonify(data), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/tulemused', methods=['POST'])
def lisa_tulemus():

    input = json.loads(request.data)
    sona = input['otsitav']
    try:

        leht = requests.get('https://err.ee')
        html = leht.text
        soup = bs4.BeautifulSoup(html, 'lxml')

        pealkirjaList = []
        sonuKokku = 0
        for artikkel in soup.find_all(class_="article"):
            pealkiri = artikkel.find("h2")

            if pealkiri is not None:
                artikkelTekst = pealkiri.get_text().lower()
                märgitaTekst = artikkelTekst.translate(str.maketrans('', '', string.punctuation))
                sonadeArv = märgitaTekst.split().count(sona.lower())
                if sonadeArv > 0:
                    sonuKokku += sonadeArv
                    pealkirjaList.append(artikkelTekst)

        aegEestis = datetime.datetime.now(zoneinfo.ZoneInfo('Europe/Helsinki'))

        print(aegEestis.isoformat())
        print(sonuKokku)
        print(pealkirjaList)

        data = {
            "sona": sona,
            "sonuKokku": sonuKokku,
            "aeg": aegEestis.isoformat(),
            "pealkirjaList": pealkirjaList
        }

        json_data = json.dumps(data)
        blob_ules_laadimine(json_data)
        return ('rida lisatud', 200)
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


