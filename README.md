# Sertão Autopeças — Sistema de E-commerce

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.3-black)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

Plataforma de e-commerce para venda de peças automotivas, desenvolvida com Flask (Python).  
O sistema suporta dois perfis de usuário: **Cliente** e **Administrador**, cada um com funcionalidades específicas.

---

## 🚀 Tecnologias utilizadas

- Python 3.11 + Flask
- SQLAlchemy + SQLite
- Flask-Login (autenticação)
- Jinja2 (templates HTML)
- HTML, CSS e JavaScript

---

## 📦 Pré-requisitos

- Python 3.11+

---

## ⚙️ Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/Odyjmm/sertao-autopecas.git
cd sertao-autopecas
```

### 2. Crie e ative o ambiente virtual

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Popule o banco de dados

```bash
python seed.py
```

### 5. Rode o projeto

```bash
python run.py
```

O servidor estará disponível em `http://localhost:5000`

---

## 🔑 Credenciais de teste

| Perfil | Email | Senha |
|---|---|---|
| Administrador | admin@sistema.com | admin123 |
| Cliente | joao.silva@email.com | cliente123 |
| Cliente | maria.o@email.com | cliente123 |
| Cliente | ricardo.auto@email.com | cliente123 |

---

## 🧩 Funcionalidades

### 👤 Cliente
- Cadastro com nome, email, senha e endereço de entrega
- Login e logout com sessão segura
- Catálogo de peças disponíveis com busca por nome, código ou categoria
- Autocomplete na barra de busca
- Página de detalhes de cada produto com imagem
- Carrinho de compras com seletor de quantidade
- Finalização de compra com geração automática de número de pedido
- Acompanhamento de pedidos com status atualizado
- Solicitação de devolução com geração de protocolo
- Aceite de Termos de Uso (LGPD) no cadastro

### 🛠️ Administrador
- Painel administrativo exclusivo
- Visualização do inventário completo incluindo produtos sem estoque
- Cadastro, edição e remoção de produtos com upload de imagem
- Histórico de todos os pedidos realizados na plataforma
- Listagem de clientes com total de pedidos e tempo de cadastro
- Visualização de pedidos por cliente
- Gerenciamento de solicitações de devolução com aprovação ou rejeição
- Atualização automática do estoque após aprovação de devolução

### ⚙️ Sistema
- Controle de acesso por perfil — clientes e administradores acessam apenas suas áreas
- Atualização automática do estoque após cada compra
- Geração de número único de pedido
- Proteção de rotas para usuários não autenticados
- Senhas armazenadas com hash BCrypt

---

## 🗂️ Estrutura do projeto

```text
sertao-autopecas/
├── app/
│   ├── __init__.py         ← inicializa a aplicação
│   ├── models.py           ← modelos do banco de dados
│   ├── routes/
│   │   ├── auth.py         ← login, cadastro e logout
│   │   ├── loja.py         ← catálogo e busca
│   │   ├── carrinho.py     ← carrinho de compras
│   │   ├── pedido.py       ← finalização e acompanhamento
│   │   ├── devolucao.py    ← solicitação de devolução
│   │   └── admin.py        ← painel administrativo
│   ├── static/
│   │   ├── css/            ← estilos
│   │   ├── js/             ← scripts
│   │   └── uploads/        ← imagens dos produtos
│   └── templates/
│       ├── base.html       ← template base
│       ├── login.html
│       ├── cadastro.html
│       ├── termos.html
│       ├── carrinho.html
│       ├── loja/
│       ├── pedido/
│       ├── devolucao/
│       └── admin/
├── instance/
│   └── banco.db            ← banco SQLite
├── seed.py                 ← popula o banco com dados iniciais
├── run.py                  ← inicia o servidor
└── requirements.txt
```
