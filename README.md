# zssn-api
Teste de codificação de desenvolvedor (Rede Social de Sobrevivência Zumbi) 2022.

## :clipboard: Descrição do Problema
ZSSN (Rede Social de Sobrevivência Zumbi). O mundo como o conheceu caiu em um cenário apocalíptico. Um vírus produzido em laboratório está transformando seres humanos e animais em zumbis, famintos por carne fresca.
Você, como membro da resistência aos zumbis (e o último sobrevivente que sabe codificar), foi designado para desenvolver um sistema para compartilhar recursos entre humanos não infectados.

## :hammer: Tecnologias utilizadas
* Python 3;
* Django 4.1;
* Djangorestframework 3.13.1

## Começando

### Pré-requisitos
* Python3
* PIP3
* Virtualenv

1. Clonando o projeto para a sua máquina:
    ```bash
    https://github.com/JelsonMatheus/zssn-api.git
    ```

2. Renomear o arquivo que contem as variáveis de ambiente `.env.example` para `.env`.

### Executando o projeto

1. Criar uma **virtualenv** na raiz do projeto:
    ```bash
    python3 -m venv venv
    ```

2. Ativar o ambiente virtual:\
   Linux: `source venv/bin/active`.\
   Windows: `venv\scripts\activate`.

3. Instalar dependências:

    ```bash
    pip3 install -r .requirements.txt
    ```

4. Realizar o migrate no banco de dados:

    ```bash
    python3 manage.py migrate
    ```
5. Iniciar servidor Django:

    ```bash
    python3 manage.py runserver
    ```
    ```bash
    System check identified no issues (0 silenced).
    August 07, 2022 - 23:08:58
    Django version 3.2.5, using settings 'zssn.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    ```

## Endpoints

**BASE URL**
- Localhost: http://127.0.0.1:8000/api/v1

