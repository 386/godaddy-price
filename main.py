import requests, sys


def get_price(site='sg.godaddy.com/zh', domain='how-much-is-this-domain-on-godaddy.com', currency='CNY'):
    params = {
        'q': domain,
        'key': 'dpp_search',
        'pc': '',
        'ptl': ''
    }
    cookies = {
        'currency': currency
    }
    url = 'https://' + site + '/domainsapi/v1/search/exact'
    r = requests.get(url, params, cookies=cookies)
    data = r.json()
    if data['ExactMatchDomain']['IsAvailable']:
        return data['Products'][0]['PriceInfo']['CurrentPriceDisplay']
    else:
        return None


def get_domain_suffix_list():
    url = 'http://data.iana.org/TLD/tlds-alpha-by-domain.txt'
    text = requests.get(url).text
    return map(lambda s: s.lower(), text.splitlines()[1:])


def get_site_list():
    return [
        "ar.godaddy.com",
        "au.godaddy.com",
        "be.godaddy.com",
        "be.godaddy.com/fr",
        "br.godaddy.com",
        "ca.godaddy.com",
        "ca.godaddy.com/fr",
        "cl.godaddy.com",
        "co.godaddy.com",
        "dk.godaddy.com",
        "de.godaddy.com",
        "es.godaddy.com",
        "www.godaddy.com/es",
        "fr.godaddy.com",
        "hk.godaddy.com/en",
        "in.godaddy.com",
        "in.godaddy.com/hi",
        "in.godaddy.com/mr",
        "in.godaddy.com/ta",
        "id.godaddy.com",
        "ie.godaddy.com",
        "it.godaddy.com",
        "my.godaddy.com",
        "my.godaddy.com/ms",
        "mx.godaddy.com",
        "nl.godaddy.com",
        "nz.godaddy.com",
        "no.godaddy.com",
        "at.godaddy.com",
        "pk.godaddy.com",
        "pe.godaddy.com",
        "ph.godaddy.com",
        "ph.godaddy.com/fil",
        "pl.godaddy.com",
        "pt.godaddy.com",
        "ch.godaddy.com",
        "sg.godaddy.com",
        "za.godaddy.com",
        "ch.godaddy.com/fr",
        "fi.godaddy.com",
        "se.godaddy.com",
        "ch.godaddy.com/it",
        "tr.godaddy.com",
        "uk.godaddy.com",
        "www.godaddy.com",
        "ve.godaddy.com",
        "vn.godaddy.com",
        "gr.godaddy.com",
        "ru.godaddy.com",
        "ua.godaddy.com",
        "th.godaddy.com",
        "kr.godaddy.com",
        "tw.godaddy.com",
        "sg.godaddy.com/zh",
        "jp.godaddy.com",
        "hk.godaddy.com"
    ]


test_domain = '499e55e57a45'
domain_suffix_list = get_domain_suffix_list()
site_list = get_site_list()
print('\t')
for site in site_list:
    print(site[:site.find('.')] + (site[site.find('/'):] if site.find('/') >= 0 else ''), end='\t')
print()
for suffix in domain_suffix_list:
    print(suffix, end='\t')
    for site in site_list:
        print(get_price(site, test_domain + suffix), end='\t')
        sys.stdout.flush()
    print()
