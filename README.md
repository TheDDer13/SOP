# Project Website quy trình làm việc chuẩn SOP CPC1

## Giới thiệu
Website quản lý tài liệu SOP cho giữa các phòng ban của Công ty Cổ phần CPC1 Hà Nội.

## Nội dung
* [Kỹ thuật](#kythuat)
* [Tính năng sử dụng](#sudung)
* [Phát triển](#phattrien)

<a name="kythuat"/></a>
## Kỹ thuật
Trang web được viết bằng:
* Back-end Development:
  * python 3.9.5
  * Django 3.2.4
  * mysqlclient 2.0.3 (Kết nối với local MySQL qua MySQL Workbench)  
* Front-end Development:
  * Bootstrap 4
* Libraries:
  * django-import-export==2.5.0: Xử lý import dữ liệu từ file excel tại admin site
  * django-crispy-forms==1.12.0: Hỗ trợ render form cho Bootstrap
  * django-filter==2.4.0: Filter table dữ liệu bằng các field
* Deploy Production (Hosted by Heroku):
  * django-heroku==0.3.1
  * gunicorn==20.1.0
  * dj-database-url==0.5.0
  * psycopg2==2.9.1
  * whitenoise==5.2.0
  * Kết nối với local PostgreSQL qua pgAdmin4



<a name="sudung"/></a>
## Tính năng sử dụng
1. Nhập/Tra cứu thông tin các SOP đã được ban hành
2. Thu hồi SOP hết hiệu lực
3. Phân quyền truy cập SOP cho các phòng ban
4. Phân loại SOP theo Hệ thống Quản lý Chất lượng, hỗ trợ việc đánh giá Hệ thống

<a name="phattrien"/></a>
## Phát triển
* Các tính năng đang/dự định được phát triển:
  * Tạo modal form để cải thiện giao diện người dùng
