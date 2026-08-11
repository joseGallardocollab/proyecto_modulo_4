import tkinter as tk
from tkinter import messagebox
from clases.clientes import ClienteRegular, ClientePremium, ClienteCorporativo
import config.config as config
import re

intentos = 3

def main():
    clientes = []
    # ---------------- Login ----------------
    def verificar_login(event=None):
        global intentos
        usuario = entry_usuario.get()
        clave = entry_clave.get()
        # La clave y contraseña se encuentran en config.py y son "admin" - "1234"
        if usuario == config.LOGIN_USUARIO and clave == config.LOGIN_CONTRASENA:
            login.destroy()
            ventana_principal()
        else:
            intentos -= 1
            if intentos > 0:
                messagebox.showerror("Error", f"Usuario o contraseña incorrectos, intentos restantes: {intentos}")
            else:       
                boton_login.config(state="disabled")       
                messagebox.showerror("Error", "Usuario bloqueado")
                

    # ---------------- Funciones ----------------

    #Función extra que permite almacenar en un log basico la lista del cliente creado, editado o eliminado
    def registrar_evento(accion, cliente):
        with open("dato_cliente_log.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"{accion}: {cliente} de tipo: f{cliente.tipo}\n")

    # Permite letras (mayúsculas/minúsculas) y espacios
    def validar_nombre(nombre):   
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$"
        return re.match(patron, nombre) is not None
    
    def validar_telefono(telefono):
        try:
            int(telefono)  # asegura que sean solo números
        except ValueError:
            return False
        
        # Validar longitud entre 8 y 12
        if len(telefono) >= 8 and len(telefono) <= 12:
            return True
        else:
            return False
    
    #formato para e-mail
    def validar_email(email):
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(patron_email, email)     

    #segun funciones de validación levanta los mensajes de error    
    def validar_campos(nombre, email, telefono, tipo, empresa):
        if not nombre or not email or not telefono:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False

        if not validar_nombre(nombre):
            messagebox.showerror("Error", "El nombre debe contener solo letras y espacios.")
            return False

        if not validar_telefono(telefono):
            messagebox.showerror("Error", "El teléfono debe contener solo números y entre 8 y 12 dígitos.")
            return False

        if not validar_email(email):
            messagebox.showerror("Error", "El email debe tener el formato xxx@xxx.xxx")
            return False

        if tipo == "Corporativo" and not empresa:
            messagebox.showerror("Error", "Debe ingresar el nombre de la empresa para clientes corporativos.")
            return False

        return True

    #verifica que el cliente no este duplicado
    def cliente_duplicado(nombre, index=None):
        for i, c in enumerate(clientes):
            # Si estamos editando, ignoramos el cliente actual (index)
            if index is not None and i == index:
                continue
            if c.nombre == nombre:
                return True
        return False

    #creación de cliente
    def crear_cliente():
        nombre = entry_nombre.get()
        email = entry_email.get()
        telefono = entry_telefono.get()
        tipo = tipo_var.get()
        empresa = entry_empresa.get()

        if not validar_campos(nombre, email, telefono, tipo, empresa):
            return

        # Validar duplicado
        if cliente_duplicado(nombre):
            messagebox.showerror("Error", "Ya existe un cliente con ese nombre.")
            return

        # Crear cliente según tipo
        if tipo == "Regular":
            cliente = ClienteRegular(nombre, email, telefono)
        elif tipo == "Premium":
            cliente = ClientePremium(nombre, email, telefono)
        else:
            cliente = ClienteCorporativo(nombre, email, telefono, empresa)

        clientes.append(cliente)

        #se añade el cliente al log
        registrar_evento("Cliente creado", cliente)

        messagebox.showinfo("Cliente creado", f"{cliente.tipo} creado:\n{cliente}")
        limpiar_campos()
        actualizar_lista()

    #edit de cliente
    def editar_cliente():
        seleccionado = lista_clientes.curselection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un cliente para editar.")
            return
        index = seleccionado[0]

        nombre = entry_nombre.get()
        email = entry_email.get()
        telefono = entry_telefono.get()
        tipo = tipo_var.get()
        empresa = entry_empresa.get()

        if not validar_campos(nombre, email, telefono, tipo, empresa):
            return

        cliente = clientes[index]
        cliente.nombre = nombre
        cliente.set_email(email)
        cliente.set_telefono(telefono)

        # Manejo de tipo
        if tipo == "Corporativo":
            if not isinstance(cliente, ClienteCorporativo):
                cliente = ClienteCorporativo(nombre, email, telefono, empresa)
                clientes[index] = cliente
            else:
                cliente.empresa = empresa
        else:
            if tipo == "Regular" and not isinstance(cliente, ClienteRegular):
                cliente = ClienteRegular(nombre, email, telefono)
                clientes[index] = cliente
            elif tipo == "Premium" and not isinstance(cliente, ClientePremium):
                cliente = ClientePremium(nombre, email, telefono)
                clientes[index] = cliente
            if hasattr(cliente, "empresa"):
                cliente.empresa = None

        registrar_evento("Cliente editado", cliente)

        messagebox.showinfo("Cliente editado", f"Cliente actualizado:\n{cliente}")
        limpiar_campos()
        actualizar_lista()


    #eliminación de cliente
    def eliminar_cliente():
        seleccionado = lista_clientes.curselection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar.")
            return
        index = seleccionado[0]
        cliente = clientes.pop(index)

        registrar_evento("Cliente eliminado", cliente)
        messagebox.showinfo("Cliente eliminado", f"Cliente eliminado:\n{cliente}")
        limpiar_campos()
        actualizar_lista()

    #Actualiza la lista y mantiene el foco en la selección de la lista al seleccionar para rellenar campos con datos para poder editarlo
    def actualizar_lista():
        seleccionado = lista_clientes.curselection()
        index = seleccionado[0] if seleccionado else None

        lista_clientes.delete(0, tk.END)
        for c in clientes:
            lista_clientes.insert(tk.END, str(c))

        if index is not None and index < len(clientes):
            lista_clientes.selection_set(index)
            lista_clientes.activate(index)
            lista_clientes.see(index)  

    #limpia el campo empresa
    def actualizar_entry(*args):
        if tipo_var.get() == "Corporativo":
            entry_empresa.config(state="normal")
        else:
            entry_empresa.delete(0, tk.END)
            entry_empresa.config(state="disabled")    

    #Limpia los demás campos
    def limpiar_campos():
        entry_nombre.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)

    #Rellena los campos con los datos del cliente al tocar la lista
    #lo uso para facilitar la edición
    def rellenar_campos(event):
        seleccionado = lista_clientes.curselection()
        if not seleccionado:
            return
        index = seleccionado[0]
        cliente = clientes[index]

        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, cliente.nombre)

        entry_email.delete(0, tk.END)
        entry_email.insert(0, cliente._Cliente__email)

        entry_telefono.delete(0, tk.END)
        entry_telefono.insert(0, cliente._Cliente__telefono)

        if isinstance(cliente, ClienteCorporativo):
            entry_empresa.config(state="normal")
            entry_empresa.delete(0, tk.END)
            entry_empresa.insert(0, cliente.empresa)
        else:
            entry_empresa.delete(0, tk.END)
            entry_empresa.config(state="disabled")


    # ---------------- Pantalla principal ----------------
    def ventana_principal():
        global entry_nombre, entry_email, entry_telefono, tipo_var, entry_empresa, lista_clientes      

        ventana = tk.Tk()
        ventana.title("Gestión de Clientes - SolutionTech")
        ventana.geometry("600x550")

        tk.Label(ventana, text="Nombre: ").place(x=50, y=30)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.place(x=150, y=30)

        tk.Label(ventana, text="Email: ").place(x=50, y=70)
        entry_email = tk.Entry(ventana)
        entry_email.place(x=150, y=70)

        tk.Label(ventana, text="Teléfono: ").place(x=50, y=110)
        entry_telefono = tk.Entry(ventana)
        entry_telefono.place(x=150, y=110)

        tk.Label(ventana, text="Seleccione el tipo de Cliente:").place(x=50, y=150)
        tipo_var = tk.StringVar(value="Regular")
        opciones = tk.OptionMenu(ventana, tipo_var, "Regular", "Premium", "Corporativo")
        opciones.place(x=250, y=145)
        tk.Label(ventana, text="Empresa (solo corporativo):").place(x=50, y=190)
        entry_empresa = tk.Entry(ventana)
        entry_empresa.place(x=250, y=190)
        entry_empresa.config(state="disabled")   
        tipo_var.trace_add("write", actualizar_entry)

        tk.Button(ventana, text="Crear Cliente", command=crear_cliente).place(x=50, y=240)
        tk.Button(ventana, text="Editar Cliente", command=editar_cliente).place(x=180, y=240)
        tk.Button(ventana, text="Eliminar Cliente", command=eliminar_cliente).place(x=310, y=240)

        tk.Label(ventana, text="Lista de Clientes/ Seleccione para eliminar o editar: ").place(x=50, y=280)
        lista_clientes = tk.Listbox(ventana, width=85, height=12)
        lista_clientes.place(x=50, y=310)

        lista_clientes.bind("<<ListboxSelect>>", rellenar_campos)
        ventana.mainloop()

    # ---------------- Ventana del login ----------------
    login = tk.Tk()
    login.title("Login - SolutionTech")
    login.geometry("400x300")

    tk.Label(login, text="Iniciar sesión", font=("Arial", 14, "bold")).place(x=130, y=30)
    linea = tk.Frame(login, bg="black", height=2, width=360)
    linea.place(x=20, y=70)

    tk.Label(login, text="Usuario:").place(x=50, y=100)
    entry_usuario = tk.Entry(login)
    entry_usuario.place(x=150, y=100)

    tk.Label(login, text="Contraseña:").place(x=50, y=150)
    entry_clave = tk.Entry(login, show="*")
    entry_clave.place(x=150, y=150)

    boton_login = tk.Button(login, text="Ingresar", command=verificar_login)
    boton_login.place(x=180, y=200)
    login.bind("<Return>", verificar_login)

    login.mainloop()

if __name__ == "__main__":
    main()