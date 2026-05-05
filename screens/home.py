import flet as ft

from components.navbar import bottom_navbar


BLUE = "#2F67E8"
TEXT = "#101828"
MUTED = "#8A94A6"
LINE = "#EEF1F5"


def _round_icon(icon_name: str, on_click=None):
    return ft.Container(
        content=ft.Icon(icon_name, size=23, color="#172033"),
        width=48,
        height=48,
        bgcolor="#F5F7FA",
        border=ft.border.all(1, "#E9EDF3"),
        border_radius=24,
        alignment=ft.Alignment(0, 0),
        shadow=ft.BoxShadow(
            blur_radius=8,
            color="#0000000D",
            offset=ft.Offset(0, 2),
        ),
        ink=True,
        on_click=on_click,
    )


def _printer_illustration():
    return ft.Stack(
        width=315,
        height=265,
        controls=[
            ft.Container(
                left=45,
                top=216,
                width=225,
                height=18,
                border_radius=40,
                gradient=ft.RadialGradient(
                    center=ft.Alignment(0, 0),
                    radius=1.0,
                    colors=["#00000026", "#00000000"],
                ),
            ),
            ft.Container(
                left=98,
                top=30,
                width=120,
                height=78,
                bgcolor="#454545",
                border=ft.border.all(1, "#2A2A2A"),
                shadow=ft.BoxShadow(
                    blur_radius=14,
                    color="#0000001A",
                    offset=ft.Offset(0, 5),
                ),
            ),
            ft.Container(
                left=42,
                top=92,
                width=232,
                height=115,
                border_radius=14,
                bgcolor="#474747",
                border=ft.border.all(1, "#2C2C2C"),
                shadow=ft.BoxShadow(
                    blur_radius=16,
                    color="#00000035",
                    offset=ft.Offset(0, 10),
                ),
            ),
            ft.Container(
                left=82,
                top=92,
                width=150,
                height=38,
                border_radius=ft.BorderRadius(0, 0, 8, 8),
                bgcolor="#4A4A4A",
                border=ft.border.only(
                    left=ft.BorderSide(1, "#222222"),
                    right=ft.BorderSide(1, "#222222"),
                    bottom=ft.BorderSide(1, "#222222"),
                ),
            ),
            ft.Container(
                left=90,
                top=166,
                width=138,
                height=52,
                border_radius=9,
                bgcolor="#1F1F1F",
                border=ft.border.all(1, "#101010"),
            ),
            ft.Container(
                left=76,
                top=188,
                width=168,
                height=48,
                border_radius=8,
                bgcolor="#111111",
                border=ft.border.all(1, "#0B0B0B"),
            ),
            ft.Container(
                left=88,
                top=196,
                width=144,
                height=24,
                border_radius=4,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(0, -1),
                    end=ft.Alignment(0, 1),
                    colors=["#3A3A3A", "#101010"],
                ),
            ),
            ft.Container(
                left=76,
                top=227,
                width=168,
                height=10,
                border_radius=6,
                bgcolor="#595959",
            ),
            ft.Container(
                left=42,
                top=92,
                width=232,
                height=30,
                border_radius=ft.BorderRadius(14, 14, 0, 0),
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(0, -1),
                    end=ft.Alignment(0, 1),
                    colors=["#6F6F6F", "#444444"],
                ),
            ),
            ft.Container(
                left=145,
                top=150,
                width=24,
                height=18,
                content=ft.Icon(ft.Icons.FINGERPRINT, size=16, color="#5C5C5C"),
                alignment=ft.Alignment(0, 0),
            ),
        ],
    )


def home_screen(page: ft.Page, on_print_now, username: str = ""):
    display_name = username or "أحمد"

    status_bar = ft.Container(
        height=42,
        bgcolor="white",
        padding=ft.padding.only(left=28, right=28, top=8),
        content=ft.Row(
            [
                
                ft.Row(
                    
                    spacing=7,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    top_bar = ft.Container(
        bgcolor="white",
        padding=ft.padding.symmetric(horizontal=22, vertical=12),
        content=ft.Row(
            [
                ft.Row(
                    [
                        _round_icon(ft.Icons.PERSON_OUTLINED, lambda e: page.run_task(page.push_route, "/profile")),
                        _round_icon(ft.Icons.NOTIFICATIONS_OUTLINED),
                    ],
                    spacing=12,
                ),
                ft.Row(
                    [
                    
                    ],
                    spacing=4,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    greeting = ft.Container(
        bgcolor="white",
        padding=ft.padding.only(left=24, right=24, top=24, bottom=20),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("👋", size=30),
                        ft.Text(
                            f"مرحباً {display_name}",
                            size=27,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT,
                            rtl=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Text(
                    "ماذا تود أن تطبع اليوم؟",
                    size=16,
                    color=MUTED,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
    )

    hero_card = ft.Container(
        bgcolor="white",
        border_radius=22,
        margin=ft.margin.symmetric(horizontal=24),
        padding=ft.padding.only(left=22, right=22, top=30, bottom=28),
        shadow=ft.BoxShadow(
            blur_radius=18,
            color="#00000012",
            offset=ft.Offset(0, 4),
        ),
        border=ft.border.all(1, LINE),
        content=ft.Column(
            [
                ft.Container(
                    height=280,
                    alignment=ft.Alignment(0, 0),
                    content=_printer_illustration(),
                ),
                ft.Text(
                    "اطبع مستنداتك بكل سهولة",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True,
                ),
                ft.Container(height=6),
                ft.Text(
                    "ارفع ملفاتك، اختر نوع الورق، واستلمها\nعند باب منزلك بكل سهولة",
                    size=16,
                    color=MUTED,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True,
                    height=1.45,
                ),
                ft.Container(height=24),
                ft.Container(
                    height=62,
                    width=float("inf"),
                    bgcolor=BLUE,
                    border_radius=14,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text(
                        "اطبع الآن",
                        size=23,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                        text_align=ft.TextAlign.CENTER,
                        rtl=True,
                    ),
                    shadow=ft.BoxShadow(
                        blur_radius=8,
                        color="#2F67E840",
                        offset=ft.Offset(0, 3),
                    ),
                    ink=True,
                    on_click=on_print_now,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
    )

    return ft.View(
        route="/home",
        bgcolor="#FFFFFF",
        padding=0,
        controls=[
            ft.Column(
                [
                    status_bar,
                    top_bar,
                    ft.Container(
                        expand=True,
                        bgcolor="#FFFFFF",
                        content=ft.ListView(
                            expand=True,
                            padding=ft.padding.only(top=0, bottom=24),
                            spacing=0,
                            controls=[
                                greeting,
                                hero_card,
                                ft.Container(height=16),
                            ],
                        ),
                    ),
                ],
                expand=True,
                spacing=0,
            )
        ],
        navigation_bar=bottom_navbar(page, current_index=0),
    )
