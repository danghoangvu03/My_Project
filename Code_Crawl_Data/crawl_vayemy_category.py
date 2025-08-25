import requests
from bs4 import BeautifulSoup
import csv

URL = "https://vayemy.vn/"  # URL của trang web

def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Lỗi khi tải trang: {response.status_code}")
            return None
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        return None

def extract_categories(html):
    soup = BeautifulSoup(html, "html.parser")
    categories = []

    # Tìm tất cả các danh mục
    category_items = soup.find_all("div", class_="product-category col")
    for item in category_items:
        try:
            # Lấy tên danh mục
            title = item.find("h5", class_="uppercase header-title").text.strip()

            # Lấy số lượng sản phẩm (nếu có)
            count_tag = item.find("p", class_="is-xsmall uppercase count")
            count = count_tag.text.strip() if count_tag else "Không rõ"

            # Lấy liên kết danh mục
            link = item.find("a")["href"]

            # Lấy hình ảnh minh họa
            image = item.find("img")["src"]

            # Thêm danh mục vào danh sách
            categories.append({
                "Tên danh mục": title,
                "Số sản phẩm": count,
                "Liên kết": link,
                "Hình ảnh": image
            })
        except Exception as e:
            print(f"Lỗi khi xử lý danh mục: {e}")
    
    return categories

def save_to_csv(categories, filename="categories.csv"):
    try:
        with open(filename, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Tên danh mục", "Số sản phẩm", "Liên kết", "Hình ảnh"])
            writer.writeheader()
            writer.writerows(categories)
        print(f"Dữ liệu danh mục đã được lưu vào file: {filename}")
    except Exception as e:
        print(f"Lỗi khi lưu dữ liệu CSV: {e}")

def main():
    print(f"Đang tải URL: {URL}")
    html = get_html(URL)

    if not html:
        print("Không thể tải nội dung. Dừng.")
        return

    print("Đang trích xuất danh mục...")
    categories = extract_categories(html)

    if not categories:
        print("Không tìm thấy danh mục nào. Dừng.")
        return

    print(f"Đã tìm thấy {len(categories)} danh mục.")
    save_to_csv(categories)

if __name__ == "__main__":
    main()