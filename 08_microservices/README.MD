# Microservices
V této kapitole aplikaci předěláme do architektury microservices. Uživatelské rozhraní a logiku aplikace oddělíme do samostatných služeb.
Část aplikace, která pracovala s databází umístíme do služby images. Uživatelské rozhraní umístíme do služby ui. 
Ale neměl by být problém vytvořit například mobilní aplikaci, která bude používat služeb služby images.

## Komunikace
V architektuře microservices se pro komunikaci používají odlehčené komunikační protokoly jako HTTP. Data se často přenáší ve formátu JSON. 
Mikroslužba má definované API rozhraní. Velmi často se používá REST API.  

### REST API
JSON jako hlavní formát - Content-Type: application/json

#### Zdroje
| API                    | Popis                      |
|------------------------|----------------------------|
| GET /images            | všechny obrázky            |
| GET /images/1          | obrázek id 1               |
| GET /images/1/comments | komentáře k obrázku s id 1 |
| GET /comments          | všechny komentáře          |

#### HTTP metody
Pro předávání příkazů se používají HTTP metody. GET, POST a DELETE jsou standardní. PUT a PATCH některé prohlížeče nepodporují, proto se nahrazují za POST

| Metoda  | Popis                                                                                                                 |
|---------|-----------------------------------------------------------------------------------------------------------------------|
| GET     | získání dat                                                                                                           |
| POST    | vytvoření zdroje                                                                                                      |
| DELETE  | smazání zdroje                                                                                                        |
| PUT     | úpravy (upraví celý zdroj - chová se jako SET, pozor klasické prohlížeče ho nepodporují a místo toho se používá POST) |
| PATCH   | částečné úpravy                                                                                                       |

#### Návratové kódy 
| Kód | String                 | Popis                                                                                                                                                                                                                                                                         |
|-----|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 | OK                     | požadavek proběhl v pořádku                                                                                                                                                                                                                                                   |
| 201 | Created                | při POST, pokud byl vytvořen nový obsah                                                                                                                                                                                                                                       |
| 204 | No Content             | když požadavek na server proběhne v pořádku, ale server nic nevrátí                                                                                                                                                                                                           |
| 304 | No Modified            | pokud nebyl od posledního požadavku nebyl změněn obsah – používá se pro nativní http cache                                                                                                                                                                                    |
| 400 | Bad Request            | požadavek na server je nějakým způsoben nečitelný (třeba špatný JSON apod.)                                                                                                                                                                                                   |
| 401 | Unauthorized           | klient není ověřen                                                                                                                                                                                                                                                            |
| 403 | Forbidden              | klient nemá přístup k danému obsahu                                                                                                                                                                                                                                           |
| 404 | Nod Found              | zdroj není nalezen                                                                                                                                                                                                                                                            |
| 405 | Method Not Allowed     | zdroj není dostupný pro tuto metodu. Například je možné použít GET /articles a POST /articles, ale už třeba nemůžeme článek smazat. Nelze tedy zavolat DELETE /articles - je vhodné uživatelům našeho API v tomto momentu poskytnout seznam podporovaných metod pro danou URL |
| 410 | Gone                   | zdroj není už na téhle adrese dostupný - to se používá při verzování                                                                                                                                                                                                          |
| 415 | Unsupported Media Type | klient v požadavku na server uvedl hlavičku Content-Type, kterou server nepodporuje                                                                                                                                                                                           |
| 422 | Unprocessable Entity   | chyba validace dat - třeba formuláře apod.                                                                                                                                                                                                                                    |
| 429 | Too-Many Requests      | pokud klient překročil maximální počet požadavků, třeba za den                                                                                                                                                                                                                |

## Docker-compose.yaml
Nově přidáme do docker-compose.yaml sekci network. V ní vytvoříme dvě oddělené sítě frontnet a backnet. To nám umožní 
oddělit externí a interní komunikaci aplikace. Například nová služba ui bude komunikovat přes frontnet. Naopak služba
database bude komunikovat pouze přes backnet. Služba images, které je spojuje komunikuje přes obě sítě.

Služby database a adminer zůstaly stejné jak v předchozí kapitole, proto se budeme věnovat hlavně službám ui a images.

