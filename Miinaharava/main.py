"""
Tekijä Don Hämäläinen, 2022 Ohjelmoinnin alkeet
Ohjelmisto käyttää haravasto apukirjastoa ja spritet kuvakansiota
Nämä edellemainitut apuvälineet on luonut/laatinut Mika Oja, Oulun Yliopisto
"""

"""
Sisällytetään moduulit
- Haravasto moduulia tarvitaan ikkunoiden ja miinaharava pelin luontiin.
- Random moduulia tarvitaan miinojen satunnaiseen asetteluun pelikentälle.
- Time moduulia tarvitaan jotta saadaan aikaa otettua.
"""
import haravasto
import random
import time

# Tietuetaulu
"""
Tämä tietutaulu toimii kaiken "tallennus" tilana jossa on peliin liitetyt tiedot
"""
pelit = {
    # Pelaaja tiedot
    "pelaaja": None,
    # Kenttä
    "x_kentta": 0,
    "y_kentta": 0,
    "kentta": [],
    "miinakentta": [],
    # Indikaattorit
    "lopputulos": None,
    "miinoja": 0,
    # Tilastot
    "yrityksia": 0,
    "ruutuja_jaljella": None,
    # Aika
    "aika": 0,
    "kesto": 0
}

# Lipun asetus
def aseta_lippu(x, y):
    """
    Antaa pelaajalle mahdollisuuden asettaa lippuja. Jos peli registeröi oikean puoleisen painalluksen se asettaa lipun
    Jos kohdassa on jo lippu niin painallus poistaa sen. 
    """
    if(pelit["kentta"][y][x] == " "):
        pelit["kentta"][y][x] = "f"
        print("Lippu asetettu")
    elif(pelit["kentta"][y][x]  == "f"):
        pelit["kentta"][y][x] = " "
        print("Lippu poistettu")

# Tarkista voitto
def tarkista_voitto():
    # Tarkistaa voiton ja lopettaa pelin kun ehto toteutuu
    if(pelit["lopputulos"] != None):
        haravasto.lopeta()
        return

# Klikkaus
def kilkkaus(x, y):
    """
    Rekisteröi hiiren vasemman puoleisin painalluksen joka avaa ruudukon tai laukaisee tulvan algorytmin
    Jos kohta on tyhjä tai liputettu niin mitään ei tapahdu
    """
    tarkista_voitto()
    if(pelit["miinakentta"][y][x] == "x" and pelit["kentta"][y][x] != "f"):
        pelit["kentta"][y][x] = "x"
        haravasto.aseta_piirto_kasittelija(piirra_kentta)
        lopetus_kello()
        pelit["lopputulos"] = "Häviö"
        print("Hävisit")
    elif(pelit["miinakentta"][y][x] == " " and pelit["kentta"][y][x] != "f"):
        tulva_algorytmi(x, y)
        haravasto.aseta_piirto_kasittelija(piirra_kentta)
        pelit["yrityksia"] += 1
        print("yrityksia", pelit["yrityksia"])
        if(pelit["ruutuja_jaljella"] == 0):
            lopetus_kello()
            pelit["lopputulos"] = "Voitto"
            print("Voitit")
   
# Tulva algorytmi
def tulva_algorytmi(x, y):
    # Tallennetaan tuntemattomat ruudut listaan
    lista = [(y, x)]

    # Tarkastellaan ympärillä olevia ruutuja niin kauan kun lista ei ole tyhjä
    while lista:
        x, y = lista.pop()
        miinoja = 0

        # Käsitellään rajaukset ja reuna-alueet min ja max arvoilla
        min_x = max(x - 1, 0)
        max_x = min(x + 1, pelit["x_kentta"] - 1)
        min_y = max(y - 1, 0)
        max_y = min(y + 1, pelit["y_kentta"] - 1)

        # Tarkastellaan ympärillä olevia ruutuja
        for i in range(min_y, max_y + 1):
            for j in range(min_x, max_x + 1):
                # Jos ruutu on miina, lisätään laskuriin
                if pelit["miinakentta"][i][j] == "x":
                    miinoja += 1
                # Jos ruutu on tyhjä ja sitä ei ole vielä käsitelty, lisätään se listaan
                elif pelit["miinakentta"][i][j] == " ":
                    pelit["miinakentta"][i][j] = miinoja
                    lista.append((j, i))
                    pelit["ruutuja_jaljella"] -= 1
        
        # Tallennetaan tapahtumat pelikenttiin josta kaikki funktiot lukevat tietoa
        pelit["miinakentta"][y][x] = str(miinoja)
        pelit["kentta"][y][x] = str(miinoja)

