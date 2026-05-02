import flet as ft
from api_client import client

STATUS_COLORS = {
    "in_progress": ("#1565A8", "#D0E8F5"),
    "upload":      ("#5C3D1A", "#FFF3D0"),
    "publish":     ("#0D6E56", "#D6F0DF"),
    "done":        ("#2D7D46", "#D6F0DF"),
    "review":      ("#6C63FF", "#EEEDFE"),
    "rework":      ("#C0392B", "#FDECEA"),
}
STATUS_LABELS = {
    "in_progress": "جاري العمل",
    "upload":      "تم الرفع",
    "publish":     "تم النشر",
    "done":        "مكتملة",
    "review":      "تم المراجعة",
    "rework":      "إعادة العمل",
}

def tasks_view(page: ft.Page):
    page.clean()
    page.title   = "المهام"
    page.rtl     = True
    page.bgcolor = "#F0F6FB"
    page.padding = 0

    user = client.user or {}
    role = user.get("role", "employee")

    def go_back(e):
        from screens.dashboard import dashboard_view
        dashboard_view(page)

    # ── State ────────────────────────────────────────────────────────────────
    current_status = ft.Ref[str]()
    current_status.current = None
    tasks_column   = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    loading_ring   = ft.ProgressRing(color="#2E86AB", width=32, height=32)
    page_info      = ft.Text("", size=11, color="#6B6B66",
                             text_align=ft.TextAlign.CENTER)

    # ── Task card ─────────────────────────────────────────────────────────────
    def task_card(task):
        status    = task.get("status", "in_progress")
        s_color, s_bg = STATUS_COLORS.get(status, ("#6B6B66", "#F5F5F3"))
        s_label   = STATUS_LABELS.get(status, status)
        title     = task.get("article_title", "")[:60]
        writer    = task.get("writer_name", "")
        site      = task.get("site_name", "")
        date      = task.get("publish_date", "")
        task_type = task.get("article_type", "")

        def open_detail(e, t=task):
            task_detail_view(page, t)

        return ft.GestureDetector(
            on_tap=open_detail,
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text(s_label, size=10,
                                           weight=ft.FontWeight.BOLD,
                                           color=s_color),
                            bgcolor=s_bg,
                            padding=ft.padding.symmetric(horizontal=8, vertical=3),
                            border_radius=20,
                        ),
                        ft.Text(date, size=11, color="#6B6B66"),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(title, size=13, weight=ft.FontWeight.BOLD,
                            color="#1A3C5E", max_lines=2),
                    ft.Row([
                        ft.Text(site,   size=11, color="#2E86AB"),
                        ft.Text("•",    size=11, color="#AAAACC"),
                        ft.Text(writer, size=11, color="#6B6B66"),
                        ft.Text("•",    size=11, color="#AAAACC"),
                        ft.Text(task_type, size=10, color="#AAAACC",
                                max_lines=1),
                    ], spacing=4),
                ], spacing=6),
                bgcolor="white",
                border_radius=12,
                padding=14,
                shadow=ft.BoxShadow(blur_radius=6, color="#00000010",
                                    offset=ft.Offset(0, 2)),
            ),
        )

    # ── Load tasks ────────────────────────────────────────────────────────────
    def load_tasks(status_filter=None):
        tasks_column.controls.clear()
        tasks_column.controls.append(
            ft.Row([loading_ring], alignment=ft.MainAxisAlignment.CENTER)
        )
        page.update()

        if role in ['manager', 'auditor']:
            data = client.get_tasks(status=status_filter)
        else:
            data = client.get_my_tasks(status=status_filter)

        tasks_column.controls.clear()

        if not data:
            tasks_column.controls.append(
                ft.Text("تعذر تحميل المهام", color="#C0392B",
                        text_align=ft.TextAlign.CENTER)
            )
            page.update()
            return

        results = data if isinstance(data, list) else data.get("results", [])
        count   = data.get("count", len(results)) if isinstance(data, dict) else len(results)
        page_info.value = f"إجمالي المهام: {count}"

        if results:
            for t in results:
                tasks_column.controls.append(task_card(t))
        else:
            tasks_column.controls.append(
                ft.Text("لا توجد مهام", color="#6B6B66",
                        text_align=ft.TextAlign.CENTER)
            )
        page.update()

    # ── Filter chips ──────────────────────────────────────────────────────────
    selected_status = {"value": None}

    def make_chip(label, status_val):
        is_selected = selected_status["value"] == status_val
        s_color, s_bg = STATUS_COLORS.get(status_val, ("#6B6B66", "#F5F5F3"))

        def on_tap(e, sv=status_val):
            if selected_status["value"] == sv:
                selected_status["value"] = None
            else:
                selected_status["value"] = sv
            build_filters()
            load_tasks(selected_status["value"])

        return ft.GestureDetector(
            on_tap=on_tap,
            content=ft.Container(
                content=ft.Text(label, size=11,
                               weight=ft.FontWeight.BOLD,
                               color="white" if is_selected else s_color),
                bgcolor=s_color if is_selected else s_bg,
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=20,
                border=ft.border.all(1, s_color),
            ),
        )

    filters_row = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=8)

    def build_filters():
        filters_row.controls = [
            make_chip("الكل",         None),
            make_chip("جاري",         "in_progress"),
            make_chip("تم الرفع",     "upload"),
            make_chip("تم النشر",     "publish"),
            make_chip("مكتملة",       "done"),
            make_chip("إعادة العمل",  "rework"),
        ]
        page.update()

    build_filters()

    # ── Header ────────────────────────────────────────────────────────────────
    header = ft.Container(
        content=ft.Row([
            ft.IconButton(ft.Icons.REFRESH, icon_color="white",
                         on_click=lambda e: load_tasks(selected_status["value"])),
            ft.Text("المهام", size=18, weight=ft.FontWeight.BOLD, color="white"),
            ft.IconButton(ft.Icons.ARROW_FORWARD, icon_color="white",
                         on_click=go_back),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor="#1A3C5E",
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
    )

    page.add(
        ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    filters_row,
                    page_info,
                    tasks_column,
                ], spacing=8, expand=True),
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                expand=True,
            ),
        ], spacing=0, expand=True),
    )

    load_tasks()


