import httpx

class APIClient:
    def __init__(self):
        self.BASE_URL = "http://127.0.0.1:8000/api/v1/auth"
        self.ORDERS_URL = "http://127.0.0.1:8000/api/v1/orders"
        self.access_token = None
        self.user_data = None

    def login(self, username, password):
        try:
            with httpx.Client(timeout=30) as client:
                response = client.post(
                    f"{self.BASE_URL}/login/",
                    json={"username": username, "password": password},
                )
            if response.status_code == 200:
                data = response.json()
                self.access_token = data['token']['access']
                self.user_data = data['user']
                return {"success": True, "data": data}
            else:
                return {"success": False, "message": "بيانات الدخول غير صحيحة"}
        except Exception as e:
            return {"success": False, "message": f"تعذر الاتصال بالسيرفر: {str(e)}"}

    def signup(self, username, password, email=""):
        try:
            with httpx.Client(timeout=30) as client:
                response = client.post(
                    f"{self.BASE_URL}/signup/",
                    json={
                        "username": username,
                        "password": password,
                        "confirm": password,
                        "email": email
                    },
                )
            if response.status_code == 201:
                data = response.json()
                return {"success": True, "data": data}
            else:
                errors = response.json()
                msg = list(errors.values())[0][0] if errors else "حدث خطأ أثناء إنشاء الحساب"
                return {"success": False, "message": msg}
        except Exception as e:
            return {"success": False, "message": f"تعذر الاتصال بالسيرفر: {str(e)}"}

    def get_paper_options(self):
        try:
            with httpx.Client(timeout=30) as client:
                response = client.get(
                    f"{self.ORDERS_URL}/options/",
                    headers={"Authorization": f"Bearer {self.access_token}"},
                )
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "message": "فشل تحميل الخيارات"}
        except Exception as e:
            return {"success": False, "message": f"تعذر الاتصال: {str(e)}"}

    async def create_order(self, file_path, paper_type_id, paper_size_id,
                        printing_color_id, printing_sides,
                        number_of_sheets, quantity, address, notes=""):
            try:
                with open(file_path, 'rb') as f:
                    file_bytes = f.read()
                
                async with httpx.AsyncClient(timeout=30) as client:
                    response = await client.post(
                        f"{self.ORDERS_URL}/create/",
                        headers={"Authorization": f"Bearer {self.access_token}"},
                        data={
                            'paper_type': paper_type_id,
                            'paper_size': paper_size_id,
                            'printing_color': printing_color_id,
                            'printing_sides': printing_sides,
                            'number_of_sheets': number_of_sheets,
                            'quantity': quantity,
                            'address': address,
                            'notes': notes,
                        },
                        files={'file_name': (file_path.split('/')[-1], file_bytes)},
                    )
                if response.status_code == 201:
                    return {"success": True, "data": response.json()}
                errors = response.json()
                msg = list(errors.values())[0][0] if errors else "فشل إنشاء الطلب"
                return {"success": False, "message": msg}
            except Exception as e:
                return {"success": False, "message": f"تعذر الاتصال: {str(e)}"}

    def get_my_orders(self):
        try:
            with httpx.Client(timeout=30) as client:
                response = client.get(
                    f"{self.ORDERS_URL}/my-orders/",
                    headers={"Authorization": f"Bearer {self.access_token}"},
                )
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "message": "فشل تحميل الطلبات"}
        except Exception as e:
            return {"success": False, "message": f"تعذر الاتصال: {str(e)}"}

    def get_page_count(self, file_path: str, file_name: str) -> int:
        try:
            with open(file_path, 'rb') as f:
                with httpx.Client(timeout=30) as client:
                    response = client.post(
                        f"{self.ORDERS_URL}/count-pages/",
                        headers={"Authorization": f"Bearer {self.access_token}"},
                        files={"file": (file_name, f)},
                    )
            if response.status_code == 200:
                pages = response.json().get("pages", 1)
                print(f"DEBUG: page count from server = {pages}")
                return pages
        except Exception as e:
            print(f"DEBUG: page count error = {e}")
        return 1

api = APIClient()