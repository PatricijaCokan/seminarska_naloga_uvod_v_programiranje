OPIS PROJEKTA

Projekt služi kot analiza podatkov o rabljenih avtomobilih na spletnem mestu avto.net. Podatke sem pridobila iz te spletne strani in jih analizirala s pomočjo pythona in različnih knjižnic za delo s podatki

Največji izziv mi je pri projektu predstavljalo pridobivanje podatkov iz spletne strani avto.net. Že na začetu sem imela precej težav ker sem kot odgovor na http zahtevke dobivala neveljavne html strani, ki so mi sporočale da me je stran blokirala. To težavo sem uspela v večji meri odpraviti tako da sem v http zahtevke dodala glavo (headers) in pa naključno čakanje med zahtevki kar je pripeljalo do veliko večjega števila uspešno pridobljenih html strani z oglasi. 
S pomočjo python skripte Preberi_podatke.py sem podatke nato uredila in pripravila za analizo. Pri samem urejanju podatkov sem naletela na kar nekaj izivov preden mi je uspelo podatke pripeljati do točke, kjer se mi je zdelo da so pripravljeni in urejeni.

Podatki ki jih lahko najdete v oglasi_avto.csv in oglasi_podrobni.json datotekah so naslednji: 
Znamka,Model,Cena_stevilka(cena avtomobila kot stevilo),Prevozenih_km,kWh (kilovatne ure),Prostornina(prostornina motorja),KM(konske moči),Gorivo(tip motorja),Prva_registracija,Menjalnik,Baterija_kWh(zmogljivost baterije, ta podatek je samo pri elektricnih motorjih)

Kako lahko projekt uporabljate:
Če želite projekt zagnati pri sebi doma sledite navodilom:
1. odprite vaše razvojno okolje in v terminalu poženite ukaz python venv venv. s tem boste ustvarili virtualno okolje kamor boste potem nameščali potrebne knjižnice 
2. nato v terminalu poženite ukaz git pull https://github.com/PatricijaCokan/seminarska_naloga_uvod_v_programiranje, kar vam bo preneslo celotno kodo v vaše razvojno okolje
3. nato poženite ukaz pip install requrements.txt da se vam v virtualno okolje namestijo vse potrebne knjižnice za delovanje projekta.
4. Nato poženite ukaz python Preberi_podatke.py in zagnala se vam bo python skripta ki prebere podatke iz interneta. V terminalu se bo prikazalo navodilo in v skladu z vašimi željami pritisnite 1 ali 2 in počakajte da se skripta izvede do konca. nato lahko odprete analiza.ipynb datoteko in izberete vaše virtualno okolje kot kernel za poganjanje ipynb datoteke. nato pritisnite run all in vse celice v analizi se bodo ponovno zagnale in uoprabile sveže podatke če ste se le te odločili ponovno prenesti iz spleta. 

Če projekta ne želite prenesti in ga poganjati lokalno si lahko analizo ogledate na githubu https://github.com/PatricijaCokan/seminarska_naloga_uvod_v_programiranje kjer samo odprete datoteko analiza.ipynb in uživate v branju.
