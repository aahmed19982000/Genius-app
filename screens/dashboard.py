import flet as ft
from api_client import client

ROLE_LABELS = {
    "manager":  "مدير",
    "employee": "موظف",
    "designer": "مصمم",
    "auditor":  "مراجع",
    "social":   "سوشيال",
}

ROLE_COLORS = {
    "manager":  "#1A3C5E",
    "employee": "#0D6E56",
    "designer": "#5C3D1A",
    "auditor":  "#6B6B66",
    "social":   "#1565A8",
}

def dashboard_view(page: ft.Page):
    page.clean()
    page.title      = "لوحة التحكم"
    page.rtl        = True
    page.bgcolor    = "#F0F6FB"
    page.padding    = 0

    user       = client.user or {}
    full_name  = user.get("full_name", user.get("username", ""))
    role       = user.get("role", "employee")
    job_title  = user.get("job_title", "")
    role_label = ROLE_LABELS.get(role, role)
    role_color = ROLE_COLORS.get(role, "#1A3C5E")

    def go_logout(e):
        client.logout()
        from screens.login import login_view
        login_view(page)

    def go_tasks(e):
        from screens.tasks import tasks_view
        tasks_view(page)

    def go_social(e):
        from screens.social import social_view
        social_view(page)


    # Header
    header = ft.Container(
        content=ft.Row([
            ft.IconButton(ft.Icons.LOGOUT, icon_color="white",
                          tooltip="تسجيل الخروج", on_click=go_logout),
            ft.Column([
                ft.Text(f"أهلاً، {full_name}", size=18,
                        weight=ft.FontWeight.BOLD, color="white"),
                ft.Text(job_title or role_label, size=12, color="#D0E8F5"),
            ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END),
            ft.Container(
                content=ft.Text(role_label[0], size=20,
                                weight=ft.FontWeight.BOLD, color="white"),
                width=48, height=48,
                bgcolor=role_color + "99",
                border_radius=24,
                alignment=ft.Alignment(0, 0),
                border=ft.Border.all(2, "white"),
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=role_color,
        padding=ft.padding.symmetric(horizontal=20, vertical=16),
    )

    # بطاقات التنقل
    def nav_card(icon, title, subtitle, color, on_click):
        return ft.GestureDetector(
            on_tap=on_click,
            content=ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(title, size=15, weight=ft.FontWeight.BOLD,
                                color="#1A3C5E"),
                        ft.Text(subtitle, size=12, color="#6B6B66"),
                    ], spacing=4, expand=True,
                       horizontal_alignment=ft.CrossAxisAlignment.END),
                    ft.Container(
                        content=ft.Icon(icon, color="white", size=28),
                        width=52, height=52,
                        bgcolor=color,
                        border_radius=14,
                        alignment=ft.Alignment(0, 0),
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor="white",
                border_radius=14,
                padding=16,
                shadow=ft.BoxShadow(blur_radius=8, color="#00000012",
                                    offset=ft.Offset(0, 2)),
            ),
        )

    cards = ft.Column([
        nav_card(ft.Icons.TASK_ALT, "المهام", "عرض وإدارة المهام",
                 "#1A3C5E", go_tasks),
        nav_card(ft.Icons.SHARE, "السوشيال ميديا", "إدارة البوستات والمنشورات",
         "#1565A8", go_social),
        nav_card(ft.Icons.ANALYTICS, "المنافسون", "تحليل المنافسين",
                 "#5C3D1A", lambda e: None),
        nav_card(ft.Icons.CALENDAR_MONTH, "تخطيط المحتوى", "خطط وبيانات GSC",
                 "#0D6E56", lambda e: None),
    ], spacing=12)

    page.add(
        ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    ft.Text("الأقسام الرئيسية", size=16,
                            weight=ft.FontWeight.BOLD, color="#1A3C5E"),
                    ft.Container(height=4),
                    cards,
                ], spacing=8),
                padding=16,
                expand=True,
            ),
        ], spacing=0, expand=True),
    )