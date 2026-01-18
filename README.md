# SõnaScrapeAPI

API hetkel üleval aadressil: https://sonascrapev6-2-eshyemckeah6b3g4.northeurope-01.azurewebsites.net <br/>

Eesmärk on teostada sõna otsingut ERR uudisteportaalis ja salvestada tulemus andmebaasi. Näiteks soovin otsida sõna "Trump", API loeb kokku mitu korda sõna "Trump" (suur-väike täht ei mängi rolli) esineb ERR pealehe artiklite pealkirjades.
Sõnaotsing arvestab vaid https//err.ee veebilehe esilehe peamiste artiklitega.<br/>

Päringud salvestatakse andmebaasis JSON failidesse, kus igas JSON failis on max 15 päringut. <br/>

POST - /tulemused <br/>
request body - {"otsitav": "SIIA_SISESTA_OTSITAV_SÕNA"} <br/>
https://sonascrapev6-2-eshyemckeah6b3g4.northeurope-01.azurewebsites.net/tulemused <br/>
Teostab sõnaotsingu ja salvestab tulemuse andmebaasi. <br/>

GET - /jarg <br/>
https://sonascrapev6-2-eshyemckeah6b3g4.northeurope-01.azurewebsites.net/jarg <br/>
Tagastab sõnumina kõige viimatise faili nr ja mitu päringut on selles failis. Antud päring on järje leidmiseks. <br/>

GET - /tulemused/SIIA_SISESTA_SOOVITUD_FAILINR <br/>
https://sonascrapev6-2-eshyemckeah6b3g4.northeurope-01.azurewebsites.net/tulemused/1 <br/>
Tagastab soovitud JSON faili sisu.<br/>

Tegu on Python flask API-ga, mis kasutab Beautiful Soup teeki ERR portaali HTML alla laadimiseks. API jookseb Docker image pealt Azure Web App teenusena. Andmebaas on dokumendipõhine, Post päring API'l salvestab sõnaotsingu tulemuse privaatsesse Azure blob storage'isse JSON faili. JSON faili sisuks on: päringu teostamise aeg, leitud sõnade arv, nimekiri sõna sisaldavatest artiklitest, sõna ise ja artiklite lingid. GET päringutel piirang- 100 per day, 50 per hour, 1 per second. POST päringul lisandub piirang- 5 per minute. <br/>

Hetkel pilves versioon: v6 <br/>
TODO:
1. andmebaasis 15 otsingu päringut ühes failis, endpointideks tulemused/1; tulemused/2; jne. Andmebaasis fail mis hoiab meeles käesolevat päringu numbrit. (v5) <br/>
2. Piirata korraga tehtavate päringute arvu. (v3) <br/>
3. legaalsus, ERR tingimused- peab salvestama koos pealkirjaga ka lingi artiklile. (v4) <br/>
4. Post päring võiks olla /tulemused endpointil (v3) <br/>
5. kas lisada ka tulemus andmebaasi kui ei leitud vastet??? jah. (v6)<br/>
6. kas võimaldada sõnapaari otsing? nt. "Siim Kallas", mitte lihtsalt "Siim" või "Kallas"??? (v7)<br/>
7. Endpoint järje kuvamiseks, et kus failis hetkel hiljutiseim päring on ja/või kuvame järge igal POST päringul. Lisatud, kuvame ainult GET /jarg päringul. (v6) <br/>







