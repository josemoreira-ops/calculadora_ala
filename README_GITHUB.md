# 💼 Calculadora de Precificação de Mão-de-Obra

Sistema web para cálculo automatizado de custos e cenários de negociação para serviços de terceirização de mão-de-obra.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

## 🎯 Funcionalidades

- ✅ **Cálculo automático** de custos baseado em CCT
- ✅ **4 cenários de negociação** pré-configurados
- ✅ Suporte para **5 escalas de trabalho**
- ✅ **Salário personalizado** ou da CCT
- ✅ **Provisão de dissídio** ajustável (0-20%)
- ✅ Interface **moderna e intuitiva**
- ✅ Estrutura **modular** para fácil expansão

## 📊 Escalas Suportadas

| Escala | Horas/Mês | Funcionários |
|--------|-----------|--------------|
| 05x02  | 176h      | 1            |
| 06x01  | 176h      | 1            |
| 12h Diurna | 365h  | 2            |
| 12h Noturna | 365h | 2            |
| 24h    | 730h      | 4            |

## 🚀 Como Usar Localmente

### Requisitos
- Python 3.8+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/calculadora-precificacao.git
cd calculadora-precificacao

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run app.py
```

A aplicação abrirá automaticamente em `http://localhost:8501`

## 💡 Como Funciona

### Estrutura de Custos

O sistema calcula o custo total através de 5 montantes:

1. **Montante A - Folha**: Salários + encargos trabalhistas
2. **Montante B - Provisionamento**: 13º, férias, ausências
3. **Montante C - Benefícios**: VT, VR, cesta básica, PPR, auxílio saúde
4. **Montante D - Coberturas**: Diluição de coberturas de férias
5. **Montante E - Despesas Gerais**: Uniformes, celular, cesta básica II

### Cenários de Negociação

| Cenário | Desp. Admin | Lucro Líquido | Perfil |
|---------|-------------|---------------|--------|
| **10+5** | 10% | 5% | Conservador |
| **5+5**  | 5%  | 5% | Balanceado |
| **5+3**  | 5%  | 3% | Competitivo |
| **3+3**  | 3%  | 3% | Agressivo |

## 📁 Estrutura do Projeto

```
calculadora-precificacao/
├── app.py                      # Interface web (Streamlit)
├── calculos.py                 # Lógica de cálculo
├── config.py                   # Dados de CCT e configurações
├── requirements.txt            # Dependências Python
├── test_calculadora.py         # Testes automatizados
├── README.md                   # Este arquivo
└── EXEMPLO_NOVA_PROFISSAO.py   # Tutorial para expansão
```

## 🔧 Adicionar Novas Profissões

Consulte o arquivo `EXEMPLO_NOVA_PROFISSAO.py` para um tutorial completo de como adicionar novas profissões ao sistema.

## 📝 Licença

Este projeto é de uso interno.

## 👥 Contribuindo

Para sugestões ou melhorias, abra uma issue ou entre em contato com o departamento responsável.

---

**Versão:** 1.1  
**Última atualização:** Fevereiro 2026
