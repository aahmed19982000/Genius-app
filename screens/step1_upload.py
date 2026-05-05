import flet as ft
from components.navbar import bottom_navbar


def step1_upload_screen(page: ft.Page, on_next):
    # مسارات الصور المخصصة بناءً على ملفاتك
    ICONS_PATH = {
        "pdf": "img/step1_upload/pdf.png",
        "png": "img/step1_upload/png.png",
        "default": "img/step1_upload/file.png"
    }

    selected_file = {"path": None, "name": None}

    # 1. تعريف العناصر كمتغيرات مستقلة ليتم تحديثها لاحقاً
    file_text = ft.Text(
        "لا توجد ملفات مختارة حتى الآن",
        color="#888888",
        size=13,
        text_align=ft.TextAlign.CENTER,
    )
    
    file_count_text = ft.Text("0 ملفات", color="#888888", size=12)

    # أيقونة افتراضية تظهر فقط عندما لا يوجد ملف
    default_icon = ft.Icon("description", size=40, color="#cccccc")

    empty_files_box = ft.Container(
        height=120,
        content=ft.Column(
            [
                default_icon,
                ft.Container(height=5),
                # هذا النص هو الذي سيعرض اسم الملف المرفوع
                file_text, 
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
        ),
        border=ft.border.all(1, "#e8eaf0"),
        border_radius=12,
        bgcolor="#f8f9ff", # لون خلفية خفيف جداً لتمييز منطقة العرض
        padding=20,
        alignment=ft.Alignment(0, 0),
    )

    # عنصر الصورة الذي سيتغير شكله عند اختيار ملف
    preview_icon = ft.Image(
        src=ICONS_PATH["default"], 
        width=48, 
        height=48, 
        fit="contain"
    )

    def set_selected_file(file):
        if file:
            selected_file["path"] = file.path
            selected_file["name"] = file.name
            
            # تحديث نص اسم الملف المختار
            file_text.value = file.name
            file_text.color = "#1a237e"  # لون غامق وواضح
            file_text.weight = ft.FontWeight.BOLD
            file_text.size = 15
            
            # تحديث عداد الملفات
            file_count_text.value = "1 ملف"
            
            # إخفاء الأيقونة الرمادية إذا أردت (اختياري)
            default_icon.visible = False 
            
            page.update()

    async def pick_file(e):
        print("DEBUG: pick_file called")
        result = await file_picker.pick_files(
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["pdf", "docx", "jpg", "jpeg", "png"],
        )
        if result and len(result) > 0:
            set_selected_file(result[0])

    file_picker = ft.FilePicker()

    def handle_next(e):
        if not selected_file["path"]:
            page.snack_bar = ft.SnackBar(
                ft.Text("يرجى اختيار ملف أولاً"),
                bgcolor="#FF4D4D",
            )
            page.snack_bar.open = True
            page.update()
            return
        page.run_task(on_next, selected_file)

    upload_zone = ft.Container(
        height=220,  # زيادة الطول قليلاً لاستيعاب الصورة
        content=ft.Column(
            [
                # استبدال ft.Icon بـ ft.Image لاستخدام الصورة من المجلد الموضح في الصورة "Screenshot 2026-05-05 at 6.54.35 PM.jpg"
                ft.Container(
                    content=ft.Image(
                        src="img/step1_upload/file.png", # المسار بناءً على هيكل ملفاتك
                        width=50,
                        height=50,
                        fit="contain"
                    ),
                    width=80,
                    height=80,
                    bgcolor="#e8eaf0",
                    border_radius=16,
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Container(height=12),
                ft.Text(
                    "اضغط هنا أو اسحب الملف",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color="#1a237e",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=6),
                ft.Text(
                    "يدعم التطبيق ملفات PDF حتى حجم 50 ميجابايت\nللملف الواحد لضمان أعلى دقة طباعة",
                    size=12,
                    color="#888888",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        border=ft.border.all(2, "#c5cae9"),
        border_radius=12,
        padding=ft.Padding(20, 30, 20, 30),
        on_click=pick_file,
        ink=True,
        # إضافة تأثير حركي بسيط عند المرور بالماوس (اختياري)
    )

    empty_files_box = ft.Container(
        height=90,
        content=ft.Column(
            [
                ft.Icon("description", size=36, color="#cccccc"),
                ft.Container(height=8),
                file_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        border=ft.border.all(1, "#e8eaf0"),
        border_radius=10,
        padding=ft.Padding(20, 24, 20, 24),
        alignment=ft.Alignment(0, 0),
    )

    def make_type_btn(img_name, label):
        # img_name: مرر اسم الصورة فقط (مثل "pdf" أو "png") بدون اللاحقة
        return ft.Container(
            height=42,
            content=ft.Row(
                [
                    # استدعاء الصورة من المسار الصحيح بناءً على ملفاتك
                    ft.Image(
                        src=f"img/step1_upload/{img_name}.png", 
                        width=20, 
                        height=20,
                        fit="contain" # نص مباشر لتجنب AttributeError
                    ),
                    ft.Text(
                        label,
                        size=12,
                        color="#555555",
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6,
            ),
            border=ft.border.all(1.5, "#cccccc"),
            border_radius=20,
            padding=ft.Padding(10, 8, 10, 8),
            expand=True,
            on_click=pick_file,
            ink=True,
        )
    stepper = _build_stepper(current=1)

    next_btn = ft.Container(
        height=54,
        content=ft.Text(
            "الخطوة التالية  ←",
            size=16,
            weight=ft.FontWeight.BOLD,
            color="white",
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor="#1a237e",
        border_radius=14,
        alignment=ft.Alignment(0, 0),
        on_click=handle_next,
        ink=True,
    )

    scrollable_content = ft.ListView(
        expand=True,
        spacing=0,
        padding=ft.Padding(16, 16, 16, 16),
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "ابدأ برفع مستنداتك",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#1a237e",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=4),
                        ft.Text(
                            "يمكنك رفع ملفات PDF، Word، أو صور عالية الجودة",
                            size=13,
                            color="#666666",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=18),
                        # منطقة الرفع التي عدلناها سابقاً لتستخدم صورة file.png
                        upload_zone, 
                        ft.Container(height=14),
                        ft.Row(
                            [
                                file_count_text,
                                ft.Text(
                                    "الملفات المختارة",
                                    size=13,
                                    color="#555555",
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=8),
                        # الصندوق الذي يعرض اسم الملف المختار مع صورته
                        empty_files_box, 
                        ft.Container(height=14),
                        ft.Row(
                            [
                                # استدعاء الأزرار بأسماء الصور الفعلية في المجلد (png.png, file.png, pdf.png)
                                make_type_btn("png", "JPG / PNG"),
                                make_type_btn("file", "DOCX"),
                                make_type_btn("pdf", "PDF"),
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=0,
                ),
                bgcolor="white",
                border_radius=16,
                padding=20,
            ),
            ft.Container(height=16),
            next_btn,
            ft.Container(height=6),
            ft.Text(
                "بإكمال هذه العملية، أنت توافق على شروط وأحكام الخدمة",
                size=11,
                color="#aaaaaa",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=20),
        ],
    )

    # ✅ file_picker في services داخل View
    return ft.View(
    route="/step1",
    services=[file_picker],
    controls=[
        ft.Column(
            [stepper, scrollable_content, bottom_navbar(page, current_index=2)],
            spacing=0,
            expand=True,
        ),
    ],
    bgcolor="#f0f2f8",
    padding=0,
)

def _build_stepper(current: int):
    steps = [
        ("1", "رفع الملف"),
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
                width=36, height=36,
                border_radius=18,
                bgcolor="#1a237e",
                alignment=ft.Alignment(0, 0),
            )
        elif is_active:
            circle = ft.Container(
                content=ft.Text(num, size=14, weight=ft.FontWeight.BOLD, color="white"),
                width=36, height=36,
                border_radius=18,
                bgcolor="#1a237e",
                alignment=ft.Alignment(0, 0),
            )
        else:
            circle = ft.Container(
                content=ft.Text(num, size=14, weight=ft.FontWeight.BOLD, color="#888888"),
                width=36, height=36,
                border_radius=18,
                bgcolor="#e8eaf0",
                alignment=ft.Alignment(0, 0),
            )

        step_col = ft.Column(
            [
                circle,
                ft.Container(height=4),
                ft.Text(
                    label,
                    size=11,
                    color="#1a237e" if is_active else "#888888",
                    weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )

        items.append(
            ft.Column(
                [step_col],
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

        if i < len(steps) - 1:
            line_color = "#1a237e" if (i + 1) < current else "#e0e0e0"
            items.append(
                ft.Container(
                    height=2,
                    expand=True,
                    bgcolor=line_color,
                    margin=ft.Margin(0, 0, 0, 20),
                )
            )

    return ft.Container(
        content=ft.Row(items, alignment=ft.MainAxisAlignment.CENTER),
        bgcolor="white",
        padding=ft.Padding(16, 14, 16, 14),
        border=ft.border.only(bottom=ft.BorderSide(1, "#e8eaf0")),
    )