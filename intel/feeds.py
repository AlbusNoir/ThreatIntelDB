"""
Feeds driver

Take in feeds (ip and domain)
Using totally_legit_useragent™ get the content
Map it into the database
"""
from utils import http

def pullMaliciousIndicators():
    totally_legit_useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

    ip_feeds = [
        "https://www.binarydefense.com/banlist.txt",
        "https://cinsscore.com/list/ci-badguys.txt"
    ]

    domain_feeds = [
        "https://raw.githubusercontent.com/stamparm/blackbook/master/blackbook.txt",
        "https://phishing.army/download/phishing_army_blocklist_extended.txt"
    ]

    combined_map = {}
    combined_map['ips'] = {}
    combined_map['domains'] = {}

    for ip_feed in ip_feeds:
        ip_feed_data = http.get_feed(ip_feed, totally_legit_useragent)
        if ip_feed_data is None:
            # If a feed is empty, we don't want to just quit
            print(f"No feed data returned for IP feed: {ip_feed}")
            continue

        # Now we want to loop through and get only the actual IPs. This will likely be better done as a regex in the future, but it's PoC right now so eh.
        for line in ip_feed_data.split('\n'):
            if line.startswith('#') or line == '':
                continue

            # Check that the IoC isn't already in the map, if it's not, put it in a sec (to prevent duplicates)
            if line not in combined_map['ips']:
                combined_map['ips'][line] = set()

            combined_map['ips'][line].add(ip_feed)

    # Now we do the same thing for the domain feeds
    for domain_feed in domain_feeds:
        domain_feed_data = http.get_feed(domain_feed, totally_legit_useragent)
        if domain_feed_data is None:
            # If a feed is empty, we don't want to just quit
            print(f"No feed data returned for domain feed: {domain_feed}")
            continue

        # Now we want to loop through and get only the actual domains. This will likely be better done as a regex in the future, but it's PoC right now so eh.
        for line in domain_feed_data.split('\n'):
            if line.startswith('#') or line == '':
                continue

            # Check that the IoC isn't already in the map, if it's not, put it in a sec (to prevent duplicates)
            if line not in combined_map['domains']:
                combined_map['domains'][line] = set()

            combined_map['domains'][line].add(domain_feed)

    return combined_map
