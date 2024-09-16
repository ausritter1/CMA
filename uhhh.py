import requests
from bs4 import BeautifulSoup

# Function to search LinkedIn
def search_linkedin(name, company):
    query = f"{name} {company} LinkedIn"
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract first LinkedIn result
    for link in soup.find_all('a'):
        url = link.get('href')
        if "linkedin.com/in" in url:
            return url
    return None


# Function to extract job title from LinkedIn profile
def get_job_title(linkedin_url):
    response = requests.get(linkedin_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract job title - This part will depend on LinkedIn's HTML structure
    job_title = soup.find('div', {'class': 'pv-text-details__left-panel'}).find('h2').text
    return job_title


# Example usage
name = "Jamie Woodard"
company = "pres10ventures"
linkedin_url = search_linkedin(name, company)
if linkedin_url:
    job_title = get_job_title(linkedin_url)
    print(f"{name} - {job_title}")
