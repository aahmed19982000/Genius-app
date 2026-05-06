import flet as ft
import asyncio
from api_client import api


def chat_screen(page: ft.Page, order_id: int, order_name: str = "", order_status: str = ""):

    messages_col = ft.Column(
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        auto_scroll=True,
    )

    message_field = ft.TextField(
        hint_text="اكتب رسالتك هنا...",
        hint_style=ft.TextStyle(color="#94A3B8", size=14),
        border=ft.InputBorder.NONE,
        expand=True,
        multiline=True,
        max_lines=4,
        min_lines=1,
        text_align=ft.TextAlign.RIGHT,
        text_style=ft.TextStyle(size=14, color="#0F172A"),
        content_padding=ft.Padding(left=0, right=4, top=8, bottom=8),
    )

    send_loading = ft.ProgressRing(
        width=20, height=20, color="white", stroke_width=2, visible=False
    )

    current_user_id = (api.user_data or {}).get("id")

    file_picker = ft.FilePicker()

    async def handle_pick(e):
        files = await file_picker.pick_files()
        if not files:
            return
        
        file_path = files[0].path
        send_loading.visible = True
        message_field.disabled = True
        page.update()

        result = await api.send_chat_message(order_id, message="", file_path=file_path)

        send_loading.visible = False
        message_field.disabled = False

        if result["success"]:
            load_messages()
        else:
            page.update()

    # ── Helpers ──────────────────────────────────────────────────

    def format_time(date_raw: str) -> str:
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(str(date_raw).replace("Z", "+00:00"))
            hour = dt.hour
            minute = dt.strftime("%M")
            period = "ص" if hour < 12 else "م"
            hour12 = hour % 12 or 12
            return f"{hour12}:{minute} {period}"
        except Exception:
            return str(date_raw)[11:16]

    def format_day(date_raw: str) -> str:
        try:
            from datetime import datetime, date
            dt = datetime.fromisoformat(str(date_raw).replace("Z", "+00:00"))
            today = date.today()
            if dt.date() == today:
                return "اليوم"
            months_ar = ["يناير","فبراير","مارس","أبريل","مايو","يونيو",
                         "يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
            return f"{dt.day} {months_ar[dt.month - 1]}"
        except Exception:
            return ""

    def is_mine(msg: dict) -> bool:
        sender = msg.get("sender", {})
        if isinstance(sender, dict):
            return sender.get("id") == current_user_id
        return str(sender) == str(current_user_id)

    def file_size_label(url: str) -> str:
        return ""  # placeholder — actual size requires HEAD request

    def file_ext(url: str) -> str:
        return str(url).split(".")[-1].lower() if url else ""

    # ── Bubble builders ──────────────────────────────────────────

    def date_separator(label: str):
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(label, size=12, color="#64748B"),
                    bgcolor="#E2E8F0",
                    border_radius=12,
                    padding=ft.Padding(left=16, right=16, top=5, bottom=5),
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def file_bubble(url: str, mine: bool):
        ext = file_ext(url)
        fname = url.split("/")[-1] if url else "مرفق"

        icon_cfg = {
            "pdf":  (ft.Icons.PICTURE_AS_PDF, "#EFF6FF", "#2563EB"),
            "docx": (ft.Icons.DESCRIPTION,    "#F0FDF4", "#16A34A"),
            "doc":  (ft.Icons.DESCRIPTION,    "#F0FDF4", "#16A34A"),
            "png":  (ft.Icons.IMAGE,          "#FFF7ED", "#EA580C"),
            "jpg":  (ft.Icons.IMAGE,          "#FFF7ED", "#EA580C"),
            "jpeg": (ft.Icons.IMAGE,          "#FFF7ED", "#EA580C"),
        }.get(ext, (ft.Icons.INSERT_DRIVE_FILE, "#F8FAFC", "#64748B"))
        icon, bg, color = icon_cfg

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.DOWNLOAD, color="#2563EB", size=20),
                    ft.Column(
                        controls=[
                            ft.Text(fname, size=13, color="#0F172A",
                                    weight=ft.FontWeight.W_600, rtl=True),
                            ft.Text("MB 1.2", size=11, color="#94A3B8"),
                        ],
                        spacing=2,
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                    ft.Container(
                        content=ft.Icon(icon, color=color, size=22),
                        width=46, height=46, bgcolor=bg,
                        border_radius=12, alignment=ft.Alignment(0, 0),
                    ),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="white",
            border_radius=16,
            padding=ft.Padding(left=14, right=14, top=12, bottom=12),
            border=ft.border.all(1, "#E2E8F0"),
            width=260,
            shadow=ft.BoxShadow(blur_radius=6, color="#0A000000", offset=ft.Offset(0, 2)),
        )

    def image_bubble(url: str, caption: str = ""):
        controls = [
            ft.Container(
                content=ft.Image(
                    src=url,
                    fit="cover",
                    border_radius=ft.BorderRadius(12, 12, 12, 12),
                ),
                width=260, height=180,
                border_radius=ft.BorderRadius(12, 12, 0, 0),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            )
        ]
        if caption:
            controls.append(
                ft.Container(
                    content=ft.Text(caption, size=12, color="white", rtl=True),
                    bgcolor="#2563EB",
                    border_radius=ft.BorderRadius(0, 0, 12, 12),
                    padding=ft.Padding(left=12, right=12, top=8, bottom=8),
                    width=260,
                )
            )
        return ft.Column(controls=controls, spacing=0)

    def message_bubble(msg: dict):
        mine = is_mine(msg)
        text = msg.get("message", "")
        time = format_time(msg.get("created_at", ""))
        file_url = msg.get("file", "")
        is_read = msg.get("is_read", False)

        bubble_bg    = "#2563EB" if mine else "#F1F5F9"
        text_color   = "white"   if mine else "#0F172A"
        time_color   = "#BFDBFE" if mine else "#94A3B8"
        align        = ft.MainAxisAlignment.END if mine else ft.MainAxisAlignment.START

        # Detect image attachment
        is_image = file_url and file_ext(file_url) in ("png", "jpg", "jpeg", "webp")
        is_file  = file_url and not is_image

        bubble_controls = []

        # Image attachment
        if is_image:
            bubble_controls.append(image_bubble(file_url, caption=text))
        else:
            # File attachment card (separate row)
            if is_file:
                pass  # rendered below separately

            # Text body
            if text:
                bubble_controls.append(
                    ft.Text(text, size=14, color=text_color, rtl=True, selectable=True)
                )

        # Timestamp + read receipt
        bubble_controls.append(
            ft.Row(
                controls=[
                    *(
                        [ft.Icon(
                            ft.Icons.DONE_ALL if is_read else ft.Icons.DONE,
                            size=14,
                            color="#93C5FD" if not is_read else "#BFDBFE",
                        )]
                        if mine else []
                    ),
                    ft.Text(time, size=10, color=time_color),
                ],
                spacing=3,
                tight=True,
                alignment=ft.MainAxisAlignment.END,
            )
        )

        row_controls = []

        if is_image:
            row_controls.append(
                ft.Column(controls=bubble_controls, spacing=4, tight=True)
            )
        elif is_file:
            row_controls = [
                ft.Column(
                    controls=[
                        file_bubble(file_url, mine),
                        ft.Row(
                            controls=[
                                *(
                                    [ft.Icon(
                                        ft.Icons.DONE_ALL if is_read else ft.Icons.DONE,
                                        size=14, color="#2563EB",
                                    )]
                                    if mine else []
                                ),
                                ft.Text(time, size=10, color="#94A3B8"),
                            ],
                            spacing=3, tight=True,
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    spacing=4, tight=True,
                )
            ]
        else:
            row_controls = [
                ft.Container(
                    content=ft.Column(
                        controls=bubble_controls, spacing=6, tight=True
                    ),
                    bgcolor=bubble_bg,
                    border_radius=ft.BorderRadius(
                        top_left=18, top_right=18,
                        bottom_left=4 if mine else 18,
                        bottom_right=18 if mine else 4,
                    ),
                    padding=ft.Padding(left=14, right=14, top=12, bottom=10),
                    shadow=ft.BoxShadow(
                        blur_radius=8, color="#0A000000", offset=ft.Offset(0, 2)
                    ),
                )
            ]

        return ft.Row(controls=row_controls, alignment=align)

    # ── Load messages ─────────────────────────────────────────────

    def load_messages():
        messages_col.controls.clear()
        page.update()

        result = api.get_order_chat(order_id)

        if result["success"]:
            data = result["data"]
            msgs = (data if isinstance(data, list)
                    else data.get("results", data.get("messages", [])))

            if not msgs:
                messages_col.controls.append(
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE,
                                        size=64, color="#E2E8F0"),
                                ft.Text("لا توجد رسائل بعد",
                                        size=15, color="#94A3B8"),
                                ft.Text("ابدأ المحادثة الآن",
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
                last_day = None
                for msg in msgs:
                    day = format_day(msg.get("created_at", ""))
                    if day and day != last_day:
                        last_day = day
                        messages_col.controls.append(date_separator(day))
                    messages_col.controls.append(message_bubble(msg))
        else:
            messages_col.controls.append(
                ft.Text(result["message"], color="#E53935", size=13,
                        text_align=ft.TextAlign.CENTER)
            )

        page.update()

    # ── Send ──────────────────────────────────────────────────────

    async def send_message(e):
        text = (message_field.value or "").strip()
        if not text:
            return
        send_loading.visible = True
        message_field.disabled = True
        page.update()

        result = await api.send_chat_message(order_id, text)

        send_loading.visible = False
        message_field.disabled = False

        if result["success"]:
            message_field.value = ""
            load_messages()
        else:
            page.update()

    def on_send(e):
        page.run_task(send_message, e)

    # ── Status dot ───────────────────────────────────────────────

    status_colors = {
        "قيد التنفيذ":   "#10B981",
        "مكتمل":         "#10B981",
        "معلقه":         "#F59E0B",
        "بانتظار الدفع": "#7C3AED",
        "ملغي":          "#F43F5E",
    }
    dot_color = status_colors.get(order_status, "#94A3B8")

    short_name = (order_name[:22] + "...") if len(order_name) > 22 else order_name

    # ── Header ───────────────────────────────────────────────────

    header = ft.Container(
        content=ft.Row(
            controls=[
                # Back arrow (left)
                ft.Container(
                    content=ft.Icon(ft.Icons.ARROW_FORWARD_IOS,
                                    color="#2563EB", size=20),
                    width=40, height=40,
                    border_radius=12,
                    ink=True,
                    on_click=lambda e: page.go("/my-orders"),
                    alignment=ft.Alignment(0, 0),
                ),

                # Title center
                ft.Column(
                    controls=[
                        ft.Text(
                            f"محادثة الطلب : {short_name}",
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color="#0F172A",
                            rtl=True,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(f"الحالة: {order_status}",
                                        size=12, color="#64748B", rtl=True),
                                ft.Container(
                                    width=8, height=8,
                                    bgcolor=dot_color,
                                    border_radius=4,
                                ),
                            ],
                            spacing=6,
                            tight=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                ),

                # Menu (right)
                ft.Container(
                    content=ft.Icon(ft.Icons.MORE_VERT, color="#64748B", size=22),
                    width=40, height=40,
                    border_radius=12,
                    ink=True,
                    alignment=ft.Alignment(0, 0),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="white",
        padding=ft.Padding(left=12, right=12, top=14, bottom=14),
        shadow=ft.BoxShadow(blur_radius=8, color="#0A000000", offset=ft.Offset(0, 2)),
    )

    # ── Input bar ────────────────────────────────────────────────

    input_bar = ft.Container(
        content=ft.Row(
            controls=[
                # Send button (left in RTL)
                ft.Container(
                    content=ft.Stack(
                        controls=[
                            ft.Icon(ft.Icons.SEND, color="white", size=20),
                            send_loading,
                        ],
                        alignment=ft.Alignment(0, 0),
                    ),
                    width=52, height=52,
                    bgcolor="#2563EB",
                    border_radius=16,
                    alignment=ft.Alignment(0, 0),
                    ink=True,
                    on_click=on_send,
                    shadow=ft.BoxShadow(
                        blur_radius=12, color="#402563EB", offset=ft.Offset(0, 4)
                    ),
                ),

                # Text field
                ft.Container(
                    content=message_field,
                    expand=True,
                    bgcolor="#F1F5F9",
                    border_radius=20,
                    padding=ft.Padding(left=16, right=16, top=4, bottom=4),
                ),

                # Attach button (right in RTL)
                ft.Container(
                    content=ft.Icon(ft.Icons.ATTACH_FILE, color="#64748B", size=22),
                    width=46, height=46,
                    bgcolor="#F1F5F9",
                    border_radius=14,
                    alignment=ft.Alignment(0, 0),
                    ink=True,
                    on_click=handle_pick,
                ),
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.END,
        ),
        bgcolor="white",
        padding=ft.Padding(left=16, right=16, top=12, bottom=16),
        shadow=ft.BoxShadow(blur_radius=8, color="#0A000000", offset=ft.Offset(0, -2)),
    )

    load_messages()

    return ft.View(
        route=f"/chat/{order_id}",
        controls=[
            ft.Column(
                controls=[
                    header,
                    ft.Container(
                        content=messages_col,
                        expand=True,
                        bgcolor="#F1F5F9",
                        padding=ft.Padding(left=16, right=16, top=16, bottom=8),
                    ),
                    input_bar,
                ],
                expand=True,
                spacing=0,
            )
        ],
        bgcolor="#F1F5F9",
        padding=0,
    )