# Aseta miinat
def miinoita(miinoja, kentta):
    """
    Funktio miinoittaa satunnaisesti pelit["miinakentta"]
    Sekä tallentaa myös ruutujen määrän pelit["ruutujen_jaljella"] tietueeseen
    """
    # Tallennetaan ruutujen todellinen määrä
    pelit["ruutuja_jaljella"] = len(kentta) * len(kentta[0]) - miinoja
    
    tyhjaa = []
    for i, korkeus in enumerate(kentta):
        for j in range(len(korkeus)):
            tyhjaa.append((i, j))
    for k in range(miinoja):
        satunnainen = random.choice(tyhjaa)
        i, j = satunnainen
        tyhjaa.remove(satunnainen)
        kentta[i][j] = "x"


    print(pelit["miinakentta"])

# Hiiren käsittelijä        
def hiiri_kasittelija(x, y, painike, kokonaisluku):
    """
    Funktio käsittelee hiiren painalluksia ja toimii pelin ohjaimena
    kokonaisluku parametri on välttämätön funktion kutsun kannalta, mutta sitä ei käytetä ollenkaan
    """
  
    # Tehdään x ja y :stä oikean kokoisia suhteessa ikkunaan nähden
    x = int(x/40)
    y = int(y/40)
   
    print("Pelikentät kohta:", y, x)
    # Tarkistaa onko peli jo läpäisty
    if(pelit["lopputulos"] != None):
        haravasto.lopeta()
        return 0

    elif(painike == haravasto.HIIRI_VASEN):
        kilkkaus(x, y)

    elif(painike == haravasto.HIIRI_OIKEA):
        aseta_lippu(x, y)

