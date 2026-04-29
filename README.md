<<<<<<< HEAD
# Sistema de Gestão de Vendas e Controle de Estoque - EletroTech Distribuidora

Sistema completo de PDV (Ponto de Venda) profissional com controle de estoque, cadastro avançado de clientes e produtos, múltiplas formas de pagamento e geração de QR Code PIX.

## 🚀 Funcionalidades Principais

### 📦 Controle de Estoque Completo
- Entrada manual de produtos
- Saída manual com motivo
- Log completo de todos os movimentos
- Alertas visuais de estoque baixo
- Controle rigoroso de quantidades

### 👥 Cadastro Avançado de Clientes
- CPF/CNPJ com validação real
- Telefone e endereço completo
- Status ativo/inativo
- Histórico das últimas 5 compras
- Busca dinâmica (autocomplete)

### 📦 Cadastro Profissional de Produtos
- Código de barras único
- Descrição, marca, categoria
- Preço de custo e margem automática
- Unidade (UN, CX, KG, etc.)
- Estoque mínimo e atual

### 💳 PDV Completo
- Busca dinâmica de clientes e produtos
- Carrinho com múltiplos itens
- Múltiplas formas de pagamento simultâneas
- Desconto até 5% (livre) ou acima (com senha gerente)
- Geração automática de QR Code PIX
- Comprovante profissional

### 🔍 Buscas Inteligentes
- Substituição completa de listagens por busca dinâmica
- Autocomplete em tempo real
- Resultados instantâneos

### 💰 Formas de Pagamento
- Cadastro de novas formas (Dinheiro, Cartão, PIX, etc.)
- Ativar/desativar formas
- Controle gerencial

## 🛠️ Instalação

1. **Clone ou baixe o projeto**
2. **Instale as dependências:**

```bash
pip install flask bcrypt qrcode[pil]
```

3. **Execute o sistema:**

```bash
python app.py
```

4. **Acesse:** `http://127.0.0.1:5000`

## 👤 Usuário Inicial

- **Usuário:** `admin`
- **Senha:** `admin123`
- **Role:** Gerente

## 📋 Estrutura do Banco

- **users:** Usuários do sistema
- **customers:** Clientes (CPF/CNPJ, telefone, endereço)
- **products:** Produtos (código, descrição, marca, estoque)
- **stock_movements:** Log de entradas/saídas
- **sales:** Vendas realizadas
- **sale_items:** Itens das vendas
- **sale_payments:** Pagamentos das vendas
- **payment_methods:** Formas de pagamento

## 🔒 Regras de Negócio

- **RN01:** Baixa automática do estoque na venda
- **RN02:** Bloqueio de venda sem estoque ou quantidade insuficiente
- **RN03:** Estorno devolve produtos ao estoque e registra motivo
- **Desconto:** >5% exige senha de gerente
- **Cliente inativo:** Bloqueado para compras

## 🎨 Interface

- Design profissional dark theme
- Bootstrap 5 + Font Awesome
- Responsivo para desktop e mobile
- Feedback visual claro (toast notifications)
- Layout consistente em todas as telas

## 📱 Navegação

- **Dashboard:** Visão geral com métricas
- **PDV:** Ponto de venda completo
- **Clientes:** Cadastro e busca
- **Produtos:** Gestão de catálogo
- **Estoque:** Entradas, saídas e movimentos
- **Pagamentos:** Configuração de formas
- **Vendas:** Histórico e comprovantes
- **Usuários:** Controle de acesso

## 🔧 Desenvolvimento

- **Python 3.8+**
- **Flask** (framework web)
- **SQLite** (banco de dados)
- **bcrypt** (hash de senhas)
- **qrcode** (geração PIX)
- **MVC** (Models, Views, Controllers)

## 📊 Dados de Teste

O sistema já vem com:
- 1 usuário gerente
- 1 cliente inicial
- 1 produto inicial
- 200 clientes diversos (dados gerados)
- 100 produtos diversos (dados gerados)
- Formas de pagamento padrão (Dinheiro, Cartão, PIX)

