import requests
from bs4 import BeautifulSoup
import time

base_url = "https://www.thivien.net"
author_url = base_url + "/Park-Cheol/author-Om8ldy5_iLX-161ZRT65HA"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_poem_links():
    response = requests.get(author_url, headers=headers)
    if response.status_code != 200:
        print(f"Không thể truy cập trang tác giả, mã lỗi: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    poem_list_div = soup.find('div', class_='poem-group-list')
    if not poem_list_div:
        print("Không tìm thấy danh sách bài thơ")
        return []

    ol = poem_list_div.find('ol')
    if not ol:
        print("Không tìm thấy danh sách <ol>")
        return []

    links = []
    for li in ol.find_all('li'):
        a_tag = li.find('a')
        if a_tag and a_tag.get('href'):
            links.append(base_url + a_tag['href'])
    return links

def get_poem_data(poem_url):
    response = requests.get(poem_url, headers=headers)
    if response.status_code != 200:
        print(f"Không thể truy cập bài thơ {poem_url}, mã lỗi: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Lấy tiêu đề nằm trong div.poem-content > h4 > strong
    title_tag = soup.select_one("div.poem-content h4 strong")
    title = title_tag.text.strip() if title_tag else "Không tìm thấy tiêu đề"

    # Lấy nội dung thơ trong các thẻ p bên trong div.poem-content
    content_div = soup.select_one("div.poem-content")
    if content_div:
        paragraphs = content_div.find_all("p")
        content_lines = []
        for p in paragraphs:
            for br in p.find_all("br"):
                br.replace_with("\n")
            text = p.get_text().strip()
            content_lines.append(text)
        content = "\n\n".join(content_lines)
    else:
        content = "Không tìm thấy nội dung thơ"

    return title, content

def main():
    # Trích xuất tên tác giả từ URL
    author_slug = author_url.replace(base_url, "").split("/")[1]  # 'Chu-Yo-han'
    filename = f"{author_slug}_dataset.txt"

    poem_links = get_poem_links()
    print(f"Tìm thấy {len(poem_links)} bài thơ. Đang tải nội dung...")

    with open(filename, "w", encoding="utf-8") as f:
        for i, link in enumerate(poem_links, 1):
            print(f"Lấy bài thơ {i}: {link}")
            data = get_poem_data(link)
            if data:
                title, content = data
                f.write(f"{i}. {title}\n")
                f.write(content + "\n")
                f.write("="*50 + "\n\n")
            time.sleep(1)  # nghỉ 1 giây tránh request quá nhanh

    print(f"Hoàn thành. Dữ liệu đã lưu vào {filename}")

# def main():
#     poem_links = get_poem_links()
#     total = len(poem_links)
#     print(f"Tìm thấy {total} bài thơ. Đang tải nội dung từ bài 42 đến 81...")

#     # Giới hạn từ bài thơ thứ 42 đến 81 (index 41 đến 80)
#     selected_links = poem_links[13:22]

#     with open("dataset.txt", "w", encoding="utf-8") as f:
#         for i, link in enumerate(selected_links, start=13):
#             print(f"Lấy bài thơ {i}: {link}")
#             data = get_poem_data(link)
#             if data:
#                 title, content = data
#                 f.write(f"{i}. {title}\n")
#                 f.write(content + "\n")
#                 f.write("="*50 + "\n\n")
#             time.sleep(1)  # nghỉ 1 giây tránh request quá nhanh

#     print("Hoàn thành. Dữ liệu đã lưu vào dataset.txt")


if __name__ == "__main__":
    main()





# import requests
# from bs4 import BeautifulSoup
# import time

# base_url = "https://www.thivien.net"
# author_url = base_url + "/Kim-Min-jeong/author-fjc5fzc61BpOjZ3_P4ax3w"

# headers = {
#     "User-Agent": "Mozilla/5.0"
# }

# def get_poem_links():
#     response = requests.get(author_url, headers=headers)
#     if response.status_code != 200:
#         print(f"Không thể truy cập trang tác giả, mã lỗi: {response.status_code}")
#         return []
    
#     soup = BeautifulSoup(response.text, "html.parser")
#     poem_group_divs = soup.find_all('div', class_='poem-group-list')
    
#     if not poem_group_divs:
#         print("Không tìm thấy bất kỳ danh sách bài thơ nào")
#         return []

#     links = []
#     for group_div in poem_group_divs:
#         ol = group_div.find('ol')
#         if not ol:
#             continue
#         for li in ol.find_all('li'):
#             a_tag = li.find('a')
#             if a_tag and a_tag.get('href'):
#                 links.append(base_url + a_tag['href'])

#     return links

# def get_poem_data(poem_url):
#     response = requests.get(poem_url, headers=headers)
#     if response.status_code != 200:
#         print(f"Không thể truy cập bài thơ {poem_url}, mã lỗi: {response.status_code}")
#         return None

#     soup = BeautifulSoup(response.text, "html.parser")

#     title_tag = soup.select_one("div.poem-content h4 strong")
#     title = title_tag.text.strip() if title_tag else "Không tìm thấy tiêu đề"

#     content_div = soup.select_one("div.poem-content")
#     if content_div:
#         paragraphs = content_div.find_all("p")
#         content_lines = []
#         for p in paragraphs:
#             for br in p.find_all("br"):
#                 br.replace_with("\n")
#             text = p.get_text().strip()
#             content_lines.append(text)
#         content = "\n\n".join(content_lines)
#     else:
#         content = "Không tìm thấy nội dung thơ"

#     return title, content

# def main():
#     author_slug = author_url.replace(base_url, "").split("/")[1]
#     filename = f"{author_slug}_dataset.txt"

#     poem_links = get_poem_links()
#     total = len(poem_links)
#     print(f"Tìm thấy {total} bài thơ. Đang tải nội dung...")

#     # Nếu muốn chỉ lấy từ bài 13 đến 22, có thể bật dòng này:
#     poem_links = poem_links[39:40]

#     with open(filename, "w", encoding="utf-8") as f:
#         for i, link in enumerate(poem_links, 39):
#             print(f"Lấy bài thơ {i}: {link}")
#             data = get_poem_data(link)
#             if data:
#                 title, content = data
#                 f.write(f"{i}. {title}\n")
#                 f.write(content + "\n")
#                 f.write("="*50 + "\n\n")
#             time.sleep(1)

#     print(f"Hoàn thành. Dữ liệu đã lưu vào {filename}")

# if __name__ == "__main__":
#     main()
