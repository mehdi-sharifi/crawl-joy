import requests
import logging, os

crawler_api_url = os.environ.get("CRAWLER_API_END_POINT")
notification_api_url = os.environ.get("NOTIFICATION_API_END_POINT")
logging.info(f"{crawler_api_url}, {notification_api_url}")

timeout = 10
state = os.environ.get("STATE")


def notification(baseurl, timeout, state, adsurl, title, year, mileage, price):
    payload = {
        "state": state,
        "url": adsurl,
        "title": title,
        "year": year,
        "mileage": mileage,
        "price": price
    }
    

    try:
        response = requests.post(baseurl, data=payload, timeout=timeout, verify=False)
        if response.status_code == 200:
            logging.info("Successfully send notification")
        else:
            print(response.status_code, response.json())
            logging.warning("Failed to send notification")
            
    except requests.Timeout:
        logging.error(f'Request timed out.')
    except requests.ConnectionError:
        logging.error(f'Connection error.')
    except Exception as e:
        logging.error(f"An error occurred in fetch_from_bama: {e}", exc_info=True)
    
    

def crawl(baseurl, timeout, state):
    payload = {
        "state": state,
    }
    try:
        response = requests.post(baseurl, data=payload, timeout=timeout ,verify=False)
        new_signe = bool(response.json()["new"])
        print(new_signe)
        print(response.json())
    
        if new_signe:
            ads = response.json()["ads"]
            for ad in ads:
                url = ad["url"]
                title = ad["title"]
                price = ad["price"]
                year = ad["year"]
                mileage = ad["mileage"]
                notification(notification_api_url, 10, state, url, title, year, mileage, price)
        logging.info(f"Successfully crwalled the ads form bama for state {state}")
    except requests.Timeout:
        logging.error(f'Request timed out.')
    except requests.ConnectionError:
        logging.error(f'Connection error.')
    except Exception as e:
        logging.error(f"An error occurred in fetch_from_bama: {e}", exc_info=True)

def main():
    crawl(crawler_api_url,timeout, state)


if __name__ == "__main__":
    main()