```
version: '3.8'

services:
  ui:
    container_name: ui
    build: ./services/ui
    command:
      python manage.py run -h 0.0.0.0
    volumes:
      - ./services/ui/:/usr/src/app/
    ports:
      - "8006:5000"
    depends_on:
      - images
    env_file:
      - .environment
    networks:
      - frontnet      

  images:
    container_name: images
    build: ./services/images
    command:
      python manage.py run -h 0.0.0.0
    volumes:
      - ./services/images/:/usr/src/app/
    env_file:
      - .environment
    depends_on:
      - database
    networks:
      - backnet
      - frontnet

  database:
    container_name: database
    restart: always
    image: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .environment
    networks:
      - backnet

...

networks:
  frontnet:
  backnet:
```

## Služba images
Služba images vznikla vlastně přepsáním původní služby web. Hlavní změny jsou v __init__.py

### __init__.py
Aplikace obsahuje implementované REST API. Jednotlivá API mimo cesty obsahují i metodu. 

@app.route('/api/images', methods=['POST'])

Hlavním rozdílem proti původní službě web je, že nekomunikuje přes HTML, ale přes JSON. Pokud funkce přijímá data, musí 
je nejprve z textové podoby parsovat do JSON. Python kód pak již pracuje s hierarchickou datovou strukturou.

Naopak, pokud má služba předat nějaká data, je připraven JSON dokument, který se posílá volajícímu.

## Služba ui
Nejvíce změn proběhlo v této službě. Jedná se o klasickou webovou aplikaci, která je postavená na frameworku Flask. 
Pro renderování HTML stránek používá jinja2. Jinja2 je moderní šablonovací systém pro jazyk Python vycházející ze syntaxe Django. 
Pro vytváření a kontrolu formulářů se používá knihovna Flask-WTF, která zajišťuje bezpečnost, kontrolu vstupních hodnot apod.
Podrobnosti o implementaci jsou nad rámec této kapitoly. A pro pochopení dockeru a microservices je to i zbytečné. Uživatelské rozhraní
aplikace by šlo postavit i na jiných technologiích.

Ve stručnosti si ukažme princip komunikace mezi službami na zobrazení náhodného obrázku.

* Uživatel v UI chce zobrazit stránku, která má zobrazit náhodný obrázek. Zavolá se funkce index()
* Nejprve se přes knihovnu urllib zavolá metodou GET API rozhraní služby images http://images:5000/api/images
* Služba images převezme požadavek a pokusí se přečíst z databáze seznam všech obrázků
* Ze všech vrácených řádků z databáze poskládá platný JSON dokument, který odešle službě UI
* Služba UI přijme textový řetězec, který se pokusí převést na JSON dokument
* Pokud se to podaří, ze seznamu vybere náhodný obrázek
* Náhodný obrázek pošle spolu se vzorem index.html pro vyrenderování. 
* Vzor index.html používá i vzor header.jinja.

UI
```
@app.route("/")
def index():
    content = urllib.request.urlopen('http://images:5000/api/images').read().decode('utf-8')
    try:
        images = json.loads(content)
    except ValueError as e:
        return render_template("errors/500.jinja"), 500

    image = random.choice(images)
    return render_template('index.html', url=image['image_url'])
```

Images
```
@app.route("/api/images")
def get_images():
    try:
        images = Image.query.all()
        if images:
            result = []
            for image in images:
                result.append({"id": image.id, "image_url": image.image_url})
            return jsonify(result)
        else:
            return jsonify({"error": f"Images not found."}), 404
    except Exception as e:
        print(f"The error '{e}' occurred.")
        return jsonify({"error": "An error occurred while getting all images."}), 500
```

## Spuštění
| Příkaz                                                                               | Popis                                                                 |
|--------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| docker compose up -d                                                                 | Build a start aplikace                                                |
| http://localhost:8080/?pgsql=database&username=admin&db=test&ns=public&select=images | Přes adminer lze zkontrolovat, že tabulka images vytvořená a naplněná |
| http://localhost:8006/                                                               | Zobrazení náhodného obrázku                                           |
| docker compose down                                                                  | Vypnutí aplikace                                                      |
| DB_INIT=0                                                                            | V souboru .environment vyplňte inicializaci databáze                  |
| docker compose up -d                                                                 