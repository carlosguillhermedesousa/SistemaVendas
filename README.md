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
