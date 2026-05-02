import flet as ft

def bottom_navbar(page: ft.Page, current_index: int = 0):

    def on_change(e):
        index = e.control.selected_index
        routes = ["/dashboard", "/step1", "/my-orders", "/profile"]
        page.run_task(page.push_route, routes[index])

    return ft.NavigationBar(
        selected_index=current_index,
        on_change=on_change,
        bgcolor="#1E1E2E",
        indicator_color="#6C63FF",
        destinations=[
            ft.NavigationBarDestination(
                icon="home_outlined",
                selected_icon="home",
                label="الرئيسية",
            ),
            ft.NavigationBarDestination(
                icon="print_outlined",
                selected_icon="print",
                label="طلب جديد",
            ),
            ft.NavigationBarDestination(
                icon="receipt_long_outlined",
                selected_icon="receipt_long",
                label="طلباتي",
            ),
            ft.NavigationBarDestination(
                icon="person_outlined",
                selected_icon="person",
                label="حسابي",
            ),
        ],
    )
