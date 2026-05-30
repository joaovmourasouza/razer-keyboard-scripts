import subprocess
import time
import os
from openrazer.client import DeviceManager

TEMPO_LIMITE_SEGUNDOS = 15
BRILHO_ATIVO = 100
PASSO_FADE = 2   
INTERVALO_FADE = 0.02

device_manager = DeviceManager()

def pegar_tempo_ocioso():
    try:
        cmd = "gdbus call --session --dest org.gnome.Mutter.IdleMonitor --object-path /org/gnome/Mutter/IdleMonitor/Core --method org.gnome.Mutter.IdleMonitor.GetIdletime"
        output = subprocess.check_output(cmd, shell=True).decode("utf-8")
        ms = int(output.split()[1].replace(",", "").replace(")", ""))
        return ms / 1000.0
    except Exception:
        return 0

def definir_brilho(valor):
    for device in device_manager.devices:
        try:
            device.brightness = valor
        except Exception:
            pass

def acender_gradualmente(brilho_inicial=0):
    brilho_atual = brilho_inicial
    while brilho_atual < BRILHO_ATIVO:
        brilho_atual += PASSO_FADE
        if brilho_atual > BRILHO_ATIVO:
            brilho_atual = BRILHO_ATIVO
            
        definir_brilho(brilho_atual)
        time.sleep(INTERVALO_FADE)

def apagar_gradualmente():
    brilho_atual = BRILHO_ATIVO
    while brilho_atual > 0:
        if pegar_tempo_ocioso() < TEMPO_LIMITE_SEGUNDOS:
            acender_gradualmente(brilho_atual)
            return False
            
        brilho_atual -= PASSO_FADE
        if brilho_atual < 0:
            brilho_atual = 0
            
        definir_brilho(brilho_atual)
        time.sleep(INTERVALO_FADE)
    return True

luzes_apagadas = False
definir_brilho(BRILHO_ATIVO)

while True:
    tempo_ocioso = pegar_tempo_ocioso()
    
    if tempo_ocioso > TEMPO_LIMITE_SEGUNDOS:
        if not luzes_apagadas:
            if apagar_gradualmente():
                luzes_apagadas = True
    else:
        if luzes_apagadas:
            acender_gradualmente(0)
            luzes_apagadas = False
            
    time.sleep(1)
