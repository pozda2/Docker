# Základní statická stránka

V této kapitole si zprovozníme jednoduchý webový server Apache, který bude obsahovat jednu statickou html stránku.

Aplikace (stránka) je umístěna v adresáři webroot

## Pojmy

### Image
**Image** je šablona, která slouží pro vytváření individuálních kontejnerů. Obsahuje soubory aplikace, konfigurační 
soubory a případně další soubory aplikace. V rámci image se připravuje prostředí (knihovny, frameworky), které potřebuje
daná aplikace. 

Image zpravidla bývá založen na jiné image, do kterého pouze něco přidá. Existují docker hub, které obsahují ověřené 
image (https://hub.docker.com/search?q=). Velmi často firmy nebo komunita sdílí software přes tyto image.

Image se ukládají do registru images. Předpřipravený image lze z registru stáhnout a případně nově vytvořený image
zpětně do registru nahrát.

Předpis pro vytvoření image je uložený v souboru Dockerfile

| Příkaz | Vysvětlení |
|--------| ---------- |
| docker pull alpine                  | stáhnutí oficiální image se základním verzí linuxu |
| docker image ls                     | zobrazení seznamu images |
| docker image id                     | smazání nepotřebného image | 

### Container

Kontejner je konkrétní běhové prostředí aplikace vytvořené na základě nějakého image. Sdílí jádro operačního systému 
s ostatními kontejnery. Z jednoho image můžeme vyvořit více kontejnerů, které poběží souběžně vedle sebe.

| Příkaz                               | Vysvětlení                      |
|--------------------------------------|---------------------------------|
| docker ps                            | Vypsání běžících kontejnerů     |
| docker ps -a                         | Vypsání všech kontejnerů        |
| docker ps -a                         | Vypsání všech kontejnerů        |
| docker ps --filter "label=abc"       | Výpis kontejnerů s daným label  |
| docker ps --filter "label=key=value" | Výpis kontejnerů s daným label  |
| docker ps --filter "name=jmeno"      | Výpis kontejnerů s daným jménem |


### Dockerfile
Textový soubor, který podle kterého se vytváří image s naší aplikací. Do souboru se zapisují různé příkazy, které 
si postupně ukážeme.

| Příkaz     | Vysvětlení                                                                                                                                                                                   |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FROM       | Výchozí image, na kterém je náš image založený. Zpravidla nic nestavíme zcela od počátku, ale vybereme si image, který například obsahuje python, php a webový server jako apache nebo ngix. |
| LABEL      | Textový popis image. Pokud použijeme vlastní klíčová slova, půjde podle nich filtrovat. Label může obsahovat i podobu KEY=value. Například LABEL buildDate=$buildDate                        |
| RUN        | Pustí příkaz linux například aktualizaci základní modulu PIP                                                                                                                                 |
| CMD        | Na pozadí spouští příkaz, pokud není specifikovaný předřadí se /bin/sh -c                                                                                                                    |  
| COPY       | kopíruje lokální soubor, adresář do image na zadané místo                                                                                                                                    |
| ADD        | Podobně jako COPY, ale navíc například rozbalí zabalený soubor se zdrojáky. tar.gz apod.                                                                                                     |
| WORKDIR    | Změna adresáře                                                                                                                                                                               |
| VOLUME     | Připojení disku pro zápis. Viz dále                                                                                                                                                          |
| USER       | Spouštění pod jiným uživatelem než je root                                                                                                                                                   |
| ENV        | Nastavení systémové proměnné                                                                                                                                                                 |
| EXPOSE | Propagace vnitřních portů v kontejneru navenek |
| ENTRYPOINT | Příkaz, který spouští aplikaci                                                                                                                                                               |


# Hello world

| Příkaz                               | Vysvětlení                                                                                    |
|--------------------------------------|-----------------------------------------------------------------------------------------------|
| docker run hello-world                         | Stažení image hello-world z dockerhub, vytvoření kontejneru s náhodným jménem a jeho spuštění |
 

# První aplikace

| Příkaz                                                              | Vysvětlení                                                                                                                           |
|---------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| docker build -t my-hello-world .                                    | Vytvořebí image my-hello-world podle Dockerfile                                                                                      |
| docker image ls                                                     | Vypsání seznamu images                                                                                                               |
| docker run -d -p 8080:80 --name my-hello-world-app-c my-hello-world | Vytvoření kontejneru z image. Kontejner se spustí a vnitřní port apache 80 je z venku dostupný na 8080. V prohlížeči zadejte adresu http://localhost:8080 |
| docker ps                                                           | výpis kontejneru |
| docker stop my-hello-world-app-c                                    | Vypnutí kontejneru |
| docker rm my-hello-world-app-c | Smazání kontejneru |