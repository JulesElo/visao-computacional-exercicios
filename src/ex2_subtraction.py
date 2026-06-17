import cv2
import numpy as np
import os

def subtract_and_detect(bg_path, body_path, output_path, threshold_value=50):
    """
    Subtrai o fundo da imagem principal, aplica limiarização e 
    desenha um retângulo vermelho (Bounding Box) ao redor do corpo detectado.
    """
    # 1. Carrega as imagens originais (Coloridas)
    img_bg = cv2.imread(bg_path)
    img_body = cv2.imread(body_path)
    
    if img_bg is None or img_body is None:
        raise FileNotFoundError("Não foi possível carregar as imagens do Exercício 2. Verifique a pasta 'data/'.")
    
    # 2. Converte para tons de cinza
    gray_bg = cv2.cvtColor(img_bg, cv2.COLOR_BGR2GRAY)
    gray_body = cv2.cvtColor(img_body, cv2.COLOR_BGR2GRAY)
    
    # 3. Subtração: Diferença Absoluta entre as imagens
    diff = cv2.absdiff(gray_bg, gray_body)
    
    # 4. Binarização (Limiar determinado empiricamente)
    # Valores de diferença maiores que 'threshold_value' viram branco (255), o resto vira preto (0).
    _, binary_mask = cv2.threshold(diff, threshold_value, 255, cv2.THRESH_BINARY)
    
    # Operação morfológica (opcional) para limpar pequenos ruídos da máscara
    kernel = np.ones((5, 5), np.uint8)
    binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel)
    binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
    
    # 5. Encontra os contornos na máscara binarizada
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Cria uma cópia da imagem colorida para desenhar o retângulo
    result_img = img_body.copy()
    
    if contours:
        # Encontra o maior contorno (que presumivelmente é o seu corpo)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Pega as coordenadas do retângulo delimitador
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Desenha o retângulo vermelho na imagem colorida (BGR: 0, 0, 255)
        cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 0, 255), 3)
    
    return gray_bg, gray_body, diff, binary_mask, result_img

# Função para exibir as janelas menores
def show_resizable_window(win_name, img, width=400):
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    aspect_ratio = img.shape[0] / img.shape[1]
    height = int(width * aspect_ratio)
    cv2.resizeWindow(win_name, width, height)
    cv2.imshow(win_name, img)

if __name__ == "__main__":
    # Resolução de caminhos dinâmica
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_dir = os.path.join(project_root, "data")
    
    bg_file = os.path.join(input_dir, "bg_ex2.jpeg")
    body_file = os.path.join(input_dir, "body_ex2.jpeg")
    output_file = os.path.join(input_dir, "output_ex2.jpeg")
    
    print("Processando Exercício 2...")
    
    gray_bg, gray_body, diff_img, mask_img, final_result = subtract_and_detect(bg_file, body_file, output_file, threshold_value=50)
    
    # Salva o resultado final
    cv2.imwrite(output_file, final_result)
    print(f"Imagem final salva em: {output_file}")
    
    # Exibe visualmente as etapas
    print("\nFeche as janelas de imagem para encerrar o script.")
    
    show_resizable_window("1. Fundo em Cinza", gray_bg)
    show_resizable_window("2. Corpo em Cinza", gray_body)
    show_resizable_window("3. Diferenca", diff_img)
    show_resizable_window("4. Binarizacao", mask_img)
    show_resizable_window("5. Deteccao Final", final_result)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()