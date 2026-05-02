import flet as ft
from api_client import api

def login_screen(page: ft.Page):

    username_field = ft.TextField(
        hint_text="أدخل اسم المستخدم",
        prefix_icon="person_outline",
        border_radius=14,
        bgcolor="#1E1E2E",
        border_color="transparent",
        focused_border_color="#6C63FF",
        color="white",
        hint_style=ft.TextStyle(color="#666680"),
        text_align=ft.TextAlign.RIGHT,
        height=56,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
    )

    password_field = ft.TextField(
        hint_text="أدخل كلمة المرور",
        prefix_icon="lock_outline",
        password=True,
        can_reveal_password=True,
        border_radius=14,
        bgcolor="#1E1E2E",
        border_color="transparent",
        focused_border_color="#6C63FF",
        color="white",
        hint_style=ft.TextStyle(color="#666680"),
        text_align=ft.TextAlign.RIGHT,
        height=56,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
    )

    error_text = ft.Text("", color="#FF4D4D", size=13, text_align=ft.TextAlign.CENTER)
    loading    = ft.ProgressRing(width=22, height=22, color="white", stroke_width=2, visible=False)

    def handle_login(e):
        error_text.value   = ""
        loading.visible    = True
        login_btn.disabled = True
        page.update()

        uname  = username_field.value.strip()
        pword  = password_field.value.strip()

        result = api.login(uname, pword)

        loading.visible    = False
        login_btn.disabled = False

        if result["success"]:
            page.run_task(page.push_route, "/dashboard")
        else:
            error_text.value = result["message"]
        page.update()

    login_btn = ft.Container(
        content=ft.Row([
            loading,
            ft.Text("تسجيل الدخول  ←", size=16, weight=ft.FontWeight.BOLD, color="white"),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        bgcolor="#6C63FF",
        border_radius=14,
        height=56,
        on_click=handle_login,
        ink=True,
    )

    logo = ft.Container(
        content=ft.Icon("print", size=36, color="white"),
        width=72, height=72,
        bgcolor="#6C63FF",
        border_radius=20,
        alignment=ft.Alignment(0, 0),
        shadow=ft.BoxShadow(blur_radius=24, color="#6C63FF55", offset=ft.Offset(0, 8)),
    )

    biometric_btn = ft.Container(
        content=ft.Icon("fingerprint", size=28, color="#AAAACC"),
        bgcolor="#1E1E2E",
        border_radius=14,
        height=56,
        expand=True,
        alignment=ft.Alignment(0, 0),
        ink=True,
    )

    google_btn = ft.Container(
        content=ft.Text("G", size=22, weight=ft.FontWeight.BOLD, color="#AAAACC"),
        bgcolor="#1E1E2E",
        border_radius=14,
        height=56,
        expand=True,
        alignment=ft.Alignment(0, 0),
        ink=True,
    )

    signup_link = ft.TextButton(
        content=ft.Text("ليس لديك حساب؟ أنشئ حساباً", color="#6C63FF", size=13),
        on_click=lambda e: page.run_task(page.push_route, "/signup"),
    )

    return ft.View(
        route="/login",
        controls=[
            ft.Container(
                expand=True,
                padding=ft.padding.symmetric(horizontal=28, vertical=40),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Container(height=20),
                        logo,
                        ft.Container(height=24),
                        ft.Text("اطبعلي - Etlobi", size=24, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text("مرحباً بك مجدداً", size=16, color="#AAAACC"),
                        ft.Container(height=32),
                        ft.Text("اسم المستخدم", size=13, color="#AAAACC", text_align=ft.TextAlign.RIGHT, width=float("inf")),
                        ft.Container(height=6),
                        username_field,
                        ft.Container(height=16),
                        ft.Text("كلمة المرور", size=13, color="#AAAACC", text_align=ft.TextAlign.RIGHT, width=float("inf")),
                        ft.Container(height=6),
                        password_field,
                        ft.Container(height=8),
                        error_text,
                        ft.Container(height=16),
                        ft.Container(content=login_btn, width=float("inf")),
                        ft.Container(height=16),
                        signup_link,
                        ft.Container(height=16),
                        ft.Row([
                            ft.Container(height=1, expand=True, bgcolor="#2A2A3A"),
                            ft.Text("أو الدخول عبر", size=12, color="#666680"),
                            ft.Container(height=1, expand=True, bgcolor="#2A2A3A"),
                        ], spacing=10),
                        ft.Container(height=16),
                        ft.Row([biometric_btn, google_btn], spacing=12),
                        ft.Container(height=40),
                        ft.Text("تصميم وتطوير / أحمد إبراهيم © 2026", size=11, color="#444455", text_align=ft.TextAlign.CENTER),
                    ],
                ),
            )
        ],
        bgcolor="#0F0F1A",
        padding=0,
    )