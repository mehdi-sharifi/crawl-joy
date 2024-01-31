import requests
import logging

logger = logging.getLogger(__name__)

def fetch_from_bama(state):
    url = f"https://bama.ir/cad/api/search?region={state}&pageIndex=0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Cookie': 'auth.globalUserContextId=e3b7a6ae-47ff-4c95-85de-96981182bd53; auth.strategy=oidc',
        'Content-Type' : 'application/json; charset=utf-8'
    }
    
    try:
        logger.info(f"Fetching data from Bama API for state: {state}")
        response = requests.get(url=url, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            ads = response.json()["data"]["ads"]
            car_ads_dict = {}
            for ad in ads:
                if ad["type"] == "ad":
                    car_ads_dict[ad["detail"]["code"]] = {
                        "code": ad["detail"]["code"],
                        "url": ad["detail"]["url"],
                        "title": ad["detail"]["title"],
                        "price": ad["price"]["price"],
                        "year": ad["detail"]["year"],
                        "mileage": ad["detail"]["mileage"],
                        "color": ad["detail"]["color"],
                        "body_status": ad["detail"]["body_status"],
                        "modified_date": ad["detail"]["modified_date"],
                    }
            logger.info(f"Data fetched successfully from Bama API for state: {state}")

            return car_ads_dict
        else:
            logger.error(f"Failed to fetch data from Bama API. Status code: {response.status_code}")
            return {}
    except Exception as e:
        logger.error(f"An error occurred in fetch_from_bama: {e}", exc_info=True)
        return {}


def fetch_from_bama_pagination(state):
    url_template = "https://bama.ir/cad/api/search?region={state}&pageIndex={page}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Cookie': 'auth.globalUserContextId=e3b7a6ae-47ff-4c95-85de-96981182bd53; auth.strategy=oidc',
        'Content-Type' : 'application/json; charset=utf-8'
    }

    try:
        car_ads_dict = {}
        page = 1

        while True:
            url = url_template.format(state=state, page=page)
            logger.info(f"Fetching data from Bama API for state: {state}, page: {page}")
            response = requests.get(url=url, headers=headers)
            print(url)

            if response.status_code == 200:
                total_pages = response.json()["metadata"]["total_pages"]
                current_page = response.json()["metadata"]["current_page"]
                ads = response.json()["data"]["ads"]

                for ad in ads:
                    if ad["type"] == "ad":
                        car_ads_dict[ad["detail"]["code"]] = {
                            "code": ad["detail"]["code"],
                            "url": ad["detail"]["url"],
                            "title": ad["detail"]["title"],
                            "price": ad["price"]["price"],
                            "year": ad["detail"]["year"],
                            "mileage": ad["detail"]["mileage"],
                            "color": ad["detail"]["color"],
                            "body_status": ad["detail"]["body_status"],
                            "modified_date": ad["detail"]["modified_date"],
                        }

                logger.info(f"Data fetched successfully from Bama API for state: {state}, page: {page}")

                if current_page >= total_pages:
                    break  # Exit the loop if all pages are fetched
                else:
                    page += 1  # Move to the next page
            else:
                logger.error(f"Failed to fetch data from Bama API. Status code: {response.status_code}")
                break

    except Exception as e:
        logger.error(f"An error occurred in fetch_from_bama: {e}", exc_info=True)

    return car_ads_dict