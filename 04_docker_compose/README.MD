# Docker compose

Vytváření kontejnerů pomocí Dockerfile je vhodné převážně pro jedno kontejnerová aplikace. 
Ve chvíli, kdy chceme vytvořit multi kontejnerovou aplikace, například webovou aplikaci s databázovým serverem, 
tak by vytváření dosavadní způsobem bylo komplikované.

Proto vznikl nástroj docker-compose, který v posledních verzích je integrovaný do samotného dockeru.

Popis aplikace a její rozdělení se definuje pomocí textového souboru docker-compose.yml

Tento soubor má hierarchickou strukturu podobně jako JSON. Pokud nebudou údaje správně zarovnány pomocí TAB, tak 
nemusí fungovat správně.

V této kapitole si pro jednoduchost vytvoříme jedno kontejnerovou aplikaci se statickou stránkou z předchozích kapitol.

## docker-compose.yaml
Syntaxe souboru prochází vývojem a je vhodné u každého souboru uvést verzi, kterou používáte. V opačném případě se 
předpokládá verze 1. Pro běžné aplikace je vhodné používat verzi minimálně 2 a vyšší.


```
# definovat verzi minimalni 2
version: "3.8"

# Služby (kontejnery)
services:
  service_1: # Sekce prvního kontejneru (zároveň DNS název)
    container_name: # název kontajneru (nepovinné)
    build: # cesta k Dockerfile pro build
    image: # nebo název hotového image (lokálne, Dockerhub)
    ports: # mapovaní portů 
    volumes: # argument -v, anebo i COPY instrukce (nepovinné)
    environment: # argument -e, environment proměnné (nepovinné)
    command: # definované příkazy po spustení kontejneru (přepisuje ty v image)(nepovinné)
  
  service_2: # další kontejner
  
  
volumes:
    # definice volume

networks:  
   # definice sítí
```

| Příkaz                       | Vysvětlení                                                          |
|------------------------------|---------------------------------------------------------------------|
| docker compose up --build -d | Při změně Dockerfile se spustí build                                |  
| docker compose up            | Build, vytvoření kontejnerů a jejich spuštění                       |
| http://localhost:8002        | Ověření aplikace a pak vypnutí přes CTRL+C                          |  
| docker compose down          | Vypnutí kontejnerů a jejich smazání (volumes a networks se nemažou) |
| docker compose up -d         | Spuštění kontejneru na pozadí                                       |