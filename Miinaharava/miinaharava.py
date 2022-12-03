# Moduulit
import haravasto 
import random
import time

# Tietuetaulukko
"""
Indikaattorit toimivat pelin ratkaisevassa osassa
"""
indikaattorit = {
    "tulva": True,
    "loppu": False
}
tila = {
    # Pelaaja tiedot
    "pelaaja": None,
    # Kentät
    "kentta": None,
    "miinakentta": None,
    # Pituudet
    "x_pituus": 0,
    "y_pituus": 0,
    # Miinojen & ruutuja jäljellä
    "miinoja": 0,
    "ruutuja_jaljella": 0,
    # Tiedosto tiedot
    "aika": None,
    "vuorot": 0,
    "kesto": None,
    "lopputulos": "Kesken",
    "Siirtoja": 0
}

# Funktiot
# PELIN FUNKTIOT

def piirra_kentta():
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for x in range(len(tila["kentta"])):
        for y, ruutu in enumerate(tila["kentta"][x]):
            haravasto.lisaa_piirrettava_ruutu(ruutu, y * 40, x * 40)
    
    haravasto.piirra_ruudut()

def luo_ruudukot(x_koko, y_koko):
	alempikentta = []
	miinakentta = []
	for rivi in range(y_koko):
		alempikentta.append([])
		miinakentta.append([])
		for sarake in range(x_koko):
			alempikentta[-1].append(" ")
			miinakentta[-1].append(" ")
	tila["kentta"] = alempikentta
	tila["miinakentta"] = miinakentta

def miinoita(miinoja, kentta, aloituspiste):
    # Laskee ruutujen määrän miinustaen miinojen määrällä, sekä tallentaa tietuetaulukkoon sen 
    tila["ruutuja_jaljella"] = (len(kentta) * len(kentta[0]) - miinoja)

    tyhjaa_tilaa = []
    for x in range(len(kentta[0])):
        for y in range(len(kentta)):
            tyhjaa_tilaa.append((x, y))
    
    tyhjaa_tilaa.remove(aloituspiste)
    # Toistaa miinoittamista niin kauan kuin lukumäärä > 0
    while miinoja > 0:
        x = random.randint(0, len(kentta) - 1)
        y = random.randint(0, len(kentta[0]) - 1)

        if(x, y) in tyhjaa_tilaa:
            tyhjaa_tilaa.remove((x, y))
            kentta[x][y] = "x"
            miinoja -= 1

def kasittele_hiiri(x, y, nappi, kokonaisluku):
    # Muokataan x ja y oikeaan suhteeseen ikkunaan nähden
    x = int(x/40)
    if(x > tila["x_pituus"]):
        x -= 1
    y = int(y/40)
    if(y > tila["y_pituus"]):
        y -= 1
    # Tarkistaa onko peli läpäisty indikaattorista.
    if(indikaattorit["loppu"] == True):
        haravasto.lopeta() 
        return
    
    if nappi == haravasto.HIIRI_VASEN:
        if(tila["miinakentta"][x][y] == "x" and tila["kentta"][x][y] != "f"):
            tila["kentta"][x][y] = "x"
            haravasto.aseta_piirto_kasittelija(piirra_kentta)
            indikaattorit["loppu"] = True
            tila["lopputulos"] = "Häviö"
            print("Hävisit")
           
        if(tila["miinakentta"][x][y] == " " and tila["kentta"][x][y] != "f"):
            if(indikaattorit["tulva"] == True):
                miinoita(tila["miinoja"], tila["miinakentta"], (x, y))
                indikaattorit["tulva"] = False
            flood_fill(x, y)
            haravasto.aseta_piirto_kasittelija(piirra_kentta)
            tila["vuorot"] += 1
            if(tila["ruutuja_jaljella"] == 0):
                indikaattorit["loppu"] = True
                tila["lopputulos"] = "Voitto"
                print("Voitit pelin")
                

    if nappi == haravasto.HIIRI_OIKEA:
        # Lippujen merkitseminen
        if (tila["kentta"][x][y] == " "):
            tila["kentta"][x][y] = "f"
        elif (tila["kentta"][x][y] == "f"):
            tila["kentta"][x][y] = " "

        haravasto.aseta_piirto_kasittelija(piirra_kentta)
                
def flood_fill(x, y):
    # Tallennetaan tuntemattomat ruudut listaan
    lista = [(y, x)]
    while lista:
        x, y = lista.pop()
        miinoja = 0

        # Käsitellään ensiksi rajaukset ja reuna kohdat min ja max arvoilla
        minX = x - 1
        if (minX < 0):
            minX = 0
        maxX = x + 1
        if(maxX >= tila["x_pituus"]):
            maxX = tila["x_pituus"] - 1
        minY = y - 1
        if(minY < 0):
            minY = 0
        maxY = y + 1
        if(maxY >= tila["y_pituus"]):
            maxY = tila["y_pituus"] - 1
       
        
        # Voimme hyödyntää näitä arvoja kun tarkastelemme etenemistä
        for j in range(minY, maxY + 1):
            for i in range(minX, maxX + 1):
                if(i == x and j == y):
                    continue

                if(tila["miinakentta"][j][i] == "x"):
                    miinoja += 1
        
        for j in range(minY, maxY + 1):
            for i in range(minX, maxX + 1):
                if(i == x and j == y):
                    continue
                if(tila["miinakentta"][j][i] == " " and miinoja == 0):
                    lista.append((i, j))
        
        if(tila["miinakentta"][y][x] == " "):
            tila["ruutuja_jaljella"] -= 1
        
        tila["miinakentta"][y][x] = str(miinoja)
        tila["kentta"][y][x] = str(miinoja)

