import flet as ft
from api_client import api
from components.navbar import bottom_navbar

def my_orders_screen(page: ft.Page):

    loading = ft.ProgressRing(width=32, height=32, color="#6C63FF", stroke_width=3)
    error_text = ft.Text("", color="#FF4D4D", size=13, text_align=ft.TextAlign.CENTER)
    orders_list = ft.Column(spacing=12)

    status_colors = {
        "معلقه": "#FFA500",
        "قيد التنفيذ": "#6C63FF",
        "مكتمل": "#4DFF91",
        "ملغي": "#FF4D4D",
    }

    def load_orders():
        orders_list.controls.clear()
        loading.visible = True
        error_text.value = ""
        page.update()

        result = api.get_my_orders()
        loading.visible = False

        if result["success"]:
            data = result["data"]

            # ✅ استخرج الـ list صح بغض النظر عن شكل الـ response
            if isinstance(data, list):
                orders = data
            elif isinstance(data, dict):
                orders = data.get("results") or data.get("orders") or data.get("data") or []
            else:
                orders = []

            # ✅ فلتر أي عنصر مش dict
            orders = [o for o in orders if isinstance(o, dict)]

            if not orders:
                orders_list.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon("receipt_long", size=64, color="#444455"),
                            ft.Text("لا توجد طلبات بعد", size=16, color="#666680"),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                        alignment=ft.Alignment(0, 0),
                        padding=40,
                    )
                )
            else:
                for order in orders:
                    status_val = order.get("status", "")
                    status_color = status_colors.get(status_val, "#AAAACC")

                    card = ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Text(status_val, size=11, color="white",
                                                    weight=ft.FontWeight.BOLD),
                                    bgcolor=status_color,
                                    border_radius=8,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                ),
                                ft.Text(f"#{order.get('id', '')}", size=13, color="#AAAACC"),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Container(height=8),
                            ft.Text(
                                str(order.get("file_name", "")).split("/")[-1],
                                size=14, color="white", weight=ft.FontWeight.W_500,
                            ),
                            ft.Container(height=4),
                            ft.Row([
                                ft.Text("التكلفة:", size=12, color="#AAAACC"),
                                ft.Text(f"{order.get('total_cost', 0)} ج.م", size=12,
                                        color="#6C63FF", weight=ft.FontWeight.BOLD),
                            ], spacing=6),
                            ft.Row([
                                ft.Text("التاريخ:", size=12, color="#AAAACC"),
                                ft.Text(str(order.get("created_at", ""))[:10],
                                        size=12, color="#AAAACC"),
                            ], spacing=6),
                        ], spacing=4),
                        bgcolor="#1E1E2E",
                        border_radius=16,
                        padding=16,
                    )
                    orders_list.controls.append(card)
        else:
            error_text.value = result["message"]

        page.update()

    refresh_btn = ft.IconButton(
        icon="refresh",
        icon_color="#6C63FF",
        on_click=lambda e: load_orders(),
    )

    load_orders()

    return ft.View(
        route="/my-orders",
        controls=[
            ft.Container(
                expand=True,
                padding=ft.padding.symmetric(horizontal=20, vertical=24),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Row([
                            ft.Text("طلباتي", size=22, weight=ft.FontWeight.BOLD, color="white"),
                            refresh_btn,
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(height=20),
                        loading,
                        error_text,
                        orders_list,
                        ft.Container(height=32),
                        bottom_navbar(page, current_index=1),
                    ],
                ),
            )
        ],
        bgcolor="#0F0F1A",
        padding=0,
    )