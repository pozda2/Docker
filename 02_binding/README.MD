# Bind mounting

V minulé kapitole jsme vytvořili image s pevnou HTML stránkou. Pokud při ladění aplikace zjistíme chybu a opravíme ji, 
tak budeme muset provést rebuild image, smazání a znovu vytvoření kontejneru, abychom opravu chyby mohli vyzkoušet.

Tento způsob vývoje aplikace bude velmi neefektivní.

Docker nabízí možnost, kdy se adresář z hostovaného serveru propojí dovnitř do kontejneru. Pokud provedeme opravu chyby,
tak se okamžitě přenese do kontejneru bez nutnosti jeho rebuildu nebo restartu. Z hlediska výkonu toto řešení není optimální,
ale velmi urychlí vývoj.

Stále můžeme využít předchozí Dockerfile, pouze při vytváření kontejneru povolíme binding. 

| Příkaz                                                                                           | Vysvětlení                                                                                                                                                |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| docker run -d --name my-hello-world-c2 -p 8001:80 -v $(pwd)/webroot:/var/www/html my-hello-world | Syntaxe pro linux a mac os.  Parametr -v říká, že adresář $(pwd)/webroot bude přemontován přes obsah adresáře /var/www/html                               |
| docker run -d --name my-hello-world-c2 -p 8001:80 -v %cd%/webroot:/var/www/html my-hello-world   | Pro Windows pouze zaměníme linuxový příkaz pro zjistění aktuální adresáře pwd za windows příkaz cd | 

* Připojte se v prohlížeči na url http://localhost:8001/
* Upravte v souboru webroot/index.html Hello world na Ahoj svete
* Obnovte v prohlížeči stránku http://localhost:8001/
