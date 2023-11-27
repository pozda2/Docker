# Volume

Soubory a adresáře vytvořené během vytváření image jsou read-only. Aplikace může zapisovat svá data, ale po vypnutí 
kontejneru se data zničí.

Pokud aplikace potřebuje někam trvale zapisovat data, musíme ji připojit zapisovatelný volume.

Ukážeme si to na databázi PostgreSQL.


| Příkaz                                                                         | Vysvětlení                                                                                                 |
|--------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| docker pull postgres                                                           | Stáhnutí oficiálního image s poslední verzí postgreSQL                                                     |
| docker run --name postgresdb -e POSTGRES_PASSWORD=mysecretpassword -d postgres | Vytvoření kontejneru. Databáze potřebuje nastavit root heslo pomocí promměné POSTGRES_PASSWORD             |
| docker container inspect postgresdb | Image postgres měl v sobě definovaný nepojmenovaný volume. Přesnou definici můžeme zobrazit pomocí inspect | 

Ve výpisu hledáme sekci Mounts. Zde je vidět, že volume f33a231365088ce230e61472a9b4b00d88c016fe2b15e24cc25e3c9274ae6b57 se připojil /var/lib/postgresql/data 
```
"Mounts": [
            {
                "Type": "volume",
                "Name": "f33a231365088ce230e61472a9b4b00d88c016fe2b15e24cc25e3c9274ae6b57",
                "Source": "/var/lib/docker/volumes/f33a231365088ce230e61472a9b4b00d88c016fe2b15e24cc25e3c9274ae6b57/_data",
                "Destination": "/var/lib/postgresql/data",
                "Driver": "local",
                "Mode": "",
                "RW": true,
                "Propagation": ""
            }
```

| Příkaz                                                                         | Vysvětlení    |
|--------------------------------------------------------------------------------|---------------|
| docker volume ls                                                               | Výpis volumes |

 Volume vydrží zastavení i smazání kontejneru. O data nepřijdeme.

| Příkaz                 | Vysvětlení                    |
|------------------------|-------------------------------|
| docker stop postgresdb | Zastavení kontejneru          |
| docker rm postgresdb   | Smazání kontejneru            |
| docker volume ls       | Výpis volumes                 |
| docker volume prune    | Smazání nepoužívaných volumes |
| docker volume ls       | Výpis volumes                 |

## Pojmenované volumes

| Příkaz                                                                                                               | Vysvětlení                                                                                     |
|----------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| docker run --name postgresdb -e POSTGRES_PASSWORD=mysecretpassword - postresdb:/var/lib/postgresql/data -d postgres  | Vytvoří kontejner s pojmenovaným volume                                                        |
| docker volume ls                                                                                                     | Vytvoření kontejneru. Databáze potřebuje nastavit root heslo pomocí proměnné POSTGRES_PASSWORD |
| docker logs postgresdb                                                                                               | Zobrazení logu kontejneru. Pomůže při zjišťování chyb                                          | 
