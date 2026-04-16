# Mini-Cloud

# Requirements
## 1. Web Frontend Server
### Basic
**Run:**
- curl.exe -I http://localhost:8080/ --> HTTP/1.1 200 OK
- curl.exe -I http://localhost:8080/blog/ --> HTTP/1.1 200 OK
### Extend
- 3 blog posts
- images and link to back to homepage
- index.html shows list of posts (hyperlink)

## 2. Application Backend Server
### Basic
**Run:**
- curl.exe http://localhost:8085/hello --> {"message":"Hello from App Server!"}
- curl.exe http://localhost/api/hello --> {"message":"Hello from App Server!"}

### Extend
**Open:** http://localhost/api/student --> json

## 3. Relational Database Server
### Basic
**Run:** 
- docker run -it --rm --network cloud-net mysql:8 sh -lc "mysql -h relational-database-server -uroot -proot -e 'USE minicloud; SHOW TABLES; SELECT * FROM notes;'"
### Extend
**Run:**:
- docker exec -it relational-database-server mariadb -u root -proot
Then MariaDB terminal open
- SHOW DATABASES;
- USE studentdb;
- SELECT * FROM students;
- INSERT INTO students (student_id, fullname, major) VALUES ('SV100','Demo User','AI');
- UPDATE students SET gpa = 3.9 WHERE student_id = 'SV100';
- DELETE FROM students WHERE student_id = 'SV100';

## 4. Authentication Identity Server
### Basic
**Open:** http://localhost:8081
- Username: admin
- Password: admin
- Create user sv01
### Extend
Create Realm named realm_sv001:
- create 2 user (sv01, sv02)
- create client (flask-app)
<pre>
$tokenResponse = Invoke-RestMethod -Uri "http://localhost:8081/realms/realm_sv001/protocol/openid-connect/token" `
    -Method Post `
    -ContentType "application/x-www-form-urlencoded" `
    -Body @{
        client_id  = "flask-app"
        grant_type = "password"
        username   = "sv01"
        password   = "123456" # Mật khẩu bạn đã đặt
   }
$ACCESS_TOKEN = $tokenResponse.access_token
Write-Host "$ACCESS_TOKEN"
</pre>

curl.exe -X GET "http://localhost:8085/secure" -H "Authorization: Bearer $ACCESS_TOKEN"

## 5. Object Storage Server (object-storage-server)
- Open: http://localhost:9001
- Login: Đăng nhập: minioadmin / minioadmin
- Create bucket which named "demo"
- Upload index.html from web-frontend-server

## 6. Internal DNS Server
**Run:** docker run --rm --network cloud-net alpine sh -c "
  apk add --no-cache bind-tools -q &&
  dig @internal-dns-server web-frontend-server.cloud.local +short &&
  dig @internal-dns-server app-backend.cloud.local +short &&
  dig @internal-dns-server minio.cloud.local +short &&
  dig @internal-dns-server keycloak.cloud.local +short
"
**Output:** 
- 10.10.10.10
- 10.10.10.20
- 10.10.10.30
- 10.10.10.40

## 7. Monitering Note Exporter
- Open: http://localhost:9090
- Status → Targets
 Kiểm tra: monitoring-node-exporter-server:9100 phải UP
 Trong tab “Graph”, thử truy vấn:
 node_cpu_seconds_total
8️ Monitoring Grafana Dashboard



# Additional Information
Authors: hieu_phan, ntkn-gulu
