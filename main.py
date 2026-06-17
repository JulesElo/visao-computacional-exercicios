import sys
from src import ex1_quantization
from src import ex2_subtraction
from src import ex3_high_boost
from src import ex4_convolution

def main():
    while True:
        print("\n" + "="*50)
        print("    MENU: TAREFA AVALIATIVA DE VISÃO COMPUTACIONAL    ")
        print("="*50)
        print("[1] Exercício 1 - Transformação de Tons (Quantização)")
        print("[2] Exercício 2 - Subtração de Fundo e Detecção")
        print("[3] Exercício 3 - Filtro High-Boost")
        print("[4] Exercício 4 - Teorema da Convolução")
        print("[0] Sair")
        print("-" * 50)
        
        escolha = input("Escolha uma opção para executar: ")
        
        if escolha == '1':
            print("\nExecutando Exercício 1...")
            ex1_quantization.run()
        elif escolha == '2':
            print("\nExecutando Exercício 2...")
            ex2_subtraction.run()
        elif escolha == '3':
            print("\nExecutando Exercício 3...")
            ex3_high_boost.run()
        elif escolha == '4':
            print("\nExecutando Exercício 4...")
            ex4_convolution.run()
        elif escolha == '0':
            print("\nEncerrando o programa. Até logo!")
            sys.exit(0)
        else:
            print("\nOpção inválida! Por favor, digite um número de 0 a 4.")

if __name__ == "__main__":
    main()