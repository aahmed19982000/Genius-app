import flet as ft
from api_client import api
from components.navbar import bottom_navbar

def profile_screen(page: ft.Page):

    user = api.user_data or {}

    def handle_logout(e):
        api.access_token = None
        api.user_data = None
        page.run_task(page.push_route, "/login")

    avatar = ft.Container(
        content=ft.Text(
            (user.get("username", "U")[0]).upper(),
            size=32, weight=ft.FontWeight.BOLD, color="white"
        ),
        width=80, height=80,
        bgcolor="#6C63FF",
        border_radius=40,
        alignment=ft.Alignment(0, 0),
        shadow=ft.BoxShadow(blur_radius=20, color="#6C63FF55", offset=ft.Offset(0, 6)),
    )

    def info_row(icon, label, value):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color="#6C63FF", size=20),
                ft.Column([
                    ft.Text(label, size=11, color="#666680"),
                    ft.Text(value or "—", size=14, color="white"),
                ], spacing=2),
            ], spacing=12),
            bgcolor="#1E1E2E",
            border_radius=14,
            padding=16,
        )

    logout_btn = ft.Container(
        content=ft.Row([
            ft.Icon("logout", color="white"),
            ft.Text("تسجيل الخروج", size=16, weight=ft.FontWeight.BOLD, color="white"),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        bgcolor="#FF4D4D",
        border_radius=14,
        height=56,
        on_click=handle_logout,
        ink=True,
    )

    return ft.View(
        route="/profile",
        controls=[
            ft.Container(
                expand=True,
                padding=ft.padding.symmetric(horizontal=24, vertical=32),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Container(height=20),
                        avatar,
                        ft.Container(height=16),
                        ft.Text(
                            user.get("username", "المستخدم"),
                            size=22, weight=ft.FontWeight.BOLD, color="white"
                        ),
                        ft.Text(
                            user.get("user_type", ""),
                            size=13, color="#AAAACC"
                        ),
                        ft.Container(height=32),

                        ft.Text("معلومات الحساب", size=14, color="#AAAACC",
                                text_align=ft.TextAlign.RIGHT, width=float("inf")),
                        ft.Container(height=10),

                        info_row("person", "اسم المستخدم", user.get("username")),
                        ft.Container(height=10),
                        info_row("mail", "البريد الإلكتروني", user.get("email")),
                        ft.Container(height=10),
                        info_row("phone", "رقم الهاتف", user.get("phone_number")),
                        ft.Container(height=10),
                        info_row("location_on", "العنوان", user.get("address")),
                        ft.Container(height=40),

                        ft.Container(content=logout_btn, width=float("inf")),
                        ft.Container(height=32),

                        ft.Text("تصميم وتطوير / أحمد إبراهيم © 2026",
                                size=11, color="#444455", text_align=ft.TextAlign.CENTER),
                        bottom_navbar(page, current_index=4),
                    ],
                ),
            )
        ],
        bgcolor="#0F0F1A",
        padding=0,
    )