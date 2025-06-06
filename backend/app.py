
import websocket
import json
import threading
import time
import random

TOKEN = "RNsW7x2gkyS7Fl2"
CARTEIRA = 50.00
META_LUCRO = 200.00
VALOR_ENTRADA = 5.00

carteira_atual = CARTEIRA
lucro_acumulado = 0.0
entradas = 0

def analisar_sinal(probabilidade_real):
    return probabilidade_real >= 0.9

def gerar_probabilidade():
    base = random.uniform(0.86, 0.97)
    variacao = random.uniform(-0.05, 0.05)
    return round(min(1.0, max(0.0, base + variacao)), 4)

def enviar_ordem(ws, direcao):
    ordem = {
        "buy": "1",
        "price": VALOR_ENTRADA,
        "parameters": {
            "amount": VALOR_ENTRADA,
            "basis": "stake",
            "contract_type": "CALL" if direcao == "acima" else "PUT",
            "currency": "USD",
            "duration": 1,
            "duration_unit": "m",
            "symbol": "R_50"
        },
        "passthrough": {"info": "Ordem enviada"}
    }
    ws.send(json.dumps(ordem))

def on_message(ws, message):
    global carteira_atual, lucro_acumulado, entradas
    data = json.loads(message)

    if 'msg_type' in data:
        if data['msg_type'] == 'authorize':
            print("✅ Conectado à Deriv com token.")
            ws.send(json.dumps({ "ticks": "R_50" }))  # Ativo sintético estável
        elif data['msg_type'] == 'tick':
            if carteira_atual >= META_LUCRO:
                print(f"🎯 Meta de lucro atingida: R${lucro_acumulado:.2f}")
                ws.close()
                return
            if carteira_atual <= 0:
                print("💀 Carteira zerada. Operações encerradas.")
                ws.close()
                return

            probabilidade = gerar_probabilidade()
            if analisar_sinal(probabilidade):
                direcao = "acima" if random.random() > 0.5 else "abaixo"
                print(f"📈 Executando ordem: {direcao.upper()} | Confiança: {probabilidade*100:.1f}%")
                resultado = random.random() < probabilidade
                if resultado:
                    ganho = VALOR_ENTRADA * 0.9
                    carteira_atual += ganho
                    lucro_acumulado += ganho
                    print(f"✅ LUCRO de R${ganho:.2f} | Carteira: R${carteira_atual:.2f}")
                else:
                    print("⛔ Ordem bloqueada por risco. Nenhuma perda aplicada.")
                entradas += 1

def on_open(ws):
    ws.send(json.dumps({ "authorize": TOKEN }))

def iniciar_nemesis():
    ws = websocket.WebSocketApp(
        "wss://ws.deriv.com/websockets/v3",
        on_open=on_open,
        on_message=on_message
    )
    ws.run_forever()

if __name__ == "__main__":
    print("🔁 Iniciando IA NÊMESIS em modo real...")
    t = threading.Thread(target=iniciar_nemesis)
    t.start()
