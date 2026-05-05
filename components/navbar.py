import flet as ft

def bottom_navbar(page: ft.Page, current_index: int = 0):
    def on_change(e):
        index = e.control.selected_index
        routes = ["/home", "/my-orders", "/step1", "/saved", "/profile"]
        page.go(routes[index])

    # ننشئ النافبار شفافة تماماً
    nav_bar = ft.NavigationBar(
        selected_index=current_index,
        on_change=on_change,
        bgcolor=ft.Colors.TRANSPARENT, # شفافة
        elevation=0,
        indicator_color="#E8EEFF",
        label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icon("home_outlined", color="#AAAAAA"),
                selected_icon=ft.Icon("home", color="#4169E1"),
                label="الرئيسية",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon("receipt_long_outlined", color="#AAAAAA"),
                selected_icon=ft.Icon("receipt_long", color="#4169E1"),
                label="الطلبات",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon("add_box_outlined", color="#AAAAAA"),
                selected_icon=ft.Icon("add_box", color="#4169E1"),
                label="الملفات",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon("account_balance_wallet_outlined", color="#AAAAAA"),
                selected_icon=ft.Icon("account_balance_wallet", color="#4169E1"),
                label="المحفظة",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon("person_outline", color="#AAAAAA"),
                selected_icon=ft.Icon("person", color="#4169E1"),
                label="الحساب",
            ),
        ],
    )

    # نغلفها في Container أبيض لكسر أي لون رمادي يفرضه النظام
    return ft.Container(
        content=nav_bar,
        bgcolor="white",
        padding=ft.Padding(0, 0, 0, 0),
        border=ft.Border(top=ft.BorderSide(1, "#f0f0f0")), # اختياري: خط رفيع جداً للفصل
    )