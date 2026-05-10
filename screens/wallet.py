import flet as ft

from components.navbar import bottom_navbar


BLUE = "#2563EB"
TEXT = "#0F172A"
MUTED = "#64748B"
BG = "#F6F8FC"
LINE = "#E8EEF7"


def wallet_screen(page: ft.Page):
    balance = 245.50
    reserved = 38.00
    transactions = [
        {
            "title": "شحن المحفظة",
            "subtitle": "بطاقة مدى",
            "amount": "+150.00 ج.م",
            "date": "اليوم، 10:24 ص",
            "icon": ft.Icons.ADD_CARD,
            "bg": "#ECFDF5",
            "color": "#059669",
        },
        {
            "title": "دفع طلب طباعة",
            "subtitle": "طلب #1024",
            "amount": "-42.00 ج.م",
            "date": "أمس، 07:15 م",
            "icon": ft.Icons.RECEIPT_LONG,
            "bg": "#EFF6FF",
            "color": BLUE,
        },
        {
            "title": "استرداد مبلغ",
            "subtitle": "طلب ملغي",
            "amount": "+18.50 ج.م",
            "date": "08 مايو 2026",
            "icon": ft.Icons.REPLAY,
            "bg": "#FFF7ED",
            "color": "#EA580C",
        },
    ]

    def show_coming_soon(message: str):
        page.snack_bar = ft.SnackBar(
            ft.Text(message, rtl=True),
            bgcolor=TEXT,
        )
        page.snack_bar.open = True
        page.update()

    def action_button(icon, label, color, bg, on_click):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, color=color, size=22),
                        width=48,
                        height=48,
                        bgcolor=bg,
                        border_radius=14,
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Text(
                        label,
                        size=12,
                        color=TEXT,
                        weight=ft.FontWeight.W_600,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            expand=True,
            padding=ft.padding.symmetric(vertical=14),
            border_radius=14,
            ink=True,
            on_click=on_click,
        )

    def stat_chip(label, value, icon, color):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color=color, size=17),
                    ft.Column(
                        controls=[
                            ft.Text(label, size=11, color="#DBEAFE", rtl=True),
                            ft.Text(
                                value,
                                size=13,
                                color="white",
                                weight=ft.FontWeight.BOLD,
                                rtl=True,
                            ),
                        ],
                        spacing=1,
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
            padding=ft.padding.symmetric(vertical=10, horizontal=8),
            bgcolor="#FFFFFF1C",
            border_radius=12,
        )

    def transaction_item(item):
        amount_color = "#059669" if item["amount"].startswith("+") else "#DC2626"
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    item["amount"],
                                    size=14,
                                    color=amount_color,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.LEFT,
                                ),
                                ft.Text(item["date"], size=11, color="#94A3B8"),
                            ],
                            spacing=3,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        ),
                    ),
                    ft.Container(expand=True),
                    ft.Column(
                        controls=[
                            ft.Text(
                                item["title"],
                                size=14,
                                color=TEXT,
                                weight=ft.FontWeight.BOLD,
                                rtl=True,
                            ),
                            ft.Text(item["subtitle"], size=12, color=MUTED, rtl=True),
                        ],
                        spacing=3,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                    ft.Container(
                        content=ft.Icon(item["icon"], color=item["color"], size=22),
                        width=46,
                        height=46,
                        bgcolor=item["bg"],
                        border_radius=13,
                        alignment=ft.Alignment(0, 0),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=14, vertical=13),
        )

    header = ft.Container(
        bgcolor="white",
        padding=ft.padding.only(left=20, right=20, top=34, bottom=18),
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED, size=21, color=TEXT),
                    width=42,
                    height=42,
                    bgcolor="#F4F7FB",
                    border=ft.border.all(1, LINE),
                    border_radius=21,
                    alignment=ft.Alignment(0, 0),
                    ink=True,
                ),
                ft.Text(
                    "المحفظة",
                    size=22,
                    color=TEXT,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True,
                ),
                ft.Container(
                    content=ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW, size=18, color=TEXT),
                    width=42,
                    height=42,
                    bgcolor="#F4F7FB",
                    border=ft.border.all(1, LINE),
                    border_radius=21,
                    alignment=ft.Alignment(0, 0),
                    ink=True,
                    on_click=lambda e: page.go("/home"),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    balance_card = ft.Container(
        margin=ft.margin.symmetric(horizontal=18),
        padding=ft.padding.all(22),
        border_radius=20,
        bgcolor=BLUE,
        shadow=ft.BoxShadow(
            blur_radius=18,
            color="#2563EB33",
            offset=ft.Offset(0, 8),
        ),
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, color="white", size=22),
                            width=44,
                            height=44,
                            bgcolor="#FFFFFF24",
                            border_radius=14,
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("رصيدك الحالي", size=13, color="#DBEAFE", rtl=True),
                                ft.Text(
                                    f"{balance:.2f} ج.م",
                                    size=34,
                                    color="white",
                                    weight=ft.FontWeight.BOLD,
                                    rtl=True,
                                ),
                            ],
                            spacing=2,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(height=18),
                ft.Row(
                    controls=[
                        stat_chip("محجوز للطلبات", f"{reserved:.2f} ج.م", ft.Icons.LOCK_CLOCK, "#BFDBFE"),
                        stat_chip("متاح للاستخدام", f"{balance - reserved:.2f} ج.م", ft.Icons.CHECK_CIRCLE_OUTLINE, "#BBF7D0"),
                    ],
                    spacing=10,
                ),
            ],
            spacing=0,
        ),
    )

    actions_card = ft.Container(
        margin=ft.margin.symmetric(horizontal=18),
        bgcolor="white",
        border_radius=16,
        border=ft.border.all(1, LINE),
        shadow=ft.BoxShadow(blur_radius=10, color="#0000000A", offset=ft.Offset(0, 2)),
        content=ft.Row(
            controls=[
                action_button(
                    ft.Icons.ADD,
                    "شحن",
                    "#059669",
                    "#ECFDF5",
                    lambda e: show_coming_soon("شحن المحفظة سيتم ربطه ببوابة الدفع قريباً"),
                ),
                action_button(
                    ft.Icons.CREDIT_CARD,
                    "بطاقة",
                    BLUE,
                    "#EFF6FF",
                    lambda e: show_coming_soon("إدارة البطاقات قيد التجهيز"),
                ),
                action_button(
                    ft.Icons.HISTORY,
                    "السجل",
                    "#7C3AED",
                    "#F3E8FF",
                    lambda e: show_coming_soon("أنت بالفعل في سجل معاملات المحفظة"),
                ),
            ],
            spacing=0,
        ),
    )

    payment_method = ft.Container(
        margin=ft.margin.symmetric(horizontal=18),
        padding=ft.padding.all(16),
        bgcolor="white",
        border_radius=16,
        border=ft.border.all(1, LINE),
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.CHEVRON_LEFT, color="#CBD5E1", size=22),
                ft.Container(expand=True),
                ft.Column(
                    controls=[
                        ft.Text("بطاقة الدفع الافتراضية", size=13, color=TEXT, weight=ft.FontWeight.BOLD, rtl=True),
                        ft.Text("مدى تنتهي بـ 4821", size=12, color=MUTED, rtl=True),
                    ],
                    spacing=3,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                ),
                ft.Container(
                    content=ft.Icon(ft.Icons.PAYMENT, color=BLUE, size=22),
                    width=46,
                    height=46,
                    bgcolor="#EFF6FF",
                    border_radius=13,
                    alignment=ft.Alignment(0, 0),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        ink=True,
        on_click=lambda e: show_coming_soon("تغيير طريقة الدفع قيد التجهيز"),
    )

    transactions_card = ft.Container(
        margin=ft.margin.symmetric(horizontal=18),
        bgcolor="white",
        border_radius=16,
        border=ft.border.all(1, LINE),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Column(
            controls=[
                ft.Container(
                    padding=ft.padding.only(left=16, right=16, top=16, bottom=10),
                    content=ft.Row(
                        controls=[
                            ft.Text("عرض الكل", size=12, color=BLUE, weight=ft.FontWeight.W_600, rtl=True),
                            ft.Container(expand=True),
                            ft.Text("آخر المعاملات", size=15, color=TEXT, weight=ft.FontWeight.BOLD, rtl=True),
                        ],
                    ),
                ),
                *[
                    control
                    for index, item in enumerate(transactions)
                    for control in (
                        transaction_item(item),
                        ft.Divider(height=1, color="#F1F5F9")
                        if index < len(transactions) - 1
                        else ft.Container(height=2),
                    )
                ],
            ],
            spacing=0,
        ),
    )

    return ft.View(
        route="/wallet",
        bgcolor=BG,
        padding=0,
        controls=[
            ft.Column(
                controls=[
                    header,
                    ft.ListView(
                        expand=True,
                        padding=ft.padding.only(top=18, bottom=22),
                        spacing=16,
                        controls=[
                            balance_card,
                            actions_card,
                            payment_method,
                            transactions_card,
                        ],
                    ),
                    bottom_navbar(page, current_index=3),
                ],
                expand=True,
                spacing=0,
            )
        ],
    )
