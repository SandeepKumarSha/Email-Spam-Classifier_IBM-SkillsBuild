import time
import threading
from app import app
from playwright.sync_api import sync_playwright

def run_flask():
    app.run(port=5050, debug=False, use_reloader=False)

def capture_screenshots():
    # Start Flask server in background thread
    server_thread = threading.Thread(target=run_flask, daemon=True)
    server_thread.start()
    time.sleep(2) # Give server time to spin up

    url = "http://127.0.0.1:5050"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Set viewport to standard full desktop resolution with device scale factor for high crisp quality
        page = browser.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=2)

        # 1. Home page screenshot
        print("Navigating to home page...")
        page.goto(url)
        page.wait_for_selector(".container")
        page.screenshot(path="static/doc_ui_home.png", full_page=True)
        print("Saved doc_ui_home.png")

        # 2. Spam test screenshot
        print("Testing Spam message...")
        page.fill("textarea[name='message']", "Congratulations! You won a free cash prize of ₹50,000. Call to claim now!")
        page.click("button[type='submit']")
        page.wait_for_selector("#prediction-result")
        page.screenshot(path="static/doc_ui_spam_output.png", full_page=True)
        print("Saved doc_ui_spam_output.png")

        # 3. Ham test screenshot
        print("Testing Ham message...")
        page.fill("textarea[name='message']", "Hey, are we still meeting tomorrow for lunch at 1 PM?")
        page.click("button[type='submit']")
        page.wait_for_selector("#prediction-result")
        page.screenshot(path="static/doc_ui_ham_output.png", full_page=True)
        print("Saved doc_ui_ham_output.png")

        browser.close()

if __name__ == "__main__":
    capture_screenshots()
