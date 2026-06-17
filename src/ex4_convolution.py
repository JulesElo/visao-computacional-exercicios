import cv2
import numpy as np
import time
import os

def apply_spatial_convolution(image, kernel):
    start = time.perf_counter()
    # O parâmetro -1 indica que a imagem de saída terá a mesma profundidade da entrada
    result = cv2.filter2D(image, -1, kernel)
    end = time.perf_counter()
    return result, (end - start)

def apply_frequency_convolution(image, kernel):
    start = time.perf_counter()
    
    # 1. Transformada Rápida de Fourier (FFT) da imagem original
    F_image = np.fft.fft2(image)
    
    # 2. Transformada de Fourier do kernel
    # O parâmetro 's' faz o padding (preenchimento com zeros) automático do kernel 
    # para que ele fique com as exatas dimensões da imagem. Essa é uma exigência 
    # matemática para que a multiplicação no domínio da frequência funcione corretamente.
    F_kernel = np.fft.fft2(kernel, s=image.shape)
    
    # 3. Teorema da Convolução: Multiplicação ponto a ponto no domínio da frequência
    F_result = F_image * F_kernel
    
    # 4. Transformada Inversa para voltar ao domínio espacial
    result_float = np.real(np.fft.ifft2(F_result))
    
    # Ajusta os valores numéricos de volta para o padrão de imagem 8-bits (0 a 255)
    result = np.clip(result_float, 0, 255).astype(np.uint8)
    
    end = time.perf_counter()
    return result, (end - start)

def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_dir = os.path.join(project_root, "data")
    
    # Reutilizando a imagem da parede do Exercício 2.
    input_image_path = os.path.join(input_dir, "bg_ex2.jpeg")
    
    if not os.path.exists(input_image_path):
        raise FileNotFoundError(f"Imagem não encontrada: {input_image_path}")
        
    # Carrega a imagem em tons de cinza para simplificar o processamento da FFT
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    
    kernel_size = 71
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
    
    print(f"Iniciando testes com imagem de tamanho: {image.shape} e Kernel: {kernel_size}x{kernel_size}")
    
    # Aquecimento (Warm-up) da CPU:
    # Executa as funções uma vez no vazio apenas para carregar as bibliotecas (NumPy/OpenCV) na RAM.
    # Isso evita que o primeiro método testado seja penalizado pelo tempo de "acordar" o sistema.
    _, _ = apply_spatial_convolution(image[:100, :100], kernel[:5, :5])
    _, _ = apply_frequency_convolution(image[:100, :100], kernel[:5, :5])
    
    # Execução Real e Cronometrada
    print("\nCalculando no Domínio Espacial...")
    spatial_result, spatial_time = apply_spatial_convolution(image, kernel)
    
    print("Calculando no Domínio da Frequência (FFT)...")
    frequency_result, frequency_time = apply_frequency_convolution(image, kernel)
    
    print("\n" + "="*35)
    print("      RESULTADOS DE DESEMPENHO      ")
    print("="*35)
    print(f"Tempo Espacial:   {spatial_time:.4f} segundos")
    print(f"Tempo Frequência: {frequency_time:.4f} segundos")
    print("-" * 35)
    
    if frequency_time < spatial_time:
        ganho = spatial_time / frequency_time
        print(f"VENCEDOR: Frequência ({ganho:.1f}x MAIS RÁPIDA)")
    else:
        print("VENCEDOR: Espacial")
        
    print("="*35 + "\n")

if __name__ == "__main__":
    run()