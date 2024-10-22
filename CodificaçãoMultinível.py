import matplotlib.pyplot as plt

# Função para converter o texto em binário usando ASCII
def text_to_binary(text):
    binary_text = ''.join(format(ord(c), '08b') for c in text)
    return binary_text

def convert_to_hex(binary):
    # Inicializa uma string para armazenar os valores hexadecimais
    hex_values = ''

    # Divide a sequência em partes de 8 bits
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]  # Pega 8 bits de cada vez
        decimal_value = int(byte, 2)  # Converte para decimal
        hex_value = hex(decimal_value)[2:].upper()  # Converte para hexadecimal
        hex_values += hex_value  # Concatena o valor hexadecimal na string

    return hex_values

def convert(element):
    if element == '0':
        return 0
    elif element == '-':
        return -1
    elif element == '+':
        return 1

hex_to_signal = {}

# Dicionário para mapear os símbolos para números
simbolo_para_numero = {
    '+': 1,
    '-': -1,
    '0': 0
}

# Função para converter a string de símbolos em uma lista de números
def converter_para_lista_numeros(simbolo_str):
    return [simbolo_para_numero[char] for char in simbolo_str]

with open('source.txt', 'r') as arquivo:
    for linha in arquivo.readlines():  # Lê o arquivo linha por linha
        linha = linha.strip()  # Remove espaços em branco no início e no fim de cada linha
        pares = linha.split()  # Divide a linha em pares de valores
        for i in range(0, len(pares), 2):
            chave = pares[i]  # O código, ex: '00'
            valor = pares[i+1]  # O padrão de símbolos, ex: '-+00-+'
            hex_to_signal[chave] = converter_para_lista_numeros(valor)

# Função para gerar gráfico de um sinal
def plot_signal(signal, title):
    time = list(range(len(signal) + 1))  # Um tempo adicional para a última transição
    extended_signal = signal + [signal[-1]]  # Repete o último valor para manter a duração

    # Adiciona mais um tempo para garantir que o último valor fique por um período
    time.append(len(signal))
    
    # Gerar gráfico usando step() com transição pós-ponto
    plt.step(time, extended_signal + [extended_signal[-1]], where='post')
    plt.title(title)
    plt.xlabel('Tempo')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

def calculate_weight(sequence):
    weight = 0
    for symbol in sequence:
        if symbol == 1:
            weight += 1
        elif symbol == -1:
            weight -= 1
    return weight

def invert_sequence(sequence):
    inverted = []
    for symbol in sequence:
        print(symbol)
        if symbol == 1:
            inverted.extend([-1])
        elif symbol == -1:
            inverted.extend([1])
        else:
            inverted.extend([0])
    return inverted

# Codificação 2B1Q
def encode_2B1Q(binary):
    # Dicionário para mapear pares de bits para níveis de sinal
    bit_to_signal_positive = {
        '00': 1,
        '01': 3,
        '10': -1,
        '11': -3
    }

    print('A')
    print(bit_to_signal_positive)
    print('A')

    bit_to_signal_negative = {
        '00': -1,
        '01': -3,
        '10': 1,
        '11': 3
    }
    
    # Lista para armazenar os níveis de sinal
    signal = []
    
    #Sinal anterior para saber se haverá inversão de sinal ou não
    prev_positive = True 

    # Dividir a string binária em pares de 2 bits
    for i in range(0, len(binary), 2):
        bit_pair = binary[i:i+2]
        
        # Garantir que o último par tenha 2 bits (completar com zero, se necessário)
        if len(bit_pair) < 2:
            bit_pair = bit_pair + '0'

        # Escolher o próximo nível de sinal com base no nível anterior
        if prev_positive:
            current_signal = bit_to_signal_positive[bit_pair]
        else:
            current_signal = bit_to_signal_negative[bit_pair]
        
        signal.append(current_signal)
        
        # Alternar a variável para indicar o nível do próximo sinal
        prev_positive = current_signal > 0

    return signal

# Codificação MLT3
def encode_MLT3(binary):
    signal = []
    current_level = 0
    prev_non_zero_positive = False

    for bit in binary:
        if bit == '1' and current_level != 0:
            signal.append(0 )
            current_level = 0
        elif bit == '1' and current_level == 0:
            if prev_non_zero_positive:
                signal.append(-1)
                current_level = -1
                prev_non_zero_positive = False
            else:
                signal.append(1)
                current_level = 1
                prev_non_zero_positive = True
        else:
            signal.append(current_level)
    return signal

# Codificação 4DPAM5
def encode_4DPAM5(binary):
    signal = []
    # Mapeamento de pares de bits para os níveis de amplitude (-2, -1, 0, 1, 2)
    bit_to_signal = {
        '00': -2,
        '01': 1,
        '10': -1,
        '11': 2
    }
    
    # Iterar pelos pares de bits
    for i in range(0, len(binary), 2):
        bit_pair = binary[i:i+2]
        if len(bit_pair) < 2:
            bit_pair += '0'  # Completar com zero se o par for incompleto
        
        # Converter o par de bits no nível de sinal correspondente
        current_signal = bit_to_signal.get(bit_pair, 0)  # Usar 0 como fallback
        signal.append(current_signal)

    return signal

# Codificação 8B6T
def encode_8B6T(binary):
    # Mapeamento simples de blocos de 8 bits para sequências de 6 níveis (-1, 0, 1)
    hex = convert_to_hex(binary)
    signal = []
    # Processar os blocos de 8 bits do binário
    weight_prev_byte = 0
    weight_byte = 0
    for i in range(0, len(hex), 2):
        byte_hex = hex[i:i+2]
        weight_byte = calculate_weight(hex_to_signal[byte_hex])
        if weight_byte == 1 and weight_prev_byte == 1:
            print(invert_sequence(hex_to_signal[byte_hex]))
            signal.extend(invert_sequence(hex_to_signal[byte_hex]))
        else:
            signal.extend(hex_to_signal[byte_hex])
        weight_prev_byte = weight_byte    
    return signal

# Função principal
def main():
    text = input("Digite um texto (até 4 caracteres): ")
    binary_text = text_to_binary(text)

    #binary_text = '000100010101001101010000'

    # Aplicar cada técnica de codificação
    signal_2B1Q = encode_2B1Q(binary_text)
    signal_MLT3 = encode_MLT3(binary_text)
    signal_4DPAM5 = encode_4DPAM5(binary_text)
    signal_8B6T = encode_8B6T(binary_text)

    print(f"Binário: {binary_text}")
    print(f"Sinal 2B1Q {signal_2B1Q}")
    print(f"Sinal MLT3 {signal_MLT3}")
    print(f"Sinal 4DPAM5 {signal_4DPAM5}")
    print(f"Signal 8B6T {signal_8B6T}")

    # Gerar gráficos
    plot_signal(signal_2B1Q, "Codificação 2B1Q")
    plot_signal(signal_MLT3, "Codificação MLT3")
    plot_signal(signal_4DPAM5, "Codificação 4DPAM5")
    plot_signal(signal_8B6T, "Codificação 8B6T")

if __name__ == "__main__":
    main()
