// server.js - File chính của API
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const Firebird = require('node-firebird');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

// Cấu hình kết nối database
const dbOptions = {
    host: '127.0.0.1',
    port: 3050,
    database: '/path/to/your/database.fdb',
    user: 'SYSDBA',
    password: 'masterkey',
    lowercase_keys: false,
    role: null,
    pageSize: 4096
};

// Cấu hình lưu trữ files
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        const dir = './uploads';
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir);
        }
        cb(null, dir);
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname);
    }
});

const upload = multer({ storage: storage });

// Khởi tạo Express
const app = express();
app.use(bodyParser.json());
app.use(cors());
app.use('/uploads', express.static('uploads'));

// Helper function để kết nối database
function getConnection(callback) {
    Firebird.attach(dbOptions, function(err, db) {
        if (err) {
            return callback(err, null);
        }
        callback(null, db);
    });
}

// Helper function để thực hiện query
function executeQuery(query, params, callback) {
    getConnection((err, db) => {
        if (err) {
            return callback(err, null);
        }
        
        db.query(query, params, (err, results) => {
            db.detach();
            if (err) {
                return callback(err, null);
            }
            callback(null, results);
        });
    });
}

// ===== API PHÒNG BAN =====
// Lấy danh sách phòng ban
app.get('/api/phongban', (req, res) => {
    executeQuery('SELECT * FROM PhongBan', [], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

// Lấy thông tin 1 phòng ban
app.get('/api/phongban/:id', (req, res) => {
    executeQuery('SELECT * FROM PhongBan WHERE MaPB = ?', [req.params.id], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (results.length === 0) {
            return res.status(404).json({ message: 'Không tìm thấy phòng ban' });
        }
        res.json(results[0]);
    });
});

// Thêm phòng ban mới
app.post('/api/phongban', (req, res) => {
    const { MaPB, TenPB, MoTa } = req.body;
    if (!MaPB || !TenPB) {
        return res.status(400).json({ message: 'Mã và tên phòng ban là bắt buộc' });
    }
    
    executeQuery('INSERT INTO PhongBan (MaPB, TenPB, MoTa) VALUES (?, ?, ?)', 
        [MaPB, TenPB, MoTa], (err, results) => {
            if (err) {
                return res.status(500).json({ error: err.message });
            }
            res.status(201).json({ message: 'Thêm phòng ban thành công', id: MaPB });
    });
});

// Cập nhật phòng ban
app.put('/api/phongban/:id', (req, res) => {
    const { TenPB, MoTa } = req.body;
    if (!TenPB) {
        return res.status(400).json({ message: 'Tên phòng ban là bắt buộc' });
    }
    
    executeQuery('UPDATE PhongBan SET TenPB = ?, MoTa = ? WHERE MaPB = ?', 
        [TenPB, MoTa, req.params.id], (err, results) => {
            if (err) {
                return res.status(500).json({ error: err.message });
            }
            res.json({ message: 'Cập nhật phòng ban thành công' });
    });
});

// Xóa phòng ban
app.delete('/api/phongban/:id', (req, res) => {
    executeQuery('DELETE FROM PhongBan WHERE MaPB = ?', [req.params.id], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ message: 'Xóa phòng ban thành công' });
    });
});

// ===== API CHỨC VỤ =====
// Lấy danh sách chức vụ
app.get('/api/chucvu', (req, res) => {
    executeQuery('SELECT * FROM ChucVu', [], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

// Lấy thông tin 1 chức vụ
app.get('/api/chucvu/:id', (req, res) => {
    executeQuery('SELECT * FROM ChucVu WHERE MaCV = ?', [req.params.id], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (results.length === 0) {
            return res.status(404).json({ message: 'Không tìm thấy chức vụ' });
        }
        res.json(results[0]);
    });
});

// Thêm chức vụ mới
app.post('/api/chucvu', (req, res) => {
    const { MaCV, TenCV, MoTa } = req.body;
    if (!MaCV || !TenCV) {
        return res.status(400).json({ message: 'Mã và tên chức vụ là bắt buộc' });
    }
    
    executeQuery('INSERT INTO ChucVu (MaCV, TenCV, MoTa) VALUES (?, ?, ?)', 
        [MaCV, TenCV, MoTa], (err, results) => {
            if (err) {
                return res.status(500).json({ error: err.message });
            }
            res.status(201).json({ message: 'Thêm chức vụ thành công', id: MaCV });
    });
});

// Cập nhật chức vụ
app.put('/api/chucvu/:id', (req, res) => {
    const { TenCV, MoTa } = req.body;
    if (!TenCV) {
        return res.status(400).json({ message: 'Tên chức vụ là bắt buộc' });
    }
    
    executeQuery('UPDATE ChucVu SET TenCV = ?, MoTa = ? WHERE MaCV = ?', 
        [TenCV, MoTa, req.params.id], (err, results) => {
            if (err) {
                return res.status(500).json({ error: err.message });
            }
            res.json({ message: 'Cập nhật chức vụ thành công' });
    });
});

// Xóa chức vụ
app.delete('/api/chucvu/:id', (req, res) => {
    executeQuery('DELETE FROM ChucVu WHERE MaCV = ?', [req.params.id], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ message: 'Xóa chức vụ thành công' });
    });
});

