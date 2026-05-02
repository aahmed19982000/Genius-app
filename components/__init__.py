import flet as ft
from api_client import api

def login_screen(page: ft.Page):
    # مراجع للعناصر عشان نعرف نجيب قيمتها
    username_field = ft.TextField(
        label="اسم المستخدم",
        hint_text="أدخل اسم المستخدم",
        prefix_icon=ft.icons.PERSON_OUTLINE,
        border_radius=15,
        border_color="#E0E0E0",
        focused_border_color="#1B5E20", # لون أخضر غامق عند الضغط
        height=60,
    )

    password_field = ft.TextField(
        label="كلمة المرور",
        hint_text="أدخل كلمة المرور",
        prefix_icon=ft.icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        border_radius=15,
        border_color="#E0E0E0",
        focused_border_color="#1B5E20",
        height=60,
    )

    error_text = ft.Text(color="red", size=12)

    def handle_login(e):
        if not username_field.value or not password_field.value:
            error_text.value = "يرجى إدخال البيانات"
            page.update()
            return
            
        res = api.login(username_field.value, password_field.value)
        if res["success"]:
            page.go("/dashboard")
        else:
            error_text.value = res["message"]
            page.update()

    # محتوى الصفحة
    return ft.View(
        "/login",
        bgcolor="#F8F9FB", # خلفية مائلة للبياض زي الصورة
        padding=0,
        controls=[
            ft.Column(
                [
                    # الشعار والترحيب
                    ft.Container(
                        content=ft.Column([
                            ft.Image(src="assets/logo.png", width=100, height=100, border_radius=20), # حط صورتك في فولدر assets
                            ft.Text("اطبعلي", size=32, weight="bold", color="#000000"),
                            ft.Text("تطوير: أحمد إبراهيم", size=14, color="#757575"),
                            ft.Text("مرحباً بك مجدداً في خدمات الطباعة", size=16, color="#424242"),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        margin=ft.margin.only(top=50, bottom=30),
                    ),

                    # الكارت الأبيض (النموذج)
                    ft.Container(
                        content=ft.Column([
                            username_field,
                            ft.Row([
                                ft.TextButton("نسيت كلمة المرور؟", style=ft.ButtonStyle(color="#1976D2")),
                            ], alignment=ft.MainAxisAlignment.END),
                            password_field,
                            ft.Row([
                                ft.Checkbox(label="تذكرني", fill_color="#1B5E20"),
                            ]),
                            ft.Container(height=10),
                            
                            # زر تسجيل الدخول (الأخضر)
                            ft.ElevatedButton(
                                content=ft.Row([
                                    ft.Icon(ft.icons.ARROW_FORWARD, color="white"),
                                    ft.Text("تسجيل الدخول", size=18, weight="bold", color="white"),
                                ], alignment=ft.MainAxisAlignment.CENTER),
                                style=ft.ButtonStyle(
                                    bgcolor="#1B5E20",
                                    shape=ft.RoundedRectangleBorder(radius=15),
                                ),
                                height=55,
                                width=float("inf"),
                                on_click=handle_login,
                            ),
                            error_text,
                            
                            ft.Divider(height=40, color="#EEEEEE"),
                            
                            ft.Text("ليس لديك حساب؟", color="#424242"),
                            ft.OutlinedButton(
                                "إنشاء حساب جديد",
                                style=ft.ButtonStyle(
                                    side={"": ft.BorderSide(1, "#1976D2")},
                                    shape=ft.RoundedRectangleBorder(radius=15),
                                    color="#1976D2",
                                ),
                                height=55,
                                width=float("inf"),
                                on_click=lambda _: print("Go to Register"),
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor="white",
                        padding=30,
                        border_radius=30,
                        shadow=ft.BoxShadow(blur_radius=20, color="#E0E0E0"),
                        width=400,
                    ),
                    
                    # الفوتر
                    ft.Container(
                        content=ft.Text(
                            "بالاستمرار، أنت توافق على شروط الخدمة وسياسة الخصوصية",
                            size=12, color="#757575", text_align=ft.TextAlign.CENTER
                        ),
                        margin=ft.margin.only(top=40, bottom=20),
                        width=300
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            )
        ]
    )