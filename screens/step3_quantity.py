import flet as ft
from components.navbar import bottom_navbar


def step3_quantity_screen(page: ft.Page, order_data: dict, on_next, on_back):

    sheets_count = {"value": int(order_data.get("number_of_sheets") or order_data.get("pages") or 1)}
    copies_count = {"value": int(order_data.get("quantity") or order_data.get("copies") or 1)}

    sheets_text = ft.Text(str(sheets_count["value"]), size=18, weight=ft.FontWeight.BOLD, color="#1a237e")
    copies_text = ft.Text(str(copies_count["value"]), size=18, weight=ft.FontWeight.BOLD, color="#1a237e")

    address_field = ft.TextField(
        hint_text="أدخل العنوان بالتفصيل (الحي، الشارع، رقم المبنى)",
        hint_style=ft.TextStyle(color="#aaaaaa", size=13),
        border=ft.border.all(1, "#e0e0e0"),
        border_radius=10,
        bgcolor="white",
        color="#222222",
        text_align=ft.TextAlign.RIGHT,
        prefix_icon="location_on",
        multiline=False,
        value=order_data.get("address", ""),
        content_padding=ft.Padding(12, 14, 12, 14),
    )

    notes_field = ft.TextField(
        hint_text="أضف أي تعليمات خاصة بالتغليف أو التوصيل هنا...",
        hint_style=ft.TextStyle(color="#aaaaaa", size=13),
        border=ft.border.all(1, "#e0e0e0"),
        border_radius=10,
        bgcolor="white",
        color="#222222",
        text_align=ft.TextAlign.RIGHT,
        multiline=True,
        min_lines=3,
        max_lines=5,
        value=order_data.get("notes", ""),
        content_padding=ft.Padding(12, 14, 12, 14),
    )

    def update_sheets(delta):
        sheets_count["value"] = max(1, sheets_count["value"] + delta)
        sheets_text.value = str(sheets_count["value"])
        page.update()

    def update_copies(delta):
        copies_count["value"] = max(1, copies_count["value"] + delta)
        copies_text.value = str(copies_count["value"])
        page.update()

    def counter_row(label, icon, count_text, on_dec, on_inc):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, size=18, color="#555555"),
                    ft.Text(label, size=14, color="#555555", weight=ft.FontWeight.W_500),
                ], alignment=ft.MainAxisAlignment.END, spacing=8),
                ft.Container(height=10),
                ft.Row([
                    ft.Container(
                        content=ft.Icon("add", color="white", size=20),
                        width=44, height=44, border_radius=10,
                        bgcolor="#1a237e", alignment=ft.Alignment(0, 0),
                        on_click=lambda e: on_inc(),
                        ink=True,
                    ),
                    ft.Container(expand=True, content=count_text, alignment=ft.Alignment(0, 0)),
                    ft.Container(
                        content=ft.Icon("remove", color="#1a237e", size=20),
                        width=44, height=44, border_radius=10,
                        bgcolor="#e8eaf0", alignment=ft.Alignment(0, 0),
                        on_click=lambda e: on_dec(),
                        ink=True,
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ], spacing=0),
            bgcolor="white",
            border_radius=14,
            padding=ft.Padding(16, 16, 16, 16),
            border=ft.border.all(1, "#e8eaf0"),
        )

    # حساب التكلفة
    printing_cost = 24.00
    delivery_cost = 15.00
    tax = round((printing_cost + delivery_cost) * 0.15, 2)
    total = printing_cost + delivery_cost + tax

    summary_box = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(f"{printing_cost:.2f} ر.س", size=14, color="#222222", weight=ft.FontWeight.BOLD),
                ft.Text("تكلفة الطباعة", size=14, color="#555555"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=8),
            ft.Row([
                ft.Text(f"{delivery_cost:.2f} ر.س", size=14, color="#222222", weight=ft.FontWeight.BOLD),
                ft.Text("رسوم التوصيل", size=14, color="#555555"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=8),
            ft.Row([
                ft.Text(f"{tax:.2f} ر.س", size=14, color="#222222", weight=ft.FontWeight.BOLD),
                ft.Text("الضريبة (15%)", size=14, color="#555555"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color="#ffffff33", height=20),
            ft.Row([
                ft.Text(f"{total:.2f} ر.س", size=20, color="white", weight=ft.FontWeight.BOLD),
                ft.Text("الإجمالي", size=16, color="white", weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=12),
            ft.Container(
                content=ft.Row([
                    ft.Icon("info_outline", color="#aaaaff", size=16),
                    ft.Text(
                        "سيتم مراجعة الطلب من قبل فريقنا قبل الطباعة لضمان أعلى جودة\nسيصلك الشعار عند بدء التنفيذ.",
                        size=11, color="#ccccff", text_align=ft.TextAlign.RIGHT,
                    ),
                ], spacing=8, alignment=ft.MainAxisAlignment.END),
                bgcolor="#ffffff11",
                border_radius=10,
                padding=ft.Padding(12, 10, 12, 10),
            ),
        ], spacing=0),
        bgcolor="#1a237e",
        border_radius=16,
        padding=ft.Padding(16, 20, 16, 20),
    )

    def handle_next(e):
        if not address_field.value or not address_field.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("يرجى إدخال عنوان التوصيل"), bgcolor="#FF4D4D")
            page.snack_bar.open = True
            page.update()
            return
        order_data["number_of_sheets"] = sheets_count["value"]
        order_data["quantity"] = copies_count["value"]
        order_data["address"] = address_field.value.strip()
        order_data["notes"] = notes_field.value.strip()
        order_data["printing_cost"] = printing_cost
        order_data["delivery_cost"] = delivery_cost
        order_data["tax"] = tax
        order_data["total"] = total
        on_next(order_data)

    stepper = _build_stepper(current=3)

    next_btn = ft.Container(
        content=ft.Text("متابعة للدفع  ←", size=16, weight=ft.FontWeight.BOLD,
                        color="white", text_align=ft.TextAlign.CENTER),
        bgcolor="#1a237e",
        border_radius=14,
        height=54,
        alignment=ft.Alignment(0, 0),
        on_click=handle_next,
        ink=True,
    )

    back_btn = ft.Container(
        content=ft.Row([
            ft.Icon("arrow_forward", color="#1a237e", size=18),
            ft.Text("رجوع", size=14, color="#1a237e", weight=ft.FontWeight.BOLD),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
        border=ft.border.all(1.5, "#1a237e"),
        border_radius=14,
        height=54,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: on_back(),
        ink=True,
    )

    return ft.View(
        route="/step3",
        controls=[
            ft.Column([
                stepper,
                ft.Container(
                    expand=True,
                    padding=ft.Padding(16, 16, 16, 16),
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        spacing=0,
                        controls=[
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("تفاصيل الكمية والعنوان", size=18,
                                            weight=ft.FontWeight.BOLD, color="#1a237e",
                                            text_align=ft.TextAlign.CENTER),
                                    ft.Container(height=18),
                                    counter_row(
                                        "عدد الصفحات (لكل نسخة)", "description",
                                        sheets_text,
                                        lambda: update_sheets(-1),
                                        lambda: update_sheets(1),
                                    ),
                                    ft.Container(height=12),
                                    counter_row(
                                        "عدد النسخ المطلوبة", "content_copy",
                                        copies_text,
                                        lambda: update_copies(-1),
                                        lambda: update_copies(1),
                                    ),
                                    ft.Container(height=16),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Row([
                                                ft.Text("عنوان التوصيل", size=14,
                                                        color="#555555", weight=ft.FontWeight.W_500),
                                            ], alignment=ft.MainAxisAlignment.END),
                                            ft.Container(height=8),
                                            address_field,
                                            ft.Container(height=10),
                                            ft.Container(
                                                content=ft.Row([
                                                    ft.Icon("map", color="#1a237e", size=18),
                                                    ft.Text("تحديد من الخريطة", size=13,
                                                            color="#1a237e", weight=ft.FontWeight.BOLD),
                                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                                bgcolor="#e8eaf0",
                                                border_radius=10,
                                                height=44,
                                                alignment=ft.Alignment(0, 0),
                                                ink=True,
                                            ),
                                        ], spacing=0),
                                        bgcolor="white",
                                        border_radius=14,
                                        padding=ft.Padding(16, 16, 16, 16),
                                        border=ft.border.all(1, "#e8eaf0"),
                                    ),
                                    ft.Container(height=12),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Row([
                                                ft.Text("ملاحظات إضافية (اختياري)", size=14,
                                                        color="#555555", weight=ft.FontWeight.W_500),
                                            ], alignment=ft.MainAxisAlignment.END),
                                            ft.Container(height=8),
                                            notes_field,
                                        ], spacing=0),
                                        bgcolor="white",
                                        border_radius=14,
                                        padding=ft.Padding(16, 16, 16, 16),
                                        border=ft.border.all(1, "#e8eaf0"),
                                    ),
                                    ft.Container(height=16),
                                    summary_box,
                                ], spacing=0),
                                bgcolor="#f0f2f8",
                                border_radius=16,
                                padding=ft.Padding(0, 0, 0, 0),
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Container(expand=True, content=back_btn),
                        ft.Container(width=12),
                        ft.Container(expand=True, content=next_btn),
                    ], spacing=0),
                    padding=ft.Padding(16, 12, 16, 12),
                    bgcolor="white",
                    border=ft.border.only(top=ft.BorderSide(1, "#e8eaf0")),
                ),
            ], spacing=0, expand=True),
        ],
        navigation_bar=bottom_navbar(page, current_index=1),
        bgcolor="#f0f2f8",
        padding=0,
    )


