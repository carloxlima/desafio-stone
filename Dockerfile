FROM quay.io/astronomer/astro-runtime:12.8.0

# Copiar o script de inicialização para dentro do container
COPY init-db.sh /init-db.sh

# Adicionar a execução do script na inicialização do container
CMD ["/bin/bash", "/init-db.sh"]

