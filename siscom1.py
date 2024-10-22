import numpy as np
import matplotlib.pyplot as plt

# Definição das variáveis
bandwidths = [3e6, 10e6, 20e6]  # Larguras de banda em Hz
snr_db = np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50])  # SNR em dB
snr_linear = 10 ** (snr_db / 10)  # Converter SNR de dB para escala linear

# Teorema de Shannon: C = B * log2(1 + SNR)
def shannon_capacity(bandwidth, snr):
    return bandwidth * np.log2(1 + snr)

# Calcular a capacidade do canal para cada largura de banda e SNR
capacities = [shannon_capacity(bw, snr_linear) for bw in bandwidths]

# Plotar o gráfico
plt.figure(figsize=(10, 6))

# Plotar para cada largura de banda
for i, bw in enumerate(bandwidths):
    plt.plot(snr_db, capacities[i] / 1e6, label=f'{bw / 1e6} MHz', marker='o')  # Adiciona marcadores nos pontos de SNR

plt.title('Capacidade do Canal vs SNR (Teorema de Shannon)')
plt.xlabel('SNR (dB)')
plt.ylabel('Capacidade do Canal (Mbps)')
plt.grid(True, which='both', linestyle='--', linewidth=0.7)  # Grid mais visível e detalhado
plt.xticks(snr_db)  # Garante que todas as SNRs sejam mostradas no eixo X
plt.legend(title='Largura de Banda')
plt.show()