def _build_stepper(current: int):
    steps = [
        ("1", "رفع الملف"),
        ("2", "الخيارات"),
        ("3", "الكمية"),
        ("4", "الدفع"),
    ]
    items = []
    for i, (num, label) in enumerate(steps):
        is_active = (i + 1) == current
        is_done = (i + 1) < current

        if is_done:
            circle = ft.Container(
                content=ft.Icon("check", size=16, color="white"),
                width=36, height=36, border_radius=18,
                bgcolor="#1a237e", alignment=ft.Alignment(0, 0),
            )
        elif is_active:
            circle = ft.Container(
                content=ft.Text(num, size=14, weight=ft.FontWeight.BOLD, color="white"),
                width=36, height=36, border_radius=18,
                bgcolor="#1a237e", alignment=ft.Alignment(0, 0),
            )
        else:
            circle = ft.Container(
                content=ft.Text(num, size=14, weight=ft.FontWeight.BOLD, color="#888888"),
                width=36, height=36, border_radius=18,
                bgcolor="#e8eaf0", alignment=ft.Alignment(0, 0),
            )

        step_col = ft.Column([
            circle,
            ft.Container(height=4),
            ft.Text(label, size=11,
                    color="#1a237e" if is_active else "#888888",
                    weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)

        items.append(ft.Column([step_col], expand=True,
                               horizontal_alignment=ft.CrossAxisAlignment.CENTER))

        if i < len(steps) - 1:
            line_color = "#1a237e" if (i + 1) < current else "#e0e0e0"
            items.append(ft.Container(
                height=2, expand=True, bgcolor=line_color,
                margin=ft.Margin(0, 0, 0, 20),
            ))

    return ft.Container(
        content=ft.Row(items, alignment=ft.MainAxisAlignment.CENTER),
        bgcolor="white",
        padding=ft.Padding(16, 14, 16, 14),
        border=ft.border.only(bottom=ft.BorderSide(1, "#e8eaf0")),
    )
