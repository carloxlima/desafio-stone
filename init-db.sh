#!/bin/bash

# Espera o Postgres ficar pronto
echo "Aguardando o Postgres iniciar..."
sleep 20

# Verifica se o banco de dados 'dbteste' existe
echo "Verificando se o banco de dados 'dbteste' existe..."
PGPASSWORD=postgres psql -h postgres -U postgres -d postgres -c "SELECT 1 FROM pg_database WHERE datname = 'dbpedrapagamentos';" | grep -q 1 || \
PGPASSWORD=postgres psql -h postgres -U postgres -d postgres -c "CREATE DATABASE dbpedrapagamentos;"

echo "Banco de dados 'dbteste' criado com sucesso ou já existe!"