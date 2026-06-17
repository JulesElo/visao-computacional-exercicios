import cv2
import numpy as np
import os

def custom_high_boost(image, A=1.2, kernel_size=(5, 5)):
    """
    Implementação manual do filtro High-Boost.
    g(x,y) = (A - 1) * original + (original - blurred)
    """
    # Garante que a imagem está em ponto flutuante para evitar estouro de 8 bits (0-255) nos cálculos
    img_float = image.astype(np.float32)
    
    # 1. Obtém a componente passa-baixa (suavizada) usando um desfoque gaussiano
    img_blur = cv2.GaussianBlur(img_float, kernel_size, 0)
    
    # 2. Obtem a componente passa-alta (detalhes/bordas)
    img_high_pass = img_float - img_blur
    
    # 3. Aplica a fórmula do High-Boost
    img_high_boost = (A - 1) * img_float + img_high_pass
    
    # 4. Normaliza os valores para o intervalo [0, 255] e converte de volta para uint8
    img_high_pass_clipped = np.clip(img_high_pass, 0, 255).astype(np.uint8)
    img_high_boost_clipped = np.clip(img_high_boost, 0, 255).astype(np.uint8)
    
    return img_high_pass_clipped, img_high_boost_clipped

def run():
    # Configuração de caminhos dinâmicos absolutos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_dir = os.path.join(project_root, "data")
    
    input_file = os.path.join(input_dir, "input_ex3.jpeg")
    
    if not os.path.exists(input_file):
        print(f"Aviso: Coloque uma imagem em '{input_file}' para testar.")
        # Se não houver, criamos uma imagem geométrica simples para teste imediato
        os.makedirs(input_dir, exist_ok=True)
        dummy_img = np.zeros((400, 400), dtype=np.uint8)
        cv2.putText(dummy_img, "CV TEST", (50, 220), cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 5)
        cv2.imwrite(input_file, dummy_img)

    # Carrega a imagem e converte para tons de cinza
    img_original = cv2.imread(input_file, cv2.IMREAD_GRAYSCALE)
    
    # Executa o filtro customizado
    # Fator A = 1.5 (A > 1 ativa o High-Boost)
    high_pass, high_boost = custom_high_boost(img_original, A=1.5, kernel_size=(7, 7))
    
    # Exibe os resultados para comparação e análise
    print("Exibindo janelas do Exercício 3. Feche-as para encerrar.")
    cv2.imshow("1. Imagem Original (Cinza)", img_original)
    cv2.imshow("2. Filtro Passa-Alta (Apenas Bordas)", high_pass)
    cv2.imshow("3. Filtro High-Boost (Bordas Realcadas + Fundo)", high_boost)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()