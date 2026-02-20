"""
Configurações e dados base da calculadora de mão-de-obra
"""

# Horas mensais por escala
HORAS_MENSAIS = {
    "05x02": 176,
    "06x01": 176,
    "12h_diurna": 365,
    "12h_noturna": 365,
    "24h": 730
}

# Número de funcionários por escala (POSTO)
NUM_FUNCIONARIOS = {
    "05x02": 1,
    "06x01": 1,
    "12h_diurna": 2,
    "12h_noturna": 2,
    "24h": 4
}

# Nomes amigáveis das escalas
ESCALAS_NOMES = {
    "05x02": "05x02",
    "06x01": "06x01",
    "12h_diurna": "12h Diurna",
    "12h_noturna": "12h Noturna",
    "24h": "24h"
}

# Encargos trabalhistas (%)
ENCARGOS = {
    "inss_patronal": 0.20,
    "inss_rat": 0.015,
    "inss_terceiros": 0.058,
    "fgts": 0.08,
    "grrf": 0.40  # 40% sobre FGTS
}

# Provisionamento
PROVISIONAMENTO = {
    "decimo_terceiro": 1/12,
    "ferias": 1/3,  # 1/3 sobre 13º
    "ausencias_legais": 0.012
}

# Tributos federais (%)
TRIBUTOS = {
    "iss": 0.05,
    "cofins": 0.076,
    "pis": 0.0165,
    "ir_lucro": 0.25,
    "csll_lucro": 0.09
}

# Descontos dos funcionários
DESCONTOS = {
    "vale_transporte": 0.06,
    "vale_refeicao": 0.20
}

# Dias de benefícios
DIAS_BENEFICIOS = {
    "vale_transporte": 31,
    "vale_refeicao": 31
}

# Cenários de negociação (desp_admin%, lucro_liquido%)
CENARIOS = {
    "10+5": {"desp_admin": 0.10, "lucro_liquido": 0.05},
    "5+5": {"desp_admin": 0.05, "lucro_liquido": 0.05},
    "5+3": {"desp_admin": 0.05, "lucro_liquido": 0.03},
    "3+3": {"desp_admin": 0.03, "lucro_liquido": 0.03}
}

