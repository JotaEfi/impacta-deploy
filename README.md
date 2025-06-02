# Documentação das Rotas da API

Este projeto fornece uma API REST para gerenciamento de ONGs, doações, necessidades, posts, FAQs e usuários. Abaixo estão descritas as rotas principais, exemplos de requisições e explicações para facilitar a integração do frontend.

---

## Autenticação e Usuário

- **POST `/api/auth/register/`**
  Cria um novo usuário (doador ou ONG).
  **JSON esperado:**
  ```json
  {
    "email": "usuario@email.com",
    "username": "usuario",
    "password": "SenhaForte123!",
    "password2": "SenhaForte123!",
    "user_type": "DONOR" ou "ONG",
    "ong_name": "Nome da ONG", // obrigatório se user_type for ONG
    "ong_description": "Descrição da ONG",
    "city": "Cidade",
    "state": "UF",
    "address": "Endereço",
    "postal_code": "00000-000",
    "first_name": "Nome",
    "last_name": "Sobrenome"
  }
  ```

- **POST `/api/auth/login/`**
  Retorna o token JWT para autenticação.
  **JSON esperado:**
  ```json
  {
    "username": "usuario",
    "password": "SenhaForte123!"
  }
  ```

- **GET `/api/auth/status/`**
  Retorna informações do usuário autenticado.

- **GET `/api/auth/profile/`**
  Perfil do usuário autenticado.

- **POST `/api/auth/change-password/`**
  Troca de senha.
  **JSON esperado:**
  ```json
  {
    "old_password": "SenhaAntiga",
    "new_password": "SenhaNova123!",
    "new_password2": "SenhaNova123!"
  }
  ```

- **GET `/api/auth/ongs/`**
  Lista todas as ONGs.

- **GET `/api/auth/ongs/<id>/`**
  Detalhes de uma ONG específica.

---

## Posts

- **GET `/api/posts/`**
  Lista todos os posts.

- **POST `/api/posts/`**
  Cria um post (apenas ONGs autenticadas).
  **JSON esperado:**
  ```json
  {
    "title": "Título do post",
    "content": "Conteúdo do post",
    "image": "url_ou_base64"
  }
  ```

---

## FAQs

- **GET `/api/faqs/`**
  Lista todas as perguntas frequentes.

- **POST `/api/faqs/`**
  Doadores podem enviar perguntas para ONGs.
  **JSON esperado:**
  ```json
  {
    "question": "Qual a missão da ONG?",
    "org_user": 1
  }
  ```

- **PATCH `/api/faqs/<id>/`**
  ONGs podem responder perguntas.
  **JSON esperado:**
  ```json
  {
    "answer": "Nossa missão é ajudar crianças."
  }
  ```

---

## Necessidades

- **GET `/api/necessities/`**
  Lista necessidades das ONGs.

- **POST `/api/necessities/`**
  ONGs cadastram necessidades.
  **JSON esperado:**
  ```json
  {
    "item": 1,
    "quantity": 10,
    "urgency": "ALTA",
    "status": "ABERTA"
  }
  ```

---

## Doações

- **GET `/api/donations/`**
  Lista doações.

- **POST `/api/donations/`**
  Realiza uma doação.
  **JSON esperado:**
  ```json
  {
    "org": 1,
    "item_id": 1,
    "donor": 2
  }
  ```

---

## Relatórios de Doação

- **GET `/api/donation-reports/`**
  Lista relatórios de doação.

- **POST `/api/donation-reports/`**
  Cria um relatório de doação.
  **JSON esperado:**
  ```json
  {
    "donation": 1,
    "confirmed": true,
    "message": "Recebido com sucesso"
  }
  ```

---

## Prestação de Contas

- **GET `/api/accountability/`**
  Lista prestações de contas.

- **POST `/api/accountability/`**
  ONG cadastra prestação de contas.
  **JSON esperado:**
  ```json
  {
    "org": 1,
    "title": "Prestação de contas de maio",
    "description": "Descrição detalhada",
    "image": "url_ou_base64"
  }
  ```

---

## Itens

- **GET `/api/items/`**
  Lista itens disponíveis.

---

## Informações de Pagamento

- **GET `/api/payment-info/`**
  Lista informações de pagamento das ONGs.

- **POST `/api/payment-info/`**
  ONG cadastra informações bancárias.
  **JSON esperado:**
  ```json
  {
    "org": 1,
    "pix_key": "chave-pix",
    "bank": "Banco",
    "agency": "0001",
    "account": "12345-6",
    "qr_code_image": "url_ou_base64"
  }
  ```

---

> Todas as rotas que exigem autenticação devem ser chamadas com o header `Authorization: Bearer <token>`.

---

Dúvidas? Consulte os exemplos acima ou veja os comentários nas rotas dos arquivos `urls.py`.
