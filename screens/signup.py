import flet as ft
from api_client import api

def signup_screen(page: ft.Page):

    username_field = ft.TextField(
        hint_text="أدخل اسم المستخدم",
        prefix_icon="person",
        border_radius=14,
        bgcolor="#1E1E2E",
        border_color="transparent",
        focused_border_color="#6C63FF",
        color="white",
        hint_style=ft.TextStyle(color="#666680"),
        text_align=ft.TextAlign.RIGHT,
        height=56,
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=16),
    )

    email_field = ft.TextField(
        hint_text="أدخل البريد الإلكتروني (اختياري)",
        prefix_icon="mail",
        border_radius=14,
        bgcolor="#1E1E2E",
        border_color="transparent",
        focused_border_color="#6C63FF",
        color="white",
        hint_style=ft.TextStyle(color="#666680"),
        text_align=ft.TextAlign.RIGHT,
        height=56,
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=16),
    )

    password_field = ft.TextField(
        hint_text="أدخل كلمة المرور",
        prefix_icon="lock",
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
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=16),
    )

    confirm_field = ft.TextField(
        hint_text="تأكيد كلمة المرور",
        prefix_icon="lock",
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
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=16),
    )

    error_text = ft.Text("", color="#FF4D4D", size=13, text_align=ft.TextAlign.CENTER)
    loading    = ft.ProgressRing(width=22, height=22, color="white", stroke_width=2, visible=False)

    def handle_signup(e):
        error_text.value    = ""
        loading.visible     = True
        signup_btn.disabled = True
        page.update()

        uname  = username_field.value.strip()
        email  = email_field.value.strip()
        pword  = password_field.value.strip()
        cpword = confirm_field.value.strip()

        if not uname or not pword:
            error_text.value    = "اسم المستخدم وكلمة المرور مطلوبان"
            loading.visible     = False
            signup_btn.disabled = False
            page.update()
            return

        if pword != cpword:
            error_text.value    = "كلمة المرور غير متطابقة"
            loading.visible     = False
            signup_btn.disabled = False
            page.update()
            return

        result = api.signup(uname, pword, email)

        loading.visible     = False
        signup_btn.disabled = False

        if result["success"]:
            page.run_task(page.push_route, "/login")
        else:
            error_text.value = result["message"]
        page.update()

    signup_btn = ft.Container(
        content=ft.Row([
            loading,
            ft.Text("إنشاء حساب  ←", size=16, weight=ft.FontWeight.BOLD, color="white"),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        bgcolor="#6C63FF",
        border_radius=14,
        height=56,
        on_click=handle_signup,
        ink=True,
    )

    logo = ft.Container(
        content=ft.Icon("person_add", size=36, color="white"),
        width=72, height=72,
        bgcolor="#6C63FF",
        border_radius=20,
        alignment=ft.Alignment(0, 0),
        shadow=ft.BoxShadow(blur_radius=24, color="#6C63FF55", offset=ft.Offset(0, 8)),
    )

    login_link = ft.TextButton(
        content=ft.Text("لديك حساب بالفعل؟ سجل دخولك", color="#6C63FF", size=13),
        on_click=lambda e: page.run_task(page.push_route, "/login"),
    )

    return ft.View(
        route="/signup",
        controls=[
            ft.Container(
                expand=True,
                padding=ft.Padding.symmetric(horizontal=28, vertical=40),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Container(height=20),
                        logo,
                        ft.Container(height=24),
                        ft.Text("إنشاء حساب جديد", size=24, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text("أهلاً بك في اطبعلي", size=16, color="#AAAACC"),
                        ft.Container(height=32),

                        ft.Text("اسم المستخدم", size=13, color="#AAAACC", text_align=ft.TextAlign.RIGHT, width=float("inf")),
                        ft.Container(height=6),
                        username_field,
                        ft.Container(height=16),

                        ft.Text("البريد الإلكتروني", size=13, color="#AAAACC", text_align=ft.TextAlign.RIGHT, width=float("inf")),
                        ft.Container(height=6),
                        email_field,
                        ft.Container(height=16),

                        ft.Text("كلمة المرور", size=13, color="#AAAACC", text_align=ft.TextAlign.RIGHT, width=float("inf")),
                        ft.Container(height=6),
                        password_field,
                        ft.Container(height=16),

                        ft.Text("تأكيد كلمة المرور", size=13, color="#AAAACC", text_align=ft.TextAlign.RIGHT, width=float("inf")),
                        ft.Container(height=6),
                        confirm_field,

                        ft.Container(height=8),
                        error_text,
                        ft.Container(height=16),

                        ft.Container(content=signup_btn, width=float("inf")),
                        ft.Container(height=20),
                        login_link,
                        ft.Container(height=20),

                        ft.Text("تصميم وتطوير / أحمد إبراهيم © 2026", size=11, color="#444455", text_align=ft.TextAlign.CENTER),
                    ],
                ),
            )
        ],
        bgcolor="#0F0F1A",
        padding=0,
    )