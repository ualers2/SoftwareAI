# Taxas por milhão de tokens
COST_INSTRUCTION_PER_MILLION = 1.10    # US$ por 1 000 000 de tokens de instrução
COST_OUTPUT_PER_MILLION      = 4.40    # US$ por 1 000 000 de tokens de output

# Convertendo para custo unitário
cost_instruction_token = COST_INSTRUCTION_PER_MILLION / 1_000_000
cost_output_token      = COST_OUTPUT_PER_MILLION      / 1_000_000

