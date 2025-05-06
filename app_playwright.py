from playwright.sync_api import sync_playwright
import datetime
import time
import json
from dotenv import load_dotenv
from services.form import make_data
import requests
import os

load_dotenv()

class WhatsAppReader:
    def __init__(self, profile_path, target_group):
        self.profile_path = profile_path
        self.target_group = target_group
        self.browser = None
        self.page = None

    def start_browser(self):
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch_persistent_context(
            user_data_dir=self.profile_path,
            headless=False,
            args=["--start-maximized"]
        )
        self.page = self.browser.pages[0]
        self.page.goto("https://web.whatsapp.com")

    def button_presser(self, count):
        rows = self.page.query_selector_all(f'(//div[@role="row"])[position() > last()-{count}]')
        for row in rows:
            button = row.query_selector('div[role="button"]')
            if button:
                button.click()
                break
    
    def get_unread_messages(self, count):
        bubbles = self.page.query_selector_all(f'(//div[@role="row"])[position() > last()-{count}]')
        messages = []

        for i, bubble in enumerate(bubbles, 1):
            text = bubble.inner_text()
            timestamp = datetime.datetime.now().isoformat()
            messages.append({
                "timestamp": timestamp,
                "message": text
            })

        json_output = json.dumps(messages, indent=4, ensure_ascii=False)
        print(json_output)
        return messages

    def run(self):
        try:
            while True:
                try:
                    selector = f'//div[@class="x1n2onr6"][.//span[@title="{self.target_group}"]]//div[@class="_ahlk"]'
                    self.page.wait_for_selector(selector, timeout=60000)
                    unread_div = self.page.query_selector(selector)
                    time.sleep(0.5)

                    if unread_div:
                        group_selector = f'//div[@class="x1n2onr6"]//span[@title="{self.target_group}"]'
                        self.page.click(group_selector)
                        count = int(unread_div.inner_text())
                        self.button_presser(count)
                        message_data = self.get_unread_messages(count)
                        make_data(message_data)
                        self.page.keyboard.press("Escape")
                        time.sleep(1)
                        self.page.keyboard.press("Escape")
                        time.sleep(1)
                        self.page.keyboard.press("Escape")
                        time.sleep(1)
                        self.page.keyboard.press("Escape")
                    else:
                        print("❌ Tidak ditemukan unread message")

                except Exception as e:
                    print(f"❌ Gagal menemukan grup '{self.target_group}': {e}")
                    time.sleep(5)

                time.sleep(5)
        except KeyboardInterrupt:
            print("\n⛔ Dihentikan oleh pengguna. Menutup browser...")
            self.browser.close()

# --- MAIN ---
if __name__ == "__main__":
    reader = WhatsAppReader(
        profile_path=os.getenv('PROFILE_PATH'),
        target_group=os.getenv('TARGET_GROUP'),
    )
    reader.start_browser()
    reader.run()