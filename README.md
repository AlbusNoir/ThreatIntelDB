### Threat Intel Database  
---  

Utilizes Python and PostGres to query feeds and indicators for threat intel.  

#### Setup and Installation:  
- Ensure you have Python installed (Python 3.13.5 used in development, Python >= 3.6 is required due to f-strings)  
- Install Docker + Docker Compose or Docker Desktop  
- Clone the repository  
- Create a .env in the root directory of your project file with the following:  
  - PG_DB = "name_of_db"
  - PG_ROOT_PASSWORD = "choose_root_password"
  - PG_USER = "user_name"
  - PG_PASSWORD = "user_password"  
- Edit the volumes in ```compose.yml``` as needed and create directories as needed (whatever volumes you specify need to be created)  
- OPTIONAL: Install some kind of PostGres client (e.g. pgAdmin)  
- Run ```docker compose up -d``` to build and start the container  
- If you have [UV](https://docs.astral.sh/uv/guides/install-python/) installed, run ```uv init``` and ```uv sync``` in whatever directory you're using.  
- If you don't have UV installed, you can create a virtual environment with ```python -m venv name_of_env_here``` and then activate your venv with ```source venv/bin/activate OR venv\Scripts\activate``` and run ```pip install -r requirements.txt```

### Usage:  
For general usage see: ```main.py -h OR --help```  

### Search example:  
Without file: ```main.py -m s your_indicator_here```  
Using file: ```main.py -m s -f ./path/to/your/indicators/file ```  

### Feeds:  
You can utilize the built in feeds or you can choose edit the ```intel/feeds.py``` file with more feeds  
The current feeds built in are:  
```python
ip_feeds = [
        "https://www.binarydefense.com/banlist.txt",
        "https://cinsscore.com/list/ci-badguys.txt",
        "https://lists.blocklist.de/lists/all.txt",
        "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",  # This one is hit or miss. It updates (seemingly) in real time so it may not be consistent
        "https://raw.githubusercontent.com/montysecurity/C2-Tracker/main/data/all.txt",
        "https://rules.emergingthreats.net/blockrules/compromised-ips.txt",
        "https://snort-org-site.s3.amazonaws.com/production/document_files/files/000/041/289/original/ip-filter.blf",
        "https://blocklist.greensnow.co/greensnow.txt",
        "https://threatview.io/Downloads/IP-High-Confidence-Feed.txt",
        # Potentially a list of TOR nodes
        "https://www.dan.me.uk/torlist/?full",
    ]

    domain_feeds = [
        "https://raw.githubusercontent.com/stamparm/blackbook/master/blackbook.txt",
        "https://phishing.army/download/phishing_army_blocklist_extended.txt",
        "https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt",
        # urlabuse.com links are updated every ~5min so results may vary
        "https://urlabuse.com/public/data/malware_url.txt",
        "https://urlabuse.com/public/data/phishing_url.txt",
        "https://urlabuse.com/public/data/hacked_url.txt",
        "https://threatview.io/Downloads/DOMAIN-High-Confidence-Feed.txt",
        "https://raw.githubusercontent.com/tsirolnik/spam-domains-list/master/spamdomains.txt",
    ]
``` 

#### Roadmap:  
  - [ ] Add further functionality for ingestion (e.g. web scrape sites to grab IoCs. Not every site gives a list like the current feeds)
  - [ ] Expand functions to include hashes and emails (starter list: https://bazaar.abuse.ch/export/txt/md5/recent/)
  - [ ] Replace gross line splitting with a proper regex in intel/feeds.py
  - [ ] Add function to add feeds (recreate feeds.py and just expand functionality)