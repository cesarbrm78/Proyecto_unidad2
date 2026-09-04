"""Programa de gestion de tareas
    1-agregar nueva tarea
    2-agregar contenidos a la tarea
    3-mostrar estado de cada tarea
    4-eliminar tarea
    5-eliminar contenido de tarea
    6-Materias
    7-agregar tarea a materias
    8-salir del programa"""
from collections import deque

class ElementoBase:
    def __init__(self, nombre):
        self.nombre = nombre

class Tarea(ElementoBase):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.contenidos = deque() 

    def mostrar_detalle(self):
        print(f"    - Tarea: {self.nombre}")
        if self.contenidos:
            for i, c in enumerate(reversed(self.contenidos), 1):
                print(f"      {i}. {c['texto']} ({c['estado']})")
        else:
            print("      (Sin contenidos)")

class Materia(ElementoBase):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.tareas = deque()  

class GestorTareas:
    def __init__(self):
        self.materias = []
        self.tareas_libres = deque() 

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            try:
                opcion = int(input("\nSeleccione una opción (1-8): "))
                print("-" * 40)
                
                if opcion == 1:
                    self.agregar_tarea()
                elif opcion == 2:
                    self.agregar_contenido()
                elif opcion == 3:
                    self.mostrar_estado()
                elif opcion == 4:
                    self.eliminar_tarea()
                elif opcion == 5:
                    self.gestionar_estado_contenido()
                elif opcion == 6:
                    self.crear_materia()
                elif opcion == 7:
                    self.asignar_tarea_materia()
                elif opcion == 8:
                    print("Saliendo del programa. ¡Hasta luego!")
                    break
                else:
                    print("Error: Opción fuera de rango (1-8).")
            
            except ValueError:
                print("Error de validación: Debe ingresar un número entero válido.")
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")

    def mostrar_menu(self):
        print("\n" + "=" * 40)
        print("    GESTIÓN DE TAREAS (PILAS CON DEQUE)")
        print("=" * 40)
        print("1. Agregar nueva tarea")
        print("2. Agregar contenidos a la tarea")
        print("3. Mostrar estado de cada tarea (Avances)")
        print("4. Eliminar tarea")
        print("5. Marcar contenido como realizado/pendiente o eliminarlo")
        print("6. Materias (Crear)")
        print("7. Agregar tarea a materias")
        print("8. Salir del programa")

    def agregar_tarea(self):
        while True:
            nombre = input("Ingrese el nombre de la tarea (o '0' para volver): ").strip()
            if nombre == '0':
                break
            if not nombre:
                print("El nombre no puede estar vacío.")
                continue
            self.tareas_libres.append(Tarea(nombre)) 
            print(f"¡Tarea '{nombre}' apilada con éxito!")

    def agregar_contenido(self):
        tarea = self.seleccionar_tarea()
        if not tarea:
            return
        
        while True:
            texto = input(f"Escriba el contenido para '{tarea.nombre}' (o '0' para volver): ").strip()
            if texto == '0':
                break
            if not texto:
                print("El contenido no puede estar vacío.")
                continue
            tarea.contenidos.append({"texto": texto, "estado": "pendiente"}) 
            print("Contenido agregado a la Pila.")

    def mostrar_estado(self):
        if not self.tareas_libres and not self.materias:
            print("No hay tareas ni materias registradas.")
            return
        
        print("\n--- ESTADO DE AVANCES (ESTRUCTURA DE PILAS) ---")
        if self.tareas_libres:
            print("Tareas Generales (Pila):")
            for tarea in reversed(self.tareas_libres):
                tarea.mostrar_detalle()
        
        for materia in self.materias:
            print(f"\nMateria: {materia.nombre} (Pila de tareas)")
            if not materia.tareas:
                print("    (Sin tareas asignadas)")
            for tarea in reversed(materia.tareas):
                tarea.mostrar_detalle()

    def eliminar_tarea(self):
        tarea = self.seleccionar_tarea()
        if not tarea:
            return
        
        if tarea in self.tareas_libres:
            self.tareas_libres.remove(tarea)
        for materia in self.materias:
            if tarea in materia.tareas:
                materia.tareas.remove(tarea)
        print(f"Tarea '{tarea.nombre}' eliminada correctamente.")

    def gestionar_estado_contenido(self):
        tarea = self.seleccionar_tarea()
        if not tarea or not tarea.contenidos:
            print("La tarea seleccionada no tiene contenidos.")
            return
        
        tarea.mostrar_detalle()
        lista_contenidos = list(tarea.contenidos)
        idx = int(input("Ingrese el número del contenido que desea modificar/eliminar: ")) - 1
        
        if 0 <= idx < len(lista_contenidos):
            print("\n¿Qué desea hacer con este contenido?")
            print("1. Cambiar estado a (realizado)")
            print("2. Cambiar estado a (pendiente)")
            print("3. Eliminarlo por completo")
            op = input("Seleccione una opción: ").strip()
            
            if op == '1':
                lista_contenidos[idx]["estado"] = "realizado"
                tarea.contenidos = deque(lista_contenidos)
                print("¡Contenido marcado como (realizado)!")
            elif op == '2':
                lista_contenidos[idx]["estado"] = "pendiente"
                tarea.contenidos = deque(lista_contenidos)
                print("¡Contenido marcado como (pendiente)!")
            elif op == '3':
                eliminado = lista_contenidos.pop(idx)
                tarea.contenidos = deque(lista_contenidos)
                print(f"Contenido '{eliminado['texto']}' eliminado por completo.")
            else:
                print("Opción no válida.")
        else:
            print("Número de contenido inválido.")

    def crear_materia(self):
        nombre = input("Ingrese el nombre de la nueva materia: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío.")
            return
        self.materias.append(Materia(nombre))
        print(f"Materia '{nombre}' creada con éxito.")

    def asignar_tarea_materia(self):
        if not self.materias:
            print("Debe crear al menos una materia primero.")
            return
        
        tarea = self.seleccionar_tarea()
        if not tarea:
            return
        
        print("\nSeleccione la materia destino:")
        for i, mat in enumerate(self.materias, 1):
            print(f"{i}. {mat.nombre}")
        
        idx = int(input("Número de materia: ")) - 1
        if 0 <= idx < len(self.materias):
            self.materias[idx].tareas.append(tarea) 
            if tarea in self.tareas_libres:
                self.tareas_libres.remove(tarea)
            print(f"Tarea asignada a la Pila de la materia '{self.materias[idx].nombre}'.")
        else:
            print("Número de materia inválido.")

    def seleccionar_tarea(self):
        todas = list(self.tareas_libres) + [t for m in self.materias for t in m.tareas]
        if not todas:
            print("No hay tareas registradas en el sistema.")
            return None
        
        print("\nListado de Tareas:")
        for i, t in enumerate(todas, 1):
            print(f"{i}. {t.name if hasattr(t, 'name') else t.nombre}")
        
        idx = int(input("Seleccione el número de la tarea (o '0' para cancelar): ")) - 1
        if idx == -1:
            return None
        if 0 <= idx < len(todas):
            return todas[idx]
        
        print("Número de tarea fuera de rango.")
        return None

if __name__ == "__main__":
    app = GestorTareas()
    app.ejecutar()