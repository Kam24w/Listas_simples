import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime


class TaskNode:
    """
    Representa un nodo en la lista enlazada.
    Cada nodo contiene una tarea y una referencia al siguiente nodo.
    """
    def __init__(self, task_description, task_id=None):
        self.description = task_description
        self.task_id = task_id or datetime.now().timestamp()
        self.completed = False
        self.next = None  # Puntero al siguiente nodo
    
    def __repr__(self):
        status = "✓" if self.completed else "○"
        return f"{status} {self.description}"


class TaskLinkedList:
    """
    Implementa una lista enlazada simple para tareas.
    La cabeza apunta al primer nodo de la lista.
    """
    def __init__(self):
        self.head = None  # Puntero a la cabeza (primer nodo)
    
    def add_task(self, description):
        """Agrega una nueva tarea al final de la lista."""
        new_node = TaskNode(description)
        
        if self.head is None:
            # Si la lista está vacía, el nuevo nodo es la cabeza
            self.head = new_node
        else:
            # Recorrer la lista hasta encontrar el último nodo
            current = self.head
            while current.next is not None:
                current = current.next
            # Enlazar el nuevo nodo al final
            current.next = new_node
    
    def insert_at_beginning(self, description):
        """Inserta una tarea al inicio de la lista."""
        new_node = TaskNode(description)
        new_node.next = self.head
        self.head = new_node
    
    def toggle_completion(self, task_id):
        """Marca una tarea como completada o no completada."""
        current = self.head
        while current is not None:
            if current.task_id == task_id:
                current.completed = not current.completed
                return True
            current = current.next
        return False
    
    def find_task(self, task_id):
        """Encuentra un nodo específico por ID."""
        current = self.head
        position = 0
        while current is not None:
            if current.task_id == task_id:
                return current, position
            current = current.next
            position += 1
        return None, -1
    
    def count_tasks(self):
        """Cuenta el número de tareas en la lista."""
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count


