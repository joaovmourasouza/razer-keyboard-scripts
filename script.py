import threading
import time
import evdev
from openrazer.client import DeviceManager

TEMPO_LIMITE_SEGUNDOS = 60
BRILHO_ATIVO = 100
PASSO_FADE = 2
INTERVALO_FADE = 0.02

RESPIRACOES = 3
PASSO_RESPIRACAO = 4
INTERVALO_RESPIRACAO = 0.015
PAUSA_RESPIRACAO = 0.25

device_manager = DeviceManager()
ultimo_evento = time.monotonic()

def monitorar_dispositivo(caminho):
    global ultimo_evento
    try:
        dispositivo = evdev.InputDevice(caminho)
        for _ in dispositivo.read_loop():
            ultimo_evento = time.monotonic()
    except (OSError, PermissionError):
        pass

def pegar_tempo_ocioso():
    return time.monotonic() - ultimo_evento

def definir_brilho(valor):
    for device in device_manager.devices:
        try:
            device.brightness = valor
        except Exception:
            pass

def rampa(inicio, destino, passo, intervalo):
    atual = inicio
    direcao = 1 if destino > inicio else -1
    while atual != destino:
        if pegar_tempo_ocioso() < TEMPO_LIMITE_SEGUNDOS:
            return atual, True
        atual += direcao * passo
        if (direcao == 1 and atual > destino) or (direcao == -1 and atual < destino):
            atual = destino
        definir_brilho(atual)
        time.sleep(intervalo)
    return atual, False

def acender_gradualmente(brilho_inicial=0):
    atual = brilho_inicial
    while atual < BRILHO_ATIVO:
        atual += PASSO_FADE
        if atual > BRILHO_ATIVO:
            atual = BRILHO_ATIVO
        definir_brilho(atual)
        time.sleep(INTERVALO_FADE)

def respirar_e_apagar():
    brilho = BRILHO_ATIVO
    for _ in range(RESPIRACOES):
        brilho, interrompido = rampa(brilho, 0, PASSO_RESPIRACAO, INTERVALO_RESPIRACAO)
        if interrompido:
            acender_gradualmente(brilho)
            return False
        time.sleep(PAUSA_RESPIRACAO)

        brilho, interrompido = rampa(brilho, BRILHO_ATIVO, PASSO_RESPIRACAO, INTERVALO_RESPIRACAO)
        if interrompido:
            acender_gradualmente(brilho)
            return False
        time.sleep(PAUSA_RESPIRACAO)

    brilho, interrompido = rampa(brilho, 0, PASSO_FADE, INTERVALO_FADE)
    if interrompido:
        acender_gradualmente(brilho)
        return False
    return True

luzes_apagadas = False
definir_brilho(BRILHO_ATIVO)

for caminho in evdev.list_devices():
    threading.Thread(target=monitorar_dispositivo, args=(caminho,), daemon=True).start()

while True:
    tempo_ocioso = pegar_tempo_ocioso()

    if tempo_ocioso > TEMPO_LIMITE_SEGUNDOS:
        if not luzes_apagadas:
            luzes_apagadas = respirar_e_apagar()
    else:
        if luzes_apagadas:
            acender_gradualmente(0)
            luzes_apagadas = False

    time.sleep(1)
