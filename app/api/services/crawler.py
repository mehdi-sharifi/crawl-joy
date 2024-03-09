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
        response = requests.get(url=url, headers=headers, timeout=10)
    
        if response.status_code == 200:
            ads = response.json()["data"]["ads"]
            status = response.status_code
            reason = response.reason
            
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
                        "state": state
                    }
            logger.info(f"Data fetched successfully from Bama API for state: {state}")
            return ({"status": status, "reason": reason, "ads": car_ads_dict})
        else:
            logger.error(f"Failed to fetch data from Bama API. Status code: {response.status_code}, reason: {reason}")
            return ({"status": status, "reason": reason, "ads": None})
    except requests.Timeout:
        logger.error(f'Request timed out.')
        return ({"status": 408, "reason": "Request Timeout", "ads": None})
    except requests.ConnectionError:
        logger.error(f'Connection error.')
        return ({"status": 503, "reason": "Connection Timeout", "ads": None})
        
    except Exception as e:
        logger.error(f"An error occurred in fetch_from_bama: {e}", exc_info=True)
        return ({"status": 500, "reason": str(e), "ads": None})
    
    