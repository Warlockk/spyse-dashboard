# spyse-dashboard
![Spyse Dashboard](https://i.imgur.com/cCtXCA8.png)

Web-based dashboard for my [spyse.py](https://github.com/zeropwn/spyse.py) library.

"Spyse is a developer of complete DAAS (Data-As-A-Service) solutions for Internet security professionals, corporate and remote system administrators, SSL / TLS encryption certificate providers, data centers and business analysts. All Spyse online solutions are represented by thematic services that have a single platform for collecting, processing and aggregating information." - spyse.com

## Installation
```bash
git clone https://github.com/zeropwn/spyse-dashboard
cd spyse-dashboard
pip3 install -r requirements.txt
```


## Usage

```
python3 app.py
```

The server should now be running on port 5000 (default). You can access the dashboard by navigating to localhost:5000 in your web browser.
Currently there is support for:
* Subdomain lookups
* Domains on IP
* DNS record lookup
* Request headers grabber

In the near future I plan on adding support for the rest of the functions in the spyse library.
