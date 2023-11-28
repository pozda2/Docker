# Produkce

V této kapitole aplikaci dokončíme a vytvoříme konfiguraci, která bude vhodná pro nasazení do produkce.

- Odebereme adminer, protože nástroj pro administraci databáze na produkci může být velmi nebezpečný
- Vytvoříme novou službu nginx, který nakonfigurujeme jako reverzní proxy server. Bude sloužit jako jeden přístupový bod, který skryje vnitřní služby aplikace. Microslužby budou komunikovat po backnet síti a nepůjde s nimi komunikovat napřímo.

## docker-compose.yaml

### ui
 - aplikaci již nespouštíme přes interní flask webový server, který je určený pouze pro vývoj. Místo použijme gunicon, Python WSGI HTTP Server. To je web server gateway interface web server, který je dostatečně lehký, ale vhodný pro provoz pyhon aplikací.
 - zrušíme možnost bindingu (/services/ui/:/usr/src/app/), kdy jsme mohli rychle upravovat zdrojové soubory
 - naopak přidáme volume static_volume, který bude obsahovat statické části aplikace. Volume bude sdílet se službou nginx
 - zrušíme mapování portu 5000 na 8006, kterým jsme umožňovali komunikovat s webovou aplikací napřímo 
 - místo toho přidáme expose 5000, který zaručí, že kontejner bude po backnet schopen komunikovat přes port 5000
 - ui odebereme ze sítě frontnet a necháme ho pouze v sítí backet

### images
 - zde upravíme pouze spouštění aplikace přes gunicorn

### nginx
 - nová služba z image, který obsahuje webový server Nginx, který nakonfigurujeme jako reverzní proxy
 - ports 8100:80 zaručí přístupnost aplikace přes port 8100
 - static volume slouží pro sdílení statických souborů uložených v ui
 - služba komunikuje přes obě sítě

```
version: '3.8'

services:
  ui:
    container_name: ui
    build: ./services/ui
    command:
      gunicorn --bind 0.0.0.0:5000 manage:app
    volumes:
      - static_volume:/home/app/web/app/static
    expose:
      - 5000
    depends_on:
      - images
    env_file:
      - .environment
    networks:
      - backnet

  images:
    container_name: images
    build: ./services/images
    command:
      gunicorn --bind 0.0.0.0:5000 manage:app
    expose:
      - 5000      
    env_file:
      - .environment
    depends_on:
      - database
    networks:
      - backnet

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

  nginx:
    container_name: nginx
    build: ./services/nginx
    ports:
      - "8100:80"
    depends_on:
      - ui
    volumes:
      - static_volume:/home/app/web/app/static
    networks:
      - frontnet
      - backnet

volumes:
  postgres_data:
  static_volume:

networks:
  frontnet:
  backnet:
```

## environment
 | Proměnná    | Hodnota       | Vysvětlení                                                                                                                       |
 |-------------|---------------|----------------------------------------------------------------------------------------------------------------------------------|
 | APP_FOLDER  | /home/app/web | Aplikaci přestaneme provozovat pod rootem, ale uživatelem app a změníme její umístění                                            |
 | FLASK_DEBUG | 0             | Vypneme ladění flasku                                                                                                            |
 | DB_INIT     | 0             | Vypneme inicializaci databáze. Pro větší bezpečnost, bychom mohli upravit i imgaes/entrypoint.sh a zrušit celou podmínku INIT_DB |


## Dockerfile
Výrazného přepracování se dočkaly Dockerfile pro služby images a ui.
- Nyní jsou rozdělené na části builder a final. Během builder se python zdrojové soubory převádí do distribuční podoby wheel. Pro převod se používá adresář /usr/src/app
- PYTHONDONTWRITEBYTECODE: Zabrání pythonu vytvářet pyc soubory na disku 
- PYTHONUNBUFFERED: Zabrání Python v buffrování stdout a stderr 
- V části final se vytváří adresář /home/app, kam se zkopíruje připravená aplikace z fáze build
- Aplikace se bude spouštět pod uživatelem app a nikoliv root

## nginx.conf
Nastavení reverzní proxy
```
upstream ui_flask {
    server ui:5000;
}

server {

    listen 80;

    location / {
        proxy_pass http://ui_flask;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /static/ {
        alias  /home/app/web/app/static/;
    }
}
```

# Spuštění aplikace
| Příkaz                                                | Vysvětlení                    |
|-------------------------------------------------------|-------------------------------|
| docker compose down -v                                | Zrušení kontejnerů i volume   |
| docker compose up -d --build                          | Vytvoření a spuštění aplikace |
| docker compose exec images python manage.py create_db | Vytvoření databáze            |
| docker compose exec images python manage.py seed_db   | Naplnění databáze             |
| http://localhost:8100                                 | Aplikace                      |