def tulostus(metodi):
    if(metodi == "kirjoita"):
        try:
            with open("tulos.txt", "a") as tiedosto:
                aika = time.strftime("%d.%m.%Y %H:%M", tila["aika"])
                minuutit = int(tila["kesto"]/60)
                sekunnit = int(tila["kesto"]%60)
                tiedosto.write("{},{},{},{},{},{},{},{},{}\n".format(tila["pelaaja"], aika, tila["vuorot"], minuutit, sekunnit, tila["x_pituus"], tila["y_pituus"], tila["miinoja"], tila["lopputulos"]))
        except IOError:
            print("Tiedostoa ei voitu avata tai sitä ei ole. Tallennus epäonnistui")
    if(metodi == "luku"):
        try:
            with open("tulos.txt", "r") as tiedosto:
                for rivi in tiedosto:
                    strimmaus = rivi.rstrip()
                    listautus = strimmaus.split(",")
                    print(strimmaus)
                    print("Pelaaja {} pelasi {}. vuoroja oli {}, sekä peli kesti {} minuuttia {} sekunttia".format(listautus[0], listautus[1], listautus[2], listautus[3], listautus[4]))
                    print("Pelin koko oli {}x{}, {} miinalla ja peli päättyi {}".format(listautus[5], listautus[6], listautus[7], listautus[8]))
        except IOError:
            print("Tilastoja ei ole tai sitten avaamisessa tapahtui virhe")


# KYSYNTÄ JA NAVIGOINTI FUNKTIOT

def ruudukon_koko():
    """
    Kysyy pelaajalta ruudukon koon.
    palauttaa pelattavan alueen
    """
    while True:
        print("\nSyötä pelialueen ensimmäinen osa, eli kanta ja sitten vasta korkeus")
        kanta = input("Syötä kanta > ")
        korkeus = input("Syötä korkeus > ")
        try:
            kanta = int(kanta)
            korkeus = int(korkeus)
        except ValueError:
            print("Havaitsimme virheellisen syötteen. Ole hyvä kirjoita kokonaisluku syötteitä.")
        
        else:
            tila["x_pituus"] = kanta
            tila["y_pituus"] = korkeus
            break           

def kuinka_monta_miinaa():
    """
    Kysytään kuinka monta miinaa pelaaja haluaa
    """
    while True:
        ruudukon_koko = tila["x_pituus"] * tila["y_pituus"]
        try:
            miinoja = int(input("Anna miinojen määrä > "))
        except ValueError:
            print("Anna miinat kokonaislukuina")
        else:
            if(miinoja > 0 and miinoja < ruudukon_koko):
                tila["miinoja"] = miinoja
                break
            else:
                print("Miinojen määrä ei voi olla suurempi kuin ruudukon koko, sekä miinojen määrä tulee olla suurempi kuin 0")

def piirra_kentta():
    """
    Käsittelijäfunktio joka piirtää miinkentän näkyviin peli ikkunaan
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for i in range(len(tila["kentta"])):
        for j, ruudut in enumerate(tila["kentta"][i]):
            haravasto.lisaa_piirrettava_ruutu(ruudut, i * 40, j * 40)

    haravasto.piirra_ruudut()

def navigointi():
    """
    Valikko on tarkoitettu navigointiin. Valikossa voit tarkastella aikaisempia pelejä,.. 
    aloittaa pelejä, sekä lopettaa ohjelman
    """
    print("\nValitse seuraavista toiminnoista")
    print("1. Uusi peli")
    print("2. Tarkastele aijempia pelejä")
    print("3. Lopeta pelaaminen")
    while True:
        try:
            valinta = int(input("Anna toiminto > "))
        except ValueError:
            print("Anna pelkästään toimintoja vastaavia numeroita")
        else:
            if(valinta > 0 and valinta < 4):
                return valinta

# PÄÄOHJELMA
def main():
    """
    Pääohjelma jossa peli ja funktioiden kutsuminen tapahtuu
    """

    print("\nTervetuloa pelaamaan miinaharavaa!")
    tila["pelaaja"] = input("Pelaajan nimi on > ")
    while True:
        valinta = navigointi()
        if(valinta == 1):
            # Peli
            # NOLLAUS
            indikaattorit["tulva"] = True
            tila["miinoja"] = 0
            ruudukon_koko()
            kuinka_monta_miinaa()
            luo_ruudukot(tila["x_pituus"], tila["y_pituus"])

            haravasto.lataa_kuvat("spritet")
            haravasto.luo_ikkuna(tila["x_pituus"] * 40, tila["y_pituus"] * 40)
            haravasto.aseta_piirto_kasittelija(piirra_kentta)
            haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)  
            
            # Tiedosto aloitus
            tila["aika"] = time.localtime()
            tila["kesto"] = time.time() 
            tila["Siirtoja"] = 0
            tila["lopputulos"] = "Kesken"

            haravasto.aloita()
            tila["kesto"] = time.time() - tila["kesto"]
            tulostus("kirjoita")
            indikaattorit["loppu"] = False
        if(valinta == 2):
            tulostus("luku")
        else:
            break


if __name__ == "__main__":
        main()
    