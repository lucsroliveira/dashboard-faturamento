import streamlit as st
import pandas as pd
import plotly.express as px


st.markdown("""
    <style>
        .big-font {
            font-size: 28px !important;
        }
        .centered {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font centered">💰 Faturamento Total por Ano</p>', unsafe_allow_html=True)

df = pd.read_excel("FaturamentoMensal.xlsx")

st.set_page_config(page_title="Dashboard Faturamento", layout="wide")
#titulo
st.title("Dashboard de Faturamento Comparativo (2022–2025)")


# Transformar de wide para long (melt)
df_long = df.melt(id_vars=["Mês"], var_name="Ano", value_name="Faturamento")

# Ordenação dos meses
meses_ordem = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
df_long["Mês"] = pd.Categorical(df_long["Mês"], categories=meses_ordem, ordered=True)
df_long = df_long.sort_values(["Ano", "Mês"])

# Garantir que ano seja string (evita problemas em gráficos)
df_long["Ano"] = df_long["Ano"].astype(str)

# Faturamento total por ano
st.subheader("📊 Faturamento Total por Ano")
total_ano = df_long.groupby("Ano")["Faturamento"].sum().reset_index()
fig_total = px.bar(total_ano, x="Ano", y="Faturamento", text="Faturamento", color="Ano")
st.plotly_chart(fig_total, use_container_width=True)

# Comparação mensal por ano
st.subheader("📆 Comparativo Mensal por Ano")
fig_linha = px.line(df_long, x="Mês", y="Faturamento", color="Ano", markers=True)
st.plotly_chart(fig_linha, use_container_width=True)

# Tabela de dados
with st.expander("📄 Ver Tabela de Dados"):
    st.dataframe(df)

    # Seletor de mês para comparação entre anos
st.subheader("📅 Comparação de um Mês em Todos os Anos")
mes_escolhido = st.selectbox("Selecione o mês para comparar:", meses_ordem)

# Filtra os dados do mês escolhido
df_mes = df_long[df_long["Mês"] == mes_escolhido]

# Gráfico de barras para o mês escolhido
fig_mes = px.bar(df_mes, x="Ano", y="Faturamento", color="Ano",
                 text="Faturamento", title=f"Faturamento em {mes_escolhido} (por Ano)")
st.plotly_chart(fig_mes, use_container_width=True)



#Faturamento total por Ano