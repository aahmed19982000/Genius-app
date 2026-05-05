import flet as ft
from api_client import api
from components.navbar import bottom_navbar


def step4_payment_screen(page: ft.Page, order_data: dict, on_back):

    selected_payment = {"method": "mada"}

    loading = ft.ProgressRing(width=22, height=22, color="white", stroke_width=2, visible=False)
    error_text = ft.Text("", color="#FF4D4D", size=13, text_align=ft.TextAlign.CENTER)

    file_name = order_data.get("file", {}).get("name", "ملف.pdf")
    paper_type = order_data.get("paper_type_label", "80 - A4 جرام")
    color = order_data.get("color_label", "ملون كامل")
    sides = order_data.get("sides_label", "وجه واحد")
    finishing = order_data.get("finishing_label", "تغليف لولبي بلاستيك")
    quantity = order_data.get("quantity", 5)
    address = order_data.get("address", "")
    printing_cost = order_data.get("printing_cost", 85.00)
    total = order_data.get("total", 0.00)

    payment_methods = [
        {"id": "apple_pay", "label": "ابل باي", "icon": "phone_iphone"},
        {"id": "visa",      "label": "فيزا",    "icon": "credit_card"},
        {"id": "mada",      "label": "مدى",     "icon": "payment"},
    ]

    payment_btns = {}

    def select_payment(method_id):
        selected_payment["method"] = method_id
        for mid, container in payment_btns.items():
            container.border = ft.Border.all(2, "#1a237e" if mid == method_id else "#e0e0e0")
            container.bgcolor = "#e8eaf0" if mid == method_id else "white"
        page.update()

    def make_payment_btn(method):
        mid = method["id"]
        is_selected = mid == selected_payment["method"]
        container = ft.Container(
            content=ft.Column([
                ft.Icon(method["icon"], size=24, color="#1a237e"),
                ft.Container(height=4),
                ft.Text(method["label"], size=11, color="#333333",
                        text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            border=ft.Border.all(2, "#1a237e" if is_selected else "#e0e0e0"),
            border_radius=12,
            bgcolor="#e8eaf0" if is_selected else "white",
            padding=ft.Padding(10, 10, 10, 10),
            height=70,
            expand=True,
            alignment=ft.Alignment(0, 0),
            on_click=lambda e, m=mid: select_payment(m),
            ink=True,
        )
        payment_btns[mid] = container
        return container

    async def handle_confirm(e):
        error_text.value = ""
        loading.visible = True
        confirm_btn.disabled = True
        page.update()

        print("DEBUG: زر الدفع اتضغط")
        print("DEBUG: order_data =", order_data)

        try:
            result = await api.create_order(
                file_path=order_data.get("file", {}).get("path", ""),
                paper_type_id=order_data.get("paper_type_id"),
                paper_size_id=order_data.get("paper_size_id"),
                printing_color_id=order_data.get("color_id"),
                printing_sides=order_data.get("sides"),
                number_of_sheets=order_data.get("number_of_sheets", 1),
                quantity=order_data.get("quantity", 1),
                address=order_data.get("address", ""),
                notes=order_data.get("notes", ""),
            )

            print("DEBUG: result =", result)

            loading.visible = False
            confirm_btn.disabled = False

            if result["success"]:
                page.snack_bar = ft.SnackBar(
                    ft.Text("✅ تم تأكيد الطلب بنجاح!"), bgcolor="#4DFF91"
                )
                page.snack_bar.open = True
                page.update()
                await page.push_route("/my-orders")
            else:
                error_text.value = result.get("message", "حدث خطأ، حاول مجدداً")
                page.update()

        except Exception as ex:
            loading.visible = False
            confirm_btn.disabled = False
            error_text.value = f"خطأ: {str(ex)}"
            print("DEBUG: exception =", ex)
            page.update()

    confirm_btn = ft.Container(
        content=ft.Row([
            loading,
            ft.Icon("payment", color="white", size=20),
            ft.Text("تأكيد ودفع", size=16, weight=ft.FontWeight.BOLD, color="white"),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        bgcolor="#1a237e",
        border_radius=14,
        height=54,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: page.run_task(handle_confirm, e),
        ink=True,
    )

    stepper = _build_stepper(current=4)

    # ── بطاقة ملخص الطلب ── ارتفاع ثابت 220
    order_summary_card = ft.Container(
        height=220,
        content=ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Icon("description", size=24, color="#1a237e"),
                    width=50, height=50, border_radius=10,
                    bgcolor="#e8eaf0", alignment=ft.Alignment(0, 0),
                ),
                ft.Container(width=12),
                ft.Column([
                    ft.Text(file_name, size=13, weight=ft.FontWeight.BOLD,
                            color="#222222", text_align=ft.TextAlign.RIGHT,
                            max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Container(height=6),
                    ft.Row([
                        ft.Column([
                            ft.Text("نوع الورق", size=10, color="#888888"),
                            ft.Text(paper_type, size=12, color="#222222",
                                    weight=ft.FontWeight.BOLD),
                        ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.END),
                        ft.Column([
                            ft.Text("الألوان", size=10, color="#888888"),
                            ft.Text(color, size=12, color="#222222",
                                    weight=ft.FontWeight.BOLD),
                        ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.END),
                    ], alignment=ft.MainAxisAlignment.END, spacing=16),
                    ft.Container(height=4),
                    ft.Row([
                        ft.Column([
                            ft.Text("التغليف", size=10, color="#888888"),
                            ft.Text(finishing, size=12, color="#222222",
                                    weight=ft.FontWeight.BOLD,
                                    max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                        ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.END),
                        ft.Column([
                            ft.Text("الكمية", size=10, color="#888888"),
                            ft.Text(f"{quantity} نسخ", size=12, color="#222222",
                                    weight=ft.FontWeight.BOLD),
                        ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.END),
                    ], alignment=ft.MainAxisAlignment.END, spacing=16),
                ], expand=True, spacing=0,
                   horizontal_alignment=ft.CrossAxisAlignment.END),
            ], alignment=ft.MainAxisAlignment.END),
        ], spacing=0, tight=True),
        bgcolor="white", border_radius=14,
        padding=ft.Padding(16, 16, 16, 16),
        border=ft.Border.all(1, "#e8eaf0"),
    )

    # ── بطاقة عنوان التوصيل ── ارتفاع ثابت 100
    address_card = ft.Container(
        height=100,
        content=ft.Column([
            ft.Row([
                ft.Icon("location_on", color="#1a237e", size=16),
                ft.Text("عنوان التوصيل", size=14,
                        color="#1a237e", weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.END, spacing=6),
            ft.Container(height=8),
            ft.Container(
                height=44,
                content=ft.Row([
                    ft.TextButton(
                        "تعديل",
                        style=ft.ButtonStyle(color="#1a237e"),
                        on_click=lambda e: on_back(),
                    ),
                    ft.Text(address, size=12, color="#333333",
                            text_align=ft.TextAlign.RIGHT, expand=True,
                            max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor="#f5f5f5",
                border_radius=10,
                padding=ft.Padding(8, 0, 8, 0),
            ),
        ], spacing=0, tight=True),
        bgcolor="white", border_radius=14,
        padding=ft.Padding(16, 14, 16, 14),
        border=ft.Border.all(1, "#e8eaf0"),
    )

    # ── بطاقة تفاصيل الدفع ── ارتفاع ثابت 240
    payment_card = ft.Container(
        height=260,
        content=ft.Column([
            ft.Text("تفاصيل الدفع", size=14, color="#1a237e",
                    weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT),
            ft.Container(height=10),
            ft.Row([
                ft.Text(f"{printing_cost:.2f} ج.م", size=13,
                        color="#222222", weight=ft.FontWeight.BOLD),
                ft.Text(f"سعر الطباعة ({quantity} نسخ)", size=12, color="#555555"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=16, color="#e8eaf0"),
            ft.Row([
                ft.Text(f"{total:.2f} ج.م", size=18, color="#1a237e",
                        weight=ft.FontWeight.BOLD),
                ft.Text("الإجمالي", size=15, color="#1a237e",
                        weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=14),
            ft.Text("اختر طريقة الدفع", size=12, color="#555555",
                    text_align=ft.TextAlign.RIGHT),
            ft.Container(height=8),
            ft.Row(
                [make_payment_btn(m) for m in payment_methods],
                spacing=8,
            ),
        ], spacing=0, tight=True),
        bgcolor="white", border_radius=14,
        padding=ft.Padding(16, 14, 16, 14),
        border=ft.Border.all(1, "#e8eaf0"),
    )

    return ft.View(
        route="/step4",
        controls=[
            ft.Column([
                stepper,
                ft.Container(
                    expand=True,
                    padding=ft.Padding(16, 12, 16, 12),
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        spacing=10,
                        controls=[
                            ft.Text("ملخص الطلب", size=18, weight=ft.FontWeight.BOLD,
                                    color="#1a237e", text_align=ft.TextAlign.CENTER),
                            order_summary_card,
                            address_card,
                            payment_card,
                            error_text,
                            confirm_btn,
                            ft.Container(height=4),
                            ft.Container(
                                height=40,
                                content=ft.TextButton(
                                    "العودة لتعديل الطلب",
                                    style=ft.ButtonStyle(color="#888888"),
                                    on_click=lambda e: on_back(),
                                ),
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Container(height=16),
                        ],
                    ),
                ),
            ], spacing=0, expand=True),
        ],
        navigation_bar=bottom_navbar(page, current_index=2),
        bgcolor="#f0f2f8",
        padding=0,
    )


def _build_stepper(current: int):
    steps = [
        ("1", "الملفات"),
        ("2", "الخيارات"),
        ("3", "العنوان"),
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
        border=ft.Border.only(bottom=ft.BorderSide(1, "#e8eaf0")),
    )