# Calculadora de Preço de Venda em Gold — Mir4

Aplicativo desktop para Windows que calcula o preço de venda e a liquidação
(valor recebido após imposto) no Mercado Unificado do jogo **Mir4**.

## O que faz

- **Anunciei por X → recebo?** — você informa o preço de venda e vê quanto recebe após o imposto.
- **Quero receber Y → anuncio?** — você informa quanto quer receber e vê por quanto anunciar.
- Taxas de imposto configuráveis: **5%** (padrão), **4%** (com o desconto de −20%) e **0%** (isento pela Torre de Conquista).
- Imposto mínimo de 1 Moeda de Ouro e arredondamento igual ao do jogo.

## Como usar (versão pronta)

Baixe o arquivo `.exe` na aba **[Releases](../../releases)** deste repositório
(`calculadora-preco-itens-mercado-mir4`), dê um duplo clique e use.
Não precisa instalar nada.

## Como rodar pelo código

Requer Python 3 instalado.

```bash
python CalculadoraPrecoMir4.py
```

## Como gerar o .exe você mesmo

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Calculadora Preco Mir4" CalculadoraPrecoMir4.py
```

O executável aparece na pasta `dist`.

## Regra de cálculo

O imposto de mercado é de 5% sobre o preço de venda, com opção de redução de −20%
(taxa efetiva de 4%). O valor recebido (liquidação) é o preço de venda menos o imposto,
arredondado como no jogo, com imposto mínimo de 1 Gold.

---

Feito para uso pessoal e da comunidade de jogadores de Mir4.
