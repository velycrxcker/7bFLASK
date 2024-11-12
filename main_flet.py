import flet as ft
import requests

def main(page: ft.Page):
    page.title = "Aplicación de Registro de Usuarios"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Función para cargar usuarios desde la API
    def cargar_usuarios():
        response = requests.get("http://127.0.0.1:5000/usuarios")
        usuarios = response.json()
        usuario_items.controls.clear()
        for usuario in usuarios:
            usuario_items.controls.append(ft.Row([
                ft.Text(usuario["Nombre_Usuario"]),
                ft.Text(usuario["Contrasena"]),
                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, id=usuario["Id_Usuario"]: eliminar_usuario(id))
            ]))
        page.update()

    # Función para agregar un nuevo usuario
    def agregar_usuario(e):
        nuevo_usuario = {
            "nombre": nombre_input.value,
            "contrasena": contrasena_input.value
        }
        requests.post("http://127.0.0.1:5000/usuarios", json=nuevo_usuario)
        cargar_usuarios()

    # Función para eliminar un usuario
    def eliminar_usuario(id):
        requests.delete(f"http://127.0.0.1:5000/usuarios/{id}")
        cargar_usuarios()

    # Inputs y botones
    nombre_input = ft.TextField(label="Nombre de Usuario", width=200)
    contrasena_input = ft.TextField(label="Contraseña", width=200, password=True)
    agregar_button = ft.ElevatedButton("Agregar Usuario", on_click=agregar_usuario)

    usuario_items = ft.Column()
    cargar_usuarios()  # Cargar usuarios al iniciar

    # Layout de la interfaz
    page.add(
        ft.Column([
            ft.Row([nombre_input, contrasena_input, agregar_button]),
            usuario_items
        ])
    )

ft.app(target=main)
