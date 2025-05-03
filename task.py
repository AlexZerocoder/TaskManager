import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


#Классы задач
class Task:
    def __init__(self, description, deadline=None, completed=False):
        if not description:
            raise ValueError("Описание задачи не может быть пустым")

        self.description = description
        self.completed = completed

        if deadline:
            if isinstance(deadline, str):
                try:
                    self.deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Формат даты должен быть 'ГГГГ-ММ-ДД'")
            elif isinstance(deadline, datetime.date):
                self.deadline = deadline
            else:
                raise ValueError("Срок должен быть строкой в формате 'ГГГГ-ММ-ДД' или объектом datetime.date")
        else:
            self.deadline = None

    def mark_completed(self):
        self.completed = True

    def mark_incomplete(self):
        self.completed = False

    def is_completed(self):
        return self.completed

    def is_overdue(self):
        if self.deadline and not self.completed:
            return self.deadline < datetime.date.today()
        return False

    def __str__(self):
        status = "✓" if self.completed else "✗"
        deadline_str = f" (Срок: {self.deadline})" if self.deadline else ""
        return f"[{status}] {self.description}{deadline_str}"


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description, deadline=None):
        task = Task(description, deadline)
        self.tasks.append(task)
        return task

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
        else:
            raise IndexError("Индекс задачи вне допустимого диапазона")

    def get_all_tasks(self):
        return self.tasks

    def get_incomplete_tasks(self):
        return [task for task in self.tasks if not task.is_completed()]

    def get_completed_tasks(self):
        return [task for task in self.tasks if task.is_completed()]

    def get_overdue_tasks(self):
        return [task for task in self.tasks if task.is_overdue()]

    def mark_task_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
        else:
            raise IndexError("Индекс задачи вне допустимого диапазона")

    def mark_task_incomplete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_incomplete()
        else:
            raise IndexError("Индекс задачи вне допустимого диапазона")


#Графический интерфейс
class TaskApp:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Менеджер задач")

        self.task_listbox = tk.Listbox(root, width=60, height=15)
        self.task_listbox.pack(pady=10)

        button_frame = tk.Frame(root)
        button_frame.pack()

        tk.Button(button_frame, text="Добавить задачу", command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Удалить задачу", command=self.remove_task).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Отметить как выполнено", command=self.mark_completed).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Обновить список", command=self.update_task_list).grid(row=0, column=3, padx=5)

        self.update_task_list()

    def add_task(self):
        desc = simpledialog.askstring("Добавление задачи", "Введите описание:")
        if desc:
            deadline = simpledialog.askstring("Срок", "Введите срок (ГГГГ-ММ-ДД), необязательно:")
            try:
                self.manager.add_task(desc, deadline if deadline else None)
                self.update_task_list()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def remove_task(self):
        index = self.task_listbox.curselection()
        if index:
            try:
                self.manager.remove_task(index[0])
                self.update_task_list()
            except IndexError as e:
                messagebox.showerror("Ошибка", str(e))

    def mark_completed(self):
        index = self.task_listbox.curselection()
        if index:
            try:
                self.manager.mark_task_completed(index[0])
                self.update_task_list()
            except IndexError as e:
                messagebox.showerror("Ошибка", str(e))

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.manager.get_all_tasks():
            self.task_listbox.insert(tk.END, str(task))


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
