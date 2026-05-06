import flet as ft

def track_order_screen(
    page: ft.Page,
    order_id: int,
    order_name: str = "طلب طباعة",
    order_status: str = "قيد التنفيذ",
    order_date: str = "",
    order_cost: str = "0.00"
):

    # --- Helpers ---
    def format_date_simple(date_raw: str):
        try:
            from datetime import datetime
            months_ar = ["يناير","فبراير","مارس","أبريل","مايو","يونيو",
                         "يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
            dt = datetime.fromisoformat(str(date_raw).replace("Z", "+00:00"))
            return f"{dt.day:02d} {months_ar[dt.month-1]} {dt.year}"
        except:
            return date_raw[:10] if date_raw else "اليوم"

    def format_time_simple(date_raw: str):
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(str(date_raw).replace("Z", "+00:00"))
            hour = dt.hour
            minute = dt.strftime("%M")
            period = "ص" if hour < 12 else "م"
            hour12 = hour % 12 or 12
            return f"{hour12}:{minute} {period}"
        except:
            return ""

    short_name = (order_name[:20] + "...") if len(order_name) > 20 else order_name
    display_date = format_date_simple(order_date)

    status_colors = {
        "قيد التنفيذ": "#2563EB",
        "مكتمل": "#10B981",
        "معلقه": "#F59E0B",
        "بانتظار الدفع": "#7C3AED",
        "ملغي": "#F43F5E",
    }
    status_color = status_colors.get(order_status, "#2563EB")

    # --- Header ---
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.NOTIFICATIONS_NONE, color="#2563EB", size=22),
                    width=40, height=40,
                    alignment=ft.Alignment(0, 0),
                    ink=True,
                ),
                ft.Text("تتبع الطلب", size=18, weight=ft.FontWeight.BOLD, color="#1E293B"),
                ft.Container(
                    content=ft.Icon(ft.Icons.ARROW_FORWARD, color="#2563EB", size=22),
                    width=40, height=40,
                    ink=True,
                    on_click=lambda e: page.go("/my-orders"),
                    alignment=ft.Alignment(0, 0),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="white",
        padding=ft.Padding(left=16, right=16, top=16, bottom=16),
    )

    # --- Order Info Card ---
    order_info_card = ft.Container(
        content=ft.Column(
            controls=[
                # Top part
                ft.Row(
                    controls=[
                        # Order Number
                        ft.Container(
                            content=ft.Text(f"ORD-#{order_id}", size=12, color="#475569", weight=ft.FontWeight.W_600),
                            bgcolor="#E2E8F0",
                            border_radius=16,
                            padding=ft.Padding(left=12, right=12, top=6, bottom=6),
                        ),
                        ft.Container(expand=True),
                        # Title and Status
                        ft.Column(
                            controls=[
                                ft.Text(short_name, size=15, weight=ft.FontWeight.BOLD, color="#0F172A", rtl=True),
                                ft.Row(
                                    controls=[
                                        ft.Text(order_status, size=12, color="#2563EB", weight=ft.FontWeight.W_600),
                                        ft.Container(width=8, height=8, bgcolor=status_color, border_radius=4),
                                    ],
                                    spacing=6,
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                            ],
                            spacing=4,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                        ),
                        # Icon
                        ft.Container(width=8),
                        ft.Container(
                            content=ft.Icon(ft.Icons.INSERT_DRIVE_FILE, color="white", size=24),
                            width=50, height=50,
                            bgcolor="#94A3B8",
                            border_radius=12,
                            alignment=ft.Alignment(0, 0),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                
                ft.Container(height=10),
                
                # Bottom part
                ft.Row(
                    controls=[
                        # Price
                        ft.Column(
                            controls=[
                                ft.Text("إجمالي المبلغ", size=11, color="#64748B"),
                                ft.Text(f"{order_cost} جنيه", size=14, color="#2563EB", weight=ft.FontWeight.BOLD),
                            ],
                            spacing=2,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        ),
                        # Date
                        ft.Column(
                            controls=[
                                ft.Text("تاريخ الطلب", size=11, color="#64748B"),
                                ft.Text(display_date, size=13, color="#1E293B", weight=ft.FontWeight.W_500),
                            ],
                            spacing=2,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=0,
        ),
        bgcolor="white",
        border_radius=16,
        padding=ft.Padding(left=20, right=20, top=20, bottom=20),
        shadow=ft.BoxShadow(blur_radius=10, color="#0A000000", offset=ft.Offset(0, 2)),
    )

    # --- Timeline State Logic ---
    # Statuses: معلقه, تم الاستلام, قيد التنفيذ, تم الشحن, مكتمل
    current_step = 1
    if order_status == "تم الاستلام":
        current_step = 2
    elif order_status == "قيد التنفيذ":
        current_step = 3
    elif order_status == "تم الشحن":
        current_step = 4
    elif order_status == "مكتمل":
        current_step = 5
    elif order_status == "ملغي":
        current_step = 0 # Can handle cancelled state

    def build_step(index, title, time_text, subtitle="", icon_name=None):
        is_completed = current_step > index
        is_current = current_step == index
        is_pending = current_step < index

        # Define colors and icons based on state
        if is_completed:
            circle_bg = "#2563EB"
            icon_color = "white"
            title_color = "#0F172A"
            icon = ft.Icons.CHECK
        elif is_current:
            circle_bg = "white"
            icon_color = "#2563EB"
            title_color = "#2563EB"
            icon = icon_name or ft.Icons.RADIO_BUTTON_CHECKED
        else: # pending
            circle_bg = "#F1F5F9"
            icon_color = "#94A3B8"
            title_color = "#94A3B8"
            icon = icon_name or ft.Icons.CIRCLE_OUTLINED

        circle_border = ft.border.all(2, "#2563EB") if is_current else None

        # Step Widget
        return ft.Row(
            controls=[
                # Details (Left)
                ft.Column(
                    controls=[
                        ft.Text(title, size=16 if is_current else 15, weight=ft.FontWeight.BOLD if is_current else ft.FontWeight.W_600, color=title_color, rtl=True),
                        ft.Text(time_text, size=12, color="#64748B", rtl=True) if time_text else ft.Container(),
                        (ft.Container(
                            content=ft.Text(subtitle, size=12, color="#2563EB", rtl=True),
                            bgcolor="#EFF6FF",
                            padding=ft.Padding(left=10, right=10, top=4, bottom=4),
                            border_radius=12,
                            margin=ft.Margin(top=4, left=0, right=0, bottom=0)
                        ) if subtitle and is_current else ft.Container()),
                    ],
                    spacing=2,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                ),
                ft.Container(width=16),
                # Circle (Right)
                ft.Container(
                    content=ft.Icon(icon, color=icon_color, size=16),
                    width=32, height=32,
                    bgcolor=circle_bg,
                    border=circle_border,
                    border_radius=16,
                    alignment=ft.Alignment(0, 0),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def build_line(is_active):
        color = "#2563EB" if is_active else "#E2E8F0"
        return ft.Container(
            width=2, height=40,
            bgcolor=color,
            margin=ft.Margin(left=0, right=15, top=4, bottom=4),
            alignment=ft.Alignment(1, 0),
        )

    timeline_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("حالة التوصيل", size=18, weight=ft.FontWeight.BOLD, color="#0F172A", rtl=True),
                ft.Container(height=16),
                
                # Steps
                build_step(1, "تم استلام الطلب", f"{display_date}, {format_time_simple(order_date) or '10:00 ص'}" if current_step >= 1 else ""),
                ft.Row([ft.Container(expand=True), build_line(current_step > 1)]),
                
                build_step(2, "قيد المراجعة", f"{display_date}, {format_time_simple(order_date) or '10:15 ص'}" if current_step >= 2 else ""),
                ft.Row([ft.Container(expand=True), build_line(current_step > 2)]),
                
                build_step(3, "جاري الطباعة", "" if current_step < 3 else f"{display_date}", subtitle="نعمل على طباعة ملفك الآن" if current_step == 3 else "", icon_name=ft.Icons.PRINT),
                ft.Row([ft.Container(expand=True), build_line(current_step > 3)]),
                
                build_step(4, "جاهز للتسليم / تم الشحن", "" if current_step < 4 else f"{display_date}", icon_name=ft.Icons.LOCAL_SHIPPING),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.END,
        ),
        bgcolor="white",
        border_radius=16,
        padding=ft.Padding(left=20, right=20, top=20, bottom=24),
        shadow=ft.BoxShadow(blur_radius=10, color="#0A000000", offset=ft.Offset(0, 2)),
    )

    # --- Support Card ---
    support_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("تحتاج مساعدة؟", size=18, weight=ft.FontWeight.BOLD, color="white", rtl=True),
                ft.Text("تواصل مع الدعم الفني لمتابعة طلبك", size=13, color="#DBEAFE", rtl=True),
                ft.Container(height=12),
                ft.Container(
                    content=ft.Text("تواصل معنا", size=14, weight=ft.FontWeight.BOLD, color="#2563EB"),
                    bgcolor="white",
                    border_radius=12,
                    padding=ft.Padding(left=24, right=24, top=12, bottom=12),
                    ink=True,
                    on_click=lambda _: page.go(f"/chat/{order_id}?name={order_name}&status={order_status}"),
                    alignment=ft.Alignment(0, 0),
                    width=130,
                ),
            ],
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.END,
        ),
        bgcolor="#1D4ED8",
        border_radius=16,
        padding=ft.Padding(left=24, right=24, top=24, bottom=24),
        shadow=ft.BoxShadow(blur_radius=12, color="#0A000000", offset=ft.Offset(0, 4)),
        margin=ft.Margin(left=0, right=0, top=10, bottom=20),
    )

    return ft.View(
        route=f"/track/{order_id}",
        controls=[
            ft.Column(
                controls=[
                    header,
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                order_info_card,
                                timeline_card,
                                support_card,
                            ],
                            spacing=16,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        expand=True,
                        padding=ft.Padding(left=16, right=16, top=8, bottom=20),
                    ),
                ],
                expand=True,
                spacing=0,
            )
        ],
        bgcolor="#F8FAFC",
        padding=0,
    )
