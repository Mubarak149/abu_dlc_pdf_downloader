from flask import Flask, render_template, request, send_file, jsonify
import os
import pdfdownload
import linkseparate
import linkdetector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Flask app initialization
app = Flask(__name__)

# Read sensitive data from environment variables
BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("MYUSERNAME")
PASSWORD = os.getenv("PASSWORD")


@app.route('/')
def index():
    print(USERNAME)
    print(PASSWORD)
    print(BASE_URL)
    return render_template('index.html')  # Render the form for the user

@app.route('/download', methods=['POST'])
def download_pdf():
    pdf_link = request.form.get('pdf_link')  # Get the input link from the user
    if not pdf_link:
        return jsonify({"error": "No link provided!"}), 400

    try:
        # Extract protected links
        links = linkdetector.extract_link(pdf_link, USERNAME, PASSWORD)
        if not links:
            return jsonify({"error": "Provided link is not valid or protected!"}), 400

        # Parse the base URL and file path
        base_url, file_path = linkseparate.parse_pdf_url(links)

        # Construct the full PDF URL
        pdf_url = f"{base_url}{file_path}"

        # Define the file name for saving locally
        file_name = file_path.split("/")[-1]
        save_path = os.path.join("downloads", file_name)

        # Ensure the downloads directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Download the PDF
        pdfdownload.download_pdf(pdf_url, save_path)

        # Serve the file to the user
        return send_file(save_path, as_attachment=True, download_name=file_name)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
