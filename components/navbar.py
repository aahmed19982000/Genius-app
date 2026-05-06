import flet as ft

def bottom_navbar(page: ft.Page, current_index: int = 0):
    def on_click(index):
        routes = ["/home", "/my-orders", "/step1", "/saved", "/profile"]
        page.go(routes[index])

    def nav_item(icon_src, label, index, is_selected, is_image=True):
        color = "#4169E1" if is_selected else "#757575"
        
        # إذا كان العنصر صورة (PNG)
        if is_image:
            icon_content = ft.Image(
                src=icon_src,
                width=24,
                height=24,
                color=color if not is_selected else None, # تطبيق اللون فقط إذا لم يكن مختاراً (أو حسب الرغبة)
                fit="contain",
            )
        else:
            # إذا كان أيقونة نظام (Material Icon)
            icon_content = ft.Icon(icon_src, color=color, size=24)

        return ft.Container(
            content=ft.Column(
                [
                    icon_content,
                    ft.Text(label, size=10, color=color, weight=ft.FontWeight.W_500),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            ),
            expand=True,
            on_click=lambda _: on_click(index),
            ink=True,
            bgcolor="white",
        )

    def logo_item():
        return ft.Container(
            content=ft.Image(
                src="icon.png",
                width=30,
                height=30,
                fit="contain",
            ),
            width=50,
            height=50,
            shape=ft.BoxShape.CIRCLE,
            alignment=ft.Alignment(0, 0),
            on_click=lambda _: on_click(2),
            margin=ft.margin.only(bottom=15),
        )

    return ft.Container(
        content=ft.Row(
            [
                nav_item("img/navbar/home.png", "الرئيسية", 0, current_index == 0),
                nav_item("img/navbar/my-orders.png", "الطلبات", 1, current_index == 1),
                ft.Column([logo_item()], alignment=ft.MainAxisAlignment.END),
                nav_item("img/navbar/wallet.png", "المحفظة", 3, current_index == 3),
                nav_item("img/navbar/profile.png", "الحساب", 4, current_index == 4),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.END,
        ),
        bgcolor="white",
        height=70,
        padding=ft.padding.symmetric(horizontal=5),
        border=ft.border.only(top=ft.BorderSide(1, "#EEEEEE")),
    )