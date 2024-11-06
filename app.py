import flet as ft

# pip install requests
import requests

def main(page: ft.Page):
    def viewBuscar():
        print("view buscar")
        row_lbl_temperatura.visible = False
        row_txt_temperatura.visible = False
        row_lbl_humedad.visible     = False
        row_txt_humedad.visible     = False
        row_btn_guardar.visible     = False

        lbl_temperatura.visible = False
        txt_temperatura.visible = False
        lbl_humedad.visible     = False
        txt_humedad.visible     = False

    def navigation_bar_change(event):
        print("navigation bar change")
        print(event)

        data = event.data

        if data == "1":
            viewBuscar()

    def btn_guardar_click(event):
        url     = "https://flask-ovh6.onrender.com/guardar"
        payload = {
            "id": "",
            "temperatura": txt_temperatura.value,
            "humedad": txt_humedad.value
        }

        print("payload")
        print(payload)

        x = requests.post(url, data=payload)

        print("response")
        print(x.text)

        txt_temperatura.value = ""
        txt_humedad.value     = ""

    lbl_temperatura = ft.Text(value="Temperatura:")
    lbl_humedad     = ft.Text(value="Humedad:")

    txt_temperatura = ft.TextField(value="", text_align=ft.TextAlign.LEFT, width=200, hint_text="Temperatura:")
    txt_humedad     = ft.TextField(value="", text_align=ft.TextAlign.LEFT, width=200, hint_text="Humedad:")
    btn_guardar     = ft.ElevatedButton(text="Guardar", on_click=btn_guardar_click)

    # RowProductA1
    row_lbl_temperatura = ft.Row([
        ft.Container(expand=1, content=ft.Text("")),
        ft.Container(expand=3, content=ft.Row([lbl_temperatura])),
        ft.Container(expand=1, content=ft.Text(""))
    ])
    row_txt_temperatura =ft.Row([
        ft.Container(expand=1, content=ft.Text("")),
        ft.Container(expand=3, content=ft.Row([txt_temperatura])),
        ft.Container(expand=1, content=ft.Text(""))
    ])

    # RowProductA2
    row_lbl_humedad = ft.Row([
        ft.Container(expand=1, content=ft.Text("")),
        ft.Container(expand=3, content=ft.Row([lbl_humedad])),
        ft.Container(expand=1, content=ft.Text(""))
    ])

    # RowProductB1
    row_txt_humedad = ft.Row([
        ft.Container(expand=1, content=ft.Text("")),
        ft.Container(expand=3, content=ft.Row([txt_humedad])),
        ft.Container(expand=1, content=ft.Text(""))
    ])
    row_btn_guardar = ft.Row([
        ft.Container(expand=1, content=ft.Text("")),
        ft.Container(expand=3, content=ft.Row([btn_guardar])),
        ft.Container(expand=1, content=ft.Text(""))
    ])

    page.title    = "App"
    page.adaptive = True

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            # Buscar icons en ---> https://gallery.flet.dev/icons-browser/
            ft.NavigationBarDestination(icon=ft.icons.SAVE, label="Guardar"),
            ft.NavigationBarDestination(icon=ft.icons.SEARCH, label="Buscar"),
            ft.NavigationBarDestination(icon=ft.icons.AUTO_GRAPH, label="Analisis")
        ],
        border=ft.Border(
            top=ft.BorderSide(color=ft.cupertino_colors.SYSTEM_GREY2, width=0)
        ),
        on_change=navigation_bar_change
    )

    page.add(
        row_lbl_temperatura,
        row_txt_temperatura,
        row_lbl_humedad,
        row_txt_humedad,
        row_btn_guardar
    )

ft.app(main)
