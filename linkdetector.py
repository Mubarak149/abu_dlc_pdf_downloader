import requests
from bs4 import BeautifulSoup

def extract_protected_links(base_url, username, password, page_count):
    """
    Logs into the website and extracts specific links from protected pages.

    Parameters:
        base_url (str): The base URL of the website.
        username (str): The username for login.
        password (str): The password for login.
        page_count (int): The number of pages to iterate through.

    Returns:
        list: A list of extracted links.
    """
    # Create a session object
    session = requests.Session()

    # Step 1: Get the login page to retrieve the authenticity token
    login_page = session.get(f"{base_url}/login")
    if login_page.status_code != 200:
        print("Failed to access the login page.")
        return []

    login_soup = BeautifulSoup(login_page.text, 'html.parser')

    # Retrieve the authenticity token
    auth_token = login_soup.find("input", {"name": "authenticity_token"})
    if not auth_token:
        print("Failed to retrieve authenticity token.")
        return []

    auth_token = auth_token["value"]

    # Step 2: Prepare the login payload
    login_payload = {
        "authenticity_token": auth_token,
        "username": username,
        "password": password,
        "commit": "Log in"
    }

    # Step 3: Post the login data to the login endpoint
    login_response = session.post(f"{base_url}/user_sessions", data=login_payload)

    # Check if login was successful
    if login_response.status_code == 200 and "Logout" in login_response.text:
        print("Login successful!")

        # Step 4: Access the protected pages and extract links
        extracted_links = []
        for count in range(1, page_count + 1):
            protected_page = session.get(f"{base_url}/books/{count}")
            if protected_page.status_code == 200:
                soup = BeautifulSoup(protected_page.text, 'html.parser')

                # Find the specific link
                link = soup.find("a", class_="button danger", string="Read")
                if link:
                    # Get the full URL for the href
                    full_url = base_url + link["href"]
                    extracted_links.append(full_url)
                else:
                    print(f"No 'Read' link found on page {count}.")
            else:
                print(f"Failed to access page {count}. Status code: {protected_page.status_code}")

        return extracted_links
    else:
        print("Login failed. Please check your credentials.")
        return []

def extract_link(pdf_url, username, password):
    """
    Logs into the /dlc elibrary website and extracts specific links from protected pages.

    Parameters:
        base_url (str): The base URL of the website.
        username (str): The username for login.
        password (str): The password for login.

    Returns:
        list: A list of extracted links.
    """
    base_url = "https://elibrary.abudlc.edu.ng"
    # Create a session object
    session = requests.Session()

    # Step 1: Get the login page to retrieve the authenticity token
    login_page = session.get(f"{base_url}/login")
    if login_page.status_code != 200:
        print("Failed to access the login page.")
        return []

    login_soup = BeautifulSoup(login_page.text, 'html.parser')

    # Retrieve the authenticity token
    auth_token = login_soup.find("input", {"name": "authenticity_token"})
    if not auth_token:
        print("Failed to retrieve authenticity token.")
        return []

    auth_token = auth_token["value"]

    # Step 2: Prepare the login payload
    login_payload = {
        "authenticity_token": auth_token,
        "username": username,
        "password": password,
        "commit": "Log in"
    }

    # Step 3: Post the login data to the login endpoint
    login_response = session.post(f"{base_url}/user_sessions", data=login_payload)

    # Check if login was successful
    if login_response.status_code == 200 and "Logout" in login_response.text:
        print("Login successful!")
        # Step 4: Access the protected pages and extract links
        protected_page = session.get(pdf_url)
        if protected_page.status_code == 200:
            soup = BeautifulSoup(protected_page.text, 'html.parser')
            # Find the specific link
            link = soup.find("a", class_="button danger", string="Read")
            if link:
                # Get the full URL for the href
                full_url = base_url + link["href"]
                
                return full_url
        else:
            print(f"Failed to access page. Status code: {protected_page.status_code}")
    else:
        print("Login failed. Please check your credentials.")
        return []
    