class TaskManagerUI:
    """
    Interfaz gráfica para gestionar las tareas.
    Visualiza los nodos, punteros y permite interactuar con la lista.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas - Listas Simples Enlazadas")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.task_list = TaskLinkedList()
        
        # Estilos
        style = ttk.Style()
        style.theme_use("clam")
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crea los widgets de la interfaz."""
        
        # Panel superior con entrada de tarea
        top_frame = tk.Frame(self.root, bg="#2c3e50", height=100)
        top_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            top_frame, 
            text="GESTOR DE TAREAS - LISTA ENLAZADA SIMPLE",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=10)
        
        # Frame para entrada de tarea
        input_frame = tk.Frame(top_frame, bg="#2c3e50")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Nueva tarea:", bg="#2c3e50", fg="white").pack(side=tk.LEFT, padx=5)
        
        self.entry_task = tk.Entry(input_frame, width=40, font=("Arial", 10))
        self.entry_task.pack(side=tk.LEFT, padx=5)
        self.entry_task.bind("<Return>", lambda e: self.add_task())
        
        tk.Button(
            input_frame,
            text="Agregar",
            command=self.add_task,
            bg="#27ae60",
            fg="white",
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Panel de información
        info_frame = tk.Frame(self.root, bg="white", relief=tk.SUNKEN, bd=1)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.info_label = tk.Label(
            info_frame,
            text="Cabeza: None | Total de tareas: 0",
            font=("Arial", 10),
            bg="white",
            justify=tk.LEFT
        )
        self.info_label.pack(pady=5)
        
        # Panel principal con scroll
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas con scrollbar
        canvas_frame = tk.Frame(main_frame, bg="white")
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(canvas_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            bg="white",
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.canvas.yview)
        
        self.canvas_frame_content = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.canvas_frame_content, anchor="nw")
        
        def on_frame_configure(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        self.canvas_frame_content.bind("<Configure>", on_frame_configure)
        
        # Panel inferior con botones
        bottom_frame = tk.Frame(self.root, bg="#ecf0f1")
        bottom_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(
            bottom_frame,
            text="Visualizar Memoria",
            command=self.show_memory_visualization,
            bg="#3498db",
            fg="white",
            padx=10
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
    
    def add_task(self):
        """Agrega una nueva tarea a la lista."""
        description = self.entry_task.get().strip()
        
        if not description:
            messagebox.showwarning("Advertencia", "Por favor, ingresa una descripción de tarea.")
            return
        
        self.task_list.add_task(description)
        self.entry_task.delete(0, tk.END)
        self.refresh_display()
    
    def toggle_task(self, task_id):
        """Marca/desmarca una tarea como completada."""
        self.task_list.toggle_completion(task_id)
        self.refresh_display()
    
    def refresh_display(self):
        """Actualiza la visualización de la lista."""
        # Limpiar canvas
        widget = self.canvas_frame_content.winfo_children().__iter__()
        while True:
            try:
                w = next(widget)
                w.destroy()
            except StopIteration:
                break
        
        # Contar tareas y completadas recorriendo con punteros
        total_tasks = 0
        completed_count = 0
        current = self.task_list.head
        while current is not None:
            total_tasks += 1
            if current.completed:
                completed_count += 1
            current = current.next
        
        # Actualizar información
        head_info = "None"
        if self.task_list.head:
            head_info = f"{self.task_list.head.description[:20]}"
        
        self.info_label.config(
            text=f"Cabeza: {head_info} | Total de tareas: {total_tasks} | Tareas completadas: {completed_count}"
        )
        
        # Mostrar cada tarea recorriendo la lista
        if self.task_list.head is None:
            empty_label = tk.Label(
                self.canvas_frame_content,
                text="La lista está vacía",
                font=("Arial", 12),
                fg="#7f8c8d",
                bg="white"
            )
            empty_label.pack(pady=20)
        else:
            index = 0
            current = self.task_list.head
            while current is not None:
                self._create_task_widget(current, index, total_tasks)
                current = current.next
                index += 1

    def _create_task_widget(self, task, index, total):
        """Crea el widget para mostrar una tarea individual."""
        task_frame = tk.Frame(
            self.canvas_frame_content,
            bg="#ecf0f1",
            relief=tk.RAISED,
            bd=1
        )
        task_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Información del nodo
        checkbox_text = "✓" if task.completed else "○"
        checkbox_color = "#27ae60" if task.completed else "#95a5a6"
        
        left_frame = tk.Frame(task_frame, bg="#ecf0f1")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Número de posición
        position_label = tk.Label(
            left_frame,
            text=f"Posición {index}:",
            font=("Arial", 9, "bold"),
            bg="#ecf0f1",
            fg="#34495e"
        )
        position_label.pack(anchor="w")
        
        # Descripción de la tarea
        desc_frame = tk.Frame(left_frame, bg="#ecf0f1")
        desc_frame.pack(anchor="w", pady=2)
        
        tk.Label(
            desc_frame,
            text=checkbox_text,
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            fg=checkbox_color
        ).pack(side=tk.LEFT, padx=5)
        
        desc_text = task.description
        if len(desc_text) > 50:
            desc_text = desc_text[:50] + "..."
        
        desc_label = tk.Label(
            desc_frame,
            text=desc_text,
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        desc_label.pack(side=tk.LEFT)
        
        # Puntero (referencia)
        pointer_label = tk.Label(
            left_frame,
            text=f"ID: {str(task.task_id)[:8]}... | Siguiente: {'→ Nodo' if task.next else 'None'}",
            font=("Arial", 8, "italic"),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        pointer_label.pack(anchor="w", pady=2)
        
        # Botones de acción
        button_frame = tk.Frame(task_frame, bg="#ecf0f1")
        button_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        tk.Button(
            button_frame,
            text="Completar" if not task.completed else "Reabrir",
            command=lambda: self.toggle_task(task.task_id),
            bg="#f39c12" if not task.completed else "#27ae60",
            fg="white",
            width=10,
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=2)
        
    
    def show_memory_visualization(self):
        """Muestra una visualización de la memoria y los punteros."""
        if self.task_list.head is None:
            messagebox.showinfo("Visualización", "La lista está vacía.")
            return
        
        visualization = "=== VISUALIZACIÓN DE MEMORIA ===\n\n"
        visualization += "ESTRUCTURA DE LISTA ENLAZADA SIMPLE:\n\n"
        
        current = self.task_list.head
        position = 0
        total_tasks = 0
        completed_count = 0
        
        # Primera pasada: contar totales
        temp = self.task_list.head
        while temp is not None:
            total_tasks += 1
            if temp.completed:
                completed_count += 1
            temp = temp.next
        
        # Segunda pasada: crear visualización
        current = self.task_list.head
        position = 0
        while current is not None:
            next_addr = "→ [Siguiente]" if current.next else "→ None"
            status = "[COMPLETADA]" if current.completed else "[PENDIENTE]"
            
            visualization += f"┌─ NODO {position} ─────────────────┐\n"
            visualization += f"│ Descripción: {current.description[:20]}\n"
            visualization += f"│ ID: {str(current.task_id)[:8]}...\n"
            visualization += f"│ Estado: {status}\n"
            visualization += f"│ Puntero: {next_addr}\n"
            visualization += f"└──────────────────────────────────┘\n"
            
            if current.next:
                visualization += "        ↓\n"
            
            current = current.next
            position += 1
        
        visualization += "\n--- RESUMEN ---\n"
        visualization += f"Cabeza (head): NODO 0 → {self.task_list.head.description[:20]}\n"
        visualization += f"Total de nodos: {total_tasks}\n"
        visualization += f"Tareas completadas: {completed_count}\n"
        # Crear una nueva ventana para mostrar la visualización
        vis_window = tk.Toplevel(self.root)
        vis_window.title("Visualización de Memoria - Lista Enlazada")
        vis_window.geometry("600x500")
        
        text_widget = tk.Text(
            vis_window,
            font=("Courier New", 9),
            bg="#2c3e50",
            fg="#ecf0f1",
            padx=10,
            pady=10
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(1.0, visualization)
        text_widget.config(state=tk.DISABLED)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerUI(root)
    app.refresh_display()
    root.mainloop()
