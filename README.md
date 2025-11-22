# SõnaScrapeAPI
API asub aadressil: https://sonascrape-f0dwdhf6adb7cmds.northeurope-01.azurewebsites.net/tulemused <br/>

Pilveversioon: v1 <br/>

API eesmärk on teostada sõna otsingut ERR uudisteportaalis. Näiteks soovin otsida sõna "Trump", API loeb kokku mitu korda sõna "Trump" (suur-väike täht ei mängi rolli) esineb ERR pealehe artiklite pealkirjades.
Sõnaotsing arvestab vaid https//err.ee veebilehe ESILEHE peamiste artiklitega.<br/>

Tegu on Python flask API-ga, mis kasutab Beautiful Soup teeki ERR portaali HTML alla laadimiseks. API jookseb Docker image pealt Azure Web App teenusena. Andmebaas on dokumendipõhine, Post päring API'l salvestab sõnaotsingu privaatsesse Azure blob storage'isse JSON failina. JSON faili sisuks on: päringu kuupäev, leitud sõnade arv, nimekiri sõna sisaldavatest artiklitest ja sõna ise.<br/>

Funktsionaalsus: <br/>

/tulemused - GET <br/>
tagastab kõik JSON failid, kus iga fail: päringu kuupäev, leitud sõnade arv, nimekiri sõna sisaldavatest artiklitest ja sõna ise. <br/>

/tulemused - POST - {"otsitav": "SIIA_SISESTA_OTSITAV_SÕNA"} <br/>
teostab sõnaotsingu ja salvestab tulemuse andmebaasi.

TODO:
1. andmebaasis 15 otsingu päringut ühes failis, endpointideks tulemused/1; tulemused/2; jne. Andmebaasis fail mis hoiab meeles käesolevat päringu numbrit. (v5) <br/>
2. Piirata korraga tehtavate päringute arvu. (v3) <br/>
3. legaalsus, ERR tingimused- peab salvestama koos pealkirjaga ka lingi artiklile. (v4) <br/>
4. Post päring võiks olla /tulemused endpointil (v3) <br/>
5. kas lisada ka tulemus andmebaasi kui ei leitud vastet??? <br/>
6. kas võimaldada sõnapaari otsing? nt. "Siim Kallas", mitte lihtsalt "Siim" või "Kallas"??? <br/>
7. Endpoint järje kuvamiseks, et kus failis hetkel hiljutiseim päring on ja/või kuvame järge igal GET päringul (v6)







