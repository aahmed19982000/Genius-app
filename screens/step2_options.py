import flet as ft
from api_client import api
from components.navbar import bottom_navbar


def step2_options_screen(page: ft.Page, file_info: dict, on_next, on_back):

    options_result = api.get_paper_options()
    options_data = options_result["data"] if options_result["success"] else {}
    paper_types    = options_data.get("paper_types", [])
    paper_sizes    = options_data.get("paper_sizes", [])
    paper_colors   = options_data.get("paper_colors", [])
    printing_sides = options_data.get("printing_sides", [])

    if not paper_types:
        paper_types = [{"id": "plain80", "paper_type": "عادي (80 جرام)", "price": 0.50}]
    if not paper_sizes:
        paper_sizes = [{"id": "A4", "size": "A4", "price": 0.10}]
    if not paper_colors:
        paper_colors = [{"id": "bw", "color_paper": "أسود وأبيض", "price": 0.20}]
    if not printing_sides:
        printing_sides = [{"value": "single", "label": "وجه واحد"}]

    paper_type_map  = {str(i): item for i, item in enumerate(paper_types)}
    paper_size_map  = {str(i): item for i, item in enumerate(paper_sizes)}
    paper_color_map = {str(i): item for i, item in enumerate(paper_colors)}
    side_labels     = {str(i): item["label"] for i, item in enumerate(printing_sides)}

    paper_type_labels  = {k: v["paper_type"] for k, v in paper_type_map.items()}
    paper_size_labels  = {k: v["size"] for k, v in paper_size_map.items()}
    paper_color_labels = {k: v["color_paper"] for k, v in paper_color_map.items()}

    selected_size  = {"value": "0"}
    selected_type  = {"value": "0"}
    selected_color = {"value": "0"}
    selected_sides = {"value": "0"}
    copies_count   = {"value": 1}

    # ✅ احسب عدد الصفحات من الباك اند
    PAGE_COUNT = api.get_page_count(
        file_info.get("path", ""),
        file_info.get("name", ""),
    )
    print(f"DEBUG: PAGE_COUNT = {PAGE_COUNT}")

    subtotal_text = ft.Text(
        "0.00 جنيه",
        size=13, weight=ft.FontWeight.BOLD, color="#1a237e",
    )
    price_detail_text = ft.Text(
        "",
        size=11, color="#888888",
    )
    copies_val_txt = ft.Text(
        str(copies_count["value"]),
        size=18, weight=ft.FontWeight.BOLD, color="#333333",
    )

    def update_price():
        size_price  = float(paper_size_map.get(selected_size["value"], {}).get("price", 0))
        type_price  = float(paper_type_map.get(selected_type["value"], {}).get("price", 0))
        color_price = float(paper_color_map.get(selected_color["value"], {}).get("price", 0))

        price_per_sheet = size_price + type_price + color_price
        
        side_label = side_labels.get(selected_sides["value"], "")
        is_double_sided = "وجهين" in side_label or "double" in str(selected_sides["value"]).lower()
        if is_double_sided:
            price_per_sheet *= 1.5
            number_of_sheets = (PAGE_COUNT + 1) // 2
        else:
            number_of_sheets = PAGE_COUNT

        total = price_per_sheet * number_of_sheets * copies_count["value"]

        subtotal_text.value = f"{total:.2f} جنيه"
        multiplier_str = " × 1.5 (وجهين)" if is_double_sided else ""
        price_detail_text.value = (
            f"({size_price:.2f} مقاس + {type_price:.2f} نوع + {color_price:.2f} لون){multiplier_str} × {number_of_sheets} ورقة"
        )
        
        try:
            if subtotal_text.page:
                subtotal_text.update()
            if price_detail_text.page:
                price_detail_text.update()
        except Exception:
            pass

    update_price()

    # ── Paper size ─────────────────────────────────────────
    size_btns: dict[str, ft.Container] = {}

    def make_size_btn(key, title, price):
        is_sel = selected_size["value"] == key
        c = ft.Container(
            height=64,
            content=ft.Column([
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD,
                        color="white" if is_sel else "#555555"),
                ft.Text(f"{float(price):.2f} جنيه", size=10,
                        color="white" if is_sel else "#aaaaaa"),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            border=ft.border.all(1.5, "#1a237e" if is_sel else "#dddddd"),
            border_radius=10,
            bgcolor="#1a237e" if is_sel else "white",
            padding=ft.Padding(6, 10, 6, 10),
            expand=True,
            alignment=ft.Alignment(0, 0),
            on_click=lambda e, k=key: select_size(k),
            ink=True,
        )
        size_btns[key] = c
        return c

    def select_size(key):
        selected_size["value"] = key
        for k, btn in size_btns.items():
            is_sel = k == key
            btn.bgcolor = "#1a237e" if is_sel else "white"
            btn.border  = ft.border.all(1.5, "#1a237e" if is_sel else "#dddddd")
            for col in btn.content.controls:
                col.color = "white" if is_sel else ("#555555" if col.size == 14 else "#aaaaaa")
            try:
                if btn.page:
                    btn.update()
            except Exception:
                pass
        update_price()

    size_row = ft.Row([
        make_size_btn(str(i), item["size"], item["price"])
        for i, item in enumerate(paper_sizes)
    ], spacing=8, wrap=False)

    # ── Paper type dropdown ────────────────────────────────
    def on_type_change(e):
        selected_type["value"] = e.control.value
        update_price()

    paper_type_dd = ft.Dropdown(
        value="0",
        options=[
            ft.dropdown.Option(
                key=str(i),
                text=f"{item['paper_type']} ({float(item['price']):.2f} جنيه)"
            )
            for i, item in enumerate(paper_types)
        ],
        border_radius=10,
        bgcolor="white",
        border_color="#e0e0e0",
        focused_border_color="#1a237e",
        color="#333333",
        text_align=ft.TextAlign.RIGHT,
        height=50,
    )
    paper_type_dd.on_change = on_type_change

    # ── Color & Sides ──────────────────────────────────────
    color_cards: dict[str, ft.Container] = {}
    sides_cards: dict[str, ft.Container] = {}

    def radio_card(key, icon, title, subtitle, group_dict, cards_dict, on_select):
        is_sel = group_dict["value"] == key
        c = ft.Container(
            height=60,
            content=ft.Row([
                ft.Container(
                    width=18, height=18, border_radius=9,
                    border=ft.border.all(2, "#1a237e" if is_sel else "#dddddd"),
                    bgcolor="#1a237e" if is_sel else "transparent",
                    content=ft.Icon("circle", size=8, color="white") if is_sel else None,
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Icon(icon, size=22, color="#555555"),
                ft.Column([
                    ft.Text(title,    size=13, weight=ft.FontWeight.BOLD, color="#333333"),
                    ft.Text(subtitle, size=11, color="#aaaaaa"),
                ], spacing=2),
            ], spacing=8),
            border=ft.border.all(1.5, "#1a237e" if is_sel else "#dddddd"),
            border_radius=12,
            padding=ft.Padding(12, 12, 12, 12),
            expand=True,
            on_click=lambda e, k=key: on_select(k),
            ink=True,
        )
        cards_dict[key] = c
        return c

    def select_color(key):
        selected_color["value"] = key
        for k, btn in color_cards.items():
            is_sel = k == key
            btn.border = ft.border.all(1.5, "#1a237e" if is_sel else "#dddddd")
            dot = btn.content.controls[0]
            dot.border  = ft.border.all(2, "#1a237e" if is_sel else "#dddddd")
            dot.bgcolor = "#1a237e" if is_sel else "transparent"
            dot.content = ft.Icon("circle", size=8, color="white") if is_sel else None
            try:
                if btn.page:
                    btn.update()
            except Exception:
                pass
        update_price()

    def select_sides(key):
        selected_sides["value"] = key
        for k, btn in sides_cards.items():
            is_sel = k == key
            btn.border = ft.border.all(1.5, "#1a237e" if is_sel else "#dddddd")
            dot = btn.content.controls[0]
            dot.border  = ft.border.all(2, "#1a237e" if is_sel else "#dddddd")
            dot.bgcolor = "#1a237e" if is_sel else "transparent"
            dot.content = ft.Icon("circle", size=8, color="white") if is_sel else None
            try:
                if btn.page:
                    btn.update()
            except Exception:
                pass
        update_price()

    color_grid = ft.Row([
        radio_card(
            str(i),
            "palette" if ("لون" in item["color_paper"] or "color" in item["color_paper"].lower()) else "contrast",
            f"{item['color_paper']} ({float(item['price']):.2f} جنيه)",
            "اختيار لون الطباعة",
            selected_color, color_cards, select_color,
        )
        for i, item in enumerate(paper_colors)
    ], spacing=10, wrap=False)

    sides_grid = ft.Row([
        radio_card(
            str(i),
            "import_contacts" if ("وجهين" in item["label"] or "double" in str(item["value"]).lower()) else "menu_book",
            item["label"],
            "اختيار وجه الطباعة",
            selected_sides, sides_cards, select_sides,
        )
        for i, item in enumerate(printing_sides)
    ], spacing=10, wrap=False)

    # ── Copies counter ─────────────────────────────────────
    def decrement(e):
        if copies_count["value"] > 1:
            copies_count["value"] -= 1
            copies_val_txt.value = str(copies_count["value"])
            update_price()
            try:
                if copies_val_txt.page:
                    copies_val_txt.update()
            except Exception:
                pass

    def increment(e):
        copies_count["value"] += 1
        copies_val_txt.value = str(copies_count["value"])
        update_price()
        try:
            if copies_val_txt.page:
                copies_val_txt.update()
        except Exception:
            pass

    counter = ft.Container(
        height=56,
        content=ft.Row([
            ft.Container(
                content=ft.Text("+", size=22, color="#333333"),
                width=36, height=36, border_radius=8,
                bgcolor="#f0f2f8", alignment=ft.Alignment(0, 0),
                on_click=increment, ink=True,
            ),
            copies_val_txt,
            ft.Container(
                content=ft.Text("−", size=22, color="#333333"),
                width=36, height=36, border_radius=8,
                bgcolor="#f0f2f8", alignment=ft.Alignment(0, 0),
                on_click=decrement, ink=True,
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        border=ft.border.all(1.5, "#e0e0e0"),
        border_radius=12,
        padding=ft.Padding(16, 10, 16, 10),
    )

    # ── Submit ─────────────────────────────────────────────
    def handle_next(e):
        size_price  = float(paper_size_map.get(selected_size["value"], {}).get("price", 0))
        type_price  = float(paper_type_map.get(selected_type["value"], {}).get("price", 0))
        color_price = float(paper_color_map.get(selected_color["value"], {}).get("price", 0))
        price_per_sheet = size_price + type_price + color_price
        
        side_label = side_labels.get(selected_sides["value"], "")
        is_double_sided = "وجهين" in side_label or "double" in str(selected_sides["value"]).lower()
        if is_double_sided:
            price_per_sheet *= 1.5
            number_of_sheets = (PAGE_COUNT + 1) // 2
        else:
            number_of_sheets = PAGE_COUNT

        page.run_task(on_next, {
            "paper_size_id":    paper_size_map.get(selected_size["value"], {}).get("id", ""),
            "paper_type_id":    paper_type_map.get(selected_type["value"], {}).get("id", ""),
            "color_id":         paper_color_map.get(selected_color["value"], {}).get("id", ""),
            "sides":            printing_sides[int(selected_sides["value"])].get("value", "") if selected_sides["value"].isdigit() else "",
            "paper_size_label": paper_size_labels.get(selected_size["value"], ""),
            "paper_type_label": paper_type_labels.get(selected_type["value"], ""),
            "color_label":      paper_color_labels.get(selected_color["value"], ""),
            "sides_label":      side_label,
            "copies":           copies_count["value"],
            "file":             file_info,
            "price_per_sheet":  price_per_sheet,
            "number_of_sheets": number_of_sheets,
            "pages":            PAGE_COUNT,
        })

    stepper = _build_stepper(current=2)

    scrollable_content = ft.ListView(
        expand=True,
        spacing=16,
        padding=ft.Padding(16, 16, 16, 16),
        controls=[
            _card([
                _section_title("📌", "ملخص الطلب"),
                ft.Container(
                    height=60,
                    content=ft.Row([
                        ft.Icon("description", size=24, color="#555555"),
                        ft.Column([
                            ft.Text(file_info.get("name", "ملف.pdf"), size=13,
                                    weight=ft.FontWeight.BOLD, color="#333333"),
                            # ✅ عدد الصفحات من الباك اند
                            ft.Text(f"{PAGE_COUNT} صفحة", size=11, color="#888888"),
                        ], spacing=2),
                    ], spacing=10),
                    bgcolor="#f8f8ff",
                    border_radius=10,
                    padding=ft.Padding(12, 12, 12, 12),
                ),
                ft.Container(height=8),
                price_detail_text,
                ft.Container(height=4),
                _price_row("الإجمالي", None, subtotal_text),
            ]),

            ft.Container(
                height=90,
                content=ft.Row([
                    ft.Column([
                        ft.Container(
                            content=ft.Text("عرض خاص", size=11, color="white"),
                            bgcolor="#FFFFFF33",
                            border_radius=20,
                            padding=ft.Padding(10, 2, 10, 2),
                        ),
                        ft.Container(height=4),
                        ft.Text("خصم 15% على أول طلب!", size=16,
                                weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text("استخدم الكود: PRINT15", size=11, color="#FFFFFFCC"),
                    ], spacing=0),
                    ft.Text("›", size=28, color="#FFFFFF99"),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor="#1a237e",
                border_radius=14,
                padding=ft.Padding(16, 14, 16, 14),
            ),

            _card([
                _section_title("📐", "الورق والقياس"),
                ft.Text("مقاس الورق", size=13, color="#888888"),
                ft.Container(height=6),
                size_row,
                ft.Container(height=12),
                ft.Text("نوع الورق", size=13, color="#888888"),
                ft.Container(height=6),
                paper_type_dd,
            ]),

            _card([
                _section_title("🎨", "لون الطباعة"),
                color_grid,
            ]),

            _card([
                _section_title("📄", "وجه الطباعة"),
                sides_grid,
            ]),

            ft.Container(height=8),
        ],
    )

    return ft.View(
        route="/step2",
        controls=[
            ft.Column([
                stepper,
                scrollable_content,
                ft.Container(
                    height=70,
                    content=ft.Row([
                        ft.Container(
                            content=ft.Text("→ الخلف", size=14, color="#333333",
                                            weight=ft.FontWeight.BOLD),
                            border=ft.border.all(1.5, "#dddddd"),
                            border_radius=14,
                            padding=ft.Padding(16, 13, 16, 13),
                            alignment=ft.Alignment(0, 0),
                            expand=True,
                            on_click=lambda e: on_back(),
                            ink=True,
                        ),
                        ft.Container(
                            content=ft.Text("التالي ←", size=14, color="white",
                                            weight=ft.FontWeight.BOLD),
                            bgcolor="#1a237e",
                            border_radius=14,
                            padding=ft.Padding(30, 13, 30, 13),
                            alignment=ft.Alignment(0, 0),
                            expand=True,
                            on_click=handle_next,
                            ink=True,
                        ),
                    ], spacing=10),
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


def _card(controls):
    return ft.Container(
        content=ft.Column(controls, spacing=8, tight=True),
        bgcolor="white",
        border_radius=16,
        padding=ft.Padding(16, 16, 16, 16),
    )


def _section_title(icon_char, label):
    return ft.Text(f"{icon_char}  {label}", size=17, weight=ft.FontWeight.BOLD, color="#222222")


def _price_row(label, value_str=None, value_control=None):
    return ft.Row([
        value_control if value_control else ft.Text(
            value_str, size=13, weight=ft.FontWeight.BOLD, color="#1a237e"
        ),
        ft.Text(label, size=13, color="#555555"),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


def _build_stepper(current: int):
    steps = [("1", "رفع الملف"), ("2", "الإعدادات"), ("3", "الكمية"), ("4", "الدفع")]
    items = []
    for i, (num, label) in enumerate(steps):
        is_active = (i + 1) == current
        is_done   = (i + 1) < current
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
        items.append(ft.Column([
            circle,
            ft.Container(height=4),
            ft.Text(label, size=11,
                    color="#1a237e" if is_active else "#888888",
                    weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0, expand=True))
        if i < len(steps) - 1:
            items.append(ft.Container(
                height=2, expand=True,
                bgcolor="#1a237e" if (i + 1) < current else "#e0e0e0",
                margin=ft.Margin(0, 0, 0, 20),
            ))
    return ft.Container(
        content=ft.Row(items, alignment=ft.MainAxisAlignment.CENTER),
        bgcolor="white",
        padding=ft.Padding(16, 14, 16, 14),
        border=ft.border.only(bottom=ft.BorderSide(1, "#e8eaf0")),
    )