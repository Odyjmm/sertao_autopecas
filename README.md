# Sertão Autopeças - Sistema de E-commerce

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.3-black)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

Plataforma de e-commerce para venda de peças automotivas, desenvolvida com Flask (Python).
O sistema suporta dois perfis de usuário: **Cliente** e **Administrador**, cada um com funcionalidades específicas.

---

## 🚀 Tecnologias utilizadas

- Python 3.11 + Flask 3.1.3
- SQLAlchemy 2.x + SQLite
- Flask-Login
- Flask-WTF 
- python-dotenv
- Jinja2
- HTML
- CSS
- JavaScript
- ngrok <br><br>

---

## 📦 Pré-requisitos Obrigatórios

- Python 3.11+
- Flask 3.1.3
- Git <br><br>

---

## ⚙️ Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/Odyjmm/sertao_autopecas.git
cd sertao_autopecas
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

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo e preencha com os seus valores:

```bash
cp .env.example .env
```

Edite o `.env`:

```env
SECRET_KEY=sua-chave-secreta-longa-e-aleatoria
DATABASE_URL=sqlite:///banco.db
```

Para gerar uma `SECRET_KEY` segura:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

> ⚠️ Nunca commite o arquivo `.env`. Ele já está no `.gitignore`.

### 5. Popule o banco de dados

```bash
python seed.py
```

### 6. Rode o projeto

```bash
python run.py
```

O servidor estará disponível em [http://localhost:5000](http://localhost:5000)

### 7. (Opcional) Expor o servidor com ngrok

O ngrok cria um túnel público para o seu servidor local, permitindo acessar o sistema de outros dispositivos (celular, por exemplo) sem precisar de deploy.

**Instale o ngrok:** [https://ngrok.com/download](https://ngrok.com/download)

Com o servidor Flask rodando (`python run.py`), abra outro terminal e execute:

```bash
ngrok http 5000
```

O ngrok vai exibir uma URL pública no formato `https://xxxx-xx-xx-xx-xx.ngrok-free.app`. Acesse essa URL em qualquer dispositivo na mesma rede ou fora dela.

> ⚠️ Enquanto o túnel estiver ativo, qualquer pessoa com a URL pode acessar o sistema. Encerre o ngrok (`Ctrl+C`) quando não estiver mais usando.

---

## 🔑 Credenciais de teste

| Perfil | Email | Senha |
|---|---|---|
| Administrador | admin@sistema.com | admin123 |
| Cliente | joao.silva@email.com | cliente123 |
| Cliente | maria.o@email.com | cliente123 |
| Cliente | ricardo.auto@email.com | cliente123 |

> ⚠️ Use apenas para testes locais.

<br><br>

---

## 🧩 Funcionalidades

### 👤 Cliente

- Cadastro com nome, e-mail, senha e endereço de entrega
- Login automático após o cadastro
- Login e logout com sessão segura
- Catálogo paginado de peças disponíveis, ordenado por nome
- Busca por nome, código ou categoria com paginação
- Autocomplete na barra de busca (com debounce)
- Página de detalhes de cada produto com imagem
- Carrinho de compras com seletor de quantidade
- Validação de estoque em tempo real ao adicionar ao carrinho e ao finalizar a compra
- Finalização de compra com geração automática de número de pedido
- Acompanhamento de pedidos com status atualizado
- Solicitação de devolução com geração de protocolo
- Aceite de Termos de Uso (LGPD) no cadastro — validado também no servidor

### 🛠️ Administrador

- Painel administrativo exclusivo
- Inventário completo com indicadores visuais de estoque baixo e sem estoque
- Cadastro de produtos com upload de imagem (formatos: JPG, JPEG, PNG, WEBP, GIF)
- Edição e remoção de produtos (remoção bloqueada se o produto tiver histórico de pedidos)
- Histórico de todos os pedidos realizados na plataforma
- Listagem de clientes com total de pedidos e tempo de cadastro
- Visualização de pedidos por cliente
- Gerenciamento de solicitações de devolução com aprovação ou rejeição
- Atualização automática do estoque após aprovação de devolução

### ⚙️ Sistema

- Proteção CSRF em todos os formulários (Flask-WTF)
- Controle de acesso por perfil via decorator `@admin_required`
- Proteção IDOR: clientes só acessam seus próprios pedidos e devoluções
- Validação de estoque no carrinho e no checkout, com abate atômico em transação
- Proteção contra devolução duplicada (uma pendente/aprovada bloqueia nova solicitação)
- Upload de imagem com validação de extensão e nome de arquivo único (UUID)
- Senhas armazenadas com hash BCrypt
- Variáveis sensíveis (`SECRET_KEY`, `DATABASE_URL`) carregadas via `.env`
- Responsividade mobile em todas as telas

---

<br> <br>

## 🗂️ Estrutura do projeto

```text
sertao_autopecas/
├── app/
│   ├── __init__.py           ← inicializa a aplicação (Flask, SQLAlchemy, CSRF, Login)
│   ├── models.py             ← modelos do banco de dados
│   ├── utils.py              ← decorator admin_required, validação de extensão de imagem
│   ├── routes/
│   │   ├── auth.py           ← login, cadastro e logout
│   │   ├── loja.py           ← catálogo, busca e autocomplete
│   │   ├── carrinho.py       ← carrinho de compras
│   │   ├── pedido.py         ← finalização e acompanhamento de pedidos
│   │   ├── devolucao.py      ← solicitação de devolução
│   │   └── admin.py          ← painel administrativo
│   ├── static/
│   │   ├── css/
│   │   │   ├── base.css      ← reset e body
│   │   │   ├── layout.css    ← navbar, container, footer, responsividade
│   │   │   ├── componentes.css ← botões, cards, formulários, mensagens
│   │   │   ├── carrinho.css  ← badge do carrinho e tabela responsiva
│   │   │   ├── utils.css     ← classes utilitárias e grid do produto
│   │   │   └── toast.css     ← notificações flutuantes
│   │   ├── js/
│   │   │   ├── main.js       ← menu hamburger e validação de inputs
│   │   │   ├── carrinho.js   ← fetch para adicionar ao carrinho com feedback
│   │   │   ├── utils.js      ← controle de quantidade e confirmação de remoção
│   │   │   ├── autocomplete.js ← sugestões de busca com debounce
│   │   │   └── senha.js      ← validação de senha e máscara de CEP
│   │   └── uploads/          ← imagens dos produtos
│   └── templates/
│       ├── base.html         ← template base (navbar, flash messages, scripts)
│       ├── login.html
│       ├── cadastro.html
│       ├── termos.html
│       ├── carrinho.html
│       ├── loja/
│       │   ├── catalogo.html
│       │   ├── busca.html
│       │   └── produto_detalhe.html
│       ├── pedido/
│       │   ├── confirmacao.html
│       │   ├── meus_pedidos.html
│       │   └── detalhe.html
│       ├── devolucao/
│       │   └── formulario.html
│       └── admin/
│           ├── inventario.html
│           ├── novo_produto.html
│           ├── editar_produto.html
│           ├── pedidos.html
│           ├── pedidos_cliente.html
│           ├── clientes.html
│           └── devolucoes.html
├── .env.example              ← modelo de configuração local
├── .gitignore
├── seed.py                   ← popula o banco com dados iniciais
├── run.py                    ← inicia o servidor
└── requirements.txt
```
