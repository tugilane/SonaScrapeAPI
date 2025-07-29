# SõnaScrapeAPI

Eesmärgiks teostada sõnaotsing veebi uudisteportaalides.
API salvestab iga otsingupäringu privaatsesse Azure blob storage'isse JSON failina. JSON faili sisuks on: päringu kuupäev, leitud sõnade arv, nimekiri sõna sisaldavatest artiklitest ja sõna ise.

ERR uudisteportaali sõnaotsing arvestab vaid https//err.ee veebilehe esilehe artiklitega.