# ══════════════════════════════════════════════════════════════════════════════
# Task Detail
# ══════════════════════════════════════════════════════════════════════════════
def task_detail_view(page: ft.Page, task: dict):
    page.clean()
    page.title   = "تفاصيل المهمة"
    page.rtl     = True
    page.bgcolor = "#F0F6FB"
    page.padding = 0

    status    = task.get("status", "in_progress")
    s_color, s_bg = STATUS_COLORS.get(status, ("#6B6B66", "#F5F5F3"))
    task_id   = task.get("id")
    user_role = (client.user or {}).get("role", "employee")

    snack = ft.SnackBar(content=ft.Text(""), bgcolor="#2D7D46")
    page.overlay.append(snack)

    def go_back(e):
        tasks_view(page)

    def show_snack(msg, color="#2D7D46"):
        snack.content = ft.Text(msg, color="white")
        snack.bgcolor = color
        snack.open    = True
        page.update()

    # ── Status update ─────────────────────────────────────────────────────────
    status_dropdown = ft.Dropdown(
        value=status,
        border_radius=10,
        bgcolor="white",
        options=[
            ft.dropdown.Option(key=k, text=v)
            for k, v in STATUS_LABELS.items()
        ],
    )

    def save_status(e):
        ok = client.update_task_status(task_id, status_dropdown.value)
        if ok:
            show_snack("تم تحديث الحالة ✓")
        else:
            show_snack("فشل التحديث", "#C0392B")

    header = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Text(STATUS_LABELS.get(status, status), size=11,
                               weight=ft.FontWeight.BOLD, color=s_color),
                bgcolor=s_bg,
                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                border_radius=20,
            ),
            ft.Text("تفاصيل المهمة", size=17,
                    weight=ft.FontWeight.BOLD, color="white"),
            ft.IconButton(ft.Icons.ARROW_FORWARD, icon_color="white",
                         on_click=go_back),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor="#1A3C5E",
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
    )

    def info_row(label, value, color="#2C2C2A"):
        return ft.Container(
            content=ft.Column([
                ft.Text(label, size=11, color="#6B6B66"),
                ft.Text(str(value) if value else "—", size=13,
                        color=color, selectable=True),
            ], spacing=2),
            bgcolor="white",
            border_radius=10,
            padding=12,
        )

    content = ft.Column([
        info_row("عنوان المقال",  task.get("article_title", ""), "#1A3C5E"),
        info_row("الكاتب",        task.get("writer_name", "")),
        info_row("موقع النشر",    task.get("site_name", "")),
        info_row("نوع المقال",    task.get("article_type", "")),
        info_row("تاريخ النشر",   task.get("publish_date", "")),
        info_row("رابط المقال",   task.get("article_link", ""), "#2E86AB"),
        info_row("تفاصيل المهمة", task.get("article_details", "")[:300]),

        # تحديث الحالة
        ft.Container(
            content=ft.Column([
                ft.Text("تحديث الحالة", size=12, color="#6B6B66"),
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Text("حفظ", color="white"),
                        on_click=save_status,
                        style=ft.ButtonStyle(
                            bgcolor="#1A3C5E",
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                    ft.Container(content=status_dropdown, expand=True),
                ], spacing=8),
            ], spacing=6) if user_role in ['manager', 'auditor', 'employee'] else ft.Container(),
            bgcolor="white",
            border_radius=10,
            padding=12,
        ),
    ], spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)

    page.add(
        ft.Column([
            header,
            ft.Container(content=content, padding=12, expand=True),
        ], spacing=0, expand=True),
    )