// ===== API NHÂN VIÊN =====
// Lấy danh sách nhân viên
app.get('/api/nhanvien', (req, res) => {
    const query = `
        SELECT nv.*, pb.TenPB, cv.TenCV 
        FROM NhanVien nv
        LEFT JOIN PhongBan pb ON nv.MaPB = pb.MaPB
        LEFT JOIN ChucVu cv ON nv.MaCV = cv.MaCV
    `;
    executeQuery(query, [], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

// Lấy thông tin 1 nhân viên
app.get('/api/nhanvien/:id', (req, res) => {
    const query = `
        SELECT nv.*, pb.TenPB, cv.TenCV 
        FROM NhanVien nv
        LEFT JOIN PhongBan pb ON nv.MaPB = pb.MaPB
        LEFT JOIN ChucVu cv ON nv.MaCV = cv.MaCV
        WHERE nv.MaNV = ?
    `;
    executeQuery(query, [req.params.id], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (results.length === 0) {
            return res.status(404).json({ message: 'Không tìm thấy nhân viên' });
        }
        res.json(results[0]);
    });
});

// Thêm nhân viên mới
app.post('/api/nhanvien', upload.single('anhDaiDien'), (req, res) => {
    const { 
        MaNV, HoTen, NgaySinh, GioiTinh, DiaChi, SoDT, 
        Email, NgayVaoLam, MaPB, MaCV, TrangThai 
    } = req.body;
    
    if (!MaNV || !HoTen || !NgayVaoLam) {
        return res.status(400).json({ message: 'Mã NV, Họ tên và Ngày vào làm là bắt buộc' });
    }
    
    // Xử lý ảnh đại diện nếu có
    let anhDaiDienPath = null;
    if (req.file) {
        anhDaiDienPath = req.file.path;
    }
    
    getConnection((err, db) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        
        // Sử dụng transaction để đảm bảo tính toàn vẹn dữ liệu
        db.transaction(Firebird.ISOLATION_READ_COMMITTED, (err, transaction) => {
            if (err) {
                db.detach();
                return res.status(500).json({ error: err.message });
            }
            
            const query = `
                INSERT INTO NhanVien (MaNV, HoTen, NgaySinh, GioiTinh, DiaChi, 
                SoDT, Email, NgayVaoLam, MaPB, MaCV, AnhDaiDien, TrangThai)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            `;
            
            // Đọc file ảnh nếu có
            if (anhDaiDienPath) {
                fs.readFile(anhDaiDienPath, (err, imageData) => {
                    if (err) {
                        transaction.rollback();
                        db.detach();
                        return res.status(500).json({ error: 'Không thể đọc file ảnh' });
                    }
                    
                    transaction.query(query, [
                        MaNV, HoTen, NgaySinh || null, GioiTinh || null, DiaChi || null,
                        SoDT || null, Email || null, NgayVaoLam, MaPB || null, MaCV || null,
                        imageData, TrangThai || 'Đang làm việc'
                    ], (err, result) => {
                        if (err) {
                            transaction.rollback();
                            db.detach();
                            return res.status(500).json({ error: err.message });
                        }
                        
                        transaction.commit((err) => {
                            db.detach();
                            if (err) {
                                return res.status(500).json({ error: err.message });
                            }
                            res.status(201).json({ message: 'Thêm nhân viên thành công', id: MaNV });
                        });
                    });
                });
            } else {
                // Trường hợp không có ảnh
                transaction.query(query, [
                    MaNV, HoTen, NgaySinh || null, GioiTinh || null, DiaChi || null,
                    SoDT || null, Email || null, NgayVaoLam, MaPB || null, MaCV || null,
                    null, TrangThai || 'Đang làm việc'
                ], (err, result) => {
                    if (err) {
                        transaction.rollback();
                        db.detach();
                        return res.status(500).json({ error: err.message });
                    }
                    
                    transaction.commit((err) => {
                        db.detach();
                        if (err) {
                            return res.status(500).json({ error: err.message });
                        }
                        res.status(201).json({ message: 'Thêm nhân viên thành công', id: MaNV });
                    });
                });
            }
        });
    });
});

// Cập nhật nhân viên
app.put('/api/nhanvien/:id', upload.single('anhDaiDien'), (req, res) => {
    const { 
        HoTen, NgaySinh, GioiTinh, DiaChi, SoDT, 
        Email, NgayVaoLam, MaPB, MaCV, TrangThai 
    } = req.body;
    
    if (!HoTen || !NgayVaoLam) {
        return res.status(400).json({ message: 'Họ tên và Ngày vào làm là bắt buộc' });
    }
    
    let anhDaiDienPath = null;
    if (req.file) {
        anhDaiDienPath = req.file.path;
    }
    
    getConnection((err, db) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        
        db.transaction(Firebird.ISOLATION_READ_COMMITTED, (err, transaction) => {
            if (err) {
                db.detach();
                return res.status(500).json({ error: err.message });
            }
            
            // Nếu có cập nhật ảnh
            if (anhDaiDienPath) {
                fs.readFile(anhDaiDienPath, (err, imageData) => {
                    if (err) {
                        transaction.rollback();
                        db.detach();
                        return res.status(500).json({ error: 'Không thể đọc file ảnh' });
                    }
                    
                    const query = `
                        UPDATE NhanVien 
                        SET HoTen = ?, NgaySinh = ?, GioiTinh = ?, DiaChi = ?, 
                            SoDT = ?, Email = ?, NgayVaoLam = ?, MaPB = ?, 
                            MaCV = ?, AnhDaiDien = ?, TrangThai = ?
                        WHERE MaNV = ?
                    `;
                    
                    transaction.query(query, [
                        HoTen, NgaySinh || null, GioiTinh || null, DiaChi || null,
                        SoDT || null, Email || null, NgayVaoLam, MaPB || null, 
                        MaCV || null, imageData, TrangThai || 'Đang làm việc',
                        req.params.id
                    ], (err, result) => {
                        if (err) {
                            transaction.rollback();
                            db.detach();
                            return res.status(500).json({ error: err.message });
                        }
                        
                        transaction.commit((err) => {
                            db.detach();
                            if (err) {
                                return res.status(500).json({ error: err.message });
                            }
                            res.json({ message: 'Cập nhật nhân viên thành công' });
                        });
                    });
                });
            } else {
                // Nếu không cập nhật ảnh
                const query = `
                    UPDATE NhanVien 
                    SET HoTen = ?, NgaySinh = ?, GioiTinh = ?, DiaChi = ?, 
                        SoDT = ?, Email = ?, NgayVaoLam = ?, MaPB = ?, 
                        MaCV = ?, TrangThai = ?
                    WHERE MaNV = ?
                `;
                
                transaction.query(query, [
                    HoTen, NgaySinh || null, GioiTinh || null, DiaChi || null,
                    SoDT || null, Email || null, NgayVaoLam, MaPB || null, 
                    MaCV || null, TrangThai || 'Đang làm việc',
                    req.params.id
                ], (err, result) => {
                    if (err) {
                        transaction.rollback();
                        db.detach();
                        return res.status(500).json({ error: err.message });
                    }
                    
                    transaction.commit((err) => {
                        db.detach();
                        if (err) {
                            return res.status(500).json({ error: err.message });
                        }
                        res.json({ message: 'Cập nhật nhân viên thành công' });
                    });
                });
            }
        });
    });
});

