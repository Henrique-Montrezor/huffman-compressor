# Compressor de Arquivos de Texto (Codificação de Huffman)

Este é um projeto de implementação do algoritmo de Codificação de Huffman em Python. O objetivo é demonstrar conceitos fundamentais de Ciência da Computação, incluindo manipulação de bits, estruturas de dados (filas de prioridade/heaps) e serialização de dados binários.

O script é capaz de comprimir arquivos de texto (.txt) em arquivos binários (.bin) significativamente menores e descomprimi-los de volta ao estado original sem perda de dados (lossless compression).

🚀 Funcionalidades

Análise de Frequência: Mapeia a ocorrência de cada caractere no texto.

Árvore de Huffman: Constrói a árvore binária ideal para gerar os prefixos de bits.

Padding de Bits: Gerencia o preenchimento necessário para alinhar os bits em bytes completos (8 bits).

Cabeçalho Inteligente: Armazena a tabela de frequências no início do arquivo binário para permitir a reconstrução da árvore durante a descompressão.

📋 Pré-requisitos

Python 3.6 ou superior.

Não há dependências externas. O projeto utiliza apenas bibliotecas nativas do Python:

heapq: Para a fila de prioridade.

os & sys: Para manipulação de arquivos e argumentos de linha de comando.

struct: Para empacotamento de dados binários (tamanho do header).

json: Para serializar o mapa de frequências no cabeçalho.

🛠️ Como Usar

O script funciona via linha de comando (CLI).

1. Comprimir um arquivo

python huffman_compressor.py compress <arquivo_entrada.txt> <arquivo_saida.bin>


Exemplo:

python huffman_compressor.py compress livro_grande.txt livro_comprimido.bin


Saída esperada: O script mostrará o tamanho original, o tamanho comprimido e a porcentagem de economia.

2. Descomprimir um arquivo

python huffman_compressor.py decompress <arquivo_entrada.bin> <arquivo_saida.txt>


Exemplo:

python huffman_compressor.py decompress livro_comprimido.bin livro_recuperado.txt


🧠 Detalhes Técnicos da Implementação

Para quem está estudando o código, aqui estão os pontos cruciais de atenção:

Estrutura do Arquivo Binário (.bin)

O arquivo gerado não é apenas uma sopa de bits. Ele segue uma estrutura rigorosa para garantir que possa ser lido depois:

Header Size (4 bytes): Um inteiro (Big Endian) que diz quantos bytes o cabeçalho JSON ocupa.

Header (JSON): O mapa de frequências (ex: {"a": 10, "b": 5}). Necessário para reconstruir a árvore.

Content: O texto comprimido em bits.

Padding (Preenchimento)

Como os sistemas operacionais gravam dados em Bytes (8 bits) e a compressão de Huffman gera sequências de tamanho variável (ex: 13 bits), o script adiciona "zeros" extras ao final para fechar o byte.

O primeiro byte do conteúdo comprimido armazena um número inteiro indicando quantos bits de "padding" foram adicionados ao final, para que eles possam ser descartados na descompressão.

Autor: Gerado via Gemini
