#!/bin/bash
# ============================================================================
# Script para subir atualizações para GitHub automaticamente
# ============================================================================

echo ""
echo "========================================"
echo "  ATUALIZADOR AUTOMÁTICO - GITHUB"
echo "========================================"
echo ""

# Verificar se está em um repositório Git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "ERRO: Esta pasta não é um repositório Git!"
    echo "Execute primeiro: git init"
    exit 1
fi

echo "[1/4] Verificando mudanças..."
git status

echo ""
echo "[2/4] Adicionando arquivos..."
git add .

echo ""
read -p "Digite a mensagem do commit: " mensagem

if [ -z "$mensagem" ]; then
    echo "ERRO: Mensagem não pode estar vazia!"
    exit 1
fi

echo ""
echo "[3/4] Fazendo commit..."
git commit -m "$mensagem"

echo ""
echo "[4/4] Enviando para GitHub..."
git push

echo ""
echo "========================================"
echo "  CONCLUÍDO COM SUCESSO!"
echo "========================================"
echo ""
echo "Aguarde 1-2 minutos para o Streamlit"
echo "Cloud aplicar as mudanças."
echo ""
