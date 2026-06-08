# 🍔 QuickBite

Nền tảng đặt đồ ăn nội bộ (canteen/công ty) — xây dựng trên **FastAPI** và triển khai trên **AWS**.

> Đề tài 3: Application Development on AWS  
> Chương trình Thực tập Tốt nghiệp — Amazon Web Services Việt Nam (HK253)

---

## 📐 Kiến trúc hệ thống

```
[Frontend - HTML/React]
         │
   [API Gateway]
         │
   [EC2 - FastAPI]
    ┌────┴────┐
[RDS/PostgreSQL] [S3 - ảnh món ăn]
         │
   [Lambda - Email]
         │
   [CloudWatch - Logs]
```

---

## ✨ Tính năng

### 👤 Khách hàng
- Đăng ký / Đăng nhập (JWT)
- Xem menu, tìm kiếm & lọc món ăn
- Thêm vào giỏ hàng, đặt đơn
- Theo dõi trạng thái đơn hàng
- Xem lịch sử đơn

### 🧑‍🍳 Admin (Quản lý canteen)
- Quản lý món ăn (thêm/sửa/xóa + upload ảnh lên S3)
- Xem & cập nhật trạng thái đơn hàng
- Dashboard doanh thu theo ngày/tuần

### ⚙️ Hệ thống
- Gửi email xác nhận đơn qua AWS Lambda + SES
- Logging toàn bộ API request với CloudWatch
- Phân quyền: `customer` / `admin`

---

## 🗂️ Cấu trúc project

```
quickbite/
├── main.py              # Entry point, CORS, include routers
├── database.py          # Kết nối PostgreSQL / RDS
├── auth_utils.py        # JWT, bcrypt, middleware phân quyền
├── requirements.txt
├── .env.example
├── models/
│   ├── user.py          # Table: users
│   ├── item.py          # Table: items, categories
│   └── order.py         # Table: orders, order_items
├── routers/
│   ├── auth.py          # POST /auth/register, /login | GET /auth/me
│   ├── menu.py          # GET /menu, /menu/{id} | POST/PATCH/DELETE (admin)
│   └── orders.py        # POST /orders | GET /orders/my, /orders/{id}
└── schemas/
    ├── user.py          # Pydantic schemas cho Auth
    └── order.py         # Pydantic schemas cho Order
```

---

## 🚀 Hướng dẫn chạy local

### 1. Clone repo & cài đặt môi trường

```bash
git clone https://github.com/<your-org>/quickbite.git
cd quickbite

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường

```bash
cp .env.example .env
# Mở .env và điền thông tin database, secret key
```

Nội dung `.env`:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/quickbite
SECRET_KEY=your-super-secret-key
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=ap-southeast-1
S3_BUCKET_NAME=quickbite-images
```

### 3. Tạo database PostgreSQL

```bash
psql -U postgres
CREATE DATABASE quickbite;
\q
```

### 4. Chạy server

```bash
uvicorn main:app --reload
```

Truy cập **Swagger UI**: http://localhost:8000/docs  
Truy cập **ReDoc**: http://localhost:8000/redoc

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| POST | `/auth/register` | Đăng ký tài khoản | ❌ |
| POST | `/auth/login` | Đăng nhập → JWT token | ❌ |
| GET | `/auth/me` | Thông tin user hiện tại | ✅ |

### Menu
| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| GET | `/menu` | Lấy danh sách món | ❌ |
| GET | `/menu/{id}` | Chi tiết món ăn | ❌ |
| POST | `/menu` | Thêm món mới | ✅ Admin |
| PATCH | `/menu/{id}` | Cập nhật món | ✅ Admin |
| DELETE | `/menu/{id}` | Xoá món | ✅ Admin |

### Orders
| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| POST | `/orders` | Tạo đơn hàng | ✅ |
| GET | `/orders/my` | Lịch sử đơn của tôi | ✅ |
| GET | `/orders/{id}` | Chi tiết đơn hàng | ✅ |
| PATCH | `/orders/{id}/status` | Cập nhật trạng thái | ✅ Admin |

### Trạng thái đơn hàng
```
pending → confirmed → preparing → ready → completed
                                        ↘ cancelled
```

---

## 🗄️ Database Schema

```
users
├── id, name, email, password_hash, role

categories
├── id, name

items
├── id, name, description, price, image_url, is_available, category_id

orders
├── id, user_id, status, total, note, created_at

order_items
├── id, order_id, item_id, quantity, price
```

---

## ☁️ AWS Services sử dụng

| Service | Mục đích |
|---------|----------|
| **EC2** | Chạy FastAPI server |
| **API Gateway** | Expose API ra ngoài internet |
| **RDS (PostgreSQL)** | Lưu trữ dữ liệu chính |
| **S3** | Lưu ảnh món ăn |
| **Lambda** | Gửi email xác nhận đơn (SES) |
| **CloudWatch** | Logging & monitoring API |

---

## 📅 Timeline thực hiện

| Tuần | Nội dung |
|------|----------|
| 1 | ✅ Thiết kế DB, API spec, dựng FastAPI skeleton + Auth |
| 2 | Hoàn thiện API Menu & Orders, test local |
| 3 | Deploy EC2 + API Gateway, kết nối S3 upload ảnh |
| 4 | Tích hợp RDS PostgreSQL trên AWS |
| 5 | Lambda gửi email + CloudWatch logging |
| 6 | Tính năng nâng cao: filter, dashboard doanh thu |
| 7 | Load test (Locust), tối ưu query, fix bug |
| 8 | Hoàn thiện UI, viết báo cáo, chuẩn bị demo |

---

## 👥 Thành viên nhóm

| Thành viên | Vai trò | Nhiệm vụ |
|------------|---------|----------|
| **A** | Backend Lead | FastAPI, Auth (JWT), API design, kết nối RDS |
| **B** | Cloud / Infra | EC2, API Gateway, S3, Lambda, CloudWatch |
| **C** | Frontend + DB | Giao diện, DB schema, tích hợp API |

---

## 🧪 Test API nhanh (với curl)

```bash
# Đăng ký
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Nguyen Van A", "email": "a@example.com", "password": "123456"}'

# Đăng nhập → lấy token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "a@example.com", "password": "123456"}'

# Xem menu (không cần token)
curl http://localhost:8000/menu

# Tạo đơn hàng (cần token)
curl -X POST http://localhost:8000/orders \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"item_id": 1, "quantity": 2}], "note": "Ít cay"}'
```

---

## 📝 Ghi chú

- File `.env` **không được commit** lên GitHub (đã có trong `.gitignore`)
- Khi deploy lên AWS, thay `DATABASE_URL` bằng endpoint RDS thực tế
- `SECRET_KEY` phải được đổi thành chuỗi ngẫu nhiên mạnh trước khi production
