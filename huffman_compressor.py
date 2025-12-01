import heapq
import os
import json
import struct
import sys

class HuffmanNode:
    """
    Representa um nó na árvore de Huffman.
    Implementa comparadores (__lt__) para que o heapq possa ordenar
    os nós baseados na frequência automaticamente.
    """
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Define como comparar dois nós (necessário para a fila de prioridade)
    # Menor frequência tem maior prioridade
    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        if(other == None):
            return False
        if(not isinstance(other, HuffmanNode)):
            return False
        return self.freq == other.freq

class HuffmanCoding:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    # 1. Mapa de Frequência
    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    # 2. Construção da Fila de Prioridade (Heap)
    def make_heap(self, frequency):
        for key in frequency:
            node = HuffmanNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    # 3. Fusão dos Nós (Construção da Árvore)
    def merge_nodes(self):
        while(len(self.heap) > 1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    # 4. Geração dos Códigos Binários (Recursivo)
    def make_codes_helper(self, root, current_code):
        if(root == None):
            return

        if(root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    # 5. Codificação do Texto
    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    # 6. Padding (Preenchimento de Bits)
    # Arquivos são escritos em Bytes (8 bits). Se nosso código tiver 13 bits,
    # precisamos adicionar 3 bits extras para fechar 2 bytes (16 bits).
    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        # Armazenamos a informação de quanto preenchimento foi usado no primeiro byte (8 bits)
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    # 7. Conversão de String de Bits para Bytes Reais
    def get_byte_array(self, padded_encoded_text):
        if(len(padded_encoded_text) % 8 != 0):
            print("ERRO CRÍTICO: Texto codificado não tem preenchimento correto")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2)) # Converte string binária "10101010" para inteiro
        return b

    # --- COMPRESSÃO ---
    def compress(self, input_path, output_path):
        print(f"Comprimindo: {input_path} -> {output_path}")
        
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()
            text = text.rstrip() # Remove espaços em branco extras no final

        frequency = self.make_frequency_dict(text)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        encoded_text = self.get_encoded_text(text)
        padded_encoded_text = self.pad_encoded_text(encoded_text)
        b = self.get_byte_array(padded_encoded_text)

        # Salvar o arquivo binário com cabeçalho
        # Formato do Arquivo: [4 bytes: tamanho do header][header JSON][dados binários]
        with open(output_path, 'wb') as output:
            # Serializa o mapa de frequência para reconstruir a árvore depois
            freq_json = json.dumps(frequency)
            freq_bytes = freq_json.encode('utf-8')
            
            # Escreve o tamanho do cabeçalho (4 bytes, big endian)
            output.write(struct.pack('>I', len(freq_bytes)))
            # Escreve o cabeçalho
            output.write(freq_bytes)
            # Escreve os dados comprimidos
            output.write(bytes(b))

        print("Compressão finalizada!")
        
        # Estatísticas
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        print(f"Original: {original_size} bytes")
        print(f"Comprimido: {compressed_size} bytes")
        print(f"Taxa de Compressão: {100 - (compressed_size/original_size * 100):.2f}% menor")

    # --- LÓGICA DE DESCOMPRESSÃO ---
    
    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = []

        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text.append(character)
                current_code = ""

        return "".join(decoded_text)

    def decompress(self, input_path, output_path):
        print(f"Descomprimindo: {input_path} -> {output_path}")
        
        with open(input_path, 'rb') as file:
            # Ler tamanho do header
            size_bytes = file.read(4)
            header_length = struct.unpack('>I', size_bytes)[0]
            
            # Ler header e reconstruir mapa de frequência
            header_bytes = file.read(header_length)
            frequency = json.loads(header_bytes.decode('utf-8'))
            
            # Reconstruir árvore Huffman
            self.heap = []
            self.codes = {}
            self.reverse_mapping = {}
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()

            # Ler o corpo binário
            bit_string = ""
            byte = file.read(1)
            while(len(byte) > 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)
            decompressed_text = self.decode_text(encoded_text)

            with open(output_path, 'w', encoding='utf-8') as output:
                output.write(decompressed_text)
            
        print("Descompressão finalizada com sucesso.")

# --- Execução via Linha de Comando ---
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python huffman_compressor.py [compress/decompress] [arquivo_entrada] [arquivo_saida]")
        print("Exemplo: python huffman_compressor.py compress livro.txt livro.bin")
        print("Exemplo: python huffman_compressor.py decompress livro.bin recuperado.txt")
        sys.exit(1)

    action = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if not os.path.exists(input_file):
        print(f"Erro: Arquivo '{input_file}' não encontrado.")
        sys.exit(1)

    h = HuffmanCoding()

    if action == "compress":
        h.compress(input_file, output_file)
    elif action == "decompress":
        h.decompress(input_file, output_file)
    else:
        print("Comando inválido. Use 'compress' ou 'decompress'.")