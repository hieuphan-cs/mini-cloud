"""
MyMiniCloud – Application Backend Server
Flask API server với các endpoint:
  GET /hello          – Public greeting
  GET /secure         – Protected (OIDC Bearer token)
  GET /student        – Danh sách sinh viên từ JSON (Mở rộng #2)
  GET /students-db    – Danh sách sinh viên từ MariaDB (Mở rộng #3)
  GET /health         – Health check
"""

from flask import Flask, jsonify, request, render_template
import time, requests, os, json, pymysql
from jose import jwt

# ─── Cấu hình OIDC ────────────────────────────────────────────────────────────
ISSUER_BASE = os.getenv("OIDC_ISSUER_BASE", "http://localhost:8081/realms")
JWKS_BASE   = os.getenv("OIDC_JWKS_BASE", "http://authentication-identity-server:8080/realms")
# Danh sách các realm được phép truy cập
ALLOWED_REALMS = os.getenv("ALLOWED_REALMS", "master,realm_sv001").split(",")
AUDIENCE    = os.getenv("OIDC_AUDIENCE", "account")

# ─── Cấu hình Database ────────────────────────────────────────────────────────
DB_HOST   = os.getenv("DB_HOST",     "relational-database-server")
DB_PORT   = int(os.getenv("DB_PORT", "3306"))
DB_USER   = os.getenv("DB_USER",     "root")
DB_PASS   = os.getenv("DB_PASS",     "root")
DB_NAME   = os.getenv("DB_NAME",     "studentdb")

# ─── JWKS Cache ───────────────────────────────────────────────────────────────
_JWKS_CACHE = {}

def get_jwks(realm):
    global _JWKS_CACHE
    now = time.time()
    cache_entry = _JWKS_CACHE.get(realm)
    
    # Cập nhật cache nếu chưa có hoặc đã quá hạn (10 phút = 600s)
    if not cache_entry or now - cache_entry['ts'] > 600:
        jwks_url = f"{JWKS_BASE}/{realm}/protocol/openid-connect/certs"
        try:
            data = requests.get(jwks_url, timeout=5).json()
            _JWKS_CACHE[realm] = {'data': data, 'ts': now}
        except Exception as e:
            print(f"[WARN] Cannot fetch JWKS for realm '{realm}': {e}")
            return None
            
    return _JWKS_CACHE[realm]['data']

# ─── Flask App ────────────────────────────────────────────────────────────────
app = Flask(__name__)

# ── Thêm CORS header cho tất cả response ──────────────────────────────────────
@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    return response

# ── GET /hello ─────────────────────────────────────────────────────────────────
@app.get("/hello")
def hello():
    return jsonify(
        message="Hello from App Server! ",
        # server="MyMiniCloud Application Backend",
        # version="1.0.0",
        # timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )

# ── GET /health ────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return jsonify(status="ok", uptime=time.time())

# ── GET /secure ────────────────────────────────────────────────────────────────
@app.get("/secure")
def secure():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify(error="Missing Bearer token — please provide Authorization: Bearer <token>"), 401
    
    token = auth.split(" ", 1)[1]
    try:
        # 1. Đọc "nháp" token (không xác thực) để biết nó phát hành từ Realm nào
        unverified_claims = jwt.get_unverified_claims(token)
        issuer = unverified_claims.get("iss", "")
        
        # 2. Kiểm tra xem Issuer có hợp lệ và Realm có nằm trong danh sách cho phép không
        realm = issuer.split("/")[-1]
        if not issuer.startswith(ISSUER_BASE) or realm not in ALLOWED_REALMS:
            return jsonify(error=f"Issuer or Realm '{realm}' is not allowed"), 401

        # 3. Lấy bộ Public Key (JWKS) đúng của Realm đó qua mạng nội bộ Docker
        jwks = get_jwks(realm)
        if not jwks:
            return jsonify(error=f"Cannot reach OIDC server to fetch keys for realm '{realm}'"), 503

        # 4. Tiến hành xác thực chữ ký (Signature)
        payload = jwt.decode(
            token, jwks,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=issuer # Xác thực đúng Issuer lấy từ token
        )
        
        return jsonify(
            message=f"✅ Secure resource OK (Validated against realm: {realm})",
            preferred_username=payload.get("preferred_username"),
            email=payload.get("email"),
            roles=payload.get("realm_access", {}).get("roles", [])
        )
    except Exception as e:
        return jsonify(error=str(e)), 401

# ── GET /student  (Mở rộng #2: đọc từ students.json) ─────────────────────────
@app.get("/student")
def student():
    json_path = os.path.join(os.path.dirname(__file__), "students.json")
    try:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(
            source="JSON file",
            count=len(data),
            students=data
        )
    except FileNotFoundError:
        return jsonify(error="students.json not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

# ── GET /students-db  (Mở rộng #3: đọc từ MariaDB studentdb) ─────────────────
@app.get("/students-db")
def students_db():
    try:
        conn = pymysql.connect(
            host=DB_HOST, port=DB_PORT,
            user=DB_USER, password=DB_PASS,
            database=DB_NAME,
            connect_timeout=5,
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, student_id, fullname, dob, major FROM students ORDER BY id")
                rows = cur.fetchall()
        # Chuyển date -> string để jsonify
        for r in rows:
            if hasattr(r.get("dob"), "isoformat"):
                r["dob"] = r["dob"].isoformat()

        # return jsonify(
        #     source="MariaDB (studentdb)",
        #     count=len(rows),
        #     students=rows
        # )

        return render_template(
            "students-db.html",
            students=rows,
            count=len(rows)
        )
    except Exception as e:
        return jsonify(error=str(e), hint="Make sure DB is running and studentdb schema exists"), 503

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8081"))
    app.run(host="0.0.0.0", port=port, debug=False)
