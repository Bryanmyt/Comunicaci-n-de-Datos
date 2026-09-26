import tkinter as tk
from tkinter import messagebox
import base64
import random


class SimuladorOSI:

    def __init__(self, root):
        self.root = root

        # ------------------------------------------------------
        # CONFIGURACIÓN DE LA VENTANA
        # ------------------------------------------------------
        self.root.title(
            "Simulador de Encapsulamiento - Modelo OSI | UNEMI 2026"
        )
        self.root.geometry("1400x900")
        self.root.minsize(1150, 750)
        self.root.configure(bg="#0b1f33")

        # ------------------------------------------------------
        # CAPAS DEL MODELO OSI
        # ------------------------------------------------------
        self.capas = [
            (7, "Aplicación", "DATOS"),
            (6, "Presentación", "DATOS"),
            (5, "Sesión", "DATOS"),
            (4, "Transporte", "SEGMENTO"),
            (3, "Red", "PAQUETE"),
            (2, "Enlace de Datos", "TRAMA"),
            (1, "Física", "BITS")
        ]

        # ------------------------------------------------------
        # VARIABLES
        # ------------------------------------------------------
        self.mensaje_original = ""
        self.dato_transformado = ""

        self.indice_encapsulamiento = 0
        self.indice_desencapsulamiento = 0

        self.en_transmision = False
        self.paso_actual = 0

        self.rects_a = []
        self.rects_b = []

        # ------------------------------------------------------
        # CREACIÓN DE LA INTERFAZ
        # ------------------------------------------------------
        self.crear_interfaz()
        self.dibujar_capas()
        self.resetear()

    # ==========================================================
    # CREAR INTERFAZ
    # ==========================================================

    def crear_interfaz(self):

        # ------------------------------------------------------
        # TÍTULO
        # ------------------------------------------------------

        titulo = tk.Label(
            self.root,
            text="UNIVERSIDAD ESTATAL DE MILAGRO - COMUNICACIÓN DE DATOS",
            font=("Arial", 20, "bold"),
            bg="#0b1f33",
            fg="white"
        )

        titulo.pack(pady=(10, 3))

        subtitulo = tk.Label(
            self.root,
            text=(
                "Simulador interactivo de encapsulamiento y "
                "desencapsulamiento del Modelo OSI"
            ),
            font=("Arial", 11),
            bg="#0b1f33",
            fg="#b9d7ea"
        )

        subtitulo.pack()

        # ------------------------------------------------------
        # INFORMACIÓN DEL RECORRIDO
        # ------------------------------------------------------

        nota = tk.Label(
            self.root,
            text=(
                "PC-A: 7 → 1 (ENCAPSULAMIENTO)     |     "
                "CANAL     |     "
                "PC-B: 1 → 7 (DESENCAPSULAMIENTO)"
            ),
            font=("Arial", 10, "bold"),
            bg="#173b5c",
            fg="#ffcc00",
            padx=15,
            pady=8
        )

        nota.pack(fill="x", padx=25, pady=10)

        # ------------------------------------------------------
        # PANEL DE CONTROL
        # ------------------------------------------------------

        control = tk.Frame(
            self.root,
            bg="#0b1f33"
        )

        control.pack(
            fill="x",
            padx=25,
            pady=5
        )

        tk.Label(
            control,
            text="Mensaje:",
            font=("Arial", 11, "bold"),
            bg="#0b1f33",
            fg="white"
        ).pack(
            side="left",
            padx=(0, 8)
        )

        self.entrada = tk.Entry(
            control,
            width=50,
            font=("Arial", 11)
        )

        self.entrada.pack(
            side="left",
            padx=5
        )

        self.entrada.insert(
            0,
            "Datos de Evaluacion UNEMI 2026"
        )

        # ------------------------------------------------------
        # BOTÓN ENVIAR
        # ------------------------------------------------------

        self.boton_enviar = tk.Button(
            control,
            text="ENVIAR",
            command=self.iniciar_transmision,
            bg="#198754",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )

        self.boton_enviar.pack(
            side="left",
            padx=5
        )

        # ------------------------------------------------------
        # BOTÓN PASO A PASO
        # ------------------------------------------------------

        self.boton_paso = tk.Button(
            control,
            text="PASO A PASO",
            command=self.paso_manual,
            bg="#0d6efd",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )

        self.boton_paso.pack(
            side="left",
            padx=5
        )

        # ------------------------------------------------------
        # BOTÓN RESET
        # ------------------------------------------------------

        self.boton_reset = tk.Button(
            control,
            text="RESET",
            command=self.resetear,
            bg="#6c757d",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )

        self.boton_reset.pack(
            side="left",
            padx=5
        )

        # ======================================================
        # CONTENEDOR PRINCIPAL
        # ======================================================

        principal = tk.Frame(
            self.root,
            bg="#0b1f33"
        )

        principal.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=5
        )

        principal.columnconfigure(0, weight=1)
        principal.columnconfigure(1, weight=0)
        principal.columnconfigure(2, weight=1)

        principal.rowconfigure(
            0,
            weight=1
        )

        # ======================================================
        # PC-A
        # ======================================================

        self.frame_a = tk.Frame(
            principal,
            bg="#0b1f33"
        )

        self.frame_a.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5
        )

        tk.Label(
            self.frame_a,
            text="PC-A | EMISOR | ENCAPSULAMIENTO",
            font=("Arial", 12, "bold"),
            bg="#0b1f33",
            fg="#ffcc00"
        ).pack(
            pady=3
        )

        self.canvas_a = tk.Canvas(
            self.frame_a,
            width=560,
            height=145,
            bg="white",
            highlightthickness=1
        )

        self.canvas_a.pack(
            fill="x",
            pady=5
        )

        self.consola_a = tk.Text(
            self.frame_a,
            height=18,
            bg="#111111",
            fg="#00ff66",
            font=("Consolas", 9),
            wrap="word"
        )

        self.consola_a.pack(
            fill="both",
            expand=True,
            pady=5
        )

        # ======================================================
        # CANAL
        # ======================================================

        self.frame_canal = tk.Frame(
            principal,
            bg="#0b1f33"
        )

        self.frame_canal.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=8
        )

        tk.Label(
            self.frame_canal,
            text="CANAL",
            font=("Arial", 10, "bold"),
            bg="#0b1f33",
            fg="white"
        ).pack(
            pady=(55, 3)
        )

        self.canvas_canal = tk.Canvas(
            self.frame_canal,
            width=120,
            height=145,
            bg="#0b1f33",
            highlightthickness=0
        )

        self.canvas_canal.pack()

        self.flecha = self.canvas_canal.create_line(
            10,
            72,
            105,
            72,
            arrow=tk.LAST,
            width=5,
            fill="#adb5bd"
        )

        self.estado_canal = tk.Label(
            self.frame_canal,
            text="ESPERA",
            font=("Arial", 9, "bold"),
            bg="#0b1f33",
            fg="#adb5bd"
        )

        self.estado_canal.pack()

        # ======================================================
        # PC-B
        # ======================================================

        self.frame_b = tk.Frame(
            principal,
            bg="#0b1f33"
        )

        self.frame_b.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=5
        )

        tk.Label(
            self.frame_b,
            text="PC-B | RECEPTOR | DESENCAPSULAMIENTO",
            font=("Arial", 12, "bold"),
            bg="#0b1f33",
            fg="#ffcc00"
        ).pack(
            pady=3
        )

        self.canvas_b = tk.Canvas(
            self.frame_b,
            width=560,
            height=145,
            bg="white",
            highlightthickness=1
        )

        self.canvas_b.pack(
            fill="x",
            pady=5
        )

        self.consola_b = tk.Text(
            self.frame_b,
            height=18,
            bg="#111111",
            fg="#33ccff",
            font=("Consolas", 9),
            wrap="word"
        )

        self.consola_b.pack(
            fill="both",
            expand=True,
            pady=5
        )

        # ======================================================
        # PANEL DE ESTADO
        # ======================================================

        info = tk.Frame(
            self.root,
            bg="#173b5c"
        )

        info.pack(
            fill="x",
            padx=25,
            pady=(5, 12)
        )

        self.estado = tk.Label(
            info,
            text="Estado: listo para transmitir",
            font=("Arial", 10, "bold"),
            bg="#173b5c",
            fg="white"
        )

        self.estado.pack(
            side="left",
            padx=10,
            pady=8
        )

        self.mensaje_final = tk.Label(
            info,
            text="Mensaje recuperado en PC-B: ---",
            font=("Arial", 10, "bold"),
            bg="#173b5c",
            fg="#66d9ff"
        )

        self.mensaje_final.pack(
            side="right",
            padx=10,
            pady=8
        )

    # ==========================================================
    # DIBUJAR LAS CAPAS
    # ==========================================================

    def dibujar_capas(self):

        # ------------------------------------------------------
        # PC-A
        # 7 → 1
        # ------------------------------------------------------

        for i, (numero, nombre, pdu) in enumerate(self.capas):

            x = 8 + i * 78

            rect = self.canvas_a.create_rectangle(
                x,
                35,
                x + 70,
                105,
                fill="#f1f3f5",
                outline="#0b1f33",
                width=2
            )

            self.canvas_a.create_text(
                x + 35,
                52,
                text=f"C{numero}",
                font=("Arial", 9, "bold")
            )

            self.canvas_a.create_text(
                x + 35,
                73,
                text=nombre,
                width=62,
                font=("Arial", 7)
            )

            self.canvas_a.create_text(
                x + 35,
                94,
                text=pdu,
                font=("Arial", 7, "bold")
            )

            self.rects_a.append(rect)

        # ------------------------------------------------------
        # PC-B
        # 1 → 7
        # ------------------------------------------------------

        capas_reversa = list(
            reversed(self.capas)
        )

        for i, (numero, nombre, pdu) in enumerate(
            capas_reversa
        ):

            x = 8 + i * 78

            rect = self.canvas_b.create_rectangle(
                x,
                35,
                x + 70,
                105,
                fill="#f1f3f5",
                outline="#0b1f33",
                width=2
            )

            self.canvas_b.create_text(
                x + 35,
                52,
                text=f"C{numero}",
                font=("Arial", 9, "bold")
            )

            self.canvas_b.create_text(
                x + 35,
                73,
                text=nombre,
                width=62,
                font=("Arial", 7)
            )

            self.canvas_b.create_text(
                x + 35,
                94,
                text=pdu,
                font=("Arial", 7, "bold")
            )

            self.rects_b.append(rect)

    # ==========================================================
    # CONSOLA PC-A
    # ==========================================================

    def log_a(self, texto):

        self.consola_a.insert(
            "end",
            texto + "\n"
        )

        self.consola_a.see("end")

    # ==========================================================
    # CONSOLA PC-B
    # ==========================================================

    def log_b(self, texto):

        self.consola_b.insert(
            "end",
            texto + "\n"
        )

        self.consola_b.see("end")

    # ==========================================================
    # RESET
    # ==========================================================

    def resetear(self):

        self.en_transmision = False

        self.paso_actual = 0

        self.indice_encapsulamiento = 0

        self.indice_desencapsulamiento = 0

        self.mensaje_original = ""

        self.dato_transformado = ""

        self.consola_a.delete(
            "1.0",
            "end"
        )

        self.consola_b.delete(
            "1.0",
            "end"
        )

        # Restaurar colores PC-A

        for rect in self.rects_a:

            self.canvas_a.itemconfig(
                rect,
                fill="#f1f3f5"
            )

        # Restaurar colores PC-B

        for rect in self.rects_b:

            self.canvas_b.itemconfig(
                rect,
                fill="#f1f3f5"
            )

        # Restaurar canal

        self.canvas_canal.itemconfig(
            self.flecha,
            fill="#adb5bd"
        )

        self.estado_canal.config(
            text="ESPERA",
            fg="#adb5bd"
        )

        self.estado.config(
            text="Estado: listo para transmitir"
        )

        self.mensaje_final.config(
            text="Mensaje recuperado en PC-B: ---"
        )

        self.log_a(
            "=============================================="
        )

        self.log_a(
            "        PC-A | EMISOR"
        )

        self.log_a(
            "=============================================="
        )

        self.log_a(
            "Esperando mensaje del usuario..."
        )

        self.log_b(
            "=============================================="
        )

        self.log_b(
            "        PC-B | RECEPTOR"
        )

        self.log_b(
            "=============================================="
        )

        self.log_b(
            "Esperando datos..."
        )

    # ==========================================================
    # INICIAR TRANSMISIÓN
    # ==========================================================

    def iniciar_transmision(self):

        if self.en_transmision:

            return

        mensaje = self.entrada.get().strip()

        if not mensaje:

            messagebox.showwarning(
                "Mensaje vacío",
                "Ingrese un mensaje antes de iniciar la transmisión."
            )

            return

        # Reiniciar variables

        self.resetear()

        self.mensaje_original = mensaje

        self.dato_transformado = mensaje

        self.en_transmision = True

        self.consola_a.delete(
            "1.0",
            "end"
        )

        self.consola_b.delete(
            "1.0",
            "end"
        )

        self.log_a(
            "=============================================="
        )

        self.log_a(
            "        INICIO DE TRANSMISIÓN"
        )

        self.log_a(
            "=============================================="
        )

        self.log_a(
            f"Mensaje original: {mensaje}"
        )

        self.log_a("")

        self.log_b(
            "=============================================="
        )

        self.log_b(
            "        PC-B | RECEPTOR"
        )

        self.log_b(
            "=============================================="
        )

        self.log_b(
            "Esperando la llegada de la información..."
        )

        self.log_b("")

        self.estado.config(
            text="Estado: encapsulando en PC-A..."
        )

        self.boton_enviar.config(
            state="disabled"
        )

        self.encapsular_siguiente()

    # ==========================================================
    # ENCAPSULAMIENTO
    # ==========================================================

    def encapsular_siguiente(self):

        if not self.en_transmision:

            return

        # Si terminó las 7 capas

        if self.indice_encapsulamiento >= 7:

            self.enviar_por_canal()

            return

        i = self.indice_encapsulamiento

        numero, nombre, pdu = self.capas[i]

        # Cambiar color

        self.canvas_a.itemconfig(
            self.rects_a[i],
            fill="#ffcc00"
        )

        # Tiempo simulado

        espera = random.uniform(
            0.01,
            0.10
        )

        # ------------------------------------------------------
        # INFORMACIÓN DE CADA CAPA
        # ------------------------------------------------------

        if numero == 7:

            info = (
                "Datos de aplicación"
            )

        elif numero == 6:

            self.dato_transformado = (
                base64.b64encode(
                    self.dato_transformado.encode(
                        "utf-8"
                    )
                ).decode(
                    "utf-8"
                )
            )

            info = (
                "Codificación Base64: "
                + self.dato_transformado
            )

        elif numero == 5:

            info = (
                "Control de sesión simulado: "
                "SES-001"
            )

        elif numero == 4:

            info = (
                "Header TCP simulado: "
                "SRC=5000 DST=80"
            )

        elif numero == 3:

            info = (
                "Header IP simulado: "
                "SRC=PC-A DST=PC-B"
            )

        elif numero == 2:

            info = (
                "Header Ethernet simulado: "
                "SRC=MAC-A DST=MAC-B"
            )

        else:

            info = (
                "Conversión a bits: "
                + str(
                    len(
                        self.dato_transformado
                    ) * 8
                )
                + " bits aprox."
            )

        # ------------------------------------------------------
        # MOSTRAR INFORMACIÓN
        # ------------------------------------------------------

        self.log_a(
            f"[PC-A] Capa {numero} - {nombre}"
        )

        self.log_a(
            f"       PDU: {pdu}"
        )

        self.log_a(
            f"       Información: {info}"
        )

        self.log_a(
            f"       Wq simulado: {espera:.4f} s"
        )

        self.log_a("")

        self.estado.config(
            text=(
                f"Estado: PC-A procesando "
                f"Capa {numero} - {nombre}"
            )
        )

        self.indice_encapsulamiento += 1

        # Esperar antes de continuar

        self.root.after(
            800,
            lambda idx=i:
            self.finalizar_capa_a(idx)
        )

    # ==========================================================
    # FINALIZAR CAPA PC-A
    # ==========================================================

    def finalizar_capa_a(self, idx):

        if not self.en_transmision:

            return

        self.canvas_a.itemconfig(
            self.rects_a[idx],
            fill="#198754"
        )

        self.encapsular_siguiente()

    # ==========================================================
    # TRANSMISIÓN POR EL CANAL
    # ==========================================================

    def enviar_por_canal(self):

        self.estado.config(
            text=(
                "Estado: información lista; "
                "transmitiendo por el canal..."
            )
        )

        self.canvas_canal.itemconfig(
            self.flecha,
            fill="#ffcc00"
        )

        self.estado_canal.config(
            text="TRANSMITIENDO",
            fg="#ffcc00"
        )

        self.log_a("")

        self.log_a(
            ">>> CANAL: propagación física en curso..."
        )

        self.log_a(
            ">>> Los bits viajan desde PC-A hacia PC-B."
        )

        # Después de 1.5 segundos recibe PC-B

        self.root.after(
            1500,
            self.recibir_en_pcb
        )

    # ==========================================================
    # RECEPCIÓN PC-B
    # ==========================================================

    def recibir_en_pcb(self):

        if not self.en_transmision:

            return

        self.canvas_canal.itemconfig(
            self.flecha,
            fill="#198754"
        )

        self.estado_canal.config(
            text="RECIBIDO",
            fg="#66ff99"
        )

        self.log_b(
            ">>> CANAL: trama de bits recibida."
        )

        self.log_b(
            ">>> Iniciando desencapsulamiento en PC-B."
        )

        self.log_b("")

        self.estado.config(
            text="Estado: desencapsulando en PC-B..."
        )

        self.desencapsular_siguiente()

    # ==========================================================
    # DESENCAPSULAMIENTO
    # ==========================================================

    def desencapsular_siguiente(self):

        if not self.en_transmision:

            return

        # Si terminó las 7 capas

        if self.indice_desencapsulamiento >= 7:

            self.finalizar_transmision()

            return

        i = self.indice_desencapsulamiento

        capas_reversa = list(
            reversed(self.capas)
        )

        numero, nombre, pdu = capas_reversa[i]

        # PC-B está ordenado 1 → 7

        idx = i

        # Cambiar color

        self.canvas_b.itemconfig(
            self.rects_b[idx],
            fill="#ffcc00"
        )

        espera = random.uniform(
            0.01,
            0.10
        )

        # ------------------------------------------------------
        # PROCESAMIENTO DE CADA CAPA
        # ------------------------------------------------------

        if numero == 1:

            info = (
                "Recepción de bits "
                "desde el medio físico"
            )

        elif numero == 2:

            info = (
                "Retiro de Header "
                "Ethernet simulado"
            )

        elif numero == 3:

            info = (
                "Retiro de Header "
                "IP simulado"
            )

        elif numero == 4:

            info = (
                "Retiro de Header "
                "TCP simulado"
            )

        elif numero == 5:

            info = (
                "Procesamiento de "
                "sesión simulado"
            )

        elif numero == 6:

            try:

                self.dato_transformado = (
                    base64.b64decode(
                        self.dato_transformado.encode(
                            "utf-8"
                        )
                    ).decode(
                        "utf-8"
                    )
                )

                info = (
                    "Decodificación Base64: "
                    + self.dato_transformado
                )

            except Exception:

                info = (
                    "Error al decodificar Base64"
                )

        else:

            info = (
                "Entrega de los datos "
                "a la aplicación"
            )

        # ------------------------------------------------------
        # MOSTRAR INFORMACIÓN
        # ------------------------------------------------------

        self.log_b(
            f"[PC-B] Capa {numero} - {nombre}"
        )

        self.log_b(
            f"       PDU: {pdu}"
        )

        self.log_b(
            f"       Acción: {info}"
        )

        self.log_b(
            f"       Wq simulado: {espera:.4f} s"
        )

        self.log_b("")

        self.estado.config(
            text=(
                f"Estado: PC-B procesando "
                f"Capa {numero} - {nombre}"
            )
        )

        self.indice_desencapsulamiento += 1

        self.root.after(
            800,
            lambda idx=i:
            self.finalizar_capa_b(idx)
        )

    # ==========================================================
    # FINALIZAR CAPA PC-B
    # ==========================================================

    def finalizar_capa_b(self, idx):

        if not self.en_transmision:

            return

        self.canvas_b.itemconfig(
            self.rects_b[idx],
            fill="#33ccff"
        )

        self.desencapsular_siguiente()

    # ==========================================================
    # FINALIZAR TRANSMISIÓN
    # ==========================================================

    def finalizar_transmision(self):

        self.en_transmision = False

        self.boton_enviar.config(
            state="normal"
        )

        recuperado = self.dato_transformado

        self.log_b("")

        self.log_b(
            "=================================================="
        )

        self.log_b(
            "             TRANSMISIÓN COMPLETADA"
        )

        self.log_b(
            "=================================================="
        )

        self.log_b(
            f"Mensaje original  : {self.mensaje_original}"
        )

        self.log_b(
            f"Mensaje recuperado: {recuperado}"
        )

        # ------------------------------------------------------
        # COMPARAR MENSAJES
        # ------------------------------------------------------

        if recuperado == self.mensaje_original:

            self.log_b(
                "RESULTADO: ÉXITO"
            )

            self.log_b(
                "El mensaje fue recuperado correctamente."
            )

            self.estado.config(
                text=(
                    "Estado: transmisión "
                    "completada correctamente"
                )
            )

            self.mensaje_final.config(
                text=(
                    "Mensaje recuperado en PC-B: "
                    + recuperado
                )
            )

        else:

            self.log_b(
                "RESULTADO: ERROR"
            )

            self.log_b(
                "El mensaje no coincide."
            )

            self.estado.config(
                text="Estado: error en la recuperación"
            )

            self.mensaje_final.config(
                text=(
                    "Mensaje recuperado en PC-B: ERROR"
                )
            )

        self.log_b(
            "=================================================="
        )

    # ==========================================================
    # MODO PASO A PASO
    # ==========================================================

    def paso_manual(self):

        mensaje = self.entrada.get().strip()

        if not mensaje:

            messagebox.showwarning(
                "Mensaje vacío",
                "Ingrese un mensaje antes de usar PASO A PASO."
            )

            return

        if self.en_transmision:

            return

        # ------------------------------------------------------
        # PRIMER CLIC
        # ------------------------------------------------------

        if self.paso_actual == 0:

            self.resetear()

            self.mensaje_original = mensaje

            self.dato_transformado = mensaje

            self.consola_a.delete(
                "1.0",
                "end"
            )

            self.consola_b.delete(
                "1.0",
                "end"
            )

            self.log_a(
                "=============================================="
            )

            self.log_a(
                "        MODO PASO A PASO"
            )

            self.log_a(
                "=============================================="
            )

            self.log_a(
                f"Mensaje original: {mensaje}"
            )

            self.log_a(
                "Haga clic nuevamente para avanzar."
            )

            self.log_a("")

            self.log_b(
                "=============================================="
            )

            self.log_b(
                "        PC-B | MODO PASO A PASO"
            )

            self.log_b(
                "=============================================="
            )

            self.log_b(
                "Aquí aparecerá el desencapsulamiento."
            )

            self.paso_actual = 1

            self.estado.config(
                text=(
                    "Paso preparado: "
                    "Capa 7 - Aplicación"
                )
            )

            return

        # ------------------------------------------------------
        # PASOS 1 - 7
        # ENCAPSULAMIENTO
        # ------------------------------------------------------

        if 1 <= self.paso_actual <= 7:

            idx = self.paso_actual - 1

            numero, nombre, pdu = self.capas[idx]

            self.canvas_a.itemconfig(
                self.rects_a[idx],
                fill="#198754"
            )

            if numero == 6:

                self.dato_transformado = (
                    base64.b64encode(
                        self.dato_transformado.encode(
                            "utf-8"
                        )
                    ).decode(
                        "utf-8"
                    )
                )

                info = (
                    "Base64: "
                    + self.dato_transformado
                )

            else:

                info = (
                    "Header/Control simulado"
                )

            self.log_a(
                f"[PASO {self.paso_actual}] "
                f"Capa {numero} - {nombre} - {pdu}"
            )

            self.log_a(
                f"Información: {info}"
            )

            self.log_a("")

            # Si llegamos a Física

            if self.paso_actual == 7:

                self.canvas_canal.itemconfig(
                    self.flecha,
                    fill="#ffcc00"
                )

                self.estado_canal.config(
                    text="CANAL",
                    fg="#ffcc00"
                )

                self.log_a(
                    ">>> CANAL: transmisión de bits..."
                )

                self.paso_actual = 8

                self.estado.config(
                    text=(
                        "Encapsulamiento terminado. "
                        "Haga clic para recibir."
                    )
                )

            else:

                self.paso_actual += 1

                siguiente = self.capas[idx + 1]

                self.estado.config(
                    text=(
                        f"Siguiente: Capa "
                        f"{siguiente[0]} - "
                        f"{siguiente[1]}"
                    )
                )

            return

        # ------------------------------------------------------
        # PASO 8
        # CANAL
        # ------------------------------------------------------

        if self.paso_actual == 8:

            self.canvas_canal.itemconfig(
                self.flecha,
                fill="#198754"
            )

            self.estado_canal.config(
                text="RECIBIDO",
                fg="#66ff99"
            )

            self.log_b(
                ">>> CANAL: bits recibidos correctamente."
            )

            self.log_b(
                ">>> Iniciando desencapsulamiento."
            )

            self.paso_actual = 9

            self.estado.config(
                text=(
                    "Haga clic para comenzar "
                    "Capa 1 - Física."
                )
            )

            return

        # ------------------------------------------------------
        # PASOS 9 - 15
        # DESENCAPSULAMIENTO
        # ------------------------------------------------------

        if 9 <= self.paso_actual <= 15:

            idx = self.paso_actual - 9

            capas_reversa = list(
                reversed(self.capas)
            )

            numero, nombre, pdu = (
                capas_reversa[idx]
            )

            self.canvas_b.itemconfig(
                self.rects_b[idx],
                fill="#33ccff"
            )

            # --------------------------------------------------
            # DECODIFICACIÓN BASE64
            # --------------------------------------------------

            if numero == 6:

                try:

                    self.dato_transformado = (
                        base64.b64decode(
                            self.dato_transformado.encode(
                                "utf-8"
                            )
                        ).decode(
                            "utf-8"
                        )
                    )

                    info = (
                        "Base64 decodificado: "
                        + self.dato_transformado
                    )

                except Exception:

                    info = "Error Base64"

            else:

                info = (
                    "Header/Control retirado "
                    "o procesado"
                )

            self.log_b(
                f"[PASO {self.paso_actual - 8}] "
                f"Capa {numero} - "
                f"{nombre} - {pdu}"
            )

            self.log_b(
                f"Acción: {info}"
            )

            self.log_b("")

            # --------------------------------------------------
            # FINAL
            # --------------------------------------------------

            if self.paso_actual == 15:

                self.log_b(
                    "=================================================="
                )

                self.log_b(
                    "            PROCESO COMPLETADO"
                )

                self.log_b(
                    f"Mensaje original: "
                    f"{self.mensaje_original}"
                )

                self.log_b(
                    f"Mensaje recuperado: "
                    f"{self.dato_transformado}"
                )

                if (
                    self.dato_transformado
                    == self.mensaje_original
                ):

                    self.log_b(
                        "RESULTADO: ÉXITO"
                    )

                    self.log_b(
                        "El mensaje fue recuperado correctamente."
                    )

                else:

                    self.log_b(
                        "RESULTADO: ERROR"
                    )

                self.log_b(
                    "=================================================="
                )

                self.estado.config(
                    text=(
                        "Proceso completo: "
                        "mensaje recuperado en PC-B"
                    )
                )

                self.mensaje_final.config(
                    text=(
                        "Mensaje recuperado en PC-B: "
                        + self.dato_transformado
                    )
                )

                self.paso_actual = 16

            else:

                self.paso_actual += 1

                siguiente = capas_reversa[idx + 1]

                self.estado.config(
                    text=(
                        f"Siguiente: Capa "
                        f"{siguiente[0]} - "
                        f"{siguiente[1]}"
                    )
                )


# ==============================================================
# PROGRAMA PRINCIPAL
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SimuladorOSI(root)

    root.mainloop()