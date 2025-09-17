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
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/tulemused/*": {"origins": "*"}}) # Origins määrata frontend lehe aadress?

# Andmebaasi ühendusvõti
blob_connection_string = os.getenv('APPSETTING_AzureWebJobsStorage')
blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
blob_container_name = os.getenv('APPSETTING_blob_container_name') # määran konteineri Azure env muutujana, igaks juhuks, äkki vaja konteinerit vahetada pärast

# Tõmbame JSON data tehtud otsingute kohta, kõik failid korraga.
def blob_tulemuste_nimekiri():
    container_client = blob_service_client.get_container_client(container= blob_container_name)
    blobs = container_client.list_blobs()
    blobidData = []

    for blob in blobs: # iga JSON faili puhul, tõmbame data alla
        blob_client = container_client.get_blob_client(blob.name)
        download_stream = blob_client.download_blob()
        blob_content = download_stream.readall()
        json_data = json.loads(blob_content)
        blobidData.append(json_data)

    return blobidData

# uue otsingu data üles laadimine, uue JSON failina.
def blob_ules_laadimine(data, aegNimeks):
    blob_client = blob_service_client.get_blob_client(container=blob_container_name, blob=aegNimeks)
    blob_client.upload_blob(data)

# Vaatame tehtud sõnaotsinguid
@app.route('/tulemused/', methods=['GET'])
def vaata_tulemusi():
    try:
        data = blob_tulemuste_nimekiri()
        print(data)
        return jsonify(data), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": str(e)}), 500

#Teeme päringu ERR pealehele ja teostama sõnaotsingu
@app.route('/tulemused/', methods=['POST'])
def lisa_tulemus():

    input = json.loads(request.data)
    sona = input['otsitav']
    try:
        leht = requests.get('https://err.ee')
        html = leht.text
        soup = bs4.BeautifulSoup(html, 'lxml')

        pealkirjaList = []
        sonuKokku = 0
        for artikkel in soup.find_all(class_="article"): # Valime kõik objektid ERR pealehel millel "article" klass määratud
            pealkiri = artikkel.find("h2") # valitud objektides on h2 elemendina artiklite pealkirjad
            peamine = pealkiri.find("span")

            if peamine is not None: # väike debug, sest sain artikli kus polnud pealkirja.
                artikkelTekst = peamine.get_text().lower()
                märgitaTekst = artikkelTekst.translate(str.maketrans('', '', string.punctuation)) #kaotan kirjavahemärgid
                sonadeArv = märgitaTekst.split().count(sona.lower())
                if sonadeArv > 0:
                    sonuKokku += sonadeArv
                    pealkirjaList.append(artikkelTekst)

        aegEestis = str(datetime.datetime.now(zoneinfo.ZoneInfo('Europe/Helsinki'))).split('.')[0]

        if sonuKokku == 0:
            return jsonify({'message': 'sõna ei leidu üheski artiklis'}, 204)

        print(aegEestis)
        print(sonuKokku)
        print(pealkirjaList)

        #koostatav fail
        data = {
            "sona": sona,
            "sonuKokku": sonuKokku,
            "aeg": aegEestis,
            "pealkirjaList": pealkirjaList
        }

        json_data = json.dumps(data)
        blob_ules_laadimine(json_data, aegEestis) # laeme üles
        return ({'message': 'rida lisatud'}, 201)
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

    #loogika kontrolli jaoks lehe allalaadimine
    #response = requests.get("https://err.ee")
    #with open("downloaded_page.html", "w", encoding="utf-8") as file:
    #    file.write(response.text)

