import flet as ft
from api_client import api


def login_screen(page: ft.Page):

    # ── Fields ──────────────────────────────────────────────
    email_field = ft.TextField(
        hint_text="أدخل الايميل",
        suffix_icon="mail_outline",
        border_radius=14,
        bgcolor="white",
        border_color="#E0E0E0",
        focused_border_color="#4169E1",
        color="#1A1A2E",
        hint_style=ft.TextStyle(color="#AAAAAA"),
        text_align=ft.TextAlign.RIGHT,
        height=56,
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=16),
    )

    password_field = ft.TextField(
        hint_text="••••••••••",
        suffix_icon="lock_outline",
        password=True,
        can_reveal_password=True,
        border_radius=14,
        bgcolor="white",
        border_color="#E0E0E0",
        focused_border_color="#4169E1",
        color="#1A1A2E",
        hint_style=ft.TextStyle(color="#AAAAAA"),
        text_align=ft.TextAlign.RIGHT,
        height=56,
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=16),
    )

    error_text = ft.Text(
        "", color="#FF4D4D", size=13, text_align=ft.TextAlign.CENTER
    )
    loading = ft.ProgressRing(
        width=22, height=22, color="white", stroke_width=2, visible=False
    )

    # ── Login handler ────────────────────────────────────────
    async def handle_login(e):
        error_text.value = ""
        loading.visible = True
        login_btn.disabled = True
        page.update()

        uname = email_field.value.strip()
        pword = password_field.value.strip()

        import asyncio
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: api.login(uname, pword)
        )

        loading.visible = False
        login_btn.disabled = False

        if result["success"]:
            await page.push_route("/home")
        else:
            error_text.value = result["message"]
        page.update()

    # ── Login button ─────────────────────────────────────────
    login_btn = ft.Container(
        content=ft.Row(
            [
                loading,
                ft.Text(
                    "تسجيل دخول",
                    size=17,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, 0),
            end=ft.Alignment(1, 0),
            colors=["#5B8DEF", "#3A5FD9"],
        ),
        border_radius=16,
        height=58,
        on_click=handle_login,
        ink=True,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color="#3A5FD950",
            offset=ft.Offset(0, 8),
        ),
    )

    # ── Social buttons ───────────────────────────────────────
    def social_btn(letter, letter_color, circle_color):
        return ft.Container(
            content=ft.Container(
                content=ft.Text(
                    letter,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=letter_color,
                ),
                width=40,
                height=40,
                border_radius=20,
                bgcolor=circle_color,
                alignment=ft.Alignment(0, 0),
            ),
            bgcolor="white",
            border_radius=40,
            width=80,
            height=56,
            alignment=ft.Alignment(0, 0),
            border=ft.Border.all(1, "#E8E8E8"),
            ink=True,
            shadow=ft.BoxShadow(
                blur_radius=8,
                color="#00000012",
                offset=ft.Offset(0, 2),
            ),
        )

    facebook_btn = social_btn("f", "#1877F2", "#E8F0FE")
    google_btn   = social_btn("G", "#DB4437", "#FDECEA")

    # ── Back button (top-right) ───────────────────────────────
    back_btn = ft.Container(
        content=ft.Icon("chevron_right", size=20, color="#F4E9E9"),
        bgcolor="white",
        border_radius=12,
        width=40,
        height=40,
        alignment=ft.Alignment(0, 0),
        shadow=ft.BoxShadow(
            blur_radius=8, color="#00000015", offset=ft.Offset(0, 2)
        ),

    )

    # ── Links ────────────────────────────────────────────────
    forgot_link = ft.TextButton(
        content=ft.Text("هل نسيت كلمة المرور؟", color="#4169E1", size=13),
        on_click=lambda e: None,
    )

    signup_row = ft.Row(
        [
            ft.TextButton(
                content=ft.Text(
                    "أنشاء حساب جديد",
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    style=ft.TextStyle(
                        color="#4169E1",
                        decoration=ft.TextDecoration.UNDERLINE,
                        decoration_color="#4169E1",
                    ),
                ),
                on_click=lambda e: page.run_task(page.push_route, "/signup"),
            ),
            ft.Text("ليس لديك حساب ؟", color="#555555", size=13),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
    )

    # ── Divider row ───────────────────────────────────────────
    divider_row = ft.Row(
        [
            ft.Container(height=1, expand=True, bgcolor="#E0E0E0"),
            ft.Text("أو متابعة التسجيل عبر", size=12, color="#AAAAAA"),
            ft.Container(height=1, expand=True, bgcolor="#E0E0E0"),
        ],
        spacing=10,
    )

    # ── Main view ────────────────────────────────────────────
    return ft.View(
        route="/login",
        controls=[
            ft.Container(
                expand=True,
                bgcolor="#F5F7FA",
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=0,
                    controls=[

                        # ── Top bar (back arrow) ──────────────
                        

                        # ── White card ────────────────────────
                        ft.Container(
                            margin=ft.margin.symmetric(horizontal=20),
                            padding=ft.Padding.symmetric(horizontal=24, vertical=32),
                            bgcolor="white",
                            border_radius=24,
                            shadow=ft.BoxShadow(
                                blur_radius=24,
                                color="#00000010",
                                offset=ft.Offset(0, 4),
                            ),
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=0,
                                controls=[

                                    # Titles
                                    ft.Text(
                                        "مرحباً بعودتك !",
                                        size=26,
                                        weight=ft.FontWeight.BOLD,
                                        color="#1A1A2E",
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Container(height=6),
                                    ft.Text(
                                        "مرحباً بك مرة أخرى، لقد افتقدناك",
                                        size=14,
                                        color="#888888",
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Container(height=28),

                                    # Email label + field
                                    ft.Container(
                                        content=ft.Text(
                                            "البريد الإلكتروني أو رقم الهاتف",
                                            size=13,
                                            color="#333333",
                                            weight=ft.FontWeight.W_500,
                                            text_align=ft.TextAlign.RIGHT,
                                        ),
                                        alignment=ft.Alignment(1, 0),
                                        width=float("inf"),
                                    ),
                                    ft.Container(height=8),
                                    email_field,
                                    ft.Container(height=16),

                                    # Password label + field
                                    ft.Container(
                                        content=ft.Text(
                                            "كلمة المرور",
                                            size=13,
                                            color="#333333",
                                            weight=ft.FontWeight.W_500,
                                            text_align=ft.TextAlign.RIGHT,
                                        ),
                                        alignment=ft.Alignment(1, 0),
                                        width=float("inf"),
                                    ),
                                    ft.Container(height=8),
                                    password_field,
                                    ft.Container(height=4),

                                    # Forgot password
                                    ft.Container(
                                        content=forgot_link,
                                        alignment=ft.Alignment(-1, 0),
                                        width=float("inf"),
                                    ),

                                    # Error
                                    error_text,
                                    ft.Container(height=20),

                                    # Login button
                                    ft.Container(
                                        content=login_btn,
                                        width=float("inf"),
                                    ),
                                    ft.Container(height=16),

                                    # Sign up link
                                    signup_row,
                                    ft.Container(height=24),

                                    # Divider
                                    divider_row,
                                    ft.Container(height=20),

                                    # Social buttons
                                    ft.Row(
                                        [facebook_btn, google_btn],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=16,
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(height=40),
                    ],
                ),
            )
        ],
        bgcolor="#F5F7FA",
        padding=0,
    )
