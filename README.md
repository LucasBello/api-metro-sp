
# Capturando e tratando informações sobre a malha metroviária de São Paulo

Neste projeto utilizaremos um Web Scrapper escrito em python com [Beaultiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) para localizar na página da [Via Quatro](https://www.viaquatro.com.br/) as informações sobre as linhas metroviárias e obter seus status de funcionamento, alimentando um arquivo json em um HTTP REQUEST que servirá de base de dados para um frontend. 

## Preparando o ambiente de trabalho
Para darmos início serão necessárias as seguintes ferramentas:
<!-- ![](src/vscode_modulos.png) -->
#### Módulos VsCode:
- Azure Tools
- Azure Functions
#### Repositório Git
Faça o clone do repositório [LucasBello/azure-functions-metro](git@github.com:LucasBello/azure-functions-metro.git)
#### Repositório Local
Crie uma pasta vazia para servir de repositório do Azure Functions e acesse via VSCode
```bash
$ mkdir funcoes && code funcoes
```
## Procedimentos

- [ ] Mercury
