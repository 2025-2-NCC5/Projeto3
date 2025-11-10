#!/bin/sh
set -e

host="$1"
shift
cmd="$@"

# O MySQL roda na porta 3306
port="3306" 

# Tenta conectar na porta TCP 3306 (Sem verificar credenciais!)
until mysql -h "$host" -u"$ROOT_USER" -p"$ROOT_PASSWORD" --skip-ssl -e "SELECT 1" >/dev/null 2>&1; do
  echo "Aguardando o banco de dados em $host ficar disponível..."
  sleep 3
done

echo "Banco de dados disponível, iniciando aplicação..."
exec $cmd