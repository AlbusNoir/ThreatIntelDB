import requests

def get_feed(url, user_agent):
    # we're relying on some sneaky agent spoofing to get around agent checks
    headers = {'User-Agent': user_agent}

    response = requests.get(url, headers=headers)

    try:
        if response.status_code == 200:
            return response.text
        else:
            print(f"HTTP GET returned error: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"Encountered error: {e} while trying attempting to get response")
        return None