"""
Main
"""

import argparse
import datetime
from intel import feeds
from db import postgres
from utils import file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Threat Intel ingest and search")
    parser.add_argument("-m", dest="mode", choices=["i", "s"], help="Use 'i' for ingest, 's' for search", required=True)
    parser.add_argument("-f", dest="input_file", help="File with indicators to be searched", required=False)

    args = parser.parse_args()

    mode = args.mode
    input_file = args.input_file

    if mode == "i":
        print("Ingesting feeds and saving them to database")
        feed_data = feeds.pullMaliciousIndicators()
        last_updated = datetime.datetime.now()

        # IPs
        malicious_ips_for_db = []
        for malicious_ip, feed_list in feed_data['ips'].items():
            record = (malicious_ip, list(feed_list), 'IP', last_updated)
            malicious_ips_for_db.append(record)

        postgres.insert_indicators(malicious_ips_for_db)

        # Domains
        malicious_domains_for_db = []
        for malicious_domain, feed_list in feed_data['domains'].items():
            record = (malicious_domain, list(feed_list), 'Domain', last_updated)
            malicious_domains_for_db.append(record)

        postgres.insert_indicators(malicious_domains_for_db)


    elif mode == "s":
        print(f"Searching database based on input file: {input_file}")
        indicators_list = file.read_file(input_file)

        # Utilize the already defined search function to search for the indicators
        for indicator in indicators_list:
            records = postgres.select_indicator(indicator)
            if len(records) > 0:
                # If found, print indicating so and what feed(s) it was in
                print(f"Indicator {indicator} found on database from feed(s) {records[0][1]}")