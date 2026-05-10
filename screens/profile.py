import flet as ft
from api_client import api
from components.navbar import bottom_navbar


def profile_screen(page: ft.Page):

    user = api.user_data or {}

    def handle_logout(e):
        api.access_token = None
        api.user_data = None
        page.go("/login")

    def nav_item(icon_name, label, on_click=None):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon_name, color="#2563EB", size=20),
                        width=38, height=38,
                        bgcolor="#EFF3FF",
                        border_radius=10,
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Text(label, size=15, weight=ft.FontWeight.W_600, color="#111111"),
                    ft.Container(expand=True),
                    ft.Icon(ft.Icons.CHEVRON_LEFT, color="#BBBBBB", size=20),
                ],
                spacing=14,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding(left=20, right=20, top=18, bottom=18),
            on_click=on_click,
            ink=True,
        )

    # Avatar with edit button overlay
    avatar = ft.Stack(
        controls=[
            ft.Container(
                content=ft.Image(
                    src="https://cdn-icons-png.flaticon.com/512/847/847969.png",
                    fit="contain",
                ),
                width=90, height=90,
                border_radius=45,
                bgcolor="#1A1A2E",
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.EDIT, color="white", size=14),
                width=28, height=28,
                bgcolor="#2563EB",
                border_radius=14,
                alignment=ft.Alignment(0, 0),
                bottom=0,
                left=0,
            ),
        ],
        width=90,
        height=90,
    )

    # Main options card
    main_card = ft.Container(
        content=ft.Column(
            controls=[
                nav_item(ft.Icons.PERSON, "تعديل الملف الشخصي"),
                ft.Divider(height=1, color="#F0F0F0"),
                nav_item(ft.Icons.LOCATION_ON, "عناوين التوصيل"),
                ft.Divider(height=1, color="#F0F0F0"),
                nav_item(ft.Icons.CREDIT_CARD, "طرق الدفع"),
            ],
            spacing=0,
        ),
        bgcolor="white",
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=8, color="#1A000000", offset=ft.Offset(0, 1)),
        margin=ft.Margin(left=18, right=18, top=0, bottom=0),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    # Logout card
    logout_card = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.LOGOUT, color="#E53935", size=20),
                    width=38, height=38,
                    bgcolor="#FFECEC",
                    border_radius=10,
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Text("تسجيل الخروج", size=15, weight=ft.FontWeight.W_600, color="#E53935"),
            ],
            spacing=14,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="white",
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=8, color="#1A000000", offset=ft.Offset(0, 1)),
        margin=ft.Margin(left=18, right=18, top=0, bottom=0),
        padding=ft.Padding(left=20, right=20, top=18, bottom=18),
        on_click=handle_logout,
        ink=True,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    return ft.View(
        route="/profile",
        controls=[
            ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    ft.ListView(
                        expand=True,
                        padding=0,
                        spacing=0,
                        controls=[
                            # Header
                            ft.Container(
                                content=ft.Text(
                                    "الملف الشخصي",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color="#111111",
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                padding=ft.Padding(left=0, right=0, top=28, bottom=20),
                                alignment=ft.Alignment(0, 0),
                            ),

                            # Avatar
                            ft.Container(content=avatar, alignment=ft.Alignment(0, 0)),
                            ft.Container(height=14),

                            # Name & email
                            ft.Text(
                                user.get("username", "أحمد بن محمد"),
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#111111",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                user.get("email", "ahmed.m@email.com"),
                                size=13,
                                color="#888888",
                                text_align=ft.TextAlign.CENTER,
                            ),

                            ft.Container(height=24),

                            # Main card
                            main_card,

                            ft.Container(height=14),

                            # Logout card
                            logout_card,

                            ft.Container(height=24),
                        ],
                    ),
                    bottom_navbar(page, current_index=4),
                ],
            )
        ],
        bgcolor="#F0F2F5",
        padding=0,
    )
