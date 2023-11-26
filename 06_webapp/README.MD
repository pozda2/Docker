# Jednoduchá web aplikace ve flasku

## Popis aplikace

V této kapitole začneme psát jednoduchou aplikaci v python framework Flask

Samotná aplikace se jmenuje app.py. Na začátku je definován list 4 URL odkazů na obrázky.

@app.route('/') dekorátor je uveden před funkcí index(), a říká, že se pouští, pokud bude URL /

Funkce index() vygeneruje náhodné url ze seznamu a zavolá funkci render_template, které je předáno url náhodného obrázku 
a soubor index.html v templates.

Soubor index.html je flask template html, který vypadá jako klasický html. V místě, kde se má použit proměnná url je {{url}}.

## Spuštění aplikace
Pro běh aplikace jsou třeba python knihovny vyjmenované v souboru requirements. Jejich instalace je zajištěna v Dockerfile pomocí 
**RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt**


Aplikaci je třeba spouštět ve webovém serveru. Šel by použít apache, ngix. V našem případě jsem použili lehký Gunicorn 'Green Unicorn' Python WSGI HTTP Server pro UNIX.

Jeho spuštění je v souboru gunicorn.sh V něm ji vidět, že aplikace poběží na portu 5000 a bude používat dvě vlákna pro obsluhu příchozích požadavků.

gunicorn.sh je ENTRYPOINT v Dockerfile

##
docker compose up 

