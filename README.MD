# Úvod do docker
V rámci tohoto projektu si postupně ukážeme postupy, jak vytvořit kontejnerizovanou aplikaci.

Aplikace bude napsaná v Python3 za použití frameworku Flask. Pro pochopení principu dockeru není třeba tyto technologie ovládat.

Projekt předpokládá, že máte na počítači nainstalovaný Docker. Na linuxu, lze nainstalovat přes repozitáře. Na Windows si stáhněte Docker Desktop a postupujte podle návodu.

Vytvářet multikontejnerovou aplikaci budeme postupně. Jednotlivé fáze jsou umístěny do očíslovaných adresářů.

## Instalace docker na Linuxu

Tento návod je určený pro Ubuntu

* sudo su -
* apt update
* apt install ca-certificates curl gnupg lsb-release
* mkdir -m 0755 -p /etc/apt/keyrings
* curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
* echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
* apt update
* apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
