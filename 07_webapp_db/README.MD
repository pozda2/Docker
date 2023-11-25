# Připojení k databázi

V této kapitole naši aplikaci napojíme na databázi, ze které si bude načítat seznam obrázků.

## docker-compose.yaml
Je dobrým zvykem parametry, které se mění s nasazením do různých prostředí umístit do samostatného souboru se 
systémovými proměnnými. V našem případě to je soubor .environment, na který odkazuje parametr env_file. Pak lze jednoduše
měnit jména, hesla, porty atd.

Flask aplikaci budeme nyní spouštět v debug režimu, pomocí příkazu python manage.py run -h 0.0.0.0
To nám umožní sledovat detailněji chyby. 

```
version: '3.8'

services:
  web:
    container_name: web
    build: ./services/web
    command:
      python manage.py run -h 0.0.0.0
    volumes:
      - ./services/web/:/usr/src/app/
    ports:
      - "8005:5000"
    env_file:
      - .environment
    depends_on:
      - database

  database:
    container_name: database
    restart: always
    image: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .environment

  adminer:
      container_name: adminer
      image: adminer
      restart: always
      ports:
          - "8080:8080"
      depends_on:
          - database

volumes:
  postgres_data:
 ```

## .environment
| Proměnná          | Hodnota          | Vysvětlení                                                                       |
|-------------------|------------------|----------------------------------------------------------------------------------|
| FLASK_APP         | app/__init__.py  | startovní program aplikace                                                       |
| FLASK_DEBUG       | 1                | Spuštění aplikace v debug režimu                                                 |
| DB_INIT           | 1                | Při 1 se během spuštění aplikace vytvoří databáze, vytvoří tabulka a naplní daty |
| DATABASE          | postgres         | Typ databáze                                                                     |
| POSTGRES_HOST     | database         | hostname databáze                                                                |
| POSTGRES_PORT     | 5432             | Port databáze                                                                    |
| POSTGRES_USER     | admin            | Admin databáze                                                                   |
| POSTGRES_PASSWORD | mysecretpassword | Heslo admina databáze                                                            |
| POSTGRES_DB       | test             | Jméno databáze                                                                   |
| DATABASE_URL      | postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}   | Connection string do databáze                                                    |

## entrypoint.sh
Skript zkontroluje, zda běží databáze. Pokud je proměnná DB_INIT nastavená na 1 spustí vytvoření tabulek a jejich 
naplnění přes zavolání programu manage.py s parametry create_db a seed_db

## manage.py
Buď vytvoří tabulky a naplní je nebo spustí Flask aplikaci app

## config.py
Základní nastavení aplikace. Ze systémové proměnné DATABASE_URL se nakonfigure Flask SQLAlchemy, knihovnu pro práci
s relačními databázemi ve Flasku.

## __init__.py
Hlavní aplikace, která na začátku načte konfiguraci z config.py a připojí se k databázi přes Flask SQLAlchemy.

Program obsahuje třídu Image, která z děděná ze třídy model. Třída obsahuje definici tabulky a konstruktor __init__ pro 
vytvoření instance Image - řádku v tabulce.

Část aplikace, která volí náhodný obrázek používá metodu images=Image.query.all(), která z databáze načte všechny řádky.
Pak se vybere náhodný záznam v seznamu, který se zobrazí.

# Spuštění
| Příkaz                                                                               | Popis                                                                 |
|--------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| docker compose up                                                                    | Build a start aplikace                                                |
| http://localhost:8080/?pgsql=database&username=admin&db=test&ns=public&select=images | Přes adminer lze zkontrolovat, že tabulka images vytvořená a naplněná |
| http://localhost:8005/                                                               | Zobrazení náhodného obrázku                                           |
| docker compose down                                                                  | Vypnutí aplikace                                                      |
| DB_INIT=0                                                                            | V souboru .environment vyplněte inicializaci databáze                 |
| docker compose up -d                                                                 | Zapnutí aplikace                                                      |
 

