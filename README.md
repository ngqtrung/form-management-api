# Form Management API

Đây là backend cho hệ thống quản lý form. Ý tưởng đơn giản: admin tạo ra các form, mỗi form gồm nhiều field (text, number, date, color, select), nhân viên vào xem form nào đang active thì điền và nộp. Dữ liệu nộp lên được validate ở server theo đúng loại field, không tin frontend. Có kèm phân quyền theo Role/Permission nữa.

Dưới đây là hướng dẫn chạy thử.

## 1. Chuẩn bị

Máy cần có sẵn:
- Python 3.8.10
- Poetry (nếu chưa có thì `pip install poetry`)
- PostgreSQL 14+ ( dùng DBeaver để xem DB cho tiện, không bắt buộc)

## 2. Cấu hình

Tạo file `.env` ở thư mục gốc, nội dung như này:

```
FLASK_ENV=development

SECRET_KEY=secret_key
JWT_SECRET_KEY=jwt_secret_key
JWT_EXPIRES_MINUTES=480

POSTGRES_URI=postgresql://user:password@localhost:5432/form_management

CORS_ORIGINS=http://localhost:8080
```

Nhớ đổi `user:password` trong `POSTGRES_URI` cho khớp với Postgres của bạn.

## 3. Cài & khởi tạo

```
poetry install
poetry shell
alembic upgrade head
python run.py seed
```

Chạy `alembic upgrade head` là xong, nó tự tạo database `form_management` nếu chưa có, không cần vào DBeaver tạo tay. `python run.py seed` thì tạo sẵn vài permission/role mặc định + 1 tài khoản admin để đăng nhập thử.

Nếu sau này sửa model (thêm field, thêm bảng...) thì nhớ chạy thêm:
```
alembic revision --autogenerate -m "mô tả thay đổi"
alembic upgrade head
```

Một lỗi hay gặp trên Windows là `poetry shell` báo "running scripts is disabled". Gặp cái này thì mở PowerShell chạy:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## 4. Chạy server

```
python run.py api
```

Mặc định chạy ở port 5000. Muốn đổi port thì thêm `--port=8000`, không muốn auto-reload thì thêm `--no-debug`.

Nếu không muốn cài gì cả (không cần Poetry, không cần Postgres cài local), có thể chạy bằng Docker:
```
docker compose up --build
```
Lệnh này lo hết mọi thứ, build image, chạy Postgres, migrate, seed, rồi start server.

## 5. Test thử API

Muốn xem nhanh có những API nào thì mở `http://localhost:5000/api/docs`, đây là Swagger UI, spec được sinh tự động từ code

Muốn test bằng Postman thì import file `postman_collection.json` ở thư mục gốc vào. Chạy request "Login" trước để lấy token, các request sau tự động dùng token đó ( có set sẵn script lưu token vào biến của collection).

Chạy `pytest` để chạy bộ test có sẵn (unit test cho phần validate + integration test cho API).

## Kiến trúc, viết sao cho dễ đọc

Mỗi resource (forms, users, roles...) có 1 folder riêng trong `app/api/`, và folder nào cũng chỉ có đúng 3 file: `__init__.py` khai báo endpoint của resource đó, `methods.py` chứa các class ứng với từng HTTP method (Get, Post, Put, Delete), và `schemas.py` là schema validate input bằng marshmallow. Route không cần đăng ký tay ở đâu cả, lúc app khởi động sẽ có 1 đoạn tự quét hết `app/api/` rồi đăng ký luôn. Field kiểu lồng nhau như `/api/forms/:id/fields/:fid` thì cũng nằm trong 1 folder con tương ứng, theo đúng pattern y hệt.

Logic xử lý nghiệp vụ (gọi DB, tính toán...)  để riêng ở `app/services/`, không viết thẳng trong `methods.py` cho dễ đọc và dễ test. Phần validate dữ liệu form (đúng loại text/number/date/color/select) cũng tách riêng ra `app/validators/`, mỗi loại field có 1 class validate riêng, test được độc lập mà không cần đụng tới database.

Về phân quyền: User, Role, Permission là 3 bảng, nối với nhau qua 2 bảng trung gian `user_role` và `role_permission`. Role admin không phải là 1 trường hợp đặc biệt được hardcode trong code, nó chỉ là 1 role bình thường được gán sẵn hết mọi permission lúc seed. Mỗi request đều check quyền lại từ DB (không tin vào thông tin trong JWT), nên nếu admin đổi quyền của ai đó thì có hiệu lực ngay, không phải đợi token cũ hết hạn.

Đăng nhập trả về 2 token: access token (ngắn hạn) và refresh token (dài hạn hơn). Khi logout,  lưu lại id của access token đó vào bảng `token_blacklist`, nên dù token chưa hết hạn tự nhiên thì vẫn không dùng được nữa sau khi logout.

Migration  dùng Alembic trực tiếp, không qua Flask-Migrate, cho gọn nhẹ hơn.

## Vài quyết định có thể bạn sẽ thắc mắc

- Xóa Form thì  chỉ đánh dấu xóa mềm (soft-delete) chứ không xóa thật, vì lịch sử submission cũ vẫn phải giữ nguyên. Field thì xóa thẳng luôn cho đơn giản, không sao vì lúc submit  đã lưu lại (snapshot) label và type của field ngay trong bản thân câu trả lời rồi, nên field gốc có bị xóa thì lịch sử vẫn đọc được bình thường.
- Submission được lưu qua các bảng quan hệ có FK đàng hoàng, không lưu kiểu JSON đổ hết vào 1 cột cho nhanh, đổi lại sau này query hay làm báo cáo sẽ dễ hơn nhiều.

## Chưa kịp làm

- Chưa làm được reorder field kiểu kéo thả, hiện tại muốn đổi thứ tự field thì phải sửa từng field một qua API PUT.
- Bảng `token_blacklist` chưa có job dọn các token đã hết hạn, để lâu bảng sẽ phình to dần, không ảnh hưởng gì tới tính đúng đắn nhưng nên dọn nếu chạy production thật.
