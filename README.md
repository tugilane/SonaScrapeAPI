# SõnaScrapeAPI

API eesmärk on teostada sõna otsingut veebi uudisteportaalides.<br/>
<br/>
API salvestab iga otsingupäringu privaatsesse Azure blob storage'isse JSON failina. JSON faili sisuks on: päringu kuupäev, leitud sõnade arv, nimekiri sõna sisaldavatest artiklitest ja sõna ise.<br/>
<br/>
ERR uudisteportaali puhul arvestab sõnaotsing vaid https//err.ee veebilehe esilehe artiklitega.
