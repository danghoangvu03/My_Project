import pandas as pd

# Đọc file CSV
df = pd.read_csv("products.csv")

# Tạo cột ID từ liên kết
df.insert(0, 'ID', df['Liên kết'].str.extract(r'chi-tiet/([^\/^-]+)')[0].str.upper())

# Lưu file mới
df.to_csv("sanpham_with_id.csv", index=False)

print("✅ Đã tạo file mới: sanpham_with_id.csv có thêm cột ID.")
