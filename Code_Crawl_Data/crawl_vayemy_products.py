import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://vayemy.vn/mua/page/{}/"  # Cấu trúc URL phân trang (dùng /page/{})
MAX_PAGES = 4  # Giới hạn số trang tối đa để crawl

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

def extract_products(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []

    # Tìm tất cả các sản phẩm
    product_items = soup.find_all("div", class_="product-small box")
    for item in product_items:
        try:
            title = item.find("p", class_="name product-title woocommerce-loop-product__title").text.strip()
            price = item.find("span", class_="woocommerce-Price-amount amount").text.strip()
            link = item.find("a", class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")["href"]
            image = item.find("img", class_="attachment-woocommerce_thumbnail size-woocommerce_thumbnail")["src"]
            products.append({"Tên sản phẩm": title, "Giá": price, "Liên kết": link, "Hình ảnh": image})
        except Exception as e:
            print(f"Lỗi khi xử lý sản phẩm: {e}")
    
    return products

def save_to_csv(products, filename="products.csv"):
    try:
        with open(filename, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Tên sản phẩm", "Giá", "Liên kết", "Hình ảnh"])
            writer.writeheader()
            writer.writerows(products)
        print(f"Dữ liệu đã được lưu vào file: {filename}")
    except Exception as e:
        print(f"Lỗi khi lưu dữ liệu CSV: {e}")

def main():
    all_products = []
    page = 1

    while page <= MAX_PAGES:
        url = BASE_URL.format(page)
        print(f"Đang tải URL: {url}")
        html = get_html(url)

        if not html:
            print("Không thể tải nội dung. Kết thúc.")
            break

        print("Đang trích xuất sản phẩm...")
        products = extract_products(html)

        if not products:  # Dừng nếu không tìm thấy sản phẩm
            print("Không tìm thấy sản phẩm nào trên trang. Kết thúc.")
            break

        # Lọc sản phẩm trùng lặp
        for product in products:
            if product not in all_products:
                all_products.append(product)

        print(f"Đã tìm thấy {len(products)} sản phẩm trên trang {page}.")
        page += 1
        time.sleep(2)  # Chờ để tránh bị chặn

    save_to_csv(all_products)

if __name__ == "__main__":
    main()