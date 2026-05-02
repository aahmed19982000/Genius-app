import flet as ft
from api_client import api
from screens.login import login_screen
from screens.signup import signup_screen
from screens.my_orders import my_orders_screen
from screens.profile import profile_screen
from screens.step1_upload import step1_upload_screen
from screens.step2_options import step2_options_screen
from screens.step3_quantity import step3_quantity_screen
from screens.step4_payment import step4_payment_screen
from components.navbar import bottom_navbar


def dashboard_view(page: ft.Page):
    return ft.View(
        route="/dashboard",
        controls=[
            ft.Container(
                expand=True,
                padding=ft.Padding(left=24, right=24, top=32, bottom=32),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    controls=[
                        ft.Container(height=20),
                        ft.Container(
                            content=ft.Icon("print", size=36, color="white"),
                            width=72, height=72,
                            bgcolor="#6C63FF",
                            border_radius=20,
                            alignment=ft.Alignment(0, 0),
                            shadow=ft.BoxShadow(
                                blur_radius=24,
                                color="#6C63FF55",
                                offset=ft.Offset(0, 8),
                            ),
                        ),
                        ft.Container(height=16),
                        ft.Text(
                            f"مرحباً، {api.user_data.get('username', 'بك') if api.user_data else 'بك'} 👋",
                            size=22, weight=ft.FontWeight.BOLD, color="white",
                        ),
                        ft.Text("اطبعلي - Etlobi", size=14, color="#AAAACC"),
                        ft.Container(height=40),
                        ft.Container(
                            content=ft.Row([
                                ft.Icon("print", color="white"),
                                ft.Text("طلب طباعة جديد", size=16,
                                        weight=ft.FontWeight.BOLD, color="white"),
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                            bgcolor="#6C63FF",
                            border_radius=14,
                            height=56,
                            width=float("inf"),
                            on_click=lambda e: page.run_task(page.push_route, "/step1"),
                            ink=True,
                        ),
                        ft.Container(height=16),
                        ft.Container(
                            content=ft.Row([
                                ft.Icon("receipt_long", color="#6C63FF"),
                                ft.Text("طلباتي", size=16,
                                        weight=ft.FontWeight.BOLD, color="#6C63FF"),
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                            bgcolor="#1E1E2E",
                            border_radius=14,
                            height=56,
                            width=float("inf"),
                            on_click=lambda e: page.run_task(page.push_route, "/my-orders"),
                            ink=True,
                        ),
                    ],
                ),
            )
        ],
        navigation_bar=bottom_navbar(page, current_index=0),
        bgcolor="#0F0F1A",
        padding=0,
    )


def main(page: ft.Page):
    page.title = "اطبعلي - نظام الإدارة"
    page.theme_mode = ft.ThemeMode.DARK
    page.rtl = True
    page.bgcolor = "#0F0F1A"
    page.padding = 0
    page.window.width = 390
    page.window.height = 844
    page.window.resizable = False

    order_draft = {}

    async def go_step1():
        order_draft.clear()
        await page.push_route("/step1")

    async def go_step2(file_info):
        order_draft.clear()
        order_draft["file"] = dict(file_info)
        await page.push_route("/step2")

    async def go_step3(options):
        order_draft.update(options)
        await page.push_route("/step3")

    async def go_step4(order_data):
        order_draft.update(order_data)
        await page.push_route("/step4")

    def route_change(e):
        page.views.clear()

        route = page.route

        if route in ("/", "/login"):
            page.views.append(login_screen(page))

        elif route == "/signup":
            page.views.append(signup_screen(page))

        elif route == "/dashboard":
            page.views.append(dashboard_view(page))

        elif route in ("/new-order", "/step1"):
            page.views.append(step1_upload_screen(page, on_next=go_step2))

        elif route == "/step2":
            if not order_draft.get("file"):
                page.views.append(step1_upload_screen(page, on_next=go_step2))
            else:
                page.views.append(step2_options_screen(
                    page,
                    file_info=order_draft["file"],
                    on_next=go_step3,
                    on_back=lambda: page.run_task(go_step1),
                ))

        elif route == "/step3":
            if not order_draft.get("file"):
                page.views.append(step1_upload_screen(page, on_next=go_step2))
            else:
                page.views.append(step3_quantity_screen(
                    page,
                    order_data=order_draft,
                    on_next=go_step4,
                    on_back=lambda: page.run_task(go_step2, order_draft["file"]),
                ))

        elif route == "/step4":
            if not order_draft.get("file"):
                page.views.append(step1_upload_screen(page, on_next=go_step2))
            else:
                page.views.append(step4_payment_screen(
                    page,
                    order_data=order_draft,
                    on_back=lambda: page.run_task(go_step3, {}),
                ))

        elif route == "/my-orders":
            page.views.append(my_orders_screen(page))

        elif route == "/profile":
            page.views.append(profile_screen(page))

        else:
            page.views.append(login_screen(page))

        page.update()

    async def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.run_task(page.push_route, "/login")


if __name__ == "__main__":
    ft.run(main)