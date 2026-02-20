"""
Calculadora de Precificação de Mão-de-Obra
Interface Web com Streamlit
"""
import streamlit as st
import pandas as pd
from calculos import CalculadoraPreco
from config import ESCALAS_NOMES, DADOS_PORTARIA

# Configuração da página
st.set_page_config(
    page_title="Calculadora de Precificação",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para design elegante
st.markdown("""
<style>
    /* Fonte principal */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 300;
        color: #2C3E50;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-size: 1rem;
        color: #7F8C8D;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Cards de resultados */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    }
    
    .result-card h3 {
        color: white;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.9;
    }
    
    .result-card .value {
        color: white;
        font-size: 2rem;
        font-weight: 600;
        margin: 0;
    }
    
    .result-card .subtitle {
        color: white;
        font-size: 0.875rem;
        opacity: 0.8;
        margin-top: 0.25rem;
    }
    
    /* Tabela de cenários */
    .scenario-table {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-top: 2rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #F8F9FA;
    }
    
    /* Botão calcular */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 500;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Inputs */
    .stSelectbox, .stNumberInput {
        margin-bottom: 1rem;
    }
    
    /* Remover padding extra */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
    }
    
    /* Tabela customizada */
    .dataframe {
        border: none !important;
    }
    
    .dataframe thead tr th {
        background-color: #F8F9FA !important;
        color: #2C3E50 !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        border: none !important;
        text-align: left !important;
    }
    
    .dataframe tbody tr td {
        padding: 0.875rem 1rem !important;
        border-bottom: 1px solid #E9ECEF !important;
        color: #495057 !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #F8F9FA !important;
    }
    
    /* Métricas */
    div[data-testid="stMetricValue"] {
        font-size: 1.75rem;
        font-weight: 600;
        color: #2C3E50;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: #7F8C8D;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">Calculadora de Precificação</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Cálculo de custos e cenários de negociação para mão-de-obra terceirizada</p>', unsafe_allow_html=True)

# Sidebar - Inputs
with st.sidebar:
    st.markdown("### Configurações")
    
    # Estado
    estado = st.selectbox(
        "Estado",
        options=["SP", "RJ"],
        help="Selecione o estado onde o serviço será prestado"
    )
    
    # Profissão (por enquanto só Portaria)
    profissao = st.selectbox(
        "Profissão",
        options=["Portaria"],
        help="Selecione a profissão"
    )
    
    # Escala
    escala_opcoes = list(ESCALAS_NOMES.keys())
    escala_labels = list(ESCALAS_NOMES.values())
    
    escala = st.selectbox(
        "Escala de Trabalho",
        options=escala_opcoes,
        format_func=lambda x: ESCALAS_NOMES[x],
        help="Selecione a escala de trabalho"
    )
    
    st.markdown("---")
    
    # Salário
    st.markdown("### Salário")
    
    salario_cct = DADOS_PORTARIA[estado][escala]['salario_bruto']
    
    tipo_salario = st.radio(
        "Tipo de Salário",
        options=["cct", "personalizado"],
        format_func=lambda x: "Usar salário da CCT" if x == "cct" else "Salário personalizado",
        help="Escolha se deseja usar o salário da CCT ou informar um valor personalizado"
    )
    
    if tipo_salario == "cct":
        st.info(f"💰 Salário CCT: R$ {salario_cct:,.2f}")
        salario_final = None
    else:
        salario_final = st.number_input(
            "Salário Bruto (R$)",
            min_value=salario_cct,
            value=salario_cct,
            step=10.0,
            help=f"Valor mínimo: R$ {salario_cct:,.2f} (piso da CCT)"
        )
    
    st.markdown("---")
    
    # Provisão de dissídio
    st.markdown("### Provisão de Dissídio")
    provisao_dissidio = st.slider(
        "Percentual de Provisão (%)",
        min_value=0.0,
        max_value=20.0,
        value=0.0,
        step=0.5,
        help="Estimativa de aumento salarial para o próximo ano"
    )
    
    st.markdown("---")
    
    # Botão calcular
    calcular = st.button("🧮 CALCULAR", type="primary")

# Área principal - Resultados
if calcular or 'calculadora' in st.session_state:
    # Criar calculadora
    calc = CalculadoraPreco(
        estado=estado,
        escala=escala,
        provisao_dissidio=provisao_dissidio,
        salario_customizado=salario_final
    )
    
    # Armazenar em session_state
    st.session_state['calculadora'] = calc
    
    # Calcular todos os cenários
    resultados = calc.calcular_todos_cenarios()
    
    # Custo total
    custo_total = resultados['custos']['custo_total']
    
    # Card de custo total
    st.markdown(f"""
    <div class="result-card">
        <h3>Custo Total Mensal</h3>
        <p class="value">R$ {custo_total:,.2f}</p>
        <p class="subtitle">Base para cálculo de todos os cenários</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cenários de negociação
    st.markdown("## 💼 Cenários de Negociação")
    
    # Criar DataFrame para exibição
    cenarios_data = []
    
    for nome in ["10+5", "5+5", "5+3", "3+3"]:
        cenario = resultados['cenarios'][nome]
        cenarios_data.append({
            "Cenário": nome,
            "Faturamento": f"R$ {cenario['faturamento']:,.2f}",
            "Valor H/H": f"R$ {cenario['valor_hh']:.2f}",
            "Desp. Admin (%)": f"{cenario['percentuais']['desp_admin']*100:.0f}%",
            "Desp. Admin (R$)": f"R$ {cenario['despesa_administrativa']:,.2f}",
            "Lucro Líquido (%)": f"{cenario['percentuais']['lucro_liquido']*100:.0f}%",
            "Lucro Líquido (R$)": f"R$ {cenario['lucro_liquido']:,.2f}"
        })
    
    df_cenarios = pd.DataFrame(cenarios_data)
    
    # Exibir tabela
    st.dataframe(
        df_cenarios,
        use_container_width=True,
        hide_index=True
    )
    
    # Detalhamento de um cenário (expansível)
    st.markdown("---")
    st.markdown("## 📊 Detalhamento de Cenário")
    
    cenario_detalhe = st.selectbox(
        "Selecione um cenário para ver detalhes",
        options=["10+5", "5+5", "5+3", "3+3"]
    )
    
    cenario_sel = resultados['cenarios'][cenario_detalhe]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Faturamento", f"R$ {cenario_sel['faturamento']:,.2f}")
    
    with col2:
        st.metric("Receita Líquida", f"R$ {cenario_sel['receita_liquida']:,.2f}")
    
    with col3:
        st.metric("Custo Final", f"R$ {cenario_sel['custo_final']:,.2f}")
    
    with col4:
        st.metric("Lucro Líquido", f"R$ {cenario_sel['lucro_liquido']:,.2f}")
    
    # Composição de custos
    with st.expander("📋 Ver composição detalhada de custos"):
        custos = resultados['custos']
        
        st.markdown("### Montante A - Folha")
        st.write(f"**Total:** R$ {custos['montante_a']['total']:,.2f}")
        st.json(custos['montante_a'])
        
        st.markdown("### Montante B - Provisionamento")
        st.write(f"**Total:** R$ {custos['montante_b']['total']:,.2f}")
        st.json(custos['montante_b'])
        
        st.markdown("### Montante C - Benefícios")
        st.write(f"**Total:** R$ {custos['montante_c']['total']:,.2f}")
        st.json(custos['montante_c'])
        
        st.markdown("### Montante D - Coberturas")
        st.write(f"**Total:** R$ {custos['montante_d']['total']:,.2f}")
        
        st.markdown("### Montante E - Despesas Gerais")
        st.write(f"**Total:** R$ {custos['montante_e']['total']:,.2f}")
        st.json(custos['montante_e'])

else:
    # Tela inicial
    st.info("👈 Configure os parâmetros na barra lateral e clique em **CALCULAR** para gerar os cenários de precificação.")
    
    # Instruções
    with st.expander("📖 Como usar esta calculadora"):
        st.markdown("""
        ### Passo a passo:
        
        1. **Selecione o Estado**: Escolha entre SP ou RJ
        2. **Escolha a Profissão**: Por enquanto, apenas Portaria está disponível
        3. **Defina a Escala**: Selecione a jornada de trabalho (12h, 24h, 05x02, 06x01)
        4. **Configure o Salário**:
           - Use o salário da CCT (padrão)
           - Ou informe um salário personalizado (sempre acima do piso)
        5. **Defina a Provisão de Dissídio**: Percentual estimado de aumento salarial
        6. **Clique em CALCULAR**: Os resultados serão exibidos com 4 cenários de negociação
        
        ### Cenários:
        - **10+5**: 10% Despesa Admin + 5% Lucro Líquido (mais conservador)
        - **5+5**: 5% Despesa Admin + 5% Lucro Líquido (balanceado)
        - **5+3**: 5% Despesa Admin + 3% Lucro Líquido (competitivo)
        - **3+3**: 3% Despesa Admin + 3% Lucro Líquido (mais agressivo)
        """)

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #7F8C8D; font-size: 0.875rem;">Calculadora de Precificação v1.0 | Desenvolvido para otimizar processos comerciais</p>',
    unsafe_allow_html=True
)
