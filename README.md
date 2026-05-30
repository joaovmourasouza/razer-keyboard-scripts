# ⌨️ Razer Keyboard Idle Dimmer

Um script leve e inteligente em Python para automatizar o brilho de teclados Razer no Linux. Ele monitora a inatividade do usuário e apaga a iluminação do teclado gradualmente (efeito *fade-out*) após um tempo limite, reativando a iluminação instantaneamente (efeito *fade-in*) ao detectar qualquer atividade.

---

## ✨ Funcionalidades

- **Esmaecimento Gradual (*Fade-out*):** Diminui a intensidade do brilho suavemente ao entrar em estado de inatividade.
- **Retorno Suave (*Fade-in*):** Restaura o brilho original de forma fluida assim que o usuário interage com o computador.
- **Detecção Eficiente de Inatividade:** Utiliza a API nativa do GNOME Mutter (`org.gnome.Mutter.IdleMonitor`) via D-Bus para um monitoramento extremamente leve e sem consumo excessivo de CPU.
- **Compatibilidade:** Funciona com qualquer dispositivo Razer compatível com o ecossistema OpenRazer.

---

## 🛠️ Requisitos do Sistema

Para rodar este script, você precisará de:

1. **Sistema Operacional:** Linux
2. **Ambiente Desktop:** GNOME (ou qualquer ambiente que utilize o gerenciador de janelas Mutter e forneça o serviço D-Bus `IdleMonitor`)
3. **Drivers & Daemon:** OpenRazer instalado e configurado
4. **Ferramenta de Linha de Comando:** `gdbus` (geralmente pré-instalado em distribuições com GNOME)

---

## 🚀 Instalação e Configuração

### 1. Instalar o OpenRazer e a biblioteca Python

O OpenRazer precisa ser instalado diretamente pelo gerenciador de pacotes do seu sistema operacional para configurar corretamente os módulos do kernel e o daemon de sistema.

#### **Ubuntu / Debian / Pop!_OS**
```bash
sudo add-apt-repository ppa:openrazer/stable
sudo apt update
sudo apt install openrazer-meta python3-openrazer
```

#### **Fedora**
```bash
sudo dnf copr enable openrazer/stable
sudo dnf install openrazer-daemon python3-openrazer
```

#### **Arch Linux**
```bash
yay -S openrazer-daemon python3-openrazer
```

*(Para outras distribuições, consulte o site oficial do [OpenRazer](https://openrazer.github.io/))*

### 2. Configurar Permissões do Usuário

O daemon do OpenRazer requer que seu usuário faça parte do grupo `plugdev` para acessar os dispositivos de hardware USB com segurança.

Adicione o seu usuário atual ao grupo `plugdev`:
```bash
sudo gpasswd -a $USER plugdev
```

> [!IMPORTANT]
> Após adicionar o usuário ao grupo, você **deve reiniciar o computador** ou fazer logoff e login novamente para aplicar as novas permissões.

---

## 💻 Como Usar

### Execução Manual
Com o daemon do OpenRazer em execução e seu teclado conectado, basta executar o script diretamente no terminal:

```bash
python3 script.py
```

### Configurações Personalizadas
Você pode ajustar o comportamento do script alterando as constantes localizadas no início do arquivo `script.py`:

```python
TEMPO_LIMITE_SEGUNDOS = 15  # Tempo de ociosidade em segundos para iniciar o fade-out
BRILHO_ATIVO = 100          # Intensidade do brilho normal quando ativo (0 a 100)
PASSO_FADE = 2              # A velocidade de mudança de brilho por iteração
INTERVALO_FADE = 0.02       # A suavidade da transição de fade (tempo de espera em segundos por passo)
```

---

## ⚙️ Inicialização Automática (Background)

Para garantir que o script sempre rode em segundo plano ao ligar o computador, você pode configurá-lo como um serviço de usuário do `systemd`.

1. Crie o diretório de serviços do usuário (se ainda não existir):
   ```bash
   mkdir -p ~/.config/systemd/user/
   ```

2. Crie o arquivo de serviço `~/.config/systemd/user/razer-idle-dimmer.service` com o seguinte conteúdo:
   ```ini
   [Unit]
   Description=Razer Keyboard Idle Dimmer Service
   After=graphical-session.target

   [Service]
   Type=simple
   ExecStart=/usr/bin/python3 /home/jvms/Projects/razer-keyboard-scripts/script.py
   Restart=on-failure
   RestartSec=5

   [Install]
   WantedBy=default.target
   ```

   *(Nota: Certifique-se de ajustar o caminho no `ExecStart` caso mova o script de diretório)*

3. Recarregue o systemd, ative e inicie o serviço:
   ```bash
   systemctl --user daemon-reload
   systemctl --user enable razer-idle-dimmer.service
   systemctl --user start razer-idle-dimmer.service
   ```

4. Para verificar se está rodando perfeitamente:
   ```bash
   systemctl --user status razer-idle-dimmer.service
   ```

---

## 📄 Licença

Este projeto é de uso livre e sob a licença MIT. Sinta-se à vontade para clonar, modificar e distribuir.
