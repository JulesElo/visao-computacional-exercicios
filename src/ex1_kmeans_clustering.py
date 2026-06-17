import cv2
import numpy as np
import os

def quantize_grayscale(image_path, k=64):
    """
    Converte uma imagem colorida para tons de cinza e reduz a quantidade
    de tons aplicando o algoritmo de clusterização K-Means.
    """
    # 1. Carrega a imagem original (Colorida / BGR)
    img_color = cv2.imread(image_path)
    if img_color is None:
        raise FileNotFoundError(f"Não foi possível carregar a imagem em: {image_path}")
    
    # 2. Converte para tons de cinza clássico (0 a 255)
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    
    # 3. Prepara os dados para o K-Means (achata a matriz e converte para float32)
    pixel_values = img_gray.reshape((-1, 1))
    pixel_values = np.float32(pixel_values)
    
    # 4. Define os critérios de parada do K-Means:
    # (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iteracoes, precisao)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    
    # 5. Aplica o K-Means
    # k = 64 (para representar agrupamentos de 4 em 4 tons partindo de 256)
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # 6. Reconstrói a imagem com os tons clusterizados
    centers = np.uint8(centers) # Converte os centros encontrados de volta para 8-bits
    img_quantized_flat = centers[labels.flatten()] # Mapeia cada pixel para seu respectivo centro
    img_quantized = img_quantized_flat.reshape(img_gray.shape) # Devolve o formato 2D da imagem
    
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
    gray, quantized = quantize_grayscale(input_image)
    
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
    cv2.imshow("Resultado", quantized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()