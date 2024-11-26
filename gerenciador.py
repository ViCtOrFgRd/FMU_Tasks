import sqlite3
import parse
from tkinter import Tk, Label, Entry, Button, Toplevel, messagebox, END, StringVar
from tkinter import ttk
from datetime import datetime

# Banco de dados
class TaskDB:
    def __init__(self):
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT CHECK(status IN ('Não Iniciado', 'Em Andamento', 'Concluído')),
                request TEXT,
                priority TEXT CHECK(priority IN ('Baixo', 'Médio', 'Alto')),
                due_date DATE
            )
        """)
        self.conn.commit()

    def add_task(self, name, description, status, request, priority, due_date):
        self.cursor.execute("""
            INSERT INTO tasks (name, description, status, request, priority, due_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, description, status, request, priority, due_date))
        self.conn.commit()

    def get_tasks(self, filter_status=None):
        if filter_status:
            self.cursor.execute("SELECT * FROM tasks WHERE status = ?", (filter_status,))
        else:
            self.cursor.execute("SELECT * FROM tasks")
        return self.cursor.fetchall()

    def update_task(self, task_id, name, description, status, request, priority, due_date):
        self.cursor.execute("""
            UPDATE tasks
            SET name = ?, description = ?, status = ?, request = ?, priority = ?, due_date = ?
            WHERE id = ?
        """, (name, description, status, request, priority, due_date, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()


# Interface gráfica
class TaskApp:
    def __init__(self, root):
        self.db = TaskDB()
        self.root = root
        self.root.title("Gerenciador de Tarefas")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f4f4")
        self.root.iconbitmap("icon.ico")
        style = ttk.Style()
        style.theme_use("default")  

        # Título
        Label(self.root, text="Gerenciador de Tarefas", font=("Helvetica", 18, "bold"), bg="#f4f4f4").pack(pady=10)

        # Filtros
        self.filter_var = ttk.Combobox(self.root, values=["Todos", "Não Iniciado", "Em Andamento", "Concluído"], state="readonly")
        self.filter_var.set("Todos")
        self.filter_var.pack(pady=5)
        self.filter_var.bind("<<ComboboxSelected>>", self.filter_tasks)

        # Tabela de tarefas
        columns = ("ID", "Nome", "Descrição", "Status", "Responsável", "Prioridade", "Data de Conclusão")
        self.task_table = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        self.task_table.pack(padx=10, pady=10, fill="both", expand=True)

        for col in columns:
            self.task_table.heading(col, text=col.capitalize())
            self.task_table.column(col, anchor="center", width=100)

        # Botões de ação
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        Button(button_frame, text="Adicionar Tarefa", command=self.open_add_task_window, width=15).grid(row=0, column=0, padx=5)
        Button(button_frame, text="Editar Tarefa", command=self.edit_task, width=15).grid(row=0, column=1, padx=5)
        Button(button_frame, text="Excluir Tarefa", command=self.delete_task, width=15).grid(row=0, column=2, padx=5)

        self.load_tasks()

    def load_tasks(self):
        for row in self.task_table.get_children():
            self.task_table.delete(row)

        tasks = self.db.get_tasks()
        for task in tasks:
            self.task_table.insert("", "end", values=(
                task[0], task[1], task[2], task[3], task[4], task[5], datetime.strptime(task[6], "%Y-%m-%d").strftime("%d/%m/%Y")
            ))

    def filter_tasks(self, event=None):
        filter_status = self.filter_var.get()
        tasks = self.db.get_tasks(filter_status if filter_status != "Todos" else None)

        for row in self.task_table.get_children():
            self.task_table.delete(row)

        for task in tasks:
            self.task_table.insert("", "end", values=(
                task[0], task[1], task[2], task[3], task[4], task[5], datetime.strptime(task[6], "%Y-%m-%d").strftime("%d/%m/%Y")
            ))

    def open_task_window(self, title, task=None):
        window = Toplevel(self.root)
        window.title(title)
        window.geometry("400x450")
        window.configure(bg="#f4f4f4")

        fields = [
            ("Nome da Tarefa:", "name"),
            ("Descrição:", "description"),
            ("Status:", "status"),
            ("Responsável:", "request"),
            ("Prioridade:", "priority"),
            ("Data de Vencimento (dd/mm/yyyy):", "due_date"),
        ]

        entries = {}
        for label_text, field in fields:
            Label(window, text=label_text, bg="#f4f4f4").pack(pady=5)

            if field in ["status", "priority"]:
                values = ["Não Iniciado", "Em Andamento", "Concluído"] if field == "status" else ["Baixo", "Médio", "Alto"]
                entries[field] = ttk.Combobox(window, values=values, state="readonly")
                entries[field].pack(pady=5)
            else:
                entries[field] = Entry(window)
                entries[field].pack(pady=5)

        if task:
            entries["name"].insert(0, task[1])
            entries["description"].insert(0, task[2])
            entries["status"].set(task[3])
            entries["request"].insert(0, task[4])
            entries["priority"].set(task[5])
            entries["due_date"].insert(0, datetime.strptime(task[6], "%Y-%m-%d").strftime("%d/%m/%Y"))

        def save_changes():
            name = entries["name"].get()
            description = entries["description"].get()
            status = entries["status"].get()
            request = entries["request"].get()
            priority = entries["priority"].get()
            due_date = entries["due_date"].get()

            try:
                parsed_date = datetime.strptime(due_date, "%d/%m/%Y").strftime("%Y-%m-%d")
                if name and parsed_date:
                    if task:
                        self.db.update_task(task[0], name, description, status, request, priority, parsed_date)
                    else:
                        self.db.add_task(name, description, status, request, priority, parsed_date)
                    self.load_tasks()
                    window.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Data de vencimento inválida!")

        Button(window, text="Salvar", command=save_changes, bg="#4CAF50", fg="white").pack(pady=20)

    def open_add_task_window(self):
        self.open_task_window("Adicionar Tarefa")

    def edit_task(self):
        selected = self.task_table.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Nenhuma tarefa selecionada.")
            return

        task_id = int(self.task_table.item(selected[0], "values")[0])
        task = next((t for t in self.db.get_tasks() if t[0] == task_id), None)
        if task:
            self.open_task_window("Editar Tarefa", task)

    def delete_task(self):
        selected = self.task_table.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Nenhuma tarefa selecionada.")
            return

        task_id = int(self.task_table.item(selected[0], "values")[0])
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta tarefa?"):
            self.db.delete_task(task_id)
            self.load_tasks()


# Rodar a aplicação
if __name__ == "__main__":
    root = Tk()
    app = TaskApp(root)
    root.mainloop()
