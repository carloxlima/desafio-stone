import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import plotly.express as px
from queries.metrics import *


COR_TEMA = "#0fa458"  # cor principal

st.set_page_config(page_title="Dashboard Técnico", layout="wide")
st.title("Dashboard de Atendimento Técnico")

sla_tecnicos = get_sla_tecnicos()
sla_bases = get_sla_bases()
produtividade = get_produtividade()
cancelamentos = get_motivos_cancelamento()
cobertura = get_cobertura_geografica()
distribuicao = get_distribuicao_terminais()
estados = get_atendimentos_por_estado()

col1, col2 = st.columns(2)
col1.plotly_chart(px.bar(sla_tecnicos, x="tecnico", y="sla_percent",
                  title="SLA por Técnico", color_discrete_sequence=[COR_TEMA],         hover_data={
                      "sla_percent": True,
                      "total_atendimentos": True,
                      "atendimentos_no_prazo": True
                  }), use_container_width=True)
col2.plotly_chart(px.bar(sla_bases, x="base", y="sla_percent",
                  title="SLA por Base", color_discrete_sequence=[COR_TEMA], hover_data={
                      "sla_percent": True,
                      "total_atendimentos": True,
                      "atendimentos_no_prazo": True
                  }), use_container_width=True)

col3, col4 = st.columns(2)
col3.plotly_chart(px.bar(produtividade, x="tecnico", y="produtividade_diaria",
                  title="Produtividade por Técnico", color_discrete_sequence=[COR_TEMA], hover_data={
                      "produtividade_diaria": True,
                      "total_atendimentos": True,
                      "dias_uteis": True
                  }), use_container_width=True)
col4.plotly_chart(px.pie(cancelamentos, names="motivo_cancelamento", values="total",
                  title="Top 5 Motivos de Cancelamento"), use_container_width=True)

col5, col6 = st.columns(2)
# col5.plotly_chart(px.bar(cobertura, x="email", y="cidades_atendidas",
#                   title="Cobertura Geográfica por Técnico", color_discrete_sequence=[COR_TEMA]), use_container_width=True)
col6.plotly_chart(px.sunburst(distribuicao, path=[
                  'type', 'model'], values='total_usos', title="Distribuição de Terminais"), use_container_width=True)

col5.plotly_chart(px.bar(estados, x="country_state", y="qtd_orders",
                         title="Atendimentos por Estado", color_discrete_sequence=[COR_TEMA]), use_container_width=True)

# st.plotly_chart(px.bar(estados, x="country_state", y="qtd_orders",
#                 title="Atendimentos por Estado", color_discrete_sequence=[COR_TEMA]), use_container_width=True)
