import flet as ft
from components.navbar import bottom_navbar


def home_screen(page: ft.Page, on_print_now, username: str = ""):
    # ── Top Bar ────────────────────────────────────────────────────────
    top_bar = ft.Container(
        bgcolor="white",
        padding=ft.Padding(16, 12, 16, 12),
        content=ft.Row(
            [
                # Left: icon buttons
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.NOTIFICATIONS_OUTLINED,
                                size=20,
                                color="#374151",
                            ),
                            width=40,
                            height=40,
                            bgcolor="#F3F4F6",
                            border_radius=20,
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.PERSON_OUTLINED,
                                size=20,
                                color="#374151",
                            ),
                            width=40,
                            height=40,
                            bgcolor="#F3F4F6",
                            border_radius=20,
                            alignment=ft.Alignment(0, 0),
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
                            color="#111827",
                            weight=ft.FontWeight.W_500,
                            rtl=True,
                        ),
                        ft.Icon(
                            ft.Icons.LOCATION_ON_OUTLINED,
                            size=14,
                            color="#2563EB",
                        ),
                        ft.Text(
                            "توصيل إلى",
                            size=13,
                            color="#2563EB",
                            weight=ft.FontWeight.BOLD,
                            rtl=True,
                        ),
                    ],
                    spacing=3,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    # ── Greeting ───────────────────────────────────────────────────────
    greeting = ft.Container(
        bgcolor="white",
        padding=ft.Padding(16, 12, 16, 20),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("👋", size=30),
                        ft.Text(
                            f"مرحباً {username}" if username else "مرحباً",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color="#111827",
                            rtl=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Text(
                    "ماذا تود أن تطبع اليوم؟",
                    size=14,
                    color="#6B7280",
                    text_align=ft.TextAlign.CENTER,
                    rtl=True,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
    )

    # ── Main Card ──────────────────────────────────────────────────────
    main_card = ft.Container(
        bgcolor="white",
        border_radius=20,
        margin=ft.Margin(16, 0, 16, 16),
        padding=ft.Padding(0, 0, 0, 24),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=16,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            [
                # Printer image area (light grey bg, no border)
                ft.Container(
                    height=240,
                    bgcolor="#F3F4F6",
                    border_radius=ft.BorderRadius(20, 20, 0, 0),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Icon(
                        ft.Icons.PRINT,
                        size=120,
                        color="#9CA3AF",
                    ),
                ),

                ft.Container(height=20),

                # Card title
                ft.Text(
                    "اطبع مستنداتك بكل سهولة",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="#111827",
                    text_align=ft.TextAlign.CENTER,
                    rtl=True,
                ),

                ft.Container(height=10),

                # Card subtitle
                ft.Text(
                    "ارفع ملفاتك، اختر نوع الورق، واستلمها\nعند باب منزلك بكل سهولة",
                    size=13,
                    color="#6B7280",
                    text_align=ft.TextAlign.CENTER,
                    rtl=True,
                ),

                ft.Container(height=20),

                # CTA Button
                ft.Container(
                    margin=ft.Margin(20, 0, 20, 0),
                    height=54,
                    content=ft.Text(
                        "اطبع الآن",
                        size=17,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                        text_align=ft.TextAlign.CENTER,
                        rtl=True,
                    ),
                    bgcolor="#2563EB",
                    border_radius=14,
                    alignment=ft.Alignment(0, 0),
                    on_click=on_print_now,
                    ink=True,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
    )

    # ── Scrollable body ────────────────────────────────────────────────
    body = ft.ListView(
        expand=True,
        spacing=0,
        padding=ft.Padding(0, 0, 0, 20),
        controls=[
            ft.Container(bgcolor="white", height=1),  # separator
            greeting,
            ft.Container(height=4, bgcolor="#F9FAFB"),
            main_card,
        ],
    )

    return ft.View(
        route="/home",
        controls=[
            ft.Column(
                [top_bar, body],
                spacing=0,
                expand=True,
            ),
        ],
        navigation_bar=bottom_navbar(page, current_index=0),
        bgcolor="#F9FAFB",
        padding=0,
    )