## 🎯 Pronto para Produção

Sistema completo e profissional, pronto para uso em ambiente real de vendas e controle de estoque.

- `app/` - inicialização da aplicação
- `routes/` - rotas Flask organizadas por área
- `models/` - abstração de banco e helpers
- `templates/` - HTML com Bootstrap 5
- `static/` - estilos CSS
- `database/` - schema SQL e script de criação
=======
# 🛒 Projeto Prático – Sistema de Gestão de Vendas e Controle de Estoque

Este repositório contém o desenvolvimento de um **projeto prático aplicado em sala de aula**, voltado para alunos do curso de **Desenvolvimento de Sistemas do SENAI**.

A proposta foi simular um **cenário real de mercado**, onde os alunos atuam como desenvolvedores responsáveis por criar uma solução completa para uma empresa fictícia, a **EletroTech Distribuidora**, que enfrentava problemas no controle manual de vendas e estoque.

---

## 🎯 Objetivo Educacional

Este projeto tem como finalidade desenvolver, na prática, competências técnicas e socioemocionais, tais como:

* Análise de requisitos
* Lógica de programação aplicada
* Desenvolvimento web com Python (Flask)
* Modelagem e manipulação de banco de dados (SQLite)
* Implementação de regras de negócio
* Organização de código e boas práticas
* Resolução de problemas reais

---

## 🧩 Contexto do Projeto

A empresa **EletroTech Distribuidora** realizava o controle de vendas e estoque de forma manual (planilhas e cadernos), o que gerava:

* Vendas de produtos sem estoque
* Falta de controle de mercadorias
* Erros operacionais
* Insatisfação de clientes

Diante disso, os alunos foram desafiados a desenvolver um sistema informatizado que resolvesse esses problemas.

---

## 🚀 Funcionalidades Desenvolvidas

Durante o projeto, os alunos implementaram:

### 🔐 Autenticação de Usuários

* Controle de acesso ao sistema
* Perfis de usuários (vendedor, gerente, etc.)

---

### 👤 Cadastro de Clientes

* Registro completo de dados
* Validação e controle de duplicidade
* Status ativo/inativo
* Histórico de compras

---

### 📦 Cadastro de Produtos

* Controle de estoque
* Precificação automática
* Categorias e organização

---

### 📊 Controle de Estoque

* Entrada e saída de produtos
* Registro de movimentações
* Atualização automática via vendas

---

### 🛒 Módulo de Vendas (PDV)

* Simulação de frente de caixa
* Carrinho de compras
* Aplicação de descontos
* Múltiplas formas de pagamento

---

### 📲 Integração com PIX

* Geração de QR Code para pagamento

---

### 🧾 Emissão de Comprovante

* Simulação de cupom não fiscal

---

## ⚠️ Regras de Negócio Aplicadas

O projeto também exigiu a implementação de regras fundamentais:

* **RN01:** Baixa automática de estoque ao finalizar venda
* **RN02:** Bloqueio de venda sem estoque disponível
* **RN03:** Estorno de vendas com retorno ao estoque

---

## 🧠 Tecnologias Utilizadas

* Python
* Flask
* SQLite
* HTML / CSS
* Bootstrap
* JavaScript

---

## 🎓 Abordagem Pedagógica

Este projeto foi aplicado como atividade prática para:

* Consolidar conhecimentos técnicos
* Simular demandas do mercado de trabalho
* Desenvolver autonomia na construção de sistemas
* Estimular pensamento crítico e resolução de problemas

---

## 📌 Aplicação em Sala de Aula

O projeto pode ser utilizado como:

* Projeto integrador
* Avaliação prática
* Atividade de laboratório
* Base para evolução em projetos mais complexos

---

## 👨‍🏫 Instrutor

Carlos Guilherme
Instrutor de Tecnologia da Informação – SENAI

---

## 📄 Licença

Este projeto possui caráter educacional e pode ser utilizado como base para estudos e aprimoramento técnico.
>>>>>>> dfef5ecb0e008dc2bf9277f789cab8cc0afe9493
