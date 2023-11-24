# Databáze

V této kapitole si pomocí docker compose vytvoříme databázi postresql. Zároveň si připravíme aplikaci adminer pro její
správu pomocí webového prostředí.

## docker-compose.yaml
První kontejner se bude jmenovat database a vytvoříme ho z image postres. V sekci environment si definujeme heslo (to je povinné) 
a případně jméno administrátora. Můžeme si rovnou i vytvořit databázi.

Aby nám databáze přežila restart, tak si vytvoříme volume db-data. Ten napapujeme do /var/lib/postresql/data

Druhý kontejner bude obsahovat aplikaci adminer, která bude poslouchat na portu 8080.

```
version: "3.8"

services:
    database:
        container_name: database
        restart: always
        image: postgres
        environment:
            - POSTGRES_USER=admin
            - POSTGRES_PASSWORD=mysecretpassword
            - POSTGRES_DB=test
        volumes:
            - db-data:/var/lib/postresql/data

    adminer:
        container_name: adminer
        image: adminer
        restart: always
        ports:
            - "8080:8080"
        depends_on:
            - database

volumes:
    db-data:
```

| Příkaz                               | Vysvětlení                            |
|--------------------------------------|---------------------------------------|
| cd docker-conf                       | Přepnutí do adresáře docker-conf      |
| docker compose up -d                 | Vytvoření a spuštění kontejnerů       |
| docker ps                            | Výpis spuštěných kontejnerů           |
| docker volume list                   | Výpis volumes                         |
| docker exec -it database /bin/bash   | Spuštění příkazové řádky v kontejneru | 

Nyní můžeme databázi ovládat z příkazové řádky

| Příkaz                                      | Vysvětlení                                       |
|---------------------------------------------|--------------------------------------------------|
| psql -Uadmin -d test                        | Přihlášení do databáze test pod uživatelem admin |
| SELECT datname FROM pg_catalog.pg_database; | Výpis databází. Případně lze zadat \l            |
| create table test (a int);                  | Vytvoření tabulky                                |
| insert into test values(1);                 | Vložení řádku do tabulky                         | 
| select * from test;                         | Výpis tabulky                                    |

Vyzkoušíme si i webový přístup. V prohlížeči otevřete URL http://localhost:8080

Zvolte typ databáze postreSQL, server je database, uživatel admin, heslo mysecretpassword a databáze test.

Měli byste být přihlášeni k databázi, kterou teď můžete administrovat.