# Piirra kentta
def piirra_kentta():
    """
    Piirtää peli- ja miinakentän näkyviin peli-ikkunaan.
    Funktiota kutsutaan aina kun ruudukkoa päivitetään
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    
    for korkeus in range(len(pelit["kentta"])):
        for leveys in range(len(pelit["kentta"][korkeus])):
            haravasto.lisaa_piirrettava_ruutu(pelit["kentta"][korkeus][leveys], leveys * 40, korkeus * 40)

    haravasto.piirra_ruudut()

# Luo kenttäs
def luo_kentta(y_koordinaatti, x_koordinaatti):
    """
    Funktio luo 2 ulotteisen pelikentän ruudut. Funktio ei aseta miinoja.
    esimerkiksi: 
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
    """
    pelikentta = []
    miinakentta = []
    for korkeus in range(y_koordinaatti):
        pelikentta.append([])
        miinakentta.append([])
        for leveys in range(x_koordinaatti):
            pelikentta[-1].append(" ")
            miinakentta[-1].append(" ")
    
    # Tallennetaan kentät tietuetaulun pelit["kentta"] ja pelit["miinakentta"] muistiin
    pelit["kentta"] = pelikentta
    pelit["miinakentta"] = miinakentta
    # Miinoitus
    miinoita(pelit["miinoja"], pelit["miinakentta"])

# Miinojen kysyminen
def kysyMiinoja(x, y):
    # Funktio kysyy miinojen määrää, sekä estää miinojen liian suurenmäärän suhteessa ruudukkojen määrään

    while True:
        try:
            miinoja = int(input(f"Syötä miinojen määrä (HUOM! Miinoja ei voi olla enempää kuin {x * y}kpl) > "))
            if(miinoja > (x * y)):
                print("Miinoja on liikaa, yritä uudelleen.")
            else:
                print("Miinojen määrän tallennus onnistui\nPelia alkaa...")
                pelit["miinoja"] = miinoja
                break
        except ValueError:
            print("Miinojen määrä tulisi olla kokonaisluku, yritä uudelleen")

# Kentän kysyminen
def kysyKentta():
    """
    Funktio kysyy kentän koon, sekä erottelee 20x40 luvut toisistaan eli 20 on omassa muuttujassa ja toinen 40 on omassa
    KysyMiinoja funktio on myös liitetty tähän funktioon
    """
    while True:
        kentta = input("Anna kentän koko ruuduissa, esim 20x20 > ")
        if("x" in kentta):
            kokoKentta = kentta.split("x")
            try:
                # Tarkistetaan syötteiden oikeallisuus
                kokoKentta[0] = int(kokoKentta[0])
                kokoKentta[1] = int(kokoKentta[1])
            except TypeError:
                print("Sinun tulisi antaa kaksi lukua jossa on 'x', joka erottaa luvut. Esim 40x40 > ")
            except ValueError:
                print("Sinun tulisi antaa kokonaislukuja")
            else:
                print("Kentän koko syötetty onnistuneesti")
                pelit["x_kentta"] = kokoKentta[0]
                pelit["y_kentta"] = kokoKentta[1]
                kysyMiinoja(pelit["x_kentta"], pelit["y_kentta"])
                break
        else: 
            print("Sinun tulisi antaa kaksi lukua jossa on 'x', joka erottaa luvut. Esim 40x40 > ")
            try:
                valinta = int(input("Mikäli haluat poistuia takaisin päävalikkon syötä numero 0, muutoin paina ENTER-painiketta jatkaaksesi > "))
                if(valinta == 0):
                    break
            except ValueError:
                continue

# Käynnistä kello
def alotus_kello():
    """
    Käynnistää kellon
    """
    pelit["aika"] = time.time()
    print("Kello on käynnistetty")

# Lopetus kello
def lopetus_kello():
    # pysäyttää kellon
    pelit["kesto"] = time.time() - pelit["aika"]

# Tiedosto tallennus / katsominen
def tiedosto():
    """
    Tiedosto funktio toimii tiedoston lukemisena ja kirjoittamisena.
    Tiedostoon voidaan tallentaa pelaajan suorittamat pelit, sekä spesifimpiä asioita kuten:
    - kesto
    - tulos
    - pelaaja
    - käytetyt yritykset
    """

    print("\nHaluatko lukea olemassa olevaa tiedostoa vai luoda uuden ?\n1. Luo uusi tiedosto\n2. Lue vanha tiedosto\n3. Palaa takaisin pääohjelmaan")
    while True:
        try:
            valinta = int(input("\nSyötä valintasi > "))

                # Tiedoston luonti
            if(valinta == 1):
                tiedostonNimi = input("Anna tiedostollesi nimi > ")
                try:
                    with open(tiedostonNimi + ".txt", "a") as tiedosto:
                        muunnettu = round(pelit["kesto"], 2)
                        tiedosto.write("{}:{}:{}:{}:{}:{}:{}\n".format(pelit["pelaaja"], pelit["x_kentta"], pelit["y_kentta"], pelit["miinoja"], pelit["lopputulos"], muunnettu, pelit["yrityksia"]))
                        print(f"Tiedoston kirjoitus onnistui! Tiedoston nimi on {tiedostonNimi}.txt")
                        break
                except IOError:
                    print("\nTiedoston kirjoittaminen epäonnistui. Syitä voival olla oikeudelliset puutteet")
                    break

            # Tiedoston lukeminen
            elif(valinta == 2):
                tiedostonNimi = input("Anna tiedosto jota haluat tarkastella (.txt kirjoittamista ei tarvita) > ")
                try:
                    with open(tiedostonNimi + ".txt", "r") as tiedosto:
                        kpl = 0
                        for rivi in tiedosto:
                            strimmaus = rivi.strip()
                            splittaus = strimmaus.split(":")
                            kpl += 1
                            print("\n{}. Pelaaja {} pelasi kentällä jonka koko oli {}x{} ja miinoja oli {}.\nnLopputulos oli {} ja peli aika oli {} sekunttia, sekä yrityksiä oli {} verran.".format(kpl, splittaus[0], splittaus[1], splittaus[2], splittaus[3], splittaus[4], splittaus[5], splittaus[6]))

                        print("\nTiedoston lukeminen onnistui")
                        break
                except IOError:
                    print("Tiedoston lukeminen epäonnistui. Syitä voivalt olla tiedoston väärä nimi tai oikeudelliset puutteet\nOhjataan pääohjelmaan...")
                    break
            # Poistuminen pääohjelmaan
            else: 
                break
        except ValueError:
            print("Sinun tulee syöttää kokonaisluku väliltä 1 - 3")
# Automaattinen
def automaattinen_tiedosto_tallennus():
    try:
        tallennanko = int(input("\nTallennetaanko tulokset ?\n1. Kyllä\nMuutoin voit vain painaa ENTER - painiketta jatkaaksesi\nSyötä valinta > "))
        if(tallennanko == 1):
            tiedostonNimi = input("Anna tiedostollesi nimi > ")
            try:
                with open(tiedostonNimi + ".txt", "a") as tiedosto:
                    muunnettu = round(pelit["kesto"], 2)
                    tiedosto.write("{}:{}:{}:{}:{}:{}:{}\n".format(pelit["pelaaja"], pelit["x_kentta"], pelit["y_kentta"], pelit["miinoja"], pelit["lopputulos"], muunnettu, pelit["yrityksia"]))
                    print(f"Tiedoston kirjoitus onnistui! Tiedoston nimi on {tiedostonNimi}.txt")
            except IOError:
                print("\nTiedoston kirjoittaminen epäonnistui. Syitä voival olla oikeudelliset puutteet\nVoit kokeilla uudelleen tallennusta päävalikon 2 vaihtoehdon kautta.\nTiedot ovat tallessa niin kauan kun et aloita uutta peliä ")
    except ValueError:
        return

# Navigointi
def navigointi():

    """
    Navigointi on tarkoitettu ohjaustavarten ja sen toiminto perustuu vain syötteen vastaanottoon.
    Syöte käsitellään vasta main() funktiossa
    """

    print("\nSinulla on mahdollista valita seuraavista vaihtoehdoista:\n1. Uusi peli\n2. Lue tiedosto\n3. Lopeta peli")
    while True:
        try: 
            valinta = int(input("Syötä valintasi > "))
            if(valinta > 3 or valinta < 1):
                print("Syötteesi ei ole 1 - 3 sisällä tai yhtäsuuri")
            else:
                return valinta
        except ValueError:
            print("\nValitettavasti valinta tulee olla kokonaisluku väliltä 1 - 3")

# Pääohjelma    
def main():
    """
    Main functio toimii pääohjelmana jossa kaikki toiminnallisuudet kutsutaan.
    Käytännössä siis muut funktiot kutsutaan tällä
    """

    print("\nTervetuloa pelaamaan miinaharavaa")
    pelit["pelaaja"] = input("Anna pelaajan nimi > ")
    while True:
        nav = navigointi()
        # Peli
        if(nav == 1):
            # Resettaus
            pelit["lopputulos"] = None
            pelit["miinoja"] = 0
            kysyKentta() 
            luo_kentta(pelit["y_kentta"], pelit["x_kentta"])

            haravasto.lataa_kuvat(r"spritet")
            haravasto.luo_ikkuna((pelit["x_kentta"] * 40), (pelit["y_kentta"] * 40))
            haravasto.aseta_piirto_kasittelija(piirra_kentta)
            haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
            alotus_kello()
            haravasto.aloita()
            automaattinen_tiedosto_tallennus()
            
        # Tiedosto
        if(nav == 2):
            tiedosto()
        # Lopetus
        if(nav == 3):
            break



if __name__ == "__main__":
    main()