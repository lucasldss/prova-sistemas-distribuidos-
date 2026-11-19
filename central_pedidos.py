import threading
import time

# Servidores simulados
principal = {"online": True, "estoque": 10}
replica = {"online": True, "estoque": 10}

# Controle de concorrência
MAXIMO_SIMULTANEO = 3
semaforo = threading.Semaphore(MAXIMO_SIMULTANEO)
trava = threading.Lock()
pedidos_confirmados = []


def processar_pedido(numero):
    # Semáforo: no máximo 3 pedidos sendo processados ao mesmo tempo
    with semaforo:
        time.sleep(0.1)  # simula o tempo de processamento

        # Lock: garante que a checagem e a baixa de estoque sejam atômicas
        with trava:
            if principal["estoque"] > 0:
                principal["estoque"] -= 1
                pedidos_confirmados.append(numero)


def sincronizar():
    replica["estoque"] = principal["estoque"]


def consultar_estoque():
    if principal["online"]:
        return "PRINCIPAL", principal["estoque"]
    if replica["online"]:
        return "REPLICA", replica["estoque"]
    return "INDISPONIVEL", None


if __name__ == "__main__":
    print("=== CENTRAL DE PEDIDOS ===")
    print("Limite simultaneo:", MAXIMO_SIMULTANEO)
    print("Estoque inicial:", principal["estoque"])

    trabalhadores = [
        threading.Thread(target=processar_pedido, args=(numero,))
        for numero in [101, 102, 103, 104, 105, 106]
    ]

    for trabalhador in trabalhadores:
        trabalhador.start()

    for trabalhador in trabalhadores:
        trabalhador.join()

    print("Pedidos confirmados:", sorted(pedidos_confirmados))
    print("Estoque principal:", principal["estoque"])
    print("Replica antes:", replica["estoque"])

    sincronizar()

    print("Replica depois:", replica["estoque"])

    # Simulação de falha do servidor principal
    principal["online"] = False

    nome, estoque = consultar_estoque()
    print("Consulta apos falha:", nome, estoque)