// Lấy ảnh đại diện của nhân viên
app.get('/api/nhanvien/:id/anhdaidien', (req, res) => {
    executeQuery('SELECT AnhDaiDien FROM NhanVien WHERE MaNV = ?', [req.params.id], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (results.length === 0 || !results[0].AnhDaiDien) {
            return res.status(404).json({ message: 'Không tìm thấy ảnh đại diện' });
        }
        
        res.setHeader('Content-Type', 'image/jpeg');
        res.send(results[0].AnhDaiDien);
    });
});

// Xóa nhân viên
app.delete('/api/nhanvien/:id', (req, res) => {
    executeQuery('DELETE FROM NhanVien WHERE MaNV = ?', [req.params.id], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ message: 'Xóa nhân viên thành công' });
    });
});

// ===== API HỢP ĐỒNG =====
// Lấy danh sách hợp đồng
app.get('/api/hopdong', (req, res) => {
    const query = `
        SELECT hd.*, nv.HoTen 
        FROM HopDong hd
        JOIN NhanVien nv ON hd.MaNV = nv.MaNV
    `;
    executeQuery(query, [], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

// Lấy hợp đồng theo nhân viên
app.get('/api/hopdong/nhanvien/:maNV', (req, res) => {
    const query = `
        SELECT * FROM HopDong
        WHERE MaNV = ?
        ORDER BY NgayKy DESC
    `;
    executeQuery(query, [req.params.maNV], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

// Lấy thông tin 1 hợp đồng
app.get('/api/hopdong/:id', (req, res) => {
    const query = `
        SELECT hd.*, nv.HoTen 
        FROM HopDong hd
        JOIN NhanVien nv ON hd.MaNV = nv.MaNV
        WHERE hd.MaHD = ?
    `;
    executeQuery(query, [req.params.id], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (results.length === 0) {
            return res.status(404).json({ message: 'Không tìm thấy hợp đồng' });
        }
        res.json(results[0]);
    });
});

// Thêm hợp đồng mới
app.post('/api/hopdong', upload.single('fileDinhKem'), (req, res) => {
    const { 
        MaHD, MaNV, LoaiHD, SoHD, NgayKy, NgayHieuLuc,
        NgayHetHan, LuongCoBan, NoiDung 
    } = req.body;
    
    if (!MaHD || !MaNV || !NgayKy || !NgayHieuLuc) {
        return res.status(400).json({ 
            message: 'Mã hợp đồng, Mã nhân viên, Ngày ký và Ngày hiệu lực là bắt buộc' 
        });
    }
    
    let fileDinhKemPath = null;
    if (req.file) {
        fileDinhKemPath = req.file.path;
    }
    
    getConnection((err, db) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        
        db.transaction(Firebird.ISOLATION_READ_COMMITTED, (err, transaction) => {
            if (err) {
                db.detach();
                return res.status(500).json({ error: err.message });
            }
            
            if (fileDinhKemPath) {
                fs.readFile(fileDinhKemPath, (err, fileData) => {
                    if (err) {
                        transaction.rollback();
                        db.detach();
                        return res.status(500).json({ error: 'Không thể đọc file đính kèm' });
                    }
                    
                    const query = `
                        INSERT INTO HopDong (MaHD, MaNV, LoaiHD, SoHD, NgayKy, 
                        NgayHieuLuc, NgayHetHan, LuongCoBan, NoiDung, FileDinhKem)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    `;
                    
                    transaction.query(query, [
                        MaHD, MaNV, LoaiHD || null, SoHD || null, NgayKy,
                        NgayHieuLuc, NgayHetHan || null, LuongCoBan || 0, NoiDung || null,
                        fileData
                    ], (err, result) => {
                        if (err) {
                            transaction.rollback();
                            db.detach();
                            return res.status(500).json({ error: err.message });
                        }
                        
                        transaction.commit((err) => {
                            db.detach();
                            if (err) {
                                return res.status(500).json({ error: err.message });
                            }
                            res.status(201).json({ message: 'Thêm hợp đồng thành công', id: MaHD });
                        });
                    });
                });
            } else {
                const query = `
                    INSERT INTO HopDong (MaHD, MaNV, LoaiHD, SoHD, NgayKy, 
                    NgayHieuLuc, NgayHetHan, LuongCoBan, NoiDung)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                `;
                
                transaction.query(query, [
                    MaHD, MaNV, LoaiHD || null, SoHD || null, NgayKy,
                    NgayHieuLuc, NgayHetHan || null, LuongCoBan || 0, NoiDung || null
                ], (err, result) => {
                    if (err) {
                        transaction.rollback();
                        db.detach();
                        return res.status(500).json({ error: err.message });
                    }
                    
                    transaction.commit((err) => {
                        db.detach();
                        if (err) {
                            return res.status(500).json({ error: err.message });
                        }
                        res.status(201).json({ message: 'Thêm hợp đồng thành công', id: MaHD });
                    });
                });
            }
        });
    });
});

// API endpoints cho ChamCong
app.get('/api/chamcong', (req, res) => {
    const query = `
        SELECT cc.*, nv.HoTen 
        FROM ChamCong cc
        JOIN NhanVien nv ON cc.MaNV = nv.MaNV
        ORDER BY cc.NgayChamCong DESC
    `;
    executeQuery(query, [], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

app.get('/api/chamcong/nhanvien/:maNV', (req, res) => {
    const { startDate, endDate } = req.query;
    let query = `
        SELECT * FROM ChamCong
        WHERE MaNV = ?
    `;
    let params = [req.params.maNV];
    
    if (startDate && endDate) {
        query += ` AND NgayChamCong BETWEEN ? AND ?`;
        params.push(startDate, endDate);
    }
    
    query += ` ORDER BY NgayChamCong DESC`;
    
    executeQuery(query, params, (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

app.post('/api/chamcong', (req, res) => {
    const { MaNV, NgayChamCong, GioVao, GioRa, TrangThaiChamCong, GhiChu } = req.body;
    
    if (!MaNV || !NgayChamCong) {
        return res.status(400).json({ message: 'Mã nhân viên và ngày chấm công là bắt buộc' });
    }
    
    // Sử dụng generator để tạo ID tự động 
    const query = `
        INSERT INTO ChamCong (MaNV, NgayChamCong, GioVao, GioRa, TrangThaiChamCong, GhiChu)
        VALUES (?, ?, ?, ?, ?, ?)
        RETURNING MaCC
    `;
    
    executeQuery(query, [
        MaNV, NgayChamCong, GioVao || null, GioRa || null, 
        TrangThaiChamCong || null, GhiChu || null
    ], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.status(201).json({ 
            message: 'Thêm chấm công thành công', 
            id: results[0].MaCC 
        });
    });
});

app.put('/api/chamcong/:id', (req, res) => {
    const { GioVao, GioRa, TrangThaiChamCong, GhiChu } = req.body;
    
    const query = `
        UPDATE ChamCong
        SET GioVao = ?, GioRa = ?, TrangThaiChamCong = ?, GhiChu = ?
        WHERE MaCC = ?
    `;
    
    executeQuery(query, [
        GioVao || null, GioRa || null, TrangThaiChamCong || null, 
        GhiChu || null, req.params.id
    ], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ message: 'Cập nhật chấm công thành công' });
    });
});

// API endpoints cho BangLuong
app.get('/api/bangluong', (req, res) => {
    const { thangNam } = req.query;
    let query = `
        SELECT bl.*, nv.HoTen 
        FROM BangLuong bl
        JOIN NhanVien nv ON bl.MaNV = nv.MaNV
    `;
    let params = [];
    
    if (thangNam) {
        query += ` WHERE bl.ThangNam = ?`;
        params.push(thangNam);
    }
    
    query += ` ORDER BY bl.ThangNam DESC, nv.HoTen ASC`;
    
    executeQuery(query, params, (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

app.get('/api/bangluong/nhanvien/:maNV', (req, res) => {
    const query = `
        SELECT * FROM BangLuong
        WHERE MaNV = ?
        ORDER BY ThangNam DESC
    `;
    executeQuery(query, [req.params.maNV], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

app.post('/api/bangluong', (req, res) => {
    const { 
        MaNV, ThangNam, LuongCoBan, PhuCapChucVu, PhuCapKhac,
        Thuong, BHXH, BHYT, BHTN, ThueTNCN, KhauTruKhac, NgayThanhToan, GhiChu
    } = req.body;
    
    if (!MaNV || !ThangNam) {
        return res.status(400).json({ message: 'Mã nhân viên và tháng năm là bắt buộc' });
    }
    
    // Kiểm tra xem đã có bảng lương cho nhân viên trong tháng này chưa
    executeQuery('SELECT MaLuong FROM BangLuong WHERE MaNV = ? AND ThangNam = ?', 
        [MaNV, ThangNam], (err, results) => {
            if (err) {
                return res.status(500).json({ error: err.message });
            }
            
            if (results.length > 0) {
                return res.status(400).json({ 
                    message: 'Đã tồn tại bảng lương cho nhân viên này trong tháng đã chọn' 
                });
            }
            
            const query = `
                INSERT INTO BangLuong (MaNV, ThangNam, LuongCoBan, PhuCapChucVu, PhuCapKhac,
                Thuong, BHXH, BHYT, BHTN, ThueTNCN, KhauTruKhac, NgayThanhToan, GhiChu)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                RETURNING MaLuong
            `;
            
            executeQuery(query, [
                MaNV, ThangNam, LuongCoBan || 0, PhuCapChucVu || 0, PhuCapKhac || 0,
                Thuong || 0, BHXH || 0, BHYT || 0, BHTN || 0, ThueTNCN || 0, 
                KhauTruKhac || 0, NgayThanhToan || null, GhiChu || null
            ], (err, results) => {
                if (err) {
                    return res.status(500).json({ error: err.message });
                }
                res.status(201).json({ 
                    message: 'Thêm bảng lương thành công', 
                    id: results[0].MaLuong 
                });
            });
    });
});

app.put('/api/bangluong/:id', (req, res) => {
    const { 
        LuongCoBan, PhuCapChucVu, PhuCapKhac, Thuong,
        BHXH, BHYT, BHTN, ThueTNCN, KhauTruKhac, NgayThanhToan, GhiChu
    } = req.body;
    
    const query = `
        UPDATE BangLuong
        SET LuongCoBan = ?, PhuCapChucVu = ?, PhuCapKhac = ?, Thuong = ?,
            BHXH = ?, BHYT = ?, BHTN = ?, ThueTNCN = ?, KhauTruKhac = ?,
            NgayThanhToan = ?, GhiChu = ?
        WHERE MaLuong = ?
    `;
    
    executeQuery(query, [
        LuongCoBan || 0, PhuCapChucVu || 0, PhuCapKhac || 0, Thuong || 0,
        BHXH || 0, BHYT || 0, BHTN || 0, ThueTNCN || 0, KhauTruKhac || 0,
        NgayThanhToan || null, GhiChu || null, req.params.id
    ], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ message: 'Cập nhật bảng lương thành công' });
    });
});

// API endpoints cho NghiPhep
app.get('/api/nghiphep', (req, res) => {
    const { trangThai } = req.query;
    let query = `
        SELECT np.*, nv.HoTen, nd.HoTen as TenNguoiDuyet
        FROM NghiPhep np
        JOIN NhanVien nv ON np.MaNV = nv.MaNV
        LEFT JOIN NhanVien nd ON np.NguoiDuyet = nd.MaNV
    `;
    let params = [];
    
    if (trangThai) {
        query += ` WHERE np.TrangThai = ?`;
        params.push(trangThai);
    }
    
    query += ` ORDER BY np.NgayGuiDon DESC`;
    
    executeQuery(query, params, (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

app.get('/api/nghiphep/nhanvien/:maNV', (req, res) => {
    const query = `
        SELECT np.*, nd.HoTen as TenNguoiDuyet
        FROM NghiPhep np
        LEFT JOIN NhanVien nd ON np.NguoiDuyet = nd.MaNV
        WHERE np.MaNV = ?
        ORDER BY np.NgayGuiDon DESC
    `;
    executeQuery(query, [req.params.maNV], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

app.post('/api/nghiphep', (req, res) => {
    const { 
        MaNV, LoaiNghiPhep, NgayBatDau, NgayKetThuc, LyDo, NgayGuiDon
    } = req.body;
    
    if (!MaNV || !NgayBatDau || !NgayKetThuc) {
        return res.status(400).json({ 
            message: 'Mã nhân viên, ngày bắt đầu và ngày kết thúc là bắt buộc' 
        });
    }
    
    const query = `
        INSERT INTO NghiPhep (MaNV, LoaiNghiPhep, NgayBatDau, NgayKetThuc, LyDo, NgayGuiDon)
        VALUES (?, ?, ?, ?, ?, COALESCE(?, CURRENT_DATE))
        RETURNING MaNP
    `;
    
    executeQuery(query, [
        MaNV, LoaiNghiPhep || null, NgayBatDau, NgayKetThuc, 
        LyDo || null, NgayGuiDon
    ], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.status(201).json({ 
            message: 'Thêm đơn nghỉ phép thành công', 
            id: results[0].MaNP 
        });
    });
});

app.put('/api/nghiphep/:id/duyet', (req, res) => {
    const { TrangThai, NguoiDuyet, NgayDuyet } = req.body;
    
    if (!TrangThai || !NguoiDuyet) {
        return res.status(400).json({ 
            message: 'Trạng thái và người duyệt là bắt buộc' 
        });
    }
    
    const query = `
        UPDATE NghiPhep
        SET TrangThai = ?, NguoiDuyet = ?, NgayDuyet = COALESCE(?, CURRENT_DATE)
        WHERE MaNP = ?
    `;
    
    executeQuery(query, [
        TrangThai, NguoiDuyet, NgayDuyet, req.params.id
    ], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ message: 'Cập nhật trạng thái nghỉ phép thành công' });
    });
});

// API endpoints cho DanhGia
app.get('/api/danhgia', (req, res) => {
    const { kyDanhGia } = req.query;
    let query = `
        SELECT dg.*, nv.HoTen, ndg.HoTen as TenNguoiDanhGia
        FROM DanhGia dg
        JOIN NhanVien nv ON dg.MaNV = nv.MaNV
        LEFT JOIN NhanVien ndg ON dg.NguoiDanhGia = ndg.MaNV
    `;
    let params = [];
    
    if (kyDanhGia) {
        query += ` WHERE dg.KyDanhGia = ?`;
        params.push(kyDanhGia);
    }
    
    query += ` ORDER BY dg.NgayDanhGia DESC`;
    
    executeQuery(query, params, (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

app.get('/api/danhgia/nhanvien/:maNV', (req, res) => {
    const query = `
        SELECT dg.*, ndg.HoTen as TenNguoiDanhGia
        FROM DanhGia dg
        LEFT JOIN NhanVien ndg ON dg.NguoiDanhGia = ndg.MaNV
        WHERE dg.MaNV = ?
        ORDER BY dg.NgayDanhGia DESC
    `;
    executeQuery(query, [req.params.maNV], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

app.post('/api/danhgia', (req, res) => {
    const { 
        MaNV, NguoiDanhGia, KyDanhGia, NgayDanhGia,
        DiemSo, XepLoai, NhanXet, MucTieuKyToi
    } = req.body;
    
    if (!MaNV || !NguoiDanhGia || !KyDanhGia) {
        return res.status(400).json({ 
            message: 'Mã nhân viên, người đánh giá và kỳ đánh giá là bắt buộc' 
        });
    }
    
    const query = `
        INSERT INTO DanhGia (MaNV, NguoiDanhGia, KyDanhGia, NgayDanhGia,
        DiemSo, XepLoai, NhanXet, MucTieuKyToi)
        VALUES (?, ?, ?, COALESCE(?, CURRENT_DATE), ?, ?, ?, ?)
        RETURNING MaDG
    `;
    
    executeQuery(query, [
        MaNV, NguoiDanhGia, KyDanhGia, NgayDanhGia,
        DiemSo || null, XepLoai || null, NhanXet || null, MucTieuKyToi || null
    ], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.status(201).json({ 
            message: 'Thêm đánh giá nhân viên thành công', 
            id: results[0].MaDG 
        });
    });
});

app.put('/api/danhgia/:id', (req, res) => {
    const { 
        DiemSo, XepLoai, NhanXet, MucTieuKyToi
    } = req.body;
    
    const query = `
        UPDATE DanhGia
        SET DiemSo = ?, XepLoai = ?, NhanXet = ?, MucTieuKyToi = ?
        WHERE MaDG = ?
    `;
    
    executeQuery(query, [
        DiemSo || null, XepLoai || null, NhanXet || null, 
        MucTieuKyToi || null, req.params.id
    ], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ message: 'Cập nhật đánh giá thành công' });
    });
});

// === API thống kê báo cáo ===
// Thống kê nhân viên theo phòng ban
app.get('/api/thongke/nhanvien-phongban', (req, res) => {
    const query = `
        SELECT pb.MaPB, pb.TenPB, COUNT(nv.MaNV) as SoLuongNV
        FROM PhongBan pb
        LEFT JOIN NhanVien nv ON pb.MaPB = nv.MaPB AND nv.TrangThai = 'Đang làm việc'
        GROUP BY pb.MaPB, pb.TenPB
        ORDER BY pb.TenPB
    `;
    
    executeQuery(query, [], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

// Thống kê chấm công theo tháng
app.get('/api/thongke/chamcong-thang', (req, res) => {
    const { thang, nam } = req.query;
    
    if (!thang || !nam) {
        return res.status(400).json({ message: 'Tháng và năm là bắt buộc' });
    }
    
    const ngayDauThang = `${nam}-${thang}-01`;
    const ngayCuoiThang = `${nam}-${thang}-${new Date(nam, thang, 0).getDate()}`;
    
    const query = `
        SELECT nv.MaNV, nv.HoTen,
            COUNT(CASE WHEN cc.TrangThaiChamCong = 'Đúng giờ' THEN 1 END) as SoNgayDungGio,
            COUNT(CASE WHEN cc.TrangThaiChamCong = 'Đi trễ' THEN 1 END) as SoNgayDiTre,
            COUNT(CASE WHEN cc.TrangThaiChamCong = 'Về sớm' THEN 1 END) as SoNgayVeSom,
            COUNT(CASE WHEN cc.TrangThaiChamCong = 'Vắng' THEN 1 END) as SoNgayVang,
            COUNT(cc.MaCC) as TongSoNgay
        FROM NhanVien nv
        LEFT JOIN ChamCong cc ON nv.MaNV = cc.MaNV 
            AND cc.NgayChamCong BETWEEN ? AND ?
        WHERE nv.TrangThai = 'Đang làm việc'
        GROUP BY nv.MaNV, nv.HoTen
        ORDER BY nv.HoTen
    `;
    
    executeQuery(query, [ngayDauThang, ngayCuoiThang], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

// Thống kê tổng lương theo tháng
app.get('/api/thongke/luong-thang', (req, res) => {
    const { thangNam } = req.query;
    
    if (!thangNam) {
        return res.status(400).json({ message: 'Tháng năm là bắt buộc (định dạng YYYYMM)' });
    }
    
    const query = `
        SELECT pb.MaPB, pb.TenPB,
            COUNT(bl.MaLuong) as SoNhanVien,
            SUM(bl.LuongCoBan) as TongLuongCoBan,
            SUM(bl.PhuCapChucVu + bl.PhuCapKhac) as TongPhuCap,
            SUM(bl.Thuong) as TongThuong,
            SUM(bl.BHXH + bl.BHYT + bl.BHTN) as TongBaoHiem,
            SUM(bl.ThueTNCN) as TongThue,
            SUM(bl.ThucNhan) as TongThucNhan
        FROM PhongBan pb
        LEFT JOIN NhanVien nv ON pb.MaPB = nv.MaPB
        LEFT JOIN BangLuong bl ON nv.MaNV = bl.MaNV AND bl.ThangNam = ?
        GROUP BY pb.MaPB, pb.TenPB
        ORDER BY pb.TenPB
    `;
    
    executeQuery(query, [thangNam], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

// Thống kê nghỉ phép
app.get('/api/thongke/nghiphep', (req, res) => {
    const { nam } = req.query;
    
    if (!nam) {
        return res.status(400).json({ message: 'Năm là bắt buộc' });
    }
    
    const ngayDauNam = `${nam}-01-01`;
    const ngayCuoiNam = `${nam}-12-31`;
    
    const query = `
        SELECT nv.MaNV, nv.HoTen,
            COUNT(np.MaNP) as TongSoDon,
            SUM(np.SoNgayNghi) as TongSoNgayNghi,
            COUNT(CASE WHEN np.TrangThai = 'Đã duyệt' THEN 1 END) as SoDonDaDuyet,
            COUNT(CASE WHEN np.TrangThai = 'Từ chối' THEN 1 END) as SoDonTuChoi,
            COUNT(CASE WHEN np.TrangThai = 'Chờ duyệt' THEN 1 END) as SoDonChoDuyet
        FROM NhanVien nv
        LEFT JOIN NghiPhep np ON nv.MaNV = np.MaNV 
            AND np.NgayGuiDon BETWEEN ? AND ?
        GROUP BY nv.MaNV, nv.HoTen
        ORDER BY nv.HoTen
    `;
    
    executeQuery(query, [ngayDauNam, ngayCuoiNam], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

// Thống kê đánh giá nhân viên
app.get('/api/thongke/danhgia', (req, res) => {
    const { kyDanhGia } = req.query;
    
    if (!kyDanhGia) {
        return res.status(400).json({ message: 'Kỳ đánh giá là bắt buộc' });
    }
    
    const query = `
        SELECT pb.MaPB, pb.TenPB,
            COUNT(dg.MaDG) as TongSoNV,
            AVG(dg.DiemSo) as DiemTrungBinh,
            COUNT(CASE WHEN dg.XepLoai = 'Xuất sắc' THEN 1 END) as SoNVXuatSac,
            COUNT(CASE WHEN dg.XepLoai = 'Tốt' THEN 1 END) as SoNVTot,
            COUNT(CASE WHEN dg.XepLoai = 'Khá' THEN 1 END) as SoNVKha,
            COUNT(CASE WHEN dg.XepLoai = 'Trung bình' THEN 1 END) as SoNVTrungBinh,
            COUNT(CASE WHEN dg.XepLoai = 'Yếu' THEN 1 END) as SoNVYeu
        FROM PhongBan pb
        LEFT JOIN NhanVien nv ON pb.MaPB = nv.MaPB
        LEFT JOIN DanhGia dg ON nv.MaNV = dg.MaNV AND dg.KyDanhGia = ?
        GROUP BY pb.MaPB, pb.TenPB
        ORDER BY pb.TenPB
    `;
    
    executeQuery(query, [kyDanhGia], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

// === API tìm kiếm ===
// Tìm kiếm nhân viên
app.get('/api/search/nhanvien', (req, res) => {
    const { keyword, phongBan, chucVu, trangThai } = req.query;
    
    let query = `
        SELECT nv.*, pb.TenPB, cv.TenCV 
        FROM NhanVien nv
        LEFT JOIN PhongBan pb ON nv.MaPB = pb.MaPB
        LEFT JOIN ChucVu cv ON nv.MaCV = cv.MaCV
        WHERE 1=1
    `;
    let params = [];
    
    if (keyword) {
        query += ` AND (nv.MaNV LIKE ? OR nv.HoTen LIKE ? OR nv.SoDT LIKE ? OR nv.Email LIKE ?)`;
        const searchTerm = `%${keyword}%`;
        params.push(searchTerm, searchTerm, searchTerm, searchTerm);
    }
    
    if (phongBan) {
        query += ` AND nv.MaPB = ?`;
        params.push(phongBan);
    }
    
    if (chucVu) {
        query += ` AND nv.MaCV = ?`;
        params.push(chucVu);
    }
    
    if (trangThai) {
        query += ` AND nv.TrangThai = ?`;
        params.push(trangThai);
    }
    
    query += ` ORDER BY nv.HoTen`;
    
    executeQuery(query, params, (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});

// Khởi động server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

module.exports = app;