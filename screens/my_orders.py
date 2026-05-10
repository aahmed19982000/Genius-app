import flet as ft
from api_client import api
from components.navbar import bottom_navbar


def my_orders_screen(page: ft.Page):

    loading = ft.ProgressRing(width=32, height=32, color="#2563EB", stroke_width=3)
    error_text = ft.Text("", color="#E53935", size=13, text_align=ft.TextAlign.CENTER)
    orders_list = ft.Column(spacing=16)

    status_config = {
        "معلقه":          ("#FFF3CD", "#92400E", "#F59E0B"),
        "قيد التنفيذ":   ("#DBEAFE", "#1E40AF", "#2563EB"),
        "مكتمل":         ("#D1FAE5", "#065F46", "#10B981"),
        "ملغي":          ("#FFE4E6", "#9F1239", "#F43F5E"),
        "بانتظار الدفع": ("#EDE9FE", "#5B21B6", "#7C3AED"),
    }

    def format_date(date_raw: str) -> str:
        try:
            from datetime import datetime
            months_ar = ["يناير","فبراير","مارس","أبريل","مايو","يونيو",
                         "يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
            dt = datetime.strptime(str(date_raw)[:10], "%Y-%m-%d")
            return f"{dt.day:02d} {months_ar[dt.month-1]} {dt.year}"
        except Exception:
            return str(date_raw)[:10]

    def fk_name(field) -> str:
        if isinstance(field, dict):
            # try common key names
            for key in ("name", "paper_type", "size", "color_paper", "status"):
                if key in field:
                    return str(field[key])
            return str(next(iter(field.values()), "—"))
        return str(field) if field else "—"

    def sides_label(val: str) -> str:
        return {"one side": "وجه واحد", "two sides": "وجهين",
                "one_side": "وجه واحد", "two_sides": "وجهين",
                "tow side": "وجهين"}.get(val, val)

    def file_icon_widget(filename: str):
        ext = str(filename).split(".")[-1].lower()
        cfg = {
            "pdf":  (ft.Icons.PICTURE_AS_PDF, "#EFF6FF", "#2563EB"),
            "docx": (ft.Icons.DESCRIPTION,    "#F0FDF4", "#16A34A"),
            "doc":  (ft.Icons.DESCRIPTION,    "#F0FDF4", "#16A34A"),
            "png":  (ft.Icons.IMAGE,          "#FFF7ED", "#EA580C"),
            "jpg":  (ft.Icons.IMAGE,          "#FFF7ED", "#EA580C"),
            "jpeg": (ft.Icons.IMAGE,          "#FFF7ED", "#EA580C"),
        }.get(ext, (ft.Icons.INSERT_DRIVE_FILE, "#F8FAFC", "#64748B"))
        icon, bg, color = cfg
        return ft.Container(
            content=ft.Icon(icon, color=color, size=28),
            width=56, height=56, bgcolor=bg,
            border_radius=14, alignment=ft.Alignment(0, 0),
        )

    def status_chip(status_val: str):
        bg, txt, dot = status_config.get(status_val, ("#F1F5F9", "#64748B", "#94A3B8"))
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(width=7, height=7, bgcolor=dot, border_radius=4),
                    ft.Text(status_val, size=11, color=txt, weight=ft.FontWeight.W_600),
                ],
                spacing=5,
                tight=True,
            ),
            bgcolor=bg,
            border_radius=20,
            padding=ft.Padding(left=10, right=10, top=5, bottom=5),
        )

    def detail_row(icon, label: str, value: str, value_color="#1E293B"):
        return ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icon, size=15, color="#94A3B8"),
                        ft.Text(label, size=12, color="#94A3B8"),
                    ],
                    spacing=4,
                    tight=True,
                ),
                ft.Text(value, size=13, color=value_color,
                        weight=ft.FontWeight.W_500, rtl=True),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def order_card(order: dict):
        # ── Extract fields ──
        filename      = str(order.get("file_name", "")).split("/")[-1]
        customer_name = order.get("customer_name", "—")
        paper_type    = fk_name(order.get("paper_type", ""))
        paper_size    = fk_name(order.get("paper_size", ""))
        color         = fk_name(order.get("printing_color", ""))
        sides         = sides_label(order.get("printing_sides", ""))
        num_sheets    = str(order.get("number_of_sheets", "—"))
        quantity      = str(order.get("quantity", "—"))
        address       = str(order.get("address", "") or "—")
        notes         = str(order.get("notes", "") or "")
        total_cost    = order.get("total_cost", 0)
        created_at    = order.get("created_at", "")
        updated_at    = order.get("updated_at", "")
        status_raw    = order.get("status", {})
        status_val    = (fk_name(status_raw) if isinstance(status_raw, dict)
                         else str(status_raw))

        is_active   = "تنفيذ" in status_val
        is_done     = status_val == "مكتمل"
        is_payment  = "دفع" in status_val

        # ── Collapsible details panel ──
        details_col = ft.Column(spacing=10, visible=False)

        details_col.controls = [
            ft.Divider(height=1, color="#F1F5F9"),
            detail_row(ft.Icons.PERSON_OUTLINE, "اسم العميل", customer_name),
            detail_row(ft.Icons.DESCRIPTION_OUTLINED, "نوع الورق", paper_type),
            detail_row(ft.Icons.STRAIGHTEN, "حجم الورق", paper_size),
            detail_row(ft.Icons.COLOR_LENS_OUTLINED, "لون الطباعة", color),
            detail_row(ft.Icons.FLIP, "الطباعة", sides),
            detail_row(ft.Icons.LAYERS_OUTLINED, "عدد الأوراق", num_sheets),
            detail_row(ft.Icons.COPY_OUTLINED, "عدد النسخ", quantity),
            detail_row(ft.Icons.LOCATION_ON_OUTLINED, "العنوان", address),
            detail_row(ft.Icons.UPDATE, "آخر تحديث", format_date(updated_at)),
        ]
        if notes:
            details_col.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(notes, size=12, color="#64748B", rtl=True, expand=True),
                            ft.Row(controls=[
                                ft.Icon(ft.Icons.NOTES, size=15, color="#94A3B8"),
                                ft.Text("ملاحظات", size=12, color="#94A3B8"),
                            ], spacing=4, tight=True),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    bgcolor="#F8FAFC",
                    border_radius=10,
                    padding=ft.Padding(left=12, right=12, top=10, bottom=10),
                )
            )

        toggle_icon = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color="#94A3B8", size=18)

        def toggle_details(e):
            details_col.visible = not details_col.visible
            toggle_icon.name = (ft.Icons.KEYBOARD_ARROW_UP
                                if details_col.visible
                                else ft.Icons.KEYBOARD_ARROW_DOWN)
            page.update()

        # ── Action buttons ──
        track_btn_primary = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.LOCATION_SEARCHING, color="white", size=16),
                    ft.Text("تتبع الطلب", size=13, color="white", weight=ft.FontWeight.BOLD),
                ],
                spacing=6, alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True, height=42, bgcolor="#2563EB",
            border_radius=12, alignment=ft.Alignment(0, 0), ink=True,
            on_click=lambda e, oid=order.get("id"), oname=customer_name, ostatus=status_val, odate=created_at, ocost=total_cost: page.run_task(page.push_route, f"/track/{oid}?name={oname}&status={ostatus}&date={odate}&cost={ocost}"),
        )
        
        track_btn_icon = ft.Container(
            content=ft.Icon(ft.Icons.LOCATION_SEARCHING, color="#2563EB", size=18),
            width=42, height=42, bgcolor="#EFF6FF", border_radius=12,
            alignment=ft.Alignment(0, 0), ink=True,
            on_click=lambda e, oid=order.get("id"), oname=customer_name, ostatus=status_val, odate=created_at, ocost=total_cost: page.run_task(page.push_route, f"/track/{oid}?name={oname}&status={ostatus}&date={odate}&cost={ocost}"),
        )

        chat_btn_icon = ft.Container(
            content=ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE, color="#2563EB", size=18),
            width=42, height=42, bgcolor="#EFF6FF", border_radius=12,
            alignment=ft.Alignment(0, 0), ink=True,
            on_click=lambda e, oid=order.get("id"), oname=customer_name, ostatus=status_val: page.run_task(page.push_route, f"/chat/{oid}?name={oname}&status={ostatus}"),
        )

        btn_row_controls = []

        if is_active:
            btn_row_controls = [chat_btn_icon, track_btn_primary]
        elif is_done:
            reorder_btn = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.REFRESH, color="#2563EB", size=16),
                        ft.Text("إعادة الطلب", size=13, color="#2563EB", weight=ft.FontWeight.BOLD),
                    ],
                    spacing=6, alignment=ft.MainAxisAlignment.CENTER,
                ),
                expand=True, height=42, bgcolor="#EFF6FF",
                border_radius=12, alignment=ft.Alignment(0, 0), ink=True,
            )
            btn_row_controls = [track_btn_icon, reorder_btn]
        elif is_payment:
            pay_btn = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.PAYMENT, color="white", size=16),
                        ft.Text("ادفع الآن", size=13, color="white", weight=ft.FontWeight.BOLD),
                    ],
                    spacing=6, alignment=ft.MainAxisAlignment.CENTER,
                ),
                expand=True, height=42, bgcolor="#2563EB",
                border_radius=12, alignment=ft.Alignment(0, 0), ink=True,
            )
            delete_btn = ft.Container(
                content=ft.Icon(ft.Icons.DELETE_OUTLINE, color="#F43F5E", size=18),
                width=42, height=42, bgcolor="#FFF1F2", border_radius=12,
                alignment=ft.Alignment(0, 0), ink=True,
            )
            btn_row_controls = [delete_btn, track_btn_icon, pay_btn]
        else:
            btn_row_controls = [track_btn_primary]

        return ft.Container(
            content=ft.Column(
                controls=[
                    # ── Card header ──
                    ft.Row(
                        controls=[
                            # Left: file icon
                            file_icon_widget(filename),
                            ft.Container(width=12),
                            # Middle: name + date
                            ft.Column(
                                controls=[
                                    ft.Text(filename, size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color="#0F172A", rtl=True),
                                    ft.Text(format_date(created_at),
                                            size=12, color="#94A3B8"),
                                ],
                                spacing=3, expand=True,
                            ),
                            # Right: status badge
                            status_chip(status_val),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),

                    ft.Container(height=12),

                    # ── Cost highlight ──
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text("التكلفة الإجمالية",
                                                size=11, color="#94A3B8"),
                                        ft.Text(f"{total_cost} جنيه", size=18,
                                                color="#2563EB",
                                                weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=2,
                                    horizontal_alignment=ft.CrossAxisAlignment.END,
                                ),
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Text("التفاصيل", size=12,
                                                    color="#64748B"),
                                            toggle_icon,
                                        ],
                                        spacing=4,
                                        tight=True,
                                    ),
                                    on_click=toggle_details,
                                    ink=True,
                                    border_radius=8,
                                    padding=ft.Padding(left=10, right=10, top=6, bottom=6),
                                    bgcolor="#F8FAFC",
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        bgcolor="#F8FAFC",
                        border_radius=12,
                        padding=ft.Padding(left=14, right=14, top=12, bottom=12),
                    ),

                    # ── Collapsible details ──
                    details_col,

                    # ── Action buttons ──
                    *(
                        [
                            ft.Container(height=12),
                            ft.Row(
                                controls=btn_row_controls,
                                spacing=10,
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                        if btn_row_controls else []
                    ),
                ],
                spacing=0,
            ),
            bgcolor="white",
            border_radius=18,
            padding=ft.Padding(left=16, right=16, top=16, bottom=16),
            shadow=ft.BoxShadow(
                blur_radius=20, color="#0A000000",
                offset=ft.Offset(0, 4),
                spread_radius=0,
            ),
        )

    def load_orders(search: str = ""):
        orders_list.controls.clear()
        loading.visible = True
        error_text.value = ""
        page.update()

        result = api.get_my_orders()
        loading.visible = False

        if result["success"]:
            data = result["data"]
            if isinstance(data, list):
                orders = data
            elif isinstance(data, dict):
                orders = (data.get("results") or data.get("orders")
                          or data.get("data") or [])
            else:
                orders = []

            orders = [o for o in orders if isinstance(o, dict)]

            if search:
                s = search.lower()
                orders = [o for o in orders
                          if s in str(o.get("file_name", "")).lower()
                          or s in str(o.get("customer_name", "")).lower()]

            if not orders:
                orders_list.controls.append(
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Icon(ft.Icons.RECEIPT_LONG, size=72, color="#E2E8F0"),
                                ft.Text("لا توجد طلبات بعد", size=16,
                                        color="#94A3B8", weight=ft.FontWeight.W_500),
                                ft.Text("ستظهر طلباتك هنا بعد إنشائها",
                                        size=12, color="#CBD5E1"),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        alignment=ft.Alignment(0, 0),
                        padding=ft.Padding(left=0, right=0, top=80, bottom=80),
                    )
                )
            else:
                for order in orders:
                    orders_list.controls.append(order_card(order))
        else:
            error_text.value = result["message"]

        page.update()

    def on_search_change(e):
        load_orders(search=e.control.value or "")

    search_bar = ft.Row(
        controls=[
            ft.Container(
                content=ft.Icon(ft.Icons.TUNE, color="#2563EB", size=20),
                width=46, height=46,
                bgcolor="white", border_radius=14,
                border=ft.border.all(1, "#E2E8F0"),
                alignment=ft.Alignment(0, 0),
                shadow=ft.BoxShadow(blur_radius=6, color="#0A000000", offset=ft.Offset(0, 2)),
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SEARCH, color="#94A3B8", size=20),
                        ft.TextField(
                            hint_text="البحث في الطلبات ...",
                            hint_style=ft.TextStyle(color="#CBD5E1", size=13),
                            border=ft.InputBorder.NONE,
                            expand=True,
                            text_align=ft.TextAlign.RIGHT,
                            text_style=ft.TextStyle(size=13, color="#0F172A"),
                            on_change=on_search_change,
                            content_padding=ft.Padding(left=0, right=8, top=0, bottom=0),
                        ),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True, height=46,
                bgcolor="white", border_radius=14,
                border=ft.border.all(1, "#E2E8F0"),
                padding=ft.Padding(left=14, right=14, top=0, bottom=0),
                shadow=ft.BoxShadow(blur_radius=6, color="#0A000000", offset=ft.Offset(0, 2)),
            ),
        ],
        spacing=10,
    )

    load_orders()

    return ft.View(
        route="/my-orders",
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
                            # ── Header ──
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Icon(ft.Icons.NOTIFICATIONS_NONE,
                                                            color="#2563EB", size=22),
                                            width=42, height=42,
                                            bgcolor="white", border_radius=13,
                                            border=ft.border.all(1, "#E2E8F0"),
                                            alignment=ft.Alignment(0, 0),
                                            shadow=ft.BoxShadow(blur_radius=6,
                                                                color="#0A000000",
                                                                offset=ft.Offset(0, 2)),
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.Text("طلباتي", size=22,
                                                        weight=ft.FontWeight.BOLD,
                                                        color="#0F172A", rtl=True),
                                                ft.Text("تتبع جميع طلباتك هنا",
                                                        size=12, color="#94A3B8", rtl=True),
                                            ],
                                            spacing=2,
                                            horizontal_alignment=ft.CrossAxisAlignment.END,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=ft.Padding(left=20, right=20, top=20, bottom=16),
                            ),

                            # ── Search ──
                            ft.Container(
                                content=search_bar,
                                padding=ft.Padding(left=20, right=20, top=0, bottom=20),
                            ),

                            # ── Loading / Error ──
                            ft.Container(
                                content=loading,
                                alignment=ft.Alignment(0, 0),
                                padding=ft.Padding(left=0, right=0, top=20, bottom=20),
                            ),
                            ft.Container(
                                content=error_text,
                                padding=ft.Padding(left=20, right=20, top=0, bottom=0),
                            ),

                            # ── Orders ──
                            ft.Container(
                                content=orders_list,
                                padding=ft.Padding(left=20, right=20, top=0, bottom=24),
                            ),
                        ],
                    ),
                    bottom_navbar(page, current_index=1),
                ],
            )
        ],
        bgcolor="#F1F5F9",
        padding=0,
    )
