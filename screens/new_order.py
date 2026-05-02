import flet as ft
from api_client import api
from components.navbar import bottom_navbar

def new_order_screen(page: ft.Page):

    selected_file = {"path": None, "name": None}

    error_text   = ft.Text("", color="#FF4D4D", size=13, text_align=ft.TextAlign.CENTER)
    success_text = ft.Text("", color="#4DFF91", size=13, text_align=ft.TextAlign.CENTER)
    loading      = ft.ProgressRing(width=22, height=22, color="white", stroke_width=2, visible=False)
    file_text    = ft.Text("لم يتم اختيار ملف", color="#666680", size=13)

    type_dd  = ft.Dropdown(border_radius=14, bgcolor="#1E1E2E", border_color="transparent",
                           focused_border_color="#6C63FF", color="white", text_align=ft.TextAlign.RIGHT)
    size_dd  = ft.Dropdown(border_radius=14, bgcolor="#1E1E2E", border_color="transparent",
                           focused_border_color="#6C63FF", color="white", text_align=ft.TextAlign.RIGHT)
    color_dd = ft.Dropdown(border_radius=14, bgcolor="#1E1E2E", border_color="transparent",
                           focused_border_color="#6C63FF", color="white", text_align=ft.TextAlign.RIGHT)
    sides_dd = ft.Dropdown(border_radius=14, bgcolor="#1E1E2E", border_color="transparent",
                           focused_border_color="#6C63FF", color="white", text_align=ft.TextAlign.RIGHT)

    sheets_field = ft.TextField(
        hint_text="عدد الأوراق",
        border_radius=14, bgcolor="#1E1E2E", border_color="transparent",
        focused_border_color="#6C63FF", color="white",
        hint_style=ft.TextStyle(color="#666680"),
        text_align=ft.TextAlign.RIGHT, height=56, keyboard_type=ft.KeyboardType.NUMBER,
        content_padding=ft.Padding(left=16, right=16, top=16, bottom=16),
    )
    quantity_field = ft.TextField(
        hint_text="عدد النسخ",
        border_radius=14, bgcolor="#1E1E2E", border_color="transparent",
        focused_border_color="#6C63FF", color="white",
        hint_style=ft.TextStyle(color="#666680"),
        text_align=ft.TextAlign.RIGHT, height=56, keyboard_type=ft.KeyboardType.NUMBER,
        content_padding=ft.Padding(left=16, right=16, top=16, bottom=16),
    )
    address_field = ft.TextField(
        hint_text="عنوان التوصيل",
        border_radius=14, bgcolor="#1E1E2E", border_color="transparent",
        focused_border_color="#6C63FF", color="white",
        hint_style=ft.TextStyle(color="#666680"),
        text_align=ft.TextAlign.RIGHT, height=56,
        content_padding=ft.Padding(left=16, right=16, top=16, bottom=16),
    )
    notes_field = ft.TextField(
        hint_text="ملاحظات (اختياري)",
        border_radius=14, bgcolor="#1E1E2E", border_color="transparent",
        focused_border_color="#6C63FF", color="white",
        hint_style=ft.TextStyle(color="#666680"),
        text_align=ft.TextAlign.RIGHT, height=80, multiline=True,
        content_padding=ft.Padding(left=16, right=16, top=16, bottom=16),
    )

    def load_options():
        result = api.get_paper_options()
        if result["success"]:
            data = result["data"]
            for pt in data["paper_types"]:
                type_dd.options.append(ft.dropdown.Option(key=str(pt["id"]), text=pt["paper_type"]))
            for ps in data["paper_sizes"]:
                size_dd.options.append(ft.dropdown.Option(key=str(ps["id"]), text=ps["size"]))
            for pc in data["paper_colors"]:
                color_dd.options.append(ft.dropdown.Option(key=str(pc["id"]), text=pc["color_paper"]))
            for s in data["printing_sides"]:
                sides_dd.options.append(ft.dropdown.Option(key=s["value"], text=s["label"]))
            page.update()
        else:
            error_text.value = result["message"]
            page.update()

    def set_selected_file(file):
        if file:
            selected_file["path"] = file.path
            selected_file["name"] = file.name
            file_text.value = file.name
            file_text.color = "white"
            page.update()

    file_picker = ft.FilePicker()

    async def pick_file_async():
        files = await file_picker.pick_files(
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["pdf", "docx", "jpg", "jpeg", "png"],
        )
        if files:
            set_selected_file(files[0])

    pick_file_btn = ft.Container(
        content=ft.Row([
            ft.Icon("upload_file", color="#AAAACC"),
            ft.Text("اختر ملف", color="#AAAACC", size=14),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        bgcolor="#1E1E2E",
        border_radius=14,
        height=56,
        on_click=lambda e: page.run_task(pick_file_async),
        ink=True,
    )

    def handle_submit(e):
        error_text.value   = ""
        success_text.value = ""

        if not selected_file["path"]:
            error_text.value = "يرجى اختيار ملف"
            page.update()
            return
        if not type_dd.value or not size_dd.value or not color_dd.value or not sides_dd.value:
            error_text.value = "يرجى اختيار جميع خيارات الورق"
            page.update()
            return
        if not sheets_field.value or not quantity_field.value or not address_field.value:
            error_text.value = "يرجى ملء جميع الحقول المطلوبة"
            page.update()
            return

        loading.visible     = True
        submit_btn.disabled = True
        page.update()

        result = api.create_order(
            file_path=selected_file["path"],
            paper_type_id=type_dd.value,
            paper_size_id=size_dd.value,
            printing_color_id=color_dd.value,
            printing_sides=sides_dd.value,
            number_of_sheets=int(sheets_field.value),
            quantity=int(quantity_field.value),
            address=address_field.value,
            notes=notes_field.value,
        )

        loading.visible     = False
        submit_btn.disabled = False

        if result["success"]:
            success_text.value = "✅ تم إرسال الطلب بنجاح!"
            selected_file["path"] = None
            selected_file["name"] = None
            file_text.value = "لم يتم اختيار ملف"
            file_text.color = "#666680"
            type_dd.value = size_dd.value = color_dd.value = sides_dd.value = None
            sheets_field.value = quantity_field.value = address_field.value = notes_field.value = ""
        else:
            error_text.value = result["message"]
        page.update()

    submit_btn = ft.Container(
        content=ft.Row([
            loading,
            ft.Text("إرسال الطلب  ←", size=16, weight=ft.FontWeight.BOLD, color="white"),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        bgcolor="#6C63FF",
        border_radius=14,
        height=56,
        on_click=handle_submit,
        ink=True,
    )

    logo = ft.Container(
        content=ft.Icon("print", size=32, color="white"),
        width=64, height=64,
        bgcolor="#6C63FF",
        border_radius=18,
        alignment=ft.Alignment(0, 0),
        shadow=ft.BoxShadow(blur_radius=20, color="#6C63FF55", offset=ft.Offset(0, 6)),
    )

    load_options()

    return ft.View(
        route="/new-order",
        services=[file_picker],
        controls=[
            ft.Container(
                expand=True,
                padding=ft.Padding(left=24, right=24, top=32, bottom=32),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Container(height=10),
                        logo,
                        ft.Container(height=16),
                        ft.Text("طلب طباعة جديد", size=22, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text("ارفع ملفك واختر مواصفات الطباعة", size=14, color="#AAAACC"),
                        ft.Container(height=24),

                        ft.Text("الملف", size=13, color="#AAAACC", text_align=ft.TextAlign.RIGHT, width=float("inf")),
                        ft.Container(height=6),
                        pick_file_btn,
                        ft.Container(height=6),
                        file_text,
                        ft.Container(height=16),

                        ft.Text("نوع الورق", size=13, color="#AAAACC", text_align=ft.TextAlign.RIGHT, width=float("inf")),
                        ft.Container(height=6),
                        type_dd,
                        ft.Container(height=16),

                        ft.Text("حجم الورق", size=13, color="#AAAACC", text_align=ft.TextAlign.RIGHT, width=float("inf")),
                        ft.Container(height=6),
                        size_dd,
                        ft.Container(height=16),

                        ft.Text("لون الطباعة", size=13, color="#AAAACC", text_align=ft.TextAlign.RIGHT, width=float("inf")),
                        ft.Container(height=6),
                        color_dd,
                        ft.Container(height=16),

                        ft.Text("الطباعة", size=13, color="#AAAACC", text_align=ft.TextAlign.RIGHT, width=float("inf")),
                        ft.Container(height=6),
                        sides_dd,
                        ft.Container(height=16),

                        ft.Row([
                            ft.Column([
                                ft.Text("عدد الأوراق", size=13, color="#AAAACC"),
                                sheets_field,
                            ], expand=True, spacing=6),
                            ft.Column([
                                ft.Text("عدد النسخ", size=13, color="#AAAACC"),
                                quantity_field,
                            ], expand=True, spacing=6),
                        ], spacing=12),
                        ft.Container(height=16),

                        ft.Text("عنوان التوصيل", size=13, color="#AAAACC", text_align=ft.TextAlign.RIGHT, width=float("inf")),
                        ft.Container(height=6),
                        address_field,
                        ft.Container(height=16),

                        ft.Text("ملاحظات", size=13, color="#AAAACC", text_align=ft.TextAlign.RIGHT, width=float("inf")),
                        ft.Container(height=6),
                        notes_field,
                        ft.Container(height=8),

                        error_text,
                        success_text,
                        ft.Container(height=16),

                        ft.Container(content=submit_btn, width=float("inf")),
                        ft.Container(height=32),
                    ],
                ),
            )
        ],
        navigation_bar=bottom_navbar(page, current_index=1),
        bgcolor="#0F0F1A",
        padding=0,
    )