# Dados de Portaria por estado
DADOS_PORTARIA = {
    "SP": {
        "12h_diurna": {
            "salario_bruto": 2162.60,
            "adicional_noturno": 0,
            "beneficios": {
                "vale_transporte_dia": 17.10,
                "vale_refeicao_dia": 21.80,
                "cesta_basica": 151.91,
                "ppr": 356.39,
                "auxilio_saude": 37.09
            },
            "beneficio_social_sindical": 16.75,
            "br_med": 9.70,
            "uniformes": 630,
            "celular_base": 1000,
            "celular_fixo": 29.90,
            "cesta_basica_ii": 315
        },
        "12h_noturna": {
            "salario_bruto": 2162.60,
            "adicional_noturno": 0.20,
            "beneficios": {
                "vale_transporte_dia": 17.10,
                "vale_refeicao_dia": 21.80,
                "cesta_basica": 151.91,
                "ppr": 356.39,
                "auxilio_saude": 37.09
            },
            "beneficio_social_sindical": 16.75,
            "br_med": 9.70,
            "uniformes": 630,
            "celular_base": 1000,
            "celular_fixo": 29.90,
            "cesta_basica_ii": 315
        },
        "24h": {
            "salario_bruto": 2162.60,
            "adicional_noturno": 0.20,
            "beneficios": {
                "vale_transporte_dia": 17.10,
                "vale_refeicao_dia": 21.80,
                "cesta_basica": 151.91,
                "ppr": 356.39,
                "auxilio_saude": 37.09
            },
            "beneficio_social_sindical": 16.75,
            "br_med": 9.70,
            "uniformes": 630,
            "celular_base": 1000,
            "celular_fixo": 29.90,
            "cesta_basica_ii": 315
        },
        "05x02": {
            "salario_bruto": 2162.60,
            "adicional_noturno": 0,
            "beneficios": {
                "vale_transporte_dia": 17.10,
                "vale_refeicao_dia": 21.80,
                "cesta_basica": 151.91,
                "ppr": 356.39,
                "auxilio_saude": 37.09
            },
            "beneficio_social_sindical": 16.75,
            "br_med": 9.70,
            "uniformes": 630,
            "celular_base": 1000,
            "celular_fixo": 29.90,
            "cesta_basica_ii": 315
        },
        "06x01": {
            "salario_bruto": 2162.60,
            "adicional_noturno": 0,
            "beneficios": {
                "vale_transporte_dia": 17.10,
                "vale_refeicao_dia": 21.80,
                "cesta_basica": 151.91,
                "ppr": 356.39,
                "auxilio_saude": 37.09
            },
            "beneficio_social_sindical": 16.75,
            "br_med": 9.70,
            "uniformes": 630,
            "celular_base": 1000,
            "celular_fixo": 29.90,
            "cesta_basica_ii": 315
        }
    },
    "RJ": {
        "12h_diurna": {
            "salario_bruto": 1917.71,
            "adicional_noturno": 0,
            "beneficios": {
                "vale_transporte_dia": 17.10,
                "vale_refeicao_dia": 21.80,
                "cesta_basica": 151.91,
                "ppr": 356.39,
                "auxilio_saude": 37.09
            },
            "beneficio_social_sindical": 16.75,
            "br_med": 9.70,
            "uniformes": 630,
            "celular_base": 1000,
            "celular_fixo": 29.90,
            "cesta_basica_ii": 315
        },
        "12h_noturna": {
            "salario_bruto": 1917.71,
            "adicional_noturno": 0.20,
            "beneficios": {
                "vale_transporte_dia": 17.10,
                "vale_refeicao_dia": 21.80,
                "cesta_basica": 151.91,
                "ppr": 356.39,
                "auxilio_saude": 37.09
            },
            "beneficio_social_sindical": 16.75,
            "br_med": 9.70,
            "uniformes": 630,
            "celular_base": 1000,
            "celular_fixo": 29.90,
            "cesta_basica_ii": 315
        },
        "24h": {
            "salario_bruto": 1917.71,
            "adicional_noturno": 0.20,
            "beneficios": {
                "vale_transporte_dia": 17.10,
                "vale_refeicao_dia": 21.80,
                "cesta_basica": 151.91,
                "ppr": 356.39,
                "auxilio_saude": 37.09
            },
            "beneficio_social_sindical": 16.75,
            "br_med": 9.70,
            "uniformes": 630,
            "celular_base": 1000,
            "celular_fixo": 29.90,
            "cesta_basica_ii": 315
        },
        "05x02": {
            "salario_bruto": 1917.71,
            "adicional_noturno": 0,
            "beneficios": {
                "vale_transporte_dia": 17.10,
                "vale_refeicao_dia": 21.80,
                "cesta_basica": 151.91,
                "ppr": 356.39,
                "auxilio_saude": 37.09
            },
            "beneficio_social_sindical": 16.75,
            "br_med": 9.70,
            "uniformes": 630,
            "celular_base": 1000,
            "celular_fixo": 29.90,
            "cesta_basica_ii": 315
        },
        "06x01": {
            "salario_bruto": 1917.71,
            "adicional_noturno": 0,
            "beneficios": {
                "vale_transporte_dia": 17.10,
                "vale_refeicao_dia": 21.80,
                "cesta_basica": 151.91,
                "ppr": 356.39,
                "auxilio_saude": 37.09
            },
            "beneficio_social_sindical": 16.75,
            "br_med": 9.70,
            "uniformes": 630,
            "celular_base": 1000,
            "celular_fixo": 29.90,
            "cesta_basica_ii": 315
        }
    }
}
