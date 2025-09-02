import os
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import time
import random
import json
import csv

def main(): #glavna funkcija ki se izvaja ob zagonu programa
    headers = { # headers za http zahtevek da ne dobimo blokirane strani
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
   'Accept-Language': 'sl-SI,sl;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    }
    url = ( #url ki ga posodabljamo glede na st. strani ki jo dodajamo na konec url-ja
        "https://www.avto.net/Ads/results.asp?"
        "znamka=&model=&modelID=&tip=katerikoli%20tip&"
        "znamka2=&model2=&tip2=katerikoli%20tip&"
        "znamka3=&model3=&tip3=katerikoli%20tip&"
        "cenaMin=100&cenaMax=100000&letnikMin=1970&letnikMax=2025&"
        "bencin=0&starost2=999&oblika=0&ccmMin=0&ccmMax=99999&"
        "mocMin=&mocMax=&kmMin=0&kmMax=250000&kwMin=0&kwMax=999&"
        "motortakt=&motorvalji=&lokacija=0&sirina=&dolzina=&"
        "dolzinaMIN=&dolzinaMAX=&nosilnostMIN=&nosilnostMAX=&"
        "sedezevMIN=&sedezevMAX=&lezisc=&presek=&premer=&col=&"
        "vijakov=&EToznaka=&vozilo=&airbag=&barva=&barvaint=&"
        "doseg=&BkType=&BkOkvir=&BkOkvirType=&Bk4=&"
        "EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&"
        "EQ5=1000000000&EQ6=1000000000&EQ7=1000000120&EQ8=101000000&"
        "EQ9=100000002&EQ10=100000000&KAT=1010000000&PIA=&PIAzero=&"
        "PIAOut=&PSLO=&akcija=&paketgarancije=&broker=&prikazkategorije=&"
        "kategorija=&ONLvid=&ONLnak=&zaloga=&arhiv=&presort=&tipsort=&"
        "stran="
    )
    
    print("Če ste podatke že brali iz spletne strani avto.net in želite podatke pripraviti za nadaljno obdelavo pritisnite 2\n"
          "-----------------------------"
          "Če podatkov še nimate in jih želite shraniti v mapo podatki pritisnite 1 (to lahko traja nekaj časa)")
    print("-----------------------------")
    izbira = input("Vpišite številko: ") #glede na stevilko ki je bila izbrana ali na novo prenesemo strani in jih obdelamo ali pa samo uporabimo podatke ki smo jih že prebrali
    if izbira == "1":
        for stStrani in range(1, 22): #najprej prenesemo vse strani
            url_strani = url + str(stStrani)
            preberi_podatke(url_strani, stStrani, headers, folder="podatki")

    oglasi_data = [] 
    for file in os.listdir("podatki"): #najprej najdemo vse oglase, nato iz teh oglasov pridobimo podatke in nato te podate uredimo
        oglasi_data = izlusci_oglas_iz_strani(file, oglasi_data)
    urejani_oglasi = izlusci_podatke_iz_oglasov(oglasi_data) 
    urejani_oglasi = uredi_podatke(urejani_oglasi)
    pretvori_v_json_csv(urejani_oglasi)


def preberi_podatke(url, stStrani, headers, folder="podatki"): # ta funkcij prenese podatke iz spleta
    if not os.path.exists(folder):
        os.makedirs(folder)
    file = "Stran" + str(stStrani) + ".html" #najprej preverimo ali je stran že shranjena in če je jo preskočimo 
    if file in os.listdir(folder):
        print(f"Stran {stStrani} je že shranjena. Ponovno branje bi morda lahko bilo neveljavno tako da stran preskočimo")
        return True
    time.sleep(random.uniform(3, 7))  # Počakaj 3-7 sekund da ne bomo blokirani
    try:
        odgovor = requests.get(url, headers=headers)
        odgovor = BeautifulSoup(odgovor.content, "html.parser", from_encoding='utf-8')
        velikost = len(str(odgovor))
        if velikost < 50000:  #manj kot 50KB = verjetno blokirana
            print(f"Stran {stStrani} je preveč majhna ({velikost} znakov), tako vemo da je bila verjetno blokirana")
            return False
        with open(folder + "/" + file, "w", encoding="utf-8") as f:
            f.write(str(odgovor))
    except Exception as e:
        print(f"Prišlo je do napake: {e}, pri branju strani {stStrani}")
        return False
    return True


def izlusci_oglas_iz_strani(html_datoteka, oglasi_data): # ta funkcij iz strani izbere vse oglase in jih shrani v slovar seznam ki ga podamo ob klicu funkcije

    html_datoteka = os.path.join("podatki", html_datoteka)
    with open(html_datoteka, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Najdi vse oglase
    oglasi = soup.find_all('div', class_='GO-Results-Row')
    for oglas in oglasi:
        oglasi_data.append(oglas)
    return oglasi_data


def izlusci_podatke_iz_oglasov(oglasi_data): # ta funkcij iz oglasov izbere vse podatke in jih shrani v slovarje ki jih doda v seznam 
    urejani_oglasi = []
    for oglas in oglasi_data:
        oglas_info = {}
        
        # Ime avtomobila
        naziv = oglas.find('div', class_='GO-Results-Naziv')
        if naziv:
            oglas_info['ime'] = naziv.get_text(strip=True)
        
        # Cena
        cena = oglas.find('div', class_='GO-Results-Price-TXT-Regular')
        if cena:
            oglas_info['cena'] = cena.get_text(strip=True)
        
        # Podrobnosti iz tabele
        tabela = oglas.find('table', class_='table-striped')
        if tabela:
            vrstice = tabela.find_all('tr')
            for vrstica in vrstice:
                celice = vrstica.find_all('td')
                if len(celice) == 2:
                    kljuc = celice[0].get_text(strip=True)
                    vrednost = celice[1].get_text(strip=True)
                    
                    if 'registracija' in kljuc.lower():
                        oglas_info['prva_registracija'] = vrednost
                    elif 'prevoženih' in kljuc.lower() or 'km' in kljuc.lower():
                        oglas_info['kilometrina'] = vrednost
                    elif 'gorivo' in kljuc.lower():
                        oglas_info['gorivo'] = vrednost
                    elif 'menjalnik' in kljuc.lower():
                        oglas_info['menjalnik'] = vrednost
                    elif 'motor' in kljuc.lower():
                        oglas_info['motor'] = vrednost
                    else:
                        oglas_info[kljuc] = vrednost
        oglas_info_ocisceno = {}
        for key, value in oglas_info.items():  # vsako vrednost v slovarjih očistimo da nimamo posebnih znakov ampak samo črke
            oglas_info_ocisceno[ocisti_besedilo(key)] = ocisti_besedilo(value)
        
        urejani_oglasi.append(oglas_info_ocisceno)

    return urejani_oglasi

def ocisti_besedilo(besedilo): # to je funkcija ki se uporablja za čiščenje besedila
    if not besedilo:
        return besedilo
    zamenjave = {
        '\x80': '€',
        '\x9e': 'ž',
        '\x9a': 'š',
        '\x8a': 'Š',
        '\x8e': 'Ž',
        '\x8d': 'č',
        '\x8c': 'Č',
        'è': 'č',
        'È': 'Č'
    }
    
    for stari, novi in zamenjave.items():
        besedilo = besedilo.replace(stari, novi)
    
    return besedilo

def uredi_podatke(podrobni_podatki): # ta funkcij gre čez vse slovarje s podatki in podatke preuredi tako da so bolj primerni za analizo+
    nov_podrobni_podatki = []
    for oglas in podrobni_podatki:
        if "ime" in oglas:
            znamka = oglas["ime"].split(" ")[0].strip()
            model = oglas["ime"].split(" ")[1].strip()
            if model == "serija":
                model = oglas["ime"].split(" ")[1].strip() + " " + oglas["ime"].split(" ")[2].strip()
            if model == "Romeo":
                znamka = "Alfa Romeo"
                model = oglas["ime"].split(" ")[2].strip()
            
        else:
            znamka = None
            model = None
            
        if "cena" in oglas:
            cena = oglas["cena"].replace(" €", "").strip()
            cena = cena.replace(".", "")
        else:
            cena = None
            
        if "kilometrina" in oglas:
            prevozenih_km = oglas["kilometrina"].replace(" km", "").strip()
        else:
            prevozenih_km = None
            
        if "motor" in oglas:
            podatki_o_motorju = oglas["motor"].split(" ")
            if len(podatki_o_motorju) == 2:
                kWh = podatki_o_motorju[0].strip()
                prostornina = None
                KM = None
                kW = None
            else:
                kWh = None
                kW = podatki_o_motorju[2].strip()
                prostornina = podatki_o_motorju[0].strip()
                KM = podatki_o_motorju[5].strip()
        else:
            kWh = None
            prostornina = None
            KM = None
            
        if "gorivo" in oglas:
            gorivo = oglas["gorivo"].split(" ")
            gorivo = gorivo[0].strip()
            match gorivo:
                case "bencinski":
                    gorivo = "bencin"
                case "diesel":
                    gorivo = "dizel"
                case "hibridni":
                    gorivo = "hibrid"
                case "elektro":
                    gorivo = "elektro"
        else:
            gorivo = None
            
        if "prva_registracija" in oglas:
            prva_registracija = oglas["prva_registracija"].strip()
        else:
            prva_registracija = None
            
        if "menjalnik" in oglas:
            menjalnik = oglas["menjalnik"].split(" ")[0].strip()
            match menjalnik:
                case "ročni":
                    menjalnik = "ročni"
                case "avtomatski":
                    menjalnik = "avtomatski"
        else:
            menjalnik = None
            
        if "Baterija" in oglas:
            baterija_kWh = oglas["Baterija"].split(" ")[0].strip()
        else:
            baterija_kWh = None

        nov_oglas = {}   
        nov_oglas["znamka"] = znamka
        nov_oglas["model"] = model
        nov_oglas["cena_stevilka"] = cena
        nov_oglas["prevozenih_km"] = prevozenih_km
        nov_oglas["kWh"] = kWh
        nov_oglas["prostornina"] = prostornina
        nov_oglas["KM"] = KM
        nov_oglas["gorivo"] = gorivo
        nov_oglas["prva_registracija"] = prva_registracija
        nov_oglas["menjalnik"] = menjalnik
        nov_oglas["baterija_kWh"] = baterija_kWh
        nov_podrobni_podatki.append(nov_oglas)
    return nov_podrobni_podatki # na koncu vrnemo nov seznam s prečiščenimi podatki

def pretvori_v_json_csv(podrobni_podatki): #podatke spremenimo v dve datoteki json in csv

    with open('oglasi_podrobni.json', 'w', encoding='utf-8') as f:
        json.dump(podrobni_podatki, f, ensure_ascii=False, indent=2)

    with open('oglasi_avto.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Znamka", "Model", "Cena_stevilka", "Prevozenih_km", "kWh", "Prostornina", "KM", "Gorivo", "Prva_registracija", "Menjalnik", "Baterija_kWh"])
        
        for oglas in podrobni_podatki:
            writer.writerow([
                oglas.get("znamka", ""),
                oglas.get("model", ""),
                oglas.get("cena_stevilka", ""),
                oglas.get("prevozenih_km", ""),
                oglas.get("kWh", ""),
                oglas.get("prostornina", ""),
                oglas.get("KM", ""),
                oglas.get("gorivo", ""),
                oglas.get("prva_registracija", ""),
                oglas.get("menjalnik", ""),
                oglas.get("baterija_kWh", "")
            ])

if __name__ == "__main__": # glavna funkcija ki se izvaja ob zagonu programa
    main()      
        
    







