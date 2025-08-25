import csv

# Đọc file CSV, xử lý dữ liệu và ghi lại kết quả vào file mới
input_file = 'sanpham_with_id.csv'  # Tên file input
output_file = 'sanpham_with_cleaned_names.csv'  # Tên file output mới

# Mở file CSV đầu vào để đọc
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    
    # Lấy danh sách các trường trong file CSV
    fieldnames = reader.fieldnames
    
    # Mở file CSV đầu ra để ghi
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Lặp qua từng dòng trong file CSV
        for row in reader:
            # Loại bỏ ID ở đầu tên sản phẩm (giả sử ID có dạng "EMXXXX")
            # Sử dụng phương thức split để cắt chuỗi theo khoảng trắng và lấy phần còn lại
            row['Tên sản phẩm'] = ' '.join(row['Tên sản phẩm'].split()[1:])
            
            # Ghi lại dòng sau khi đã xử lý
            writer.writerow(row)

print("Đã xử lý và tạo file mới: sanpham_with_cleaned_names.csv")
