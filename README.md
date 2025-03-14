# Parceiros API

## Descrição

Esta é uma API desenvolvida para gerenciar estabelecimentos parceiros, permitindo o cadastro, consulta por ID e busca do parceiro mais próximo com cobertura na localização do usuário.

Este projeto foi desenvolvido com base no desafio open-source do Zé Delivery, disponível [aqui](https://github.com/ab-inbev-ze-company/ze-code-challenges/blob/master/backend_pt.md).

## Tecnologias Utilizadas

- **FastAPI** - Framework para desenvolvimento da API
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM para interação com o banco de dados
- **Shapely** - Biblioteca para manipulação de dados geoespaciais
- **Haversine** - Cálculo de distância geodésica entre pontos
- **Uvicorn** - Servidor ASGI para execução da API

## Instalação e Configuração

### Requisitos

- Python 3.10+
- PostgreSQL 16.8 instalado e configurado

### Configurar e Executar a API

1. Clone o repositório:
   ```sh
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_REPOSITORIO>
   ```
2. Crie um ambiente virtual e instale as dependências:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
3. Configure as variáveis de ambiente no arquivo `.env` (use como base o arquivo `.env.example`):

4. (Opcional) Para popular o banco de dados com dados fictícios de parceiros, execute o script `populate_db_script.py`:
   ```sh
   python -m app.utils.populate_db_script
   ```
5. Inicie a API:
   ```sh
   uvicorn app.main:app --reload
   ```

A API estará acessível em `http://localhost:8000`.


## Documentação da API

A documentação interativa da API está disponível em:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints Principais

### Criar um parceiro
**POST /partners/create_partner**
- Cadastro de um novo parceiro de negócio
- Corpo da requisição (JSON):
```sh
{
  "id": "1", 
  "tradingName": "Adega da Cerveja - Pinheiros",
  "ownerName": "Zé da Silva",
  "document": "1432132123891/0001",
  "coverageArea": { "type": "MultiPolygon", "coordinates": [[[[-46.5, -23.5], [-46.6, -23.6], [-46.7, -23.7], [-46.5, -23.5]]]] },
  "address": { "type": "Point", "coordinates": [-46.57421, -21.785741] }
}
```

### Buscar parceiro por ID
**GET /partners/fetch_partner/{partner_id}**
- Retorna os detalhes de um parceiro cadastrado

### Buscar parceiro mais próximo
**POST /partners/closest_available_partner**
- Retorna o parceiro mais próximo que cobre a localização informada
```sh
{
    "lon": -43.297338, // float
    "lat": -23.013537 // float
}
```

## Autor

Desenvolvido por Carlos Alberto Siqueri Dias.

