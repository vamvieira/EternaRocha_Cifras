import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

DB_FILE = "musicas.db"

# Criação e conexão ao banco
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS musicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            artista TEXT NOT NULL,
            cifra TEXT NOT NULL
        )
    ''')

    # Verificar se o banco está vazio
    c.execute("SELECT COUNT(*) FROM musicas")
    if c.fetchone()[0] == 0:
        musicas_exemplo = [
            ("Porque Ele Vive", "Harpa Cristã", """C       Am   Dm      G
Deus enviou Seu Filho amado
     C      Am     Dm     G
Pra me salvar e perdoar
   C       C7         F
Na cruz morreu por meus pecados
    C        G        C
Mas ressurgiu e vivo com o Pai está"""),

            ("Grandioso És Tu", "Harpa Cristã", """C         G       C
Senhor meu Deus, quando eu maravilhado
     F        C        G
Contemplo a Tua imensa criação
  C         G         C
O céu azul de estrelas pontilhado
    F        C     G     C
O Teu poder mostrando a criação"""),

            ("Tu És Fiel, Senhor", "Harpa Cristã", """C        G      C
Tu és fiel, Senhor, meu Pai celeste
   F       C       G
Pleno poder aos Teus filhos darás
C        G       C
Nunca mudaste, Tu nunca faltaste
    F        C      G     C
Tal como eras, Tu sempre serás""")
        ]

        c.executemany("INSERT INTO musicas (titulo, artista, cifra) VALUES (?, ?, ?)", musicas_exemplo)

    conn.commit()
    conn.close()

def get_musicas():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, titulo, artista FROM musicas")
    dados = c.fetchall()
    conn.close()
    return dados

def get_musica_by_id(mid):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT titulo, artista, cifra FROM musicas WHERE id = ?", (mid,))
    m = c.fetchone()
    conn.close()
    return m

def add_musica(titulo, artista, cifra):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO musicas (titulo, artista, cifra) VALUES (?, ?, ?)", (titulo, artista, cifra))
    conn.commit()
    conn.close()

# Interface
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Eterna Rocha Cifra")

        self.tree = ttk.Treeview(root, columns=("Título", "Artista"), show='headings')
        self.tree.heading("Título", text="Título")
        self.tree.heading("Artista", text="Artista")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind('<Double-1>', self.ver_detalhes)

        btn_add = tk.Button(root, text="Adicionar Nova Música", command=self.adicionar_musica)
        btn_add.pack(pady=10)

        self.carregar_musicas()

    def carregar_musicas(self):
        self.tree.delete(*self.tree.get_children())
        for mid, titulo, artista in get_musicas():
            self.tree.insert('', 'end', iid=mid, values=(titulo, artista))

    def ver_detalhes(self, event):
        selecionado = self.tree.focus()
        if selecionado:
            titulo, artista, cifra = get_musica_by_id(selecionado)
            messagebox.showinfo(f"{titulo} - {artista}", cifra)

    def adicionar_musica(self):
        titulo = simpledialog.askstring("Título", "Digite o título da música:")
        artista = simpledialog.askstring("Artista", "Digite o nome do artista:")
        cifra = simpledialog.askstring("Cifra", "Digite a cifra completa:")

        if titulo and artista and cifra:
            add_musica(titulo, artista, cifra)
            self.carregar_musicas()

# Inicialização
if __name__ == '__main__':
    init_db()
    root = tk.Tk()
    app = App(root)
    root.mainloop()

