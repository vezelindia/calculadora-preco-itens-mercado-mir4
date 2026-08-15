# -*- coding: utf-8 -*-
"""
Calculadora de Preço de Venda em Gold - Mir4
Aplicativo desktop (Tkinter). Compile em .exe com PyInstaller.
"""

import tkinter as tk
from tkinter import ttk

# ---------- Cores (tema Mir4) ----------
BG      = "#0b1020"
PANEL   = "#111a33"
EDGE    = "#2f4570"
INK     = "#e8eefc"
INK_DIM = "#94a3c4"
GOLD    = "#f2c14e"
GREEN   = "#4ade80"
RED     = "#f87171"
ACCENT  = "#3a5bd9"


# ---------- Lógica de cálculo ----------
def liquidacao(venda, taxa):
    """Retorna (imposto, liquido) do jeito que o Mir4 arredonda."""
    liquido = round(venda * (1 - taxa))
    imposto = venda - liquido
    if taxa > 0 and imposto < 1:      # imposto mínimo de 1 Gold
        imposto = 1
        liquido = venda - 1
    return imposto, liquido


def preco_para_receber(desejado, taxa):
    """Menor preço de venda cuja liquidação seja >= valor desejado."""
    if taxa <= 0:
        return desejado, 0, desejado
    venda = round(desejado / (1 - taxa))
    while venda > 1 and liquidacao(venda - 1, taxa)[1] >= desejado:
        venda -= 1
    while liquidacao(venda, taxa)[1] < desejado:
        venda += 1
    imposto, liquido = liquidacao(venda, taxa)
    return venda, imposto, liquido


def fmt(n):
    return f"{int(round(n)):,}".replace(",", ".")


# ---------- Interface ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Preço de Venda em Gold Mir4")
        self.configure(bg=BG)
        self.geometry("520x560")
        self.resizable(False, False)

        self.taxa = 0.05
        self.modo = "venda"

        self._build()
        self.calc()

    def _label(self, parent, text, **kw):
        return tk.Label(parent, text=text, bg=kw.pop("bg", BG),
                        fg=kw.pop("fg", INK_DIM), **kw)

    def _build(self):
        # Cabeçalho
        tk.Label(self, text="MERCADO UNIFICADO", bg=BG, fg=GOLD,
                 font=("Segoe UI", 9, "bold")).pack(pady=(18, 2))
        tk.Label(self, text="Calculadora de Preço de Venda em Gold",
                 bg=BG, fg=INK, font=("Segoe UI", 16, "bold")).pack()
        tk.Label(self, text="Mir4 · cálculo de imposto e liquidação",
                 bg=BG, fg=INK_DIM, font=("Segoe UI", 9)).pack(pady=(2, 16))

        card = tk.Frame(self, bg=PANEL, highlightbackground=EDGE,
                        highlightthickness=1)
        card.pack(fill="x", padx=20)
        card.configure(padx=18, pady=18)

        # Modo
        modo_fr = tk.Frame(card, bg=PANEL)
        modo_fr.pack(fill="x")
        self.btn_venda = self._modo_btn(modo_fr, "Anunciei por X → recebo?", "venda")
        self.btn_venda.pack(side="left", expand=True, fill="x", padx=(0, 4))
        self.btn_liq = self._modo_btn(modo_fr, "Quero receber Y → anuncio?", "liquido")
        self.btn_liq.pack(side="left", expand=True, fill="x", padx=(4, 0))

        # Taxa
        self._label(card, "Taxa de imposto do mercado", bg=PANEL, fg=GOLD,
                    font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(16, 6))
        taxa_fr = tk.Frame(card, bg=PANEL)
        taxa_fr.pack(fill="x")
        self.taxa_btns = {}
        for val, txt in [(0.05, "5% (padrão)"), (0.04, "4% (−20%)"), (0.0, "0% (isento)")]:
            b = tk.Button(taxa_fr, text=txt, font=("Segoe UI", 9, "bold"),
                          relief="flat", cursor="hand2",
                          command=lambda v=val: self.set_taxa(v))
            b.pack(side="left", expand=True, fill="x", padx=2)
            self.taxa_btns[val] = b

        # Campo de entrada
        self.lbl_campo = self._label(card, "Preço de venda (anunciado)", bg=PANEL)
        self.lbl_campo.pack(anchor="w", pady=(16, 6))
        self.entry = tk.Entry(card, font=("Segoe UI", 18, "bold"),
                              bg="#0a1122", fg=INK, insertbackground=GOLD,
                              relief="flat", justify="left")
        self.entry.pack(fill="x", ipady=8)
        self.entry.bind("<KeyRelease>", lambda e: self.calc())

        # Resultado
        self.res = tk.Frame(card, bg=PANEL)
        self.res.pack(fill="x", pady=(18, 0))

        tk.Label(self,
                 text="Imposto mín. 1 Gold · valores arredondados como no jogo",
                 bg=BG, fg="#5b6b8f", font=("Segoe UI", 8)).pack(pady=(14, 0))

        self.set_modo("venda")
        self.set_taxa(0.05)

    def _modo_btn(self, parent, text, modo):
        return tk.Button(parent, text=text, font=("Segoe UI", 9, "bold"),
                         relief="flat", cursor="hand2", wraplength=180,
                         command=lambda: self.set_modo(modo))

    def set_modo(self, modo):
        self.modo = modo
        for b, m in [(self.btn_venda, "venda"), (self.btn_liq, "liquido")]:
            on = (m == modo)
            b.configure(bg=ACCENT if on else "#0d152b",
                        fg="#ffffff" if on else INK_DIM)
        self.lbl_campo.configure(
            text="Preço de venda (anunciado)" if modo == "venda"
            else "Quanto você quer receber (líquido)")
        self.calc()

    def set_taxa(self, taxa):
        self.taxa = taxa
        for v, b in self.taxa_btns.items():
            on = (v == taxa)
            b.configure(bg="#1c2a4f" if on else "#0d152b",
                        fg="#ffffff" if on else INK_DIM)
        self.calc()

    def _linha(self, lbl, val, cor=INK, destaque=False):
        fr = tk.Frame(self.res, bg="#12251a" if destaque else PANEL)
        fr.pack(fill="x", pady=(6 if destaque else 2), ipady=8 if destaque else 2)
        tk.Label(fr, text=lbl, bg=fr["bg"],
                 fg="#a7f3c4" if destaque else INK_DIM,
                 font=("Segoe UI", 10)).pack(side="left", padx=8)
        tk.Label(fr, text=val, bg=fr["bg"], fg=cor,
                 font=("Segoe UI", 16 if destaque else 11, "bold")).pack(side="right", padx=8)

    def calc(self):
        for w in self.res.winfo_children():
            w.destroy()

        raw = self.entry.get().strip().replace(".", "").replace(",", "")
        try:
            valor = int(raw) if raw else 0
        except ValueError:
            valor = 0
        if valor <= 0:
            return

        if self.modo == "venda":
            imposto, liquido = liquidacao(valor, self.taxa)
            self._linha("Preço de venda", fmt(valor))
            self._linha(f"Imposto ({self.taxa*100:.0f}%)", "− " + fmt(imposto), RED)
            self._linha("Você recebe", fmt(liquido), GREEN, destaque=True)
        else:
            venda, imposto, liquido = preco_para_receber(valor, self.taxa)
            self._linha("Anuncie por", fmt(venda))
            self._linha(f"Imposto ({self.taxa*100:.0f}%)", "− " + fmt(imposto), RED)
            self._linha("Você recebe", fmt(liquido), GREEN, destaque=True)


if __name__ == "__main__":
    App().mainloop()
