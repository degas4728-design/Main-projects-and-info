import httpx
import psycopg2
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from config import DSN
from datetime import datetime
import uuid

def parse_dsn(dsn):
    parts = dsn.replace("postgresql://", "").split("@")
    user_pass = parts[0].split(":")
    host_port_db = parts[1].split("/")
    host_port = host_port_db[0].split(":")
    return {
        'user': user_pass[0],
        'password': user_pass[1],
        'host': host_port[0],
        'port': host_port[1] if len(host_port) > 1 else 5432,
        'database': host_port_db[1]
    }

def extract_image_info(image_bytes):
    try:
        img = Image.open(BytesIO(image_bytes))
        info = {'width': img.width, 'height': img.height, 'capture_date': None}
        if hasattr(img, '_getexif') and img._getexif():
            exif = img._getexif()
            if 306 in exif:
                date_str = exif[306]
                if isinstance(date_str, bytes):
                    date_str = date_str.decode('utf-8')
                info['capture_date'] = date_str
        return info
    except:
        return {'width': None, 'height': None, 'capture_date': None}

def save_image_to_db(conn, session_id, image_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = httpx.get(image_url, headers=headers, timeout=30, follow_redirects=True)
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}")
        
        image_bytes = response.content
        info = extract_image_info(image_bytes)
        
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO scraped_images (session_id, url, image_data, width, height, capture_date, downloaded_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (session_id, image_url, image_bytes, info['width'], info['height'], info['capture_date'], datetime.now()))
        image_id = cur.fetchone()[0]
        
        cur.execute("""
            INSERT INTO download_audit (image_id, session_id, download_status, downloaded_at)
            VALUES (%s, %s, 'success', %s)
        """, (image_id, session_id, datetime.now()))
        conn.commit()
        cur.close()
        
        print(f"    {image_url[:60]}... (ширина={info['width']}, высота={info['height']})")
        return True
    except Exception as e:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO download_audit (image_id, session_id, download_status, error_message, downloaded_at)
            VALUES (0, %s, 'failed', %s, %s)
        """, (session_id, str(e), datetime.now()))
        conn.commit()
        cur.close()
        print(f"    {image_url[:60]}... ({e})")
        return False

def process_page(url, conn, session_id):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    print(f"\n Загружаем страницу: {url}")
    
    try:
        response = httpx.get(url, headers=headers, timeout=30, follow_redirects=True)
        response.raise_for_status()
    except Exception as e:
        print(f" Ошибка загрузки страницы: {e}")
        return 0, 0  
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    
    links = soup.find_all('a', href=True)
    link_count = 0
    for a in links:
        href = urljoin(url, a['href'])
        if urlparse(href).scheme in ('http', 'https'):
            try:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO links (session_id, url, status_code, checked_at)
                    VALUES (%s, %s, %s, %s)
                """, (session_id, href, response.status_code, datetime.now()))
                conn.commit()
                cur.close()
                link_count += 1
            except:
                pass
    print(f" Сохранено ссылок: {link_count}")
    
    
    images = soup.find_all('img', src=True)
    print(f" Найдено изображений: {len(images)}")
    
    image_count = 0
    for img in images:
        img_url = urljoin(url, img['src'])
        if save_image_to_db(conn, session_id, img_url):
            image_count += 1
    
    return link_count, image_count

def main():
    params = parse_dsn(DSN)
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    print("Режимы работы:")
    print("1. Обработать HTML-страницу (найти все ссылки и картинки)")
    print("2. Сохранить одно изображение по прямой ссылке")
    choice = input("Выберите (1/2): ")
    
    if choice == "1":
        url = input("Введите URL страницы: ")
        session_id = str(uuid.uuid4())
        cur.execute("""
            INSERT INTO scraping_sessions (id, target_url, status, started_at)
            VALUES (%s, %s, 'running', %s)
        """, (session_id, url, datetime.now()))
        conn.commit()
        
        link_count, image_count = process_page(url, conn, session_id)
        
        cur.execute("""
            UPDATE scraping_sessions
            SET completed_at = %s, status = 'completed', links_found = %s, images_found = %s
            WHERE id = %s
        """, (datetime.now(), link_count, image_count, session_id))
        conn.commit()
        
        print(f"\n Сессия завершена: ссылок={link_count}, изображений={image_count}")
        
    else:
        image_url = input("Введите прямую ссылку на изображение: ")
        session_id = str(uuid.uuid4())
        cur.execute("""
            INSERT INTO scraping_sessions (id, target_url, status, started_at)
            VALUES (%s, %s, 'running', %s)
        """, (session_id, image_url, datetime.now()))
        conn.commit()
        
        save_image_to_db(conn, session_id, image_url)
        
        cur.execute("""
            UPDATE scraping_sessions
            SET completed_at = %s, status = 'completed', images_found = 1
            WHERE id = %s
        """, (datetime.now(), session_id))
        conn.commit()
        print(f" Сессия завершена")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()