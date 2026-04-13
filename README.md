# Mini-Cloud

# Requirements
1. web-frontend-serverr

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

# Additional Information
Authors: hieu_phan, ntkn-gulu
