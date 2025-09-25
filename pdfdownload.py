import requests


# Function to download a PDF from a given URL
def download_pdf(pdf_url, save_path):
    # Download the PDF
    response = requests.get(pdf_url, stream=True)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Save the PDF locally
        with open(save_path, "wb") as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)
        print(f"PDF saved successfully as {save_path}!")
    else:
        print(f"Failed to download the PDF. Status code: {response.status_code}")


