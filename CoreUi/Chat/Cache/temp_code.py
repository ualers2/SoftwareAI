import csv

def ler_csv(nome_arquivo):
    try:
        with open(nome_arquivo, mode='r', newline='', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            cabecalho = next(leitor)  # Lê o cabeçalho
            print(f"{' | '.join(cabecalho)}")  # Exibe o cabeçalho

            for linha in leitor:
                print(f"{' | '.join(linha)}")  # Exibe cada linha de dados

    except FileNotFoundError:
        print(f"O arquivo '{nome_arquivo}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def main():
    nome_arquivo = 'data.csv'  # Nome do arquivo CSV
    ler_csv(nome_arquivo)

# Executando o programa
if __name__ == "__main__":
    main()