### Sobreviventes
| Método | URL                     | Descrição                                  |
|--------|-------------------------|--------------------------------------------|
| GET    | /survivors/             | [Lista todos os Sobreviventes.](#listsurvivors)|
| GET    | /survivors/:pk/         | [Exibe um Sobrevivente específico.](#onesurvivor)|
| GET    | /survivors/:pk/inventory/ | [Lista os itens de um Sobrevivente.](#itemssurvivor)|
| POST   | /survivors/             | [Cria um novo Sobrevivente.](#newsurvivor)|
| PATCH  | /survivors/:pk/         | [Atualiza o local de um Sobrevivente.](#updatesurvivor)|

### Informar infecção
| Método | URL                     | Descrição                                  |
|--------|-------------------------|--------------------------------------------|
| POST   | /report-contamination/  | [Informa sobre uma nova infecção.](#infected)|

### Troca de itens entre os Sobreviventes
| Método | URL                     | Descrição                                  |
|--------|-------------------------|--------------------------------------------|
| POST   | /trades/                | [Realiza a troca de itens entre os Sobreviventes.](#trade)|

### Relatórios
| Método | URL                     | Descrição                                  |
|--------|-------------------------|--------------------------------------------|
| GET    | /reports/infected/      | [Porcentagem de sobreviventes infectados.](#reportinfected)|
| GET    | /reports/uninfected/    | [Porcentagem de sobreviventes não infectados.](#reportuninfected)|
| GET    | /reports/avg-resources/ | [Média de recurso por sobrevivente.](#reportavg)|
| GET    | /reports/lost-points/   | [Pontos perdidos por causa do sobrevivente infectado.](#reportlost)|

# 

#### <a id="listsurvivors"></a> Listar todos os Sobreviventes
*URL:* `/survivors/` <br>
*Method:* `GET`
#### Response
*Status code*: `200 OK`

```json
[
   {
      "name": "João",
      "age": 21,
      "gender": "M",
      "is_infected": false,
      "latitude": "5.000",
      "longitude": "150.000"
   },
   "..."
]
```

#### <a id="onesurvivor"></a> Exibe um Sobrevivente específico
*URL:* `/survivors/:pk/`<br>
*Method:* `GET`

#### Response
*Status code*: `200 OK`

```json
{
   "pk": 1,
   "name": "João",
   "age": 21,
   "gender": "M",
   "is_infected": false,
   "latitude": "5.000",
   "longitude": "150.000"
}
```

#### <a id="itemssurvivor"></a> Lista os itens de um Sobrevivente
*URL:* `/survivors/:pk/inventory/`<br>
*Method:* `GET`

#### Response
*Status code*: `200 OK`

```json
{
   "water": 2,
   "food": 1,
   "medication": 3,
   "ammunition": 1
}
```

#### <a id="newsurvivor"></a> Cria um novo Sobrevivente
*URL:* `/survivors/`<br>
*Method:* `POST`
*Body:*
```json
{
   "name": "João",
   "age": "21",
   "gender": "M",
   "latitude": 5,
   "longitude": 10,
   "inventory": {
      "water": 2,
      "food": 1,
      "medication": 3,
      "ammunition": 1
   }
}
```
Para criar um Sobrevivente com nenhum recurso (consulte a tabela de itens):
```json
{
   "name": "João",
   "age": "21",
   "gender": "M",
   "latitude": 5,
   "longitude": 10,
   "inventory": {}
}
```

#### Response
*Status code*: `200 OK`
```json
{
   "pk": 1,
   "name": "João",
   "age": 21,
   "gender": "M",
   "is_infected": false,
   "latitude": "5.000",
   "longitude": "10.000",
   "inventory": {
      "water": 2,
      "food": 1,
      "medication": 3,
      "ammunition": 1
   }
}
```

#### <a id="updatesurvivor"></a> Atualiza o local de um Sobrevivente
*URL:* `/survivors/:pk/`<br>
*Method:* `PATCH`
*Body:*
```json
{
   "latitude": 5,
   "longitude": 150
}
```
#### Response
*Status code*: `200 OK`
```json
{
   "latitude": "5.000",
   "longitude": "150.000"
}
```

#### <a id="infected"></a> Informa sobre uma nova infecção
*URL:* `/report-contamination/`<br>
*Method:* `POST`
*Body:*
```json
{
   "informant": 1, 
   "infected":  1
}
```

- **informant:** Survivor que está informando da contaminação.
- **infected:** O suposto Survivor que está infectado.

#### Response
*Status code*: `200 OK`
```json
{
   "pk": 4,
   "informant": 1,
   "infected": 4,
   "date_report": "2022-08-07T18:59:01.684164Z"
}
```
#### <a id="trade"></a> Realiza a troca de itens entre os Sobreviventes
*URL:* `/trades/`<br>
*Method:* `POST`
*Body:*
```json
{
   "survivor_seller": 2,
   "survivor_buyer": 3,
   "sends": {
      "water": 1
   },
   "pickup": {
      "food": 1,
      "ammunition": 1
   }
}
```

- **survivor_seller:** Survivor que esta oferecendo os itens.
- **sends:** Os itens que estão sendo oferecidos para o 'survivor_buyer'.
- **survivor_buyer:** O Survivor que está comprando os itens.
- **pickup:** Os itens que estão sendo oferecido para o 'survivor_seller'.


#### Response
*Status code*: `200 OK`
```json
{
   "survivor_seller": 2,
   "survivor_buyer": 3,
   "sends": {
      "water": 1
   },
   "pickup": {
     "food": 1,
     "ammunition": 1
   }
}
```

#### <a id="reportinfected"></a> Porcentagem de sobreviventes infectados
*URL:* `/reports/infected/`<br>
*Method:* `GET`

#### Response
*Status code*: `200 OK`
```json
{
   "infected": 1,
   "percentage": "12.5"
}
```

#### <a id="reportuninfected"></a> Porcentagem de sobreviventes não infectados
*URL:* `/reports/uninfected/`<br>
*Method:* `GET`

#### Response
*Status code*: `200 OK`
```json
{
   "uninfected": 7,
   "percentage": 87.5
}
```

#### <a id="reportavg"></a> Média de recurso por sobrevivente
*URL:* `/reports/avg-resources/`<br>
*Method:* `GET`

#### Response
*Status code*: `200 OK`
```json
{
   "avg_water": 1.75,
   "avg_food": 1.25,
   "avg_medication": 3.0,
   "avg_ammunition": 1.0
}
```

#### <a id="reportlost"></a> Pontos perdidos por causa do sobrevivente infectado
*URL:* `/reports/lost-points/`<br>
*Method:* `GET`

#### Response
*Status code*: `200 OK`
```json
{
   "lost_points": 6
}
```

## Itens Comerciais
| Item       | Pontos |
|------------|--------|
| WATER      | 4      |
| FOOD       | 3      |
| MEDICATION | 2      |
| AMMUNITION | 1      |

A comercialização dos itens deve respeitar a tabela de preços abaixo, onde o valor de um item é descrito em termos de pontos. Ambos os lados do comércio devem oferecer a mesma quantidade de pontos. Por exemplo, 1 água e 1 medicamento (1 x 4 + 1 x 2) valem 6 munições (6 x 1) ou 2 itens alimentares (2 x 3).

## Diagrama Entidade Relacionamento - DER
Representação da estrutura do banco de dados utilizada no projeto.

![ZSSN DATABASE](https://user-images.githubusercontent.com/58706567/183316413-de30da7f-a92f-46cb-8767-56e9442ad621.png)
