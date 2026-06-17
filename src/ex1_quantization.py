import cv2
import numpy as np
import os

def quantize_grayscale(image_path, factor=4):
    """
    Converte uma imagem colorida para tons de cinza e reduz a quantidade
    de tons agrupando-os a cada 'factor' níveis (Quantização Uniforme).
    """
    # 1. Carrega a imagem original (Colorida / BGR)
    img_color = cv2.imread(image_path)
    if img_color is None:
        raise FileNotFoundError(f"Não foi possível carregar a imagem em: {image_path}")
    
    # 2. Converte para tons de cinza clássico (0 a 255)
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    
    # 3. Aplica o agrupamento a cada 'factor' tons (divisão inteira seguida de multiplicação)
    # Ex: (de 0 a 3) // 4 = 0 -> 0 * 4 = 0
    # Ex: (de 4 a 7) // 4 = 1 -> 1 * 4 = 4
    img_quantized = (img_gray // factor) * factor
    
    return img_gray, img_quantized

def generate_test_gradient(output_path):
    """Gera uma imagem de gradiente suave para testar a quantização de tons."""
    gradient = np.tile(np.arange(256, dtype=np.uint8), (256, 1))
    cv2.imwrite(output_path, gradient)
    print(f"Imagem de teste sintética gerada em: {output_path}")

if __name__ == "__main__":
    # Descobre o caminho absoluto de onde este script (ex1_clustering.py) está
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Retorna o caminho até a pasta /src
    
    # Sobe um nível para encontrar a raiz do projeto e alcançar a pasta /data
    project_root = os.path.dirname(script_dir)
    input_dir = os.path.join(project_root, "data")

    # Define os caminhos dos arquivos
    input_image = os.path.join(input_dir, "input_ex1.png")
    output_image = os.path.join(input_dir, "output_ex1.png")
    
    # Garante que a pasta de dados exista
    os.makedirs(input_dir, exist_ok=True)
    
    # Se não houver imagem de teste, cria um gradiente automático
    if not os.path.exists(input_image):
        generate_test_gradient(input_image)
        
    print("Processando Exercício 1...")
    gray, quantized = quantize_grayscale(input_image, factor=4)
    
    # Salva o resultado
    cv2.imwrite(output_image, quantized)
    print(f"Imagem resultante salva em: {output_image}")
    
    # Conta a quantidade de tons únicos para validação do exercício
    unique_gray = len(np.unique(gray))
    unique_quantized = len(np.unique(quantized))
    
    print("\n=== VALIDAÇÃO DOS RESULTADOS ===")
    print(f"Tons únicos na imagem de cinza original: {unique_gray}")
    print(f"Tons únicos na imagem quantizada: {unique_quantized}")
    print("=================================")
    
    # Exibe visualmente o resultado na tela
    print("\nFeche as janelas de imagem para encerrar o script.")
    cv2.imshow("Original em Tons de Cinza", gray)
    cv2.imshow("Resultado Quantizado", quantized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()