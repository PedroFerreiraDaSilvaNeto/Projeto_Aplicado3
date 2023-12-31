import tkinter as tk
from tkinter import ttk
import mariadb

class ProdutoModel:
    def __init__(self):
        self.conexao = mariadb.connect(
            host="localhost",
            user="root",
            password="123456",
            database="trabalhofinal"
        )
        self.cursor = self.conexao.cursor()

    def adicionar_produto(self, nome, marca, quantidade):
        query = "INSERT INTO produtos (nome, marca, quantidade) VALUES (%s, %s, %s)"
        valores = (nome, marca, quantidade)
        self.cursor.execute(query, valores)
        self.conexao.commit()

    def listar_produto(self):
        query = "SELECT id, nome, marca, quantidade FROM produtos"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def listar_produtos_menos_10(self):
        query = "SELECT id, nome, marca, quantidade FROM produtos WHERE quantidade < 10"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def atualizar_produto(self, id, nova_quantidade):
        query = "UPDATE produtos SET quantidade=%s WHERE id=%s"
        valores = (nova_quantidade, id)
        self.cursor.execute(query, valores)
        self.conexao.commit()

    def excluir_produto(self, id):
        query = "DELETE FROM produtos WHERE id=%s"
        valores = (id,)
        self.cursor.execute(query, valores)
        self.conexao.commit()

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.label_usuario = tk.Label(self.frame, text="Usuário:")
        self.label_usuario.grid(row=0, column=0)

        self.entry_usuario = tk.Entry(self.frame)
        self.entry_usuario.grid(row=0, column=1)

        self.label_senha = tk.Label(self.frame, text="Senha:")
        self.label_senha.grid(row=1, column=0)

        self.entry_senha = tk.Entry(self.frame, show="*")
        self.entry_senha.grid(row=1, column=1)

        self.button_login = tk.Button(self.frame, text="Login", command=self.login)
        self.button_login.grid(row=2, column=0, columnspan=2)

    def login(self):
        # Adicione sua lógica de autenticação aqui
        # Exemplo simples: (usuário=admin, senha=admin)
        if self.entry_usuario.get() == "admin" and self.entry_senha.get() == "admin":
            self.abrir_janela_principal()
        else:
            tk.messagebox.showerror("Erro de Login", "Usuário ou senha incorretos")

    def abrir_janela_principal(self):
        self.root.destroy()
        root = tk.Tk()
        app = ProdutoView(root)
        root.mainloop()

class ProdutoView:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Produto")

        self.produto_model = ProdutoModel()

        self.tree = ttk.Treeview(self.root, columns=("ID", "Nome", "Marca", "Quantidade"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("#1", text="Nome")
        self.tree.heading("#2", text="Marca")
        self.tree.heading("#3", text="Quantidade")
        self.tree.pack(padx=10, pady=10)

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.label_nome = tk.Label(self.frame, text="Nome:")
        self.label_nome.grid(row=0, column=0)

        self.entry_nome = tk.Entry(self.frame)
        self.entry_nome.grid(row=0, column=1)

        self.label_marca = tk.Label(self.frame, text="Marca:")
        self.label_marca.grid(row=1, column=0)

        self.entry_marca = tk.Entry(self.frame)
        self.entry_marca.grid(row=1, column=1)

        self.label_quantidade = tk.Label(self.frame, text="Quantidade:")
        self.label_quantidade.grid(row=2, column=0)

        self.entry_quantidade = tk.Entry(self.frame)
        self.entry_quantidade.grid(row=2, column=1)

        self.button_adicionar = tk.Button(self.frame, text="Adicionar", command=self.adicionar_produto)
        self.button_adicionar.grid(row=3, column=0)

        self.button_atualizar = tk.Button(self.frame, text="Atualizar", command=self.atualizar_produto)
        self.button_atualizar.grid(row=3, column=1)

        self.button_excluir = tk.Button(self.frame, text="Excluir", command=self.excluir_produto)
        self.button_excluir.grid(row=3, column=2)

        self.button_listar_menos_10 = tk.Button(self.frame, text="Listar < 10", command=self.listar_menos_10)
        self.button_listar_menos_10.grid(row=4, column=0, columnspan=3, pady=5)

        self.button_listar_todos = tk.Button(self.frame, text="Listar Todos", command=self.listar_todos)
        self.button_listar_todos.grid(row=5, column=0, columnspan=3, pady=5)

        self.carregar_produto()

    def carregar_produto(self):
        self.tree.delete(*self.tree.get_children())
        produtos = self.produto_model.listar_produto()
        for produto in produtos:
            self.tree.insert("", "end", values=produto)

    def listar_menos_10(self):
        self.tree.delete(*self.tree.get_children())
        produtos = self.produto_model.listar_produtos_menos_10()
        for produto in produtos:
            self.tree.insert("", "end", values=produto)

    def listar_todos(self):
        self.tree.delete(*self.tree.get_children())
        produtos = self.produto_model.listar_produto()
        for produto in produtos:
            self.tree.insert("", "end", values=produto)

    def adicionar_produto(self):
        nome = self.entry_nome.get()
        marca = self.entry_marca.get()
        quantidade = self.entry_quantidade.get()
        if nome and marca and quantidade:
            self.produto_model.adicionar_produto(nome, marca, quantidade)
            self.carregar_produto()
        else:
            tk.messagebox.showerror("Erro", "Preencha todos os campos!")

    def atualizar_produto(self):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            id = self.tree.item(item_selecionado, "values")[0]
            nova_quantidade = self.entry_quantidade.get()
            self.produto_model.atualizar_produto(id, nova_quantidade)
            self.carregar_produto()

    def excluir_produto(self):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            id = self.tree.item(item_selecionado, "values")[0]
            self.produto_model.excluir_produto(id)
            self.carregar_produto()

if __name__ == "__main__":
    root_login = tk.Tk()
    login_view = LoginView(root_login)
    root_login.mainloop()