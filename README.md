# 🏦 Sistema Bancário em Python 💰

Este é um sistema bancário simples implementado em Python que permite realizar operações básicas como:

* 🧑‍🤝‍🧑 Criar clientes
* 💳 Criar contas correntes
* 📥 Realizar depósitos
* 📤 Realizar saques
* 🧾 Exibir extrato

## 💻 Implementação

O sistema é construído com conceitos de programação orientada a objetos, com classes que representam os diferentes elementos do sistema:

**👤 Clientes:**

* Representados pela classe `Cliente` e sua especialização `PessoaFisica`.
* Armazenam informações como nome, CPF, data de nascimento, endereço e suas contas bancárias.

**💳 Contas:**

* Representadas pela classe `ContaCorrente`.
* Armazenam informações como número da conta, agência, saldo, cliente titular e histórico de transações.
* Implementam as operações de depósito e saque, com regras específicas como limites de saque e saldo.

**💸 Transações:**

* Representadas pelas classes `Deposito` e `Saque`.
* Implementam a lógica de cada tipo de transação e registram as informações no histórico da conta.

**📜 Histórico:**

* Representado pela classe `Historico`.
* Armazena as transações realizadas na conta, permitindo a geração de extratos.

## ✨ Funcionalidades adicionais:

* 🪵 O sistema implementa um sistema de log que registra todas as operações realizadas, incluindo data, hora, função executada, argumentos e resultado.
* 🧭 Um menu interativo permite ao usuário navegar pelas funcionalidades do sistema.

## 🚀 Como usar

1. ⬇️ Clone o repositório do GitHub.
2. ▶️ Execute o arquivo `main.py`.
3. 🧭 Siga as instruções do menu interativo para realizar as operações desejadas.

## ⚠️ Observações

* Este sistema é uma implementação básica para fins educacionais e não se destina ao uso em produção.
* 🏗️ O código pode ser estendido e melhorado para incluir funcionalidades mais avançadas, como transferências entre contas, empréstimos, investimentos, etc.

## 🙌 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um pull request com suas sugestões de melhorias ou novas funcionalidades.