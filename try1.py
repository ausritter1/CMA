import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime


def scrape_events(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    events = []
    event_list = soup.find_all('div', class_='post-listing')

    for event in event_list:
        title = event.find('a', class_='post-title').text.strip()
        link = event.find('a', class_='post-title')['href']
        date = event.find('time', class_='post-date')['datetime']
        description = event.find('div', class_='post-excerpt').text.strip()

        events.append({
            'title': title,
            'link': link,
            'date': date,
            'description': description
        })

    return events


def generate_rss(events, output_file='events.xml'):
    fg = FeedGenerator()
    fg.title('GarysGuide Events')
    fg.link(href='https://www.garysguide.com/events')
    fg.description('Latest events from GarysGuide')

    for event in events:
        fe = fg.add_entry()
        fe.title(event['title'])
        fe.link(href=event['link'])
        fe.description(event['description'])
        fe.pubDate(datetime.fromisoformat(event['date']).strftime('%a, %d %b %Y %H:%M:%S GMT'))

    fg.rss_file(output_file)
    print(f'RSS feed generated: {output_file}')


if __name__ == "__main__":
    url = 'https://www.garysguide.com/events'
    events = scrape_events(url)
    generate_rss(events)
