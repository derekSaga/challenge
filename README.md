
# Projeto FastAPI com Autenticação JWT

Este projeto é uma API desenvolvida em Python usando FastAPI, com autenticação JWT e rotas protegidas por papéis de usuário (`user` e `admin`). A autenticação é realizada por meio de um token JWT, gerado na rota `/token`, e as rotas protegidas requerem esse token para acesso.

## Funcionalidades

- **Autenticação JWT:** O token é gerado na rota `/token` ao fornecer credenciais corretas e deve ser usado no cabeçalho de autorização para acessar as rotas protegidas.
- **Rotas protegidas:**
  - `/user`: Acessível apenas por usuários com o papel `user`.
  - `/admin`: Acessível apenas por usuários com o papel `admin`.
  
## Usuários fictícios

Os usuários abaixo são usados para testes locais:

```python
fake_users_db = {
    "user": {"username": "user", "role": "user", "password": "L0XuwPOdS5U"},
    "admin": {"username": "admin", "role": "admin", "password": "JKSipm0YH"},
}
```

## Requisitos

- **Docker** e **Docker Compose** instalados na máquina.

## Configuração do Ambiente

### Passos para rodar o projeto localmente

1. Clone este repositório:

   ```bash
   git clone https://github.com/derekSaga/challenge.git
   cd challenge
   ```

2. Configure o arquivo `.env` (se necessário).

3. Execute o Docker Compose para subir os containers:

   ```bash
   docker-compose up --build
   ```

   Isso irá iniciar o serviço da API junto com todos os containers necessários.

4. Acesse a documentação interativa da API (Swagger) no navegador:

   ```
   http://localhost:8000/docs
   ```

### Testando o Sistema

Você pode testar as seguintes rotas:

- **Geração de Token:**  
  Faça uma requisição POST para a rota `/token` com as credenciais de um dos usuários fictícios (exemplo: `user` ou `admin`).
  
  **Exemplo de payload:**
  
  ```json
  {
      "username": "user",
      "password": "L0XuwPOdS5U"
  }
  ```

- **Acesso às rotas protegidas:**  
  Use o token gerado para acessar as rotas `/user` ou `/admin`, dependendo do papel do usuário. O token deve ser enviado no cabeçalho `Authorization` como:

  ```
  Authorization: Bearer <token>
  ```
