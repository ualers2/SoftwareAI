
def calculate_dollar_value(tokens_entrada, tokens_saida, tokens_cache=0):
    """
    Calcula o custo total com base nos tokens de entrada, cache (opcional) e saída.
    
    :param tokens_entrada: Quantidade de tokens de entrada.
    :param tokens_saida: Quantidade de tokens de saída.
    :param tokens_cache: Quantidade de tokens de entrada em cache (padrão é 0).
    :return: Custo total em dólares.
    """
    # Custos por 1 milhão de tokens
    custo_por_milhao_entrada = 0.150
    custo_por_milhao_cache = 0.075
    custo_por_milhao_saida = 0.600
    
    # Cálculo dos custos individuais
    custo_entrada = (tokens_entrada / 1_000_000) * custo_por_milhao_entrada
    custo_cache = (tokens_cache / 1_000_000) * custo_por_milhao_cache
    custo_saida = (tokens_saida / 1_000_000) * custo_por_milhao_saida
    
    # Cálculo do custo total
    custo_total = custo_entrada + custo_cache + custo_saida
    
    return round(custo_total, 6)
