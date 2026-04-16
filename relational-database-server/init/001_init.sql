-- ─────────────────────────────────────────────────────────────────────────────
-- MyMiniCloud – Database Initialization Script
-- Tạo 2 database: minicloud (cơ bản) và studentdb (mở rộng #3)
-- ─────────────────────────────────────────────────────────────────────────────

-- ═══ Database 1: minicloud (yêu cầu cơ bản) ══════════════════════════════════
CREATE DATABASE IF NOT EXISTS minicloud CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE minicloud;

CREATE TABLE IF NOT EXISTS notes (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    title      VARCHAR(200) NOT NULL,
    content    TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO notes (title, content) VALUES
    ('Hello from MariaDB!', 'Đây là ghi chú đầu tiên được tạo tự động khi khởi động container.'),
    ('MyMiniCloud is running', 'Hệ thống 9 server đã được khởi động thành công qua Docker Compose.'),
    ('Docker + MariaDB', 'Container hóa cơ sở dữ liệu giúp di chuyển và sao lưu dễ dàng hơn.');

-- ═══ Database 2: studentdb (mở rộng #3) ═══════════════════════════════════════
CREATE DATABASE IF NOT EXISTS studentdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE studentdb;

CREATE TABLE IF NOT EXISTS students (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(10)  NOT NULL UNIQUE COMMENT 'Mã số sinh viên',
    fullname   VARCHAR(100) NOT NULL             COMMENT 'Họ và tên đầy đủ',
    dob        DATE                              COMMENT 'Ngày sinh',
    major      VARCHAR(50)  NOT NULL             COMMENT 'Chuyên ngành',
    gpa        DECIMAL(3,2) DEFAULT 0.00         COMMENT 'Điểm trung bình tích lũy',
    email      VARCHAR(100)                      COMMENT 'Email sinh viên',
    year       TINYINT      DEFAULT 1            COMMENT 'Năm học',
    created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO students (student_id, fullname, dob, major, gpa, email, year) VALUES
    ('SV001', 'Nguyen Van A', '2002-03-15', 'Computer Science',    3.50, 'nguyenvana@student.edu.vn', 3),
    ('SV002', 'Tran Thi B',   '2001-11-02', 'Data Science',        3.70, 'tranthib@student.edu.vn',   2),
    ('SV003', 'Le Van C',     '2002-07-20', 'Cybersecurity',       3.20, 'levanc@student.edu.vn',     4),
    ('SV004', 'Pham Thi D',   '2003-01-08', 'Software Engineering',3.80, 'phamthid@student.edu.vn',   3),
    ('SV005', 'Hoang Van E',  '2001-05-25', 'Information Systems', 3.40, 'hoangvane@student.edu.vn',  2);

-- ═══ Xác nhận dữ liệu ═════════════════════════════════════════════════════════
SELECT 'minicloud.notes' AS table_name, COUNT(*) AS row_count FROM minicloud.notes
UNION ALL
SELECT 'studentdb.students', COUNT(*) FROM studentdb.students;
