#!/usr/bin/env python3

from flask import Flask, render_template, request
from spyse.spyse import spyse
import requests

s = spyse()
app = Flask(__name__)

def get_headers(target):
    r = requests.get("https://api.hackertarget.com/httpheaders/?q={}".format(target))
    return(r.text)

def get_subdomains(target, param, page, raw=False):
    retval = ""
    data = s.subdomains_aggregate(target, param=param, page=page)['cidr']
    keys = data.keys()
    for key in keys:
        domains = data[key]['results']
        for d in domains:
            domain = d['data']['domains']
            if len(domain) > 1:
                for i in domain:
                    retval += "{}\n".format(i)
                else:
                    retval += "{}\n".format(domain[0])
    return retval

def get_dns_ptr(target, param, page, raw=False):
    data = s.dns_ptr(target, param=param, page=1)
    retval = ""
    for record in data['records']:
        retval += "PTR RECORD @ {} FROM HOSTNAME {}\n".format(
        record['ip']['ip'],
        record['hostname']
        )
    return retval


def get_dns_soa(target, param, page, raw=False):
    data = s.dns_soa(target, param=param, page=1)
    retval = ""
    for record in data['records']:
        retval += "SOA RECORD @ {} FROM {} WITH SERIAL {}\n".format(
        record['domain']['domain'],
        record['domain']['ip']['ip'],
        record['serial']
        )
    return retval

def get_dns_mx(target, param, page, raw=False):
    data = s.dns_mx(target, param=param, page=1)
    retval = ""
    for record in data['records']:
        retval += "MX RECORD @ {} FROM IP {}\n".format(
        record['mx_domain']['domain'],
        record['mx_domain']['ip']['ip']
        )
    return retval

def get_dns_aaaa(target, param, page, raw=False):
    data = s.dns_aaaa(target, param=param, page=1)
    retval = ""
    for record in data['records']:
        retval += "AAAA RECORD @ {} FROM IP {}\n".format(
        record['domain']['domain'],
        record['ipv6']
        )
    return retval

def get_dns_ns(target, param, page, raw=False):
    data = s.dns_ns(target, param=param, page=1)
    retval = ""
    for record in data['records']:
        retval += "NS RECORD @ {} FROM {}\n".format(
        record['ns_domain']['domain'],
        record['ns_domain']['ip']['ip']
        )
    return retval

def get_dns_a(target, param, page, raw=False):
    data = s.dns_a(target, param=param, page=1)
    retval = ""
    for record in data['records']:
        retval += "A RECORD @ {} FROM {}\n".format(
        record['domain']['domain'],
        record['ip']['ip']
        )
    return retval

def get_dns_txt(target, param, page, raw=False):
	data = s.dns_txt(target, param=param, page=1)
	retval = "TXT RECORDS FROM {}\n".format(target)
	for record in data['records']:
		retval += '> {}\n'.format(record['data'])
	return retval

def get_dns_all(target, param, raw=False):
    data = ""
    data += get_dns_ptr(target, param=param, page=None)
    data += get_dns_soa(target, param=param, page=None)
    data += get_dns_mx(target, param=param, page=None)
    data += get_dns_aaaa(target, param=param, page=None)
    data += get_dns_a(target, param=param, page=None)
    data += get_dns_ns(target, param=param, page=None)
    data += get_dns_txt(target, param=param, page=None)
    return data

def get_domains_on_ip(target, param, page, raw=False):
    retval = ""
    data = s.domains_on_ip(target, param=param, page=page)
    for record in data['records']:
        retval += "{}\n".format(record['domain'])
    return retval


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target = ""
        if request.form.get('lookupfunc') and request.form.get('target'):
            lookupfunc = request.form.get('lookupfunc')
            if lookupfunc == 'subdomains':
                page = 1
                if request.form.get('param'):
                    param = request.form.get('param')
                    target = request.form.get('target')
                    subdomains = get_subdomains(target, param, page)
                    return render_template('index.html', target=subdomains)
            if lookupfunc == 'dnslookup':
                if request.form.get('param'):
                    param = request.form.get('param')
                    target = request.form.get('target')
                    dnsresults = get_dns_all(target, param)
                    return render_template('index.html', target=dnsresults)
                return render_template('index.html')
            if lookupfunc == 'domainsonip':
                page = 1
                if request.form.get('param'):
                    param = request.form.get('param')
                    target = request.form.get('target')
                    domainsonip = get_domains_on_ip(target, param, page)
                    return render_template('index.html', target=domainsonip)
                return render_template('index.html')
            if lookupfunc == 'getheaders':
                target = request.form.get('target')
                headers = get_headers(target)
                return render_template('index.html', target=headers)
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
