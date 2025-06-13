# Image Editor

Este projeto é um editor de imagens simples feito em Python utilizando Tkinter para a interface gráfica e Pillow (PIL) para manipulação de imagens. Ele permite aplicar diversos efeitos e filtros em imagens, além de salvar o resultado.

## Funcionalidades

- **Selecionar Imagem:** Carregue uma imagem dos formatos JPG, JPEG ou PNG.
- **Preto e Branco:** Converte a imagem para tons de cinza.
- **Efeito Sépia:** Aplica um efeito sépia à imagem.
- **Efeito Negativo:** Inverte as cores da imagem.
- **Efeito de Nitidez:** Realça os detalhes da imagem.
- **Efeito Blur:** Aplica um desfoque na imagem.
- **Detecção de Bordas:** Realça as bordas da imagem.
- **Zoom:** Utilize o controle deslizante para aumentar ou diminuir o zoom da imagem.
- **Salvar Imagem:** Salve a imagem editada em PNG, JPEG ou outro formato.

## Como Usar

1. **Instale as dependências:**
   ```sh
   pip install pillow numpy
   ```

2. **Execute o programa:**
   ```sh
   python oat_ImageEditor.py
   ```

3. **Utilize os botões para aplicar efeitos e o controle deslizante para zoom.**

## Estrutura do Código

- A interface é construída com Tkinter.
- Os efeitos são aplicados utilizando operações de matriz com NumPy e Pillow.
- O zoom é controlado por um `Scale` horizontal.

## Requisitos

- Python 3.x
- Pillow
- NumPy

## Observações

- O editor não sobrescreve a imagem original, permitindo experimentar diferentes efeitos.
- O controle de zoom permite ampliar ou reduzir a imagem sem perder a originalidade.

---

**Autor:**  
Desenvolvido para fins educacionais.

---

Arquivo principal: [`oat_ImageEditor.py`](oat_ImageEditor.py)  
Classe principal: `ImageEditor`