# Desafio Stone — ETL com Apache Airflow

Este projeto tem como objetivo demonstrar a construção de um pipeline de ETL utilizando Apache Airflow com o Astro CLI.

## ✅ Como Executar o Projeto

Siga os passos abaixo para configurar e executar o ambiente.

### 1. Clonando o Repositório

```bash
git clone https://github.com/carloxlima/desafio-stone.git
cd desafio-stone
```

### 2. Instalando o Astro CLI

#### Mac e Linux:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install astro
```

#### Windows:

Instale o WSL (Windows Subsystem for Linux). Em seguida, siga os passos para Mac/Linux dentro do terminal WSL.

### 3. Iniciando o Ambiente

```bash
astro dev start
```

Esse comando criará os containers do Airflow e do banco de dados Postgres, além de instalar as dependências.

---

## 🗄️ Configuração do Banco de Dados

### Cliente (ex: DBeaver):

- Host: `localhost`
- Porta: `5132`
- Usuário: `postgres`
- Senha: `postgres`

Crie a base de dados manualmente:

```sql
CREATE DATABASE dbpedrapagamentos;
```

### Conexão no Airflow:

- Connection Id: `postgres_conn`
- Connection Type: `Postgres`
- Host: `postgres`
- Database: `dbpedrapagamentos`
- Login: `postgres`
- Password: `postgres`
- Port: `5432`

---

## 🧩 DAGs Disponíveis

### 1. `init_create_tables`

Cria as tabelas necessárias no banco.  
**Execute esta DAG primeiro.**

### 2. `dag_etl_pedrapagamento`

DAG principal com 8 tasks:

1. Leitura dos arquivos no bucket.
2. Tratamento dos dados.
3. Carga nas tabelas normalizadas.
4. Armazenamento dos comprovantes.
5. Verificação de logs processados.
6. Extração de dados das tabelas normalizadas.
7. Transformação e carga nas dimensões.
8. Carga na tabela fato.

---

## ✨ Observações

- Utilize o Airflow UI em `http://localhost:8080`
- Todas as DAGs estão no diretório `dags/`
- As conexões e variáveis devem ser configuradas na interface do Airflow

---

## 📬 Contato

Em caso de dúvidas ou sugestões, sinta-se à vontade para abrir uma issue ou entrar em contato.

---