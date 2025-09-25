import linkdetector
import linkseparate
import pdfdownload
import os
import time
import requests

# Telegram bot token (replace with your bot's token from BotFather)
BOT_TOKEN =os.getenv("BOT_TOKEN")  # Replace with your bot token
CHAT_ID =os.getenv("CHAT_ID")  # Replace with your Telegram chat ID (or group ID)

def send_pdf_with_retry(bot_token, chat_id, file_path, retries=3, delay=5):
    """
    Sends a PDF file to Telegram with retry logic.

    :param bot_token: Telegram bot token
    :param chat_id: Telegram chat ID (or group ID)
    :param file_path: Path to the PDF file
    :param retries: Number of retry attempts
    :param delay: Delay between retries (in seconds)
    """
    for attempt in range(retries):
        try:
            with open(file_path, "rb") as pdf_file:
                files = {"document": pdf_file}
                response = requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendDocument",
                    data={"chat_id": chat_id},
                    files=files,
                )
                if response.status_code == 200:
                    print(f"PDF sent successfully: {file_path}")
                    os.remove(file_path)  # Delete the file after successful send
                    return
                else:
                    print(
                        f"Attempt {attempt + 1} failed: {response.status_code} - {response.text}"
                    )
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(delay)
    print(f"Failed to send PDF after {retries} attempts")
    if os.path.exists(file_path):
        os.remove(file_path)  # Delete the file if retries fail

def main():
    # Base URL and login credentials
    base_url = os.getenv("BASE_URL")
    username = os.getenv("MYUSERNAME")  # Replace with your username
    password = os.getenv("PASSWORD")    # Replace with your password
    page_count = 10  # Number of pages to scrape for PDF links

    # Extract protected links
    links = linkdetector.extract_protected_links(base_url, username, password, page_count)
    print("Links extracted")

    # Process and download each PDF
    for url in links:
        base_url, file_path = linkseparate.parse_pdf_url(url)
        pdf_url = f"{base_url}{file_path}"
        file_name = file_path.split("/")[-1]
        save_path = file_name

        print("Download starting...")
        pdfdownload.download_pdf(pdf_url, save_path)

        if os.path.exists(save_path):
            file_size = os.path.getsize(save_path)
            if file_size > 50 * 1024 * 1024:  # Check file size
                print(
                    f"Error: File size exceeds Telegram's limit (50 MB). Size: {file_size / (1024 * 1024):.2f} MB"
                )
                os.remove(save_path)
                continue

            print(f"Sending {file_name} to Telegram...")
            send_pdf_with_retry(BOT_TOKEN, CHAT_ID, save_path)
        else:
            print(f"File not found: {save_path}")

if __name__ == "__main__":
    main()
