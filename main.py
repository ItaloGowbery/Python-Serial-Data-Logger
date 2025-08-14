import serial
import serial.tools.list_ports
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog
import ttkbootstrap as tb
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Variáveis globais ---
ser = None
baud_rate = 9600
running = False
data = []
tempo_total = 0

# --- Funções de porta serial ---
def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def atualizar_portas():
    portas = list_serial_ports()
    porta_menu['values'] = portas
    if portas:
        porta_menu.current(0)

# --- Funções principais ---
def start_reading():
    global ser, running, data, tempo_total

    port = porta_var.get()
    if not port:
        status_label.config(text="Selecione uma porta antes de iniciar.")
        return

    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        running = True
        data = []
        tempo_total = 0
        start_btn.config(state="disabled")
        stop_btn.config(state="normal")
        status_label.config(text=f"Lendo dados de {port}...")

        threading.Thread(target=read_serial, daemon=True).start()
    except serial.SerialException as e:
        status_label.config(text=f"Erro: porta em uso ou inacessível ({e})")

def read_serial():
    global running, data, ser, tempo_total

    while running:
        try:
            if ser.in_waiting:
                line = ser.readline().decode("utf-8", errors='replace').strip()
                print(line)  # mantém saída no terminal
                valores = line.split(",")

                if len(valores) == 6:
                    tempo_total += 1
                    inserir_tabela(tempo_total, valores)
                    atualizar_grafico()
        except Exception as e:
            status_label.config(text=f"Erro na leitura: {e}")
            break

def stop_and_save():
    global running, ser, data

    running = False
    if ser:
        ser.close()

    start_btn.config(state="normal")
    stop_btn.config(state="disabled")
    status_label.config(text="Leitura parada.")

    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Arquivo texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )

    if filename:
        with open(filename, "w") as f:
            for row in data:
                f.write(",".join(map(str, row)) + "\n")
        status_label.config(text=f"Dados salvos em {filename}")
    else:
        status_label.config(text="Salvamento cancelado.")

# --- Funções auxiliares ---
def inserir_tabela(tempo, valores):
    global data
    linha = [tempo] + [int(v) for v in valores]
    data.append(linha)
    tree.insert("", "end", values=linha)
    tree.yview_moveto(1)

def atualizar_grafico():
    ax.clear()
    ax.set_title("Sensores Arduino")
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Valor (0-1023)")
    ax.set_ylim(0, 1023)

    if not data:
        return

    tempos = [row[0] for row in data]
    nomes = ["MQ3v", "MQ4", "MQ6", "MQ7", "MQ135", "MCU1100"]

    for i, label in enumerate(nomes, start=1):
        valores = [row[i] for row in data]
        ax.plot(tempos, valores, label=label)

    ax.legend()
    canvas.draw()

# --- Interface gráfica ---
root = tb.Window(themename="litera")
root.title("Leitor Serial Arduino")
root.geometry("1200x700")

# Top Frame
top_frame = ttk.Frame(root)
top_frame.pack(side="top", fill="x", pady=5, padx=5)

# Porta selector
porta_var = tk.StringVar()
porta_menu = ttk.Combobox(top_frame, textvariable=porta_var, width=20, state="readonly")
porta_menu.pack(side="right", padx=5)
atualizar_btn = tb.Button(top_frame, text="Atualizar Portas", command=atualizar_portas, bootstyle="secondary")
atualizar_btn.pack(side="right", padx=5)

# Main Frame
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=5, pady=5)

# Treeview
colunas = ["Tempo (s)", "MQ3v", "MQ4", "MQ6", "MQ7", "MQ135", "MCU1100"]
tree = ttk.Treeview(main_frame, columns=colunas, show="headings")
for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")

scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="left", fill="y")

# Gráfico
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=main_frame)
canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

# Footer
footer = ttk.Frame(root)
footer.pack(side="bottom", fill="x", pady=5, padx=5)

start_btn = tb.Button(footer, text="Iniciar", command=start_reading, bootstyle="success")
start_btn.pack(side="left", padx=5)

stop_btn = tb.Button(footer, text="Parar e Salvar", command=stop_and_save, bootstyle="danger", state="disabled")
stop_btn.pack(side="left", padx=5)

status_label = ttk.Label(footer, text="Status: Aguardando...")
status_label.pack(side="right")

# Inicializar lista de portas
atualizar_portas()

root.mainloop()
