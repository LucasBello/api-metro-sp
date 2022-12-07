
# Capturando e tratando informações sobre a malha metroviária de São Paulo

Neste projeto utilizaremos um Web Scrapper escrito em python com [Beaultiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) para localizar na página da [Via Quatro](https://www.viaquatro.com.br/) as informações sobre as linhas metroviárias e obter seus status de funcionamento, alimentando um arquivo json em um HTTP REQUEST que servirá de base de dados para um frontend. 

## Preparando o ambiente de trabalho
Para darmos início serão necessárias as seguintes ferramentas:
<!-- ![](src/vscode_modulos.png) -->
#### npm
Tenha o npm instalado para fazermos o ambiente de virtualização
[Instalação npm](https://docs.npmjs.com/cli/v6/commands/npm-install)Instalação npm
#### Azure functions core tools
Instale o azure functions core tools
```npm install -g azure-functions-core-tools@4 --unsafe-perm true```

#### Azure Cli
Para instalação do azure cli, segue [documentação](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) para instalação em todos os sistemas operacionais
#### Módulos VsCode:
- Azure Tools
- Azure Functions
#### Repositório Git
Faça o clone do repositório [LucasBello/azure-functions-metro](git@github.com:LucasBello/azure-functions-metro.git)
#### Repositório Local
Crie uma pasta para servir de repositório local do Azure Functions e acesse via VSCode
```bash
$ mkdir funcoes && code funcoes
```
## Preparando o Azure

<img src="src/azure_cli.png" alt="drawing" style="width:50px;"/> Autenticar uma sessão do Azure pelo Azure Cli
```bash
az login
```
### Recursos para Azure Functions

Como visto, o Azure Functions utiliza diversos recursos para seu funcionamento. Sua árvore de recursos é a seguinte:

Resource Group
<br>├── Storage
<br>├── functionApp
<br>└── skuStorage

O primeiro passo é configurar a subscrição que receberá os recursos, no caso deste laboratório utilizaremos uma subscrição Pay-As-You-Go

Para que você pegue a ID de sua subscrição iremos utilizar o seguinte comando:
```bash
##Desta forma irá retornar somente a id que precisaremos para o próximo passo
az account show --query id
```

```bash
#Crie uma variável para sua id de subscrição para caso precise mais tarde
subscription="<subscriptionId>"

#Faça a definição de sua subscrição no azure cli
az account set -s $subscription
```
Agora vamos começar a criação dos recursos do Azure Functions

> **_NOTA:_** Esta etapa pode ser realizada com a criação de um script de execução automático ou sendo executado linha a linha para melhor entendimento.

<img src="src/resource_group.png" alt="drawing" style="width:20px;"/> Criar resource group
```
az group create --name api-metro-sp --location eastus
```
<img src="src/storage_account.png" alt="drawing" style="width:20px;"/> Criar storage
```
az storage account create --name apimetrospstorage --location eastus --resource-group api-metro-sp --sku Standard_LRS
```
<img src="src/functions.png" alt="drawing" style="width:30px;"/> Criar FunctionApp
```
az functionapp create --name api-metro-sp-function --storage-account apimetrospstorage --consumption-plan-location eastus --resource-group api-metro-sp --functions-version 4
```
> **_IMPORTANTE:_** Para realizar o teardown do ambiente basta executar: ```az group delete --name api-metro-sp```

## Implantando aplicação
A partir de agora iremos utilizar os módulos do VSCode instalados anteriormente

### Configurando ambiente de desenvolvimento
- Em seu VSCode acesse o módulo do Azure para verificar os recursos criados
<!-- ![](src/vscode_recursos.png) -->

- Em Workspace clique em ```add``` e depois em ```Create Http Function```
<!-- ![](src/vscode_add_2.png) -->

- Selecione a linguagem ```Python```
- Nomeie a Função para ```HttpTrigger```

Agora o ambiente virtual será criado para ser trabalhado.

### Criando a primeira Function App - HttpTrigger

- Abra a pasta ```HttpTrigger``` e adicione o ```HttpTrigger.py``` do repositório clonado anteriormente

<!-- ![](src/httptrigger_1.png) -->

- vamos editar o arquivo ```function.json``` deixando-o desta forma:
```json
{
  "scriptFile": "HttpTrigger.py",
  "bindings": [
    {
      "authLevel": "anonymous",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": [
        "get",
        "post"
      ]
    },
    {
      "type": "http",
      "direction": "out",
      "name": "$return"
    }
  ]
}
```
Assim quando o function receber um ```get``` irá responder com o nosso python.
> **_NOTA:_** Neste arquivo podemos fazer isso para chamar qualquer python que desejar, inclusive alterar o método de request.

Com isso temos a nossa primeira ```FunctionApp``` configurada no ambiente de desenvolvimento.

### Criando a segunda Function App - ViaQuatroScrapper
- Crie mais uma ```Http Function``` em sua workspace como fizemos anteriormente, apenas altere o nome da função para ```ViaQuatroScrapper```
- Copie o arquivo ```Scrapper.py``` da pasta ```ViaQuatroScrapper``` do repositório clonado para a pasta em sua workspace e altere o arquivo ```function.json``` desta forma

```json
{
  "scriptFile": "Scrapper.py",
  "bindings": [
    {
      "authLevel": "anonymous",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": [
        "get",
        "post"
      ]
    },
    {
      "type": "http",
      "direction": "out",
      "name": "$return"
    }
  ]
}
```
Observe que o arquivo ```Scrapper.py``` utiliza os seguintes módulos
```py
import logging
import os
import requests
import time
import datetime
from bs4 import BeautifulSoup
import json
```
Sendo que os módulos ```bs4``` e ```requests``` não fazem parte da instalação do Azure Functions nativamente e devem ser adicionados ao arquivo ```requirements.txt```

Vamos faze-lo agora.

- Abra o arquivo ```requirements.txt``` e adicione os módulos da seguinte forma e salve
```txt
# DO NOT include azure-functions-worker in this file
# The Python Worker is managed by Azure Functions platform
# Manually managing azure-functions-worker may cause unexpected issues

azure-functions
requests==2.28.1
bs4
```
Agora estamos prontos para fazer a primeira implantação

```
func azure functionapp publish api-metro-sp-function --build remote
```
