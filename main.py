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
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
cors = CORS(app, resources={r"/tulemused/*": {"origins": "*"}}) # Origins määrata frontend lehe aadress?
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "50 per hour", "1 per second"],
    storage_uri="memory://",
)

# Andmebaasi ühendusvõti
blob_connection_string = os.getenv('BLOB_CONNECTION_STRING') # azure muutuja- APPSETTING_AzureWebJobsStorage, lokaalne testimise muutuja- BLOB_CONNECTION_STRING
blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
#blob_container_name = os.getenv('BLOB_CONTAINER_NAME') # azure muutuja- APPSETTING_blob_container_name, vaikimisi konteiner- tulemused, lokaalne testimise muutuja- BLOB_CONTAINER_NAME

# Otsime Azure konteinerist blobi mida vajame ja tõmbame jsoni alla
def blob_lae_alla_json(failiNimi):
    blob_client = blob_service_client.get_blob_client(container= "tulemused", blob= failiNimi)
    download_stream = blob_client.download_blob()
    blob_content = download_stream.readall()
    json_data = json.loads(blob_content)
    return json_data

# uue otsingu data üles laadimine, uue JSON failina.
def blob_ules_laadimine(data, failiJarjekord, uusFail):
    fail = failiJarjekord + ".json" # selgitame mis faili saadame uue päringu
    blob_client = blob_service_client.get_blob_client(container="tulemused", blob=fail)

    if uusFail: # kui päring läheb uude faili, loome ka selle faili
        blob_client.upload_blob(data, overwrite=True)
    else: # kui ei lähe uude faili, lisame käesolevasse
        blob_client.upload_blob(data)

#selgitame kus maal on järjekord
def blob_lae_alla_jarjekord():
    blob_client = blob_service_client.get_blob_client(container="jarg", blob="jarjekord.txt") #järjefail
    return blob_client.download_blob().readall()

#laeme uue järjekorra üles
def blob_lae_ules_jarjekord(jarjekorraFail):
    blob_client = blob_service_client.get_blob_client(container="jarg", blob= "jarjekord.txt")
    blob_client.upload_blob(jarjekorraFail, overwrite=True)

# Vaatame tehtud sõnaotsinguid
@app.route('/tulemused/<id>', methods=['GET'])
def vaata_tulemusi(id):
    try:
        otsitavJson = id + ".json"
        data = blob_lae_alla_json(otsitavJson)
        print(data)
        return jsonify(data), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": str(e)}), 500

#Teeme päringu ERR pealehele ja teostama sõnaotsingu
@app.route('/tulemused', methods=['POST'])
@limiter.limit("5 per minute")
def lisa_tulemus():

    input = json.loads(request.data)
    sona = input['otsitav']
    try:
        leht = requests.get('https://err.ee')
        html = leht.text
        soup = bs4.BeautifulSoup(html, 'lxml')

        pealkirjaList = []
        artikliteLingid = []
        sonuKokku = 0
        for artikkel in soup.find_all(class_="article"): # Valime kõik objektid ERR pealehel millel "article" klass määratud
            pealkiri = artikkel.find("h2") # valitud objektides on h2 elemendina artiklite pealkirjad
            peamine = pealkiri.find("span")
            aadressLink = artikkel.find("a").attrs["href"] # salvestan artikli lingi

            if peamine is not None: # väike debug, sest sain artikli kus polnud pealkirja.
                artikkelTekst = peamine.get_text().lower() # artikkel väikesteks tähtedeks
                märgitaTekst = artikkelTekst.translate(str.maketrans('', '', string.punctuation)) #kaotan kirjavahemärgid
                sonadeArv = märgitaTekst.split().count(sona.lower()) # loen sõnad kokku
                if sonadeArv > 0:
                    sonuKokku += sonadeArv
                    pealkirjaList.append(artikkelTekst)
                    artikliteLingid.append(aadressLink)

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
            "pealkirjaList": pealkirjaList,
            "artikliteLingid": artikliteLingid,
        }

        json_data = json.dumps(data)

        try:
            #vaatame järjekorda ja uuendame järge
            jarjekord = blob_lae_alla_jarjekord().split(",") # failis esimene arv on käesolev fail ja teine arv on päringute arv failis
            uusFail = False  # kas vaja uus fail luua
            if jarjekord[1] == 15: # kui on 15 päringut failis
                jarjekord[0] = jarjekord[0] + 1 # muudame uueks faililaiendiks ühe võrra suurema arvu
                jarjekord[1] = 0 # nullime päringute arvu failis
                uusFail = True
            else:
                jarjekord[1] = jarjekord[1] + 1 # kui pole veel 15 päringut, lisama päringute arvule +1
            uuendatudJärjekord = jarjekord[0] + jarjekord[1]

            blob_lae_ules_jarjekord(uuendatudJärjekord) #laeme üles uue järjekorra
        except Exception as e:
            return jsonify({"message": "viga järjekorra failiga suhtluses " + str(e)}), 500

        blob_ules_laadimine(json_data, jarjekord[0], uusFail) # laeme üles uue päringu
        return ({'message': 'rida lisatud'}, 201)
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "viga sõnaotsingus " + str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

    #loogika kontrolli jaoks lehe allalaadimine
    #response = requests.get("https://err.ee")
    #with open("downloaded_page.html", "w", encoding="utf-8") as file:
    #    file.write(response.text)

