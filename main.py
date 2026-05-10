import flet as ft
from api_client import api
from screens.login import login_screen
from screens.signup import signup_screen
from screens.home import home_screen
from screens.my_orders import my_orders_screen
from screens.profile import profile_screen
from screens.wallet import wallet_screen
from screens.step1_upload import step1_upload_screen
from screens.step2_options import step2_options_screen
from screens.step3_quantity import step3_quantity_screen
from screens.step4_payment import step4_payment_screen
from screens.chat import chat_screen
from screens.track_order import track_order_screen
import urllib.parse

from components.navbar import bottom_navbar


def dashboard_view(page: ft.Page):
    username = api.user_data.get("username", "أحمد") if api.user_data else "أحمد"

    # ── Top bar ──────────────────────────────────────────────
    top_bar = ft.Container(
        bgcolor="white",
        padding=ft.padding.symmetric(horizontal=20, vertical=12),
        content=ft.Row(
            [
                # Left: icons
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon("person_outline", size=20, color="#444444"),
                            width=42, height=42,
                            bgcolor="#F2F2F2",
                            border_radius=21,
                            alignment=ft.Alignment(0, 0),
                            ink=True,
                            on_click=lambda e: page.run_task(page.push_route, "/profile"),
                        ),
                        ft.Container(
                            content=ft.Icon("notifications_outlined", size=20, color="#444444"),
                            width=42, height=42,
                            bgcolor="#F2F2F2",
                            border_radius=21,
                            alignment=ft.Alignment(0, 0),
                            ink=True,
                        ),
                    ],
                    spacing=8,
                ),
                # Right: location
                ft.Row(
                    [
                        ft.Text(
                            "مجمع الملك فهد...",
                            size=13,
                            color="#1A1A2E",
                            weight=ft.FontWeight.W_500,
                        ),
                        ft.Icon("location_on", size=15, color="#4169E1"),
                        ft.Text(
                            "توصيل إلى",
                            size=13,
                            color="#4169E1",
                            weight=ft.FontWeight.W_600,
                        ),
                    ],
                    spacing=3,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    # ── Hero card ─────────────────────────────────────────────
    hero_card = ft.Container(
        margin=ft.margin.symmetric(horizontal=16),
        bgcolor="white",
        border_radius=20,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color="#00000012",
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            [
                # Printer image area
                ft.Container(
                    height=220,
                    bgcolor="#EEF2FF",
                    border_radius=ft.BorderRadius(20, 20, 0, 0),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Icon("print", size=110, color="#5B7FD4"),
                ),
                # Text + button
                ft.Container(
                    padding=ft.padding.all(24),
                    content=ft.Column(
                        [
                            ft.Text(
                                "اطبع مستنداتك بكل سهولة",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#1A1A2E",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(height=10),
                            ft.Text(
                                "ارفع ملفاتك، اختر نوع الورق، واستلمها\nعند باب منزلك بكل سهولة",
                                size=13,
                                color="#888888",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(height=24),
                            ft.Container(
                                content=ft.Text(
                                    "اطبع الآن",
                                    size=17,
                                    weight=ft.FontWeight.BOLD,
                                    color="white",
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                bgcolor="#4169E1",
                                border_radius=14,
                                height=54,
                                alignment=ft.Alignment(0, 0),
                                on_click=lambda e: page.run_task(page.push_route, "/step1"),
                                ink=True,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    ),
                ),
            ],
            spacing=0,
        ),
    )

    return ft.View(
        route="/dashboard",
        bgcolor="#F5F7FA",
        padding=0,
        controls=[
            ft.Column(
                [
                    top_bar,
                    ft.ListView(
                        expand=True,
                        controls=[
                            # Greeting
                            ft.Container(
                                padding=ft.padding.symmetric(horizontal=20, vertical=20),
                                alignment=ft.Alignment(0, 0),
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            f"مرحباً {username} 👋",
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                            color="#1A1A2E",
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        ft.Container(height=4),
                                        ft.Text(
                                            "ماذا تود أن تطبع اليوم؟",
                                            size=14,
                                            color="#888888",
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=0,
                                ),
                            ),
                            hero_card,
                            ft.Container(height=20),
                        ],
                    ),
                    bottom_navbar(page, current_index=0),
                ],
                spacing=0,
                expand=True,
            ),
        ],
    )


def main(page: ft.Page):
    page.title = "اطبعلي - نظام الإدارة"
    page.window.icon = "assets/icon.png"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.bgcolor = "#F5F7FA"
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

        elif route in ("/home", "/dashboard"):
            username = api.user_data.get("username", "أحمد") if api.user_data else "أحمد"
            page.views.append(home_screen(
                page,
                on_print_now=lambda e: page.run_task(go_step1),
                username=username,
            ))

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

        elif route in ("/wallet", "/saved"):
            page.views.append(wallet_screen(page))

        elif route.startswith("/chat/"):
            parsed_url = urllib.parse.urlparse(route)
            path = parsed_url.path
            query = urllib.parse.parse_qs(parsed_url.query)
            
            order_id_str = path.split("/")[-1]
            try:
                order_id = int(order_id_str)
            except ValueError:
                order_id = 0
                
            order_name = query.get("name", [""])[0]
            order_status = query.get("status", [""])[0]
            
            page.views.append(chat_screen(page, order_id, order_name, order_status))

        elif route.startswith("/track/"):
            parsed_url = urllib.parse.urlparse(route)
            path = parsed_url.path
            query = urllib.parse.parse_qs(parsed_url.query)
            
            order_id_str = path.split("/")[-1]
            try:
                order_id = int(order_id_str)
            except ValueError:
                order_id = 0
                
            order_name = query.get("name", [""])[0]
            order_status = query.get("status", [""])[0]
            order_date = query.get("date", [""])[0]
            order_cost = query.get("cost", ["0.00"])[0]
            
            page.views.append(track_order_screen(
                page, order_id, order_name, order_status, order_date, order_cost
            ))

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
    ft.app(target=main, assets_dir="assets")
