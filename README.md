# Mini-Cloud

# Requirements
## 1. web-frontend-serverr

test command:
curl.exe -I http://localhost:8080/ --> HTTP/1.1 200 OK
curl.exe -I http://localhost:8080/blog/ --> HTTP/1.1 200 OK
3. application-backend-server
  - Return JSON: {"message":"Hello from App Server!"} - 100%
  - Added a new API: /student → returns a list of students from a JSON file or database - 0%


## Application Backend Server (application-backend-server)
Run commands (PowerShell):
- curl.exe http://localhost:8085/hello --> {"message":"Hello from App Server!"}
- curl.exe http://localhost/api/hello --> {"message":"Hello from App Server!"}

## Relationship Database Server
Run commands:
- docker run -it --rm --network cloud-net mysql:8 sh -lc "mysql -h relational-database-server -uroot -proot -e 'USE minicloud; SHOW TABLES; SELECT * FROM notes;'"
+---------------------+
| Tables_in_minicloud |
+---------------------+
| notes               |
+---------------------+
+----+------------------------+--------------------------------------------------------------------+---------------------+
| id | title                  | content                                                            | created_at          |
+----+------------------------+--------------------------------------------------------------------+---------------------+
|  1 | Hello from MariaDB!    | ?�y l� ghi ch� ??u ti�n ???c t?o t? ??ng khi kh?i ??ng container.  | 2026-04-13 06:33:29 |
|  2 | MyMiniCloud is running | H? th?ng 9 server ?� ???c kh?i ??ng th�nh c�ng qua Docker Compose. | 2026-04-13 06:33:29 |
|  3 | Docker + MariaDB       | Container h�a c? s? d? li?u gi�p di chuy?n v� sao l?u d? d�ng h?n. | 2026-04-13 06:33:29 |
+----+------------------------+--------------------------------------------------------------------+---------------------+

## 5. Object Storage Server (object-storage-server)
- Open: http://localhost:9001
- Login: Đăng nhập: minioadmin / minioadmin
- Create bucket which named "demo"
- Upload index.html from web-frontend-server

## 7. Monitering Note Exporter
- Open: http://localhost:9090
- Status → Targets
 Kiểm tra: monitoring-node-exporter-server:9100 phải UP
 Trong tab “Graph”, thử truy vấn:
 node_cpu_seconds_total
8️ Monitoring Grafana Dashboard



# Additional Information
Authors: hieu_phan, ntkn-gulu
