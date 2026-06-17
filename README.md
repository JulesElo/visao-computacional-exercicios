# Tarefa Avaliativa de Visão Computacional

Este repositório contém a implementação de quatro exercícios da disciplina de Visão Computacional, abordando conceitos de processamento de imagens.

## 🛠️ Estrutura do Projeto

```
.
├── LICENSE
├── README.md
├── data/
├── main.py
├── requirements.txt
└── src/
    ├── __init__.py
    ├── ex1_kmeans_clustering.py
    ├── ex1_quantization.py
    ├── ex2_subtraction.py
    ├── ex3_high_boost.py
    ├── ex4_convolution.py
    └── ex4_convolution_manual.py
```

## ⚙️ Pré-requisitos e Instalação

Certifique-se de ter o [Python 3.x](https://www.python.org/) instalado. Siga os passos abaixo para clonar o repositório, criar um ambiente virtual (recomendado) e instalar as dependências.

Os comandos abaixo são destinados a usuários do **Windows**:

1. Clone este repositório e acesse a pasta:

```
git clone https://github.com/JulesElo/visao-computacional-exercicios.git
cd visao-computacional-exercicios
```

2. Crie e ative o ambiente virtual(venv):

```
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências necessárias:

```
pip install -r requirements.txt
```

## 🖼️ Preparação dos Dados (Imagens)

Para que os scripts funcionem corretamente, coloque as suas imagens de teste dentro da pasta `data/`. É esperado que as seguintes imagens sejam fornecidas:

* `input_ex1.jpeg`: Imagem colorida para os testes do Exercício 1.
* `bg_ex2.jpeg`: Imagem apenas do fundo (parede) para o Exercício 2.
* `body_ex2.jpeg`: Imagem do corpo com o mesmo fundo para o Exercício 2.
* `input_ex3.jpeg`: Imagem base para o filtro de bordas do Exercício 3.

**Atenção às extensões dos arquivos:**

Se as suas imagens possuírem extensões diferentes das padronizadas acima (por exemplo, `.png` em vez de `.jpeg`), você precisará alterar o nome do arquivo diretamente no código, dentro da função `run()` do exercício correspondente na pasta `src/`.

Exemplo de alteração no código:

```
# Como está no código:
bg_file = os.path.join(input_dir, "bg_ex2.jpeg")

# Como deve ficar se a sua imagem for PNG:
bg_file = os.path.join(input_dir, "bg_ex2.png")
```

## 🚀 Como Executar

A forma mais simples de testar e avaliar o projeto é executando o script principal, que abrirá um menu interativo no terminal.

Execute o comando abaixo na raiz do projeto (certifique-se de estar com o ambiente virtual ativado):

```
python main.py
```

Siga as instruções na tela digitando o número correspondente ao exercício que deseja avaliar. As janelas com os resultados visuais serão abertas automaticamente. **Pressione qualquer tecla ou feche as janelas de imagem para encerrar o script de um exercício e voltar ao menu.**

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).