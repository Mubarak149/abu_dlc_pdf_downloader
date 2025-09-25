# DLCPDFDOWNLOADER
A program to help download pdf from dlc abu web site
## Features
- Input a PDF link to download the file.
- Extract protected links using credentials stored in environment variables.
- Parse the provided URL to construct the full path of the PDF file.
- Download the PDF file and serve it as an attachment.
## Requirements
- Python 3.x
- Flask
- python-dotenv
### Install the required dependencies:
```bash
pip install -r requirements.txt
```
## Setup

1. Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/pdf-downloader-app.git
cd pdf-downloader-app
```
2. Create a `.env` file in the root directory and add your sensitive environment variables:
```
BASE_URL=https://elibrary.abudlc.edu.ng
USERNAME=your_username
PASSWORD=your_password
```
3. Run the application:

```bash
python app.py
```
4. Open your browser and go to `http://127.0.0.1:5000/` to use the app.
## File Structure
```
pdf-downloader-app/
├── app.py                # Main application file
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables for sensitive data
└── templates/
    └── index.html        # HTML form for user input
```
## How It Works
1. **Home Page**: The app renders an HTML form where users can input the PDF link.
2. **Download**: Upon form submission, the app:
   - Extracts the link using the provided credentials (username and password).
   - Parses the URL to generate the full PDF file path.
   - Downloads the PDF and serves it back to the user.
## Error Handling
- If no link is provided, a 400 error will be returned with the message "No link provided!".
- If the link is invalid or protected, a 400 error will be returned with the message "Provided link is not valid or protected!".
- If an unexpected error occurs, a 500 error will be returned with the error message.
