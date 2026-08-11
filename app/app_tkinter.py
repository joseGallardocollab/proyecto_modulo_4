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

    # Permite letras (mayúsculas/minúsculas) y espacios
    def validar_nombre(nombre):   
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$"
        return re.match(patron, nombre) is not None
    
    def validar_telefono(telefono):
        try:
            int(telefono)
        except ValueError:
            return False
        
        if len(telefono) < 8:
            return False
  
        return True

    def crear_cliente():
        nombre = entry_nombre.get()
        email = entry_email.get()
        telefono = entry_telefono.get()
        tipo = tipo_var.get()
        empresa = entry_empresa.get()

        # Validación: campos obligatorios
        if not nombre or not email or not telefono:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Validación: nombre solo letras y espacios
        if not validar_nombre(nombre):
            messagebox.showerror("Error", "El nombre debe contener solo letras y espacios.")
            return

        # Validación: teléfono solo números y mínimo 8 dígitos
        if not validar_telefono(telefono):
            messagebox.showerror("Error", "El teléfono debe contener solo números y al menos 8 dígitos.")
            return

        # Validación: formato de email
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, email):
            messagebox.showerror("Error", "El email debe tener el formato xxx@xxx.xxx")
            return

        # Validación para corporativo
        if tipo == "Corporativo" and not empresa:
            messagebox.showerror("Error", "Debe ingresar el nombre de la empresa para clientes corporativos.")
            return

        # Crear cliente según tipo
        if tipo == "Regular":
            cliente = ClienteRegular(nombre, email, telefono)
        elif tipo == "Premium":
            cliente = ClientePremium(nombre, email, telefono)
        else:
            cliente = ClienteCorporativo(nombre, email, telefono, empresa)

        clientes.append(cliente)
        messagebox.showinfo("Cliente creado", f"{cliente.tipo} creado:\n{cliente}")
        actualizar_lista()

    
    def editar_cliente():
        seleccionado = lista_clientes.curselection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un cliente para editar.")
            return
        index = seleccionado[0]
        cliente = clientes[index]

        nombre = entry_nombre.get()
        email = entry_email.get()
        telefono = entry_telefono.get()
        tipo = tipo_var.get()
        empresa = entry_empresa.get()

        # Actualizar datos comunes
        cliente.nombre = nombre
        cliente.set_email(email)
        cliente.set_telefono(telefono)

        # Si el tipo cambió a Corporativo
        if tipo == "Corporativo":
            if not empresa:
                messagebox.showerror("Error", "Debe ingresar el nombre de la empresa para clientes corporativos.")
                return
            # Si el cliente no era corporativo, lo reemplazo por uno nuevo
            if not isinstance(cliente, ClienteCorporativo):
                cliente = ClienteCorporativo(nombre, email, telefono, empresa)
                clientes[index] = cliente
            else:
                cliente.empresa = empresa
        else:
            # Si el tipo cambió a Regular o Premium
            if tipo == "Regular" and not isinstance(cliente, ClienteRegular):
                cliente = ClienteRegular(nombre, email, telefono)
                clientes[index] = cliente
            elif tipo == "Premium" and not isinstance(cliente, ClientePremium):
                cliente = ClientePremium(nombre, email, telefono)
                clientes[index] = cliente
            # Si era corporativo y ahora no, eliminamos empresa
            if hasattr(cliente, "empresa"):
                cliente.empresa = None

        messagebox.showinfo("Cliente editado", f"Cliente actualizado:\n{cliente}")
        actualizar_lista()

    def eliminar_cliente():
        seleccionado = lista_clientes.curselection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar.")
            return
        index = seleccionado[0]
        cliente = clientes.pop(index)
        messagebox.showinfo("Cliente eliminado", f"Cliente eliminado:\n{cliente}")
        actualizar_lista()

    def actualizar_lista():
        lista_clientes.delete(0, tk.END)
        for c in clientes:
            lista_clientes.insert(tk.END, str(c))

    def actualizar_entry(*args):
        if tipo_var.get() == "Corporativo":
            entry_empresa.config(state="normal")
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
        lista_clientes = tk.Listbox(ventana, width=50, height=10)
        lista_clientes.place(x=50, y=310)

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