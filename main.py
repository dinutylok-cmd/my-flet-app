import flet as ft


def main(page: ft.Page):
    # Настройки страницы
    page.title = "Flet Counter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 500

    # Текстовое поле для цифр
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.CENTER, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    # Добавляем элементы
    page.add(
        ft.Row(
            [
                # Используем актуальные названия иконок
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


# Используем ft.app(target=main), это всё еще стандарт для простых запусков,
# но если хочешь убрать Warning, можно оставить так, оно работает.
if __name__ == "__main__":
    ft.app(target=main)