import cv2
import numpy as np
import time
import os

def manual_spatial_convolution(image, kernel):
    """
    Implementação 'raiz' da convolução espacial, sem otimizações de C++.
    Desliza a janela do kernel pixel a pixel sobre a imagem.
    """
    h, w = image.shape
    k_h, k_w = kernel.shape
    pad_h, pad_w = k_h // 2, k_w // 2
    
    # Preenche as bordas com zeros (padding) para o kernel não sair da imagem
    padded_img = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
    result = np.zeros_like(image, dtype=np.float32)
    
    # O gargalo computacional: 
    # Para cada pixel da imagem, iteramos sobre toda a área do kernel
    for i in range(h):
        for j in range(w):
            # Extrai a região da imagem (patch) coberta pelo kernel
            patch = padded_img[i:i+k_h, j:j+k_w]
            # Multiplica ponto a ponto e soma (a definição exata de convolução 2D)
            result[i, j] = np.sum(patch * kernel)
            
    return np.clip(result, 0, 255).astype(np.uint8)

def apply_frequency_convolution(image, kernel):
    """
    Mantido igual: Aplica o Teorema da Convolução usando a FFT padrão do NumPy.
    """
    start = time.perf_counter()
    
    F_image = np.fft.fft2(image)
    F_kernel = np.fft.fft2(kernel, s=image.shape)
    
    # Teorema da Convolução: A multiplicação mágica no domínio da frequência
    F_result = F_image * F_kernel
    
    result_float = np.real(np.fft.ifft2(F_result))
    result = np.clip(result_float, 0, 255).astype(np.uint8)
    
    end = time.perf_counter()
    return result, (end - start)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_dir = os.path.join(project_root, "data")
    
    input_image_path = os.path.join(input_dir, "bg_ex2.jpeg")
    
    if not os.path.exists(input_image_path):
        raise FileNotFoundError(f"Imagem não encontrada: {input_image_path}")
        
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    
    # Reduzindo a imagem para o teste em Python puro não travar o seu PC
    image = cv2.resize(image, (512, 512))
    
    # Reduzi o kernel inicial para 31, pois a convolução manual é extremamente pesada.
    # Você pode aumentar para 51 ou 71, mas prepare-se para esperar alguns minutos!
    kernel_size = 31
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
    
    print(f"Iniciando testes de MATEMÁTICA PURA")
    print(f"Imagem: {image.shape} | Kernel: {kernel_size}x{kernel_size}")
    
    # Execução Real e Cronometrada
    print("\nCalculando no Domínio da Frequência (FFT)...")
    frequency_result, frequency_time = apply_frequency_convolution(image, kernel)
    
    print("Calculando no Domínio Espacial Manual ...\n")
    
    start_spatial = time.perf_counter()
    spatial_result = manual_spatial_convolution(image, kernel)
    end_spatial = time.perf_counter()
    spatial_time = end_spatial - start_spatial
    
    print("="*40)
    print("      RESULTADOS DE DESEMPENHO      ")
    print("="*40)
    print(f"Tempo Espacial (Manual): {spatial_time:.4f} segundos")
    print(f"Tempo Frequência (FFT):  {frequency_time:.4f} segundos")
    print("-" * 40)
    
    if frequency_time < spatial_time:
        ganho = spatial_time / frequency_time
        print(f"VENCEDOR: Frequência ({ganho:.1f}x MAIS RÁPIDA)")
    else:
        print("VENCEDOR: Espacial")
        
    print("="*40)