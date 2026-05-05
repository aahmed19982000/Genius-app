import flet as ft


def bottom_navbar(page: ft.Page, current_index: int = 0):

    def on_change(e):
        index = e.control.selected_index
        routes = ["/dashboard", "/my-orders", "/step1", "/saved", "/profile"]
        page.run_task(page.push_route, routes[index])

    return ft.NavigationBar(
        selected_index=current_index,
        on_change=on_change,
        bgcolor="white",
        indicator_color="transparent",
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