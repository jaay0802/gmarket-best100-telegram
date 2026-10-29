# -*- coding: utf-8 -*-
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

URL = "https://www.gmarket.co.kr/n/best"
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
})

def clean(value):
    return re.sub(r"\s+", " ", value or "").strip()

def product_id(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    for key in ("goodscode", "goodsCode", "itemNo", "itemno"):
        if query.get(key):
            return query[key][0]
    return url.split("#")[0].rstrip("/")

def scrape(html):
    soup = BeautifulSoup(html, "html.parser")
    products, seen = [], set()

    for a in soup.find_all("a", href=True):
        href = urljoin(URL, a["href"])
        parsed = urlparse(href)
        if "gmarket.co.kr" not in parsed.netloc:
            continue
        if "/item" not in parsed.path.lower() and "goodscode=" not in parsed.query.lower():
            continue

        ident = product_id(href)
        if ident in seen:
            continue

        title = clean(a.get("title") or a.get_text(" ", strip=True))
        node = a
        card_text = ""
        for _ in range(7):
            if not node.parent:
                break
            node = node.parent
            if node.name in ("li", "div", "article"):
                txt = clean(node.get_text(" ", strip=True))
                if len(txt) < 1200 and (
                    "판매가" in txt or "쿠폰적용가" in txt or
                    re.search(r"\d[\d,]{2,}\s*원", txt)
                ):
                    card_text = txt
                    break

        if len(title) < 3:
            img = node.find("img") if node else None
            title = clean(img.get("alt", "") if img else "")
        if len(title) < 3 or title in ("바로가기", "더보기", "장바구니", "찜하기"):
            continue

        seen.add(ident)
        prices = re.findall(
            r"(?:판매가|쿠폰적용가|즉시할인가|가격)\s*[:：]?\s*([0-9][0-9,]*)\s*원",
            card_text
        )
        if not prices:
            prices = re.findall(r"([0-9][0-9,]{2,})\s*원", card_text)

        products.append({
            "title": title[:180],
            "price": prices[-1] + "원" if prices else "가격 확인 필요",
            "url": href.split("#")[0],
        })
        if len(products) >= 100:
            break
    return products

def send_message(text):
    response = session.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text, "disable_web_page_preview": True},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError("Telegram 전송 실패: " + str(data))

def split_messages(lines, limit=3600):
    chunks, current = [], ""
    for line in lines:
        candidate = current + ("\n" if current else "") + line
        if len(candidate) > limit and current:
            chunks.append(current)
            current = line
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks

def main():
    if not TOKEN or not CHAT_ID:
        raise RuntimeError("GitHub Secrets에 TELEGRAM_BOT_TOKEN과 TELEGRAM_CHAT_ID를 등록하세요.")

    print("G마켓 베스트 페이지 수집 중...")
    response = session.get(URL, timeout=40)
    response.raise_for_status()
    products = scrape(response.text)

    # 너무 적게 수집된 경우 잘못된 보고서를 보내지 않도록 중단합니다.
    if len(products) < 80:
        raise RuntimeError(
            f"상품을 {len(products)}개만 감지했습니다. G마켓 페이지 구조 변경 또는 접속 제한 가능성이 있어 전송을 중단합니다."
        )

    collected_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"🛒 G마켓 베스트 상품 {len(products)}개",
        f"수집 시각: {collected_at}",
        "※ 페이지에서 감지된 순서 기준입니다. 가격은 옵션·쿠폰 조건에 따라 다를 수 있어요.",
        "",
    ]
    for rank, product in enumerate(products, start=1):
        lines.extend([
            f"{rank}위. {product['title']}",
            f"가격: {product['price']}",
            product["url"],
            "",
        ])

    messages = split_messages(lines)
    for message in messages:
        send_message(message)
        time.sleep(0.4)
    print(f"완료: {len(products)}개 상품을 {len(messages)}개 메시지로 전송했습니다.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("오류:", exc, file=sys.stderr)
        raise
