"""
Módulo de cálculos para precificação de mão-de-obra
"""
from config import (
    HORAS_MENSAIS, NUM_FUNCIONARIOS, ENCARGOS, PROVISIONAMENTO, TRIBUTOS, 
    DESCONTOS, DIAS_BENEFICIOS, CENARIOS, DADOS_PORTARIA
)


class CalculadoraPreco:
    """Calculadora de precificação de mão-de-obra"""
    
    def __init__(self, estado, escala, provisao_dissidio=0, salario_customizado=None):
        """
        Inicializa a calculadora
        
        Args:
            estado: 'SP' ou 'RJ'
            escala: '12h_diurna', '12h_noturna', '24h', '05x02', '06x01'
            provisao_dissidio: % de provisão (0-100)
            salario_customizado: Salário customizado (opcional)
        """
        self.estado = estado
        self.escala = escala
        self.provisao_dissidio = provisao_dissidio / 100  # converter para decimal
        self.dados = DADOS_PORTARIA[estado][escala].copy()
        
        # Se salário customizado, substituir
        if salario_customizado:
            self.dados['salario_bruto'] = salario_customizado
        
        self.horas_mensais = HORAS_MENSAIS[escala]
        self.num_funcionarios = NUM_FUNCIONARIOS[escala]  # CORRIGIDO: número varia por escala
    
    def calcular_montante_a_folha(self):
        """Calcula MONTANTE A - FOLHA"""
        salario = self.dados['salario_bruto'] * self.num_funcionarios
        salario_com_dissidio = salario * (1 + self.provisao_dissidio)
        
        # Adicional noturno (se aplicável)
        adicional_noturno = 0
        if self.dados['adicional_noturno'] > 0:
            adicional_noturno = (self.dados['salario_bruto'] / 220) * self.dados['adicional_noturno'] * 248
            adicional_noturno_com_dissidio = adicional_noturno * (1 + self.provisao_dissidio)
        else:
            adicional_noturno_com_dissidio = 0
        
        # Base para encargos
        base_encargos = salario_com_dissidio + adicional_noturno_com_dissidio
        
        # Encargos
        inss_patronal = base_encargos * ENCARGOS['inss_patronal']
        inss_rat = base_encargos * ENCARGOS['inss_rat']
        inss_terceiros = base_encargos * ENCARGOS['inss_terceiros']
        fgts = base_encargos * ENCARGOS['fgts']
        
        # Benefícios fixos
        beneficio_social = self.dados['beneficio_social_sindical'] * self.num_funcionarios
        beneficio_social_com_dissidio = beneficio_social * (1 + self.provisao_dissidio)
        
        br_med = self.dados['br_med'] * self.num_funcionarios
        br_med_com_dissidio = br_med * (1 + self.provisao_dissidio)
        
        total_a = (salario_com_dissidio + adicional_noturno_com_dissidio + 
                   inss_patronal + inss_rat + inss_terceiros + fgts +
                   beneficio_social_com_dissidio + br_med_com_dissidio)
        
        return {
            'salario_bruto': salario_com_dissidio,
            'adicional_noturno': adicional_noturno_com_dissidio,
            'inss_patronal': inss_patronal,
            'inss_rat': inss_rat,
            'inss_terceiros': inss_terceiros,
            'fgts': fgts,
            'beneficio_social': beneficio_social_com_dissidio,
            'br_med': br_med_com_dissidio,
            'total': total_a
        }
    
    def calcular_montante_b_provisionamento(self, montante_a):
        """Calcula MONTANTE B - PROVISIONAMENTO"""
        # Base para cálculo
        base = montante_a['salario_bruto'] + montante_a['adicional_noturno']
        
        # 13º salário
        decimo_terceiro = base * PROVISIONAMENTO['decimo_terceiro']
        
        # Férias (1/3 sobre 13º)
        ferias = decimo_terceiro * PROVISIONAMENTO['ferias']
        
        # Ausências legais
        ausencias = base * PROVISIONAMENTO['ausencias_legais']
        
        # Base para encargos do provisionamento
        base_provisionamento = decimo_terceiro + ferias + ausencias
        
        # Encargos sobre provisionamento
        inss_patronal = base_provisionamento * ENCARGOS['inss_patronal']
        inss_rat = base_provisionamento * ENCARGOS['inss_rat']
        inss_terceiros = base_provisionamento * ENCARGOS['inss_terceiros']
        fgts_provisao = base_provisionamento * ENCARGOS['fgts']
        
        # GRRF (40% sobre FGTS total)
        fgts_total = montante_a['fgts']
        grrf = fgts_total * ENCARGOS['grrf']
        
        total_b = (decimo_terceiro + ferias + ausencias + 
                   inss_patronal + inss_rat + inss_terceiros + 
                   fgts_provisao + grrf)
        
        return {
            'decimo_terceiro': decimo_terceiro,
            'ferias': ferias,
            'ausencias': ausencias,
            'inss_patronal': inss_patronal,
            'inss_rat': inss_rat,
            'inss_terceiros': inss_terceiros,
            'fgts': fgts_provisao,
            'grrf': grrf,
            'total': total_b
        }
    
    def calcular_montante_c_beneficios(self):
        """Calcula MONTANTE C - BENEFÍCIOS"""
        beneficios = self.dados['beneficios']
        
        # Vale Transporte - NÃO MULTIPLICA por número de funcionários
        vt = beneficios['vale_transporte_dia'] * DIAS_BENEFICIOS['vale_transporte']
        desconto_vt = -(self.dados['salario_bruto'] * self.num_funcionarios * DESCONTOS['vale_transporte'])
        vt_total = vt + desconto_vt
        vt_com_dissidio = vt_total * (1 + self.provisao_dissidio)
        
        # Cesta Básica - MULTIPLICA por número de funcionários
        cesta = beneficios['cesta_basica'] * self.num_funcionarios
        cesta_com_dissidio = cesta * (1 + self.provisao_dissidio)
        
        # PPR - MULTIPLICA por número de funcionários
        ppr = (beneficios['ppr'] / 12) * self.num_funcionarios
        ppr_com_dissidio = ppr * (1 + self.provisao_dissidio)
        
        # Auxílio Saúde - MULTIPLICA por número de funcionários
        aux_saude = beneficios['auxilio_saude'] * self.num_funcionarios
        aux_saude_com_dissidio = aux_saude * (1 + self.provisao_dissidio)
        
        # Vale Refeição - MULTIPLICA por número de funcionários
        vr = beneficios['vale_refeicao_dia'] * DIAS_BENEFICIOS['vale_refeicao'] * self.num_funcionarios
        desconto_vr = vr * DESCONTOS['vale_refeicao']
        vr_total = vr - desconto_vr
        vr_com_dissidio = vr_total * (1 + self.provisao_dissidio)
        
        total_c = (vt_com_dissidio + cesta_com_dissidio + 
                   ppr_com_dissidio + aux_saude_com_dissidio + 
                   vr_com_dissidio)
        
        return {
            'vale_transporte': vt_com_dissidio,
            'cesta_basica': cesta_com_dissidio,
            'ppr': ppr_com_dissidio,
            'auxilio_saude': aux_saude_com_dissidio,
            'vale_refeicao': vr_com_dissidio,
            'total': total_c
        }
    
    def calcular_montante_d_coberturas(self, montante_a):
        """Calcula MONTANTE D - COBERTURAS (diluição de férias)"""
        # Parte 1: Diluição de custos de folha para coberturas (C65)
        # Salário bruto + adicional noturno / 12
        salario_cobertura = (montante_a['salario_bruto'] + montante_a['adicional_noturno']) / 12
        
        # Encargos sobre cobertura / 12
        inss_patronal = montante_a['inss_patronal'] / 12
        inss_rat = montante_a['inss_rat'] / 12
        inss_terceiros = montante_a['inss_terceiros'] / 12
        fgts = montante_a['fgts'] / 12
        
        # Benefícios / 12
        beneficio_social = montante_a['beneficio_social'] / 12
        br_med = montante_a['br_med'] / 12
        
        # PPR e Cesta Básica (com fórmulas específicas)
        ppr = (self.dados['beneficio_social_sindical'] / 12 * self.num_funcionarios) / 12
        cesta = (self.dados['beneficios']['cesta_basica'] / 12) * self.num_funcionarios
        auxilio_saude = (self.dados['beneficios']['auxilio_saude'] / 12) * self.num_funcionarios
        
        total_parte1 = (salario_cobertura + inss_patronal + inss_rat + 
                       inss_terceiros + fgts + beneficio_social + 
                       ppr + cesta + auxilio_saude + br_med)
        
        # Parte 2: Provisionamento sobre cobertura (C74)
        # Base para provisionamento (soma dos encargos da cobertura)
        base_provisao_cobertura = inss_patronal + inss_rat + inss_terceiros + fgts
        
        # 13º sobre cobertura
        decimo_cobertura = base_provisao_cobertura / 12
        
        # Férias sobre 13º de cobertura
        ferias_cobertura = decimo_cobertura / 3
        
        # Base para encargos do provisionamento de cobertura
        base_encargos_cobertura = decimo_cobertura + ferias_cobertura
        
        # Encargos sobre provisionamento de cobertura
        inss_patronal_prov = base_encargos_cobertura * ENCARGOS['inss_patronal']
        inss_rat_prov = base_encargos_cobertura * ENCARGOS['inss_rat']
        inss_terceiros_prov = base_encargos_cobertura * ENCARGOS['inss_terceiros']
        fgts_prov = base_encargos_cobertura * ENCARGOS['fgts']
        
        # GRRF sobre FGTS de cobertura
        grrf_cobertura = fgts * ENCARGOS['grrf']
        
        total_parte2 = (decimo_cobertura + ferias_cobertura + 
                       inss_patronal_prov + inss_rat_prov + 
                       inss_terceiros_prov + fgts_prov + grrf_cobertura)
        
        return {
            'coberturas_ferias': total_parte1,
            'provisionamento_cobertura': total_parte2,
            'total': total_parte1 + total_parte2
        }
    
    def calcular_montante_e_despesas_gerais(self):
        """Calcula MONTANTE E - DESPESAS GERAIS (uniformes, celular, etc)"""
        # Uniformes (diluição semestral) - MULTIPLICA por número de funcionários
        uniformes = (self.dados['uniformes'] * self.num_funcionarios) / 6
        
        # Celular - NÃO multiplica (é 1 por posto)
        celular = (self.dados['celular_base'] / 12) + self.dados['celular_fixo']
        
        # Cesta Básica II - MULTIPLICA por número de funcionários
        cesta_ii = self.dados['cesta_basica_ii'] * self.num_funcionarios
        
        total_e = uniformes + celular + cesta_ii
        
        return {
            'uniformes': uniformes,
            'celular': celular,
            'cesta_basica_ii': cesta_ii,
            'total': total_e
        }
    
    def calcular_custo_total(self):
        """Calcula o custo total mensal (soma de todos os montantes)"""
        montante_a = self.calcular_montante_a_folha()
        montante_b = self.calcular_montante_b_provisionamento(montante_a)
        montante_c = self.calcular_montante_c_beneficios()
        montante_d = self.calcular_montante_d_coberturas(montante_a)
        montante_e = self.calcular_montante_e_despesas_gerais()
        
        custo_total = (montante_a['total'] + montante_b['total'] + 
                       montante_c['total'] + montante_d['total'] + 
                       montante_e['total'])
        
        return {
            'montante_a': montante_a,
            'montante_b': montante_b,
            'montante_c': montante_c,
            'montante_d': montante_d,
            'montante_e': montante_e,
            'custo_total': custo_total
        }
    
    def calcular_faturamento_cenario(self, custo_total, desp_admin_percent, lucro_liquido_percent):
        """
        Calcula o faturamento necessário para um cenário específico
        
        Fórmula reversa:
        Faturamento = (Custo + (Faturamento * desp_admin)) / (1 - tributos - IR - CSLL)
        """
        # Tributos fixos sobre faturamento
        tributos_total = TRIBUTOS['iss'] + TRIBUTOS['cofins'] + TRIBUTOS['pis']
        
        # Iteração para encontrar faturamento (método numérico)
        faturamento = custo_total * 1.5  # chute inicial
        
        for _ in range(100):  # iterações
            desp_admin = (custo_total / (1 - desp_admin_percent)) * desp_admin_percent
            custo_final = custo_total + desp_admin
            
            tributos_valor = faturamento * tributos_total
            receita_liquida = faturamento - tributos_valor
            
            margem = receita_liquida - custo_final
            
            # Impostos sobre lucro
            ir = margem * TRIBUTOS['ir_lucro']
            csll = margem * TRIBUTOS['csll_lucro']
            lucro_liquido = margem - ir - csll
            
            # Verificar se lucro líquido está correto
            lucro_target = faturamento * lucro_liquido_percent
            
            if abs(lucro_liquido - lucro_target) < 0.01:  # convergiu
                break
            
            # Ajustar faturamento
            faturamento = custo_final / (1 - tributos_total - desp_admin_percent - 
                                         lucro_liquido_percent * (1 + TRIBUTOS['ir_lucro'] + 
                                         TRIBUTOS['csll_lucro']))
        
        # Cálculos finais
        tributos_valor = faturamento * tributos_total
        iss = faturamento * TRIBUTOS['iss']
        cofins = faturamento * TRIBUTOS['cofins']
        pis = faturamento * TRIBUTOS['pis']
        
        receita_liquida = faturamento - tributos_valor
        desp_admin = (custo_total / (1 - desp_admin_percent)) * desp_admin_percent
        custo_final = custo_total + desp_admin
        
        margem = receita_liquida - custo_final
        ir = margem * TRIBUTOS['ir_lucro']
        csll = margem * TRIBUTOS['csll_lucro']
        lucro_liquido = margem - ir - csll
        
        valor_hh = faturamento / self.horas_mensais
        
        return {
            'faturamento': faturamento,
            'tributos': {
                'iss': iss,
                'cofins': cofins,
                'pis': pis,
                'total': tributos_valor
            },
            'receita_liquida': receita_liquida,
            'despesa_administrativa': desp_admin,
            'custo_final': custo_final,
            'margem': margem,
            'ir': ir,
            'csll': csll,
            'lucro_liquido': lucro_liquido,
            'valor_hh': valor_hh,
            'percentuais': {
                'desp_admin': desp_admin_percent,
                'lucro_liquido': lucro_liquido_percent
            }
        }
    
    def calcular_todos_cenarios(self):
        """Calcula todos os 4 cenários de negociação"""
        resultado_custos = self.calcular_custo_total()
        custo_total = resultado_custos['custo_total']
        
        cenarios_resultado = {}
        
        for nome, params in CENARIOS.items():
            cenarios_resultado[nome] = self.calcular_faturamento_cenario(
                custo_total,
                params['desp_admin'],
                params['lucro_liquido']
            )
        
        return {
            'custos': resultado_custos,
            'cenarios': cenarios_resultado
        }
