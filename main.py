import requests
from multiprocessing.pool import ThreadPool as Pool
import xlsxwriter


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
    try:
        r = requests.get(url, params, cookies=cookies)
        data = r.json()
        if data['ExactMatchDomain']['IsAvailable']:
            price = data['Products'][0]['PriceInfo']['CurrentPriceDisplay']
        else:
            price = None
        return price
    except Exception as e:
        print("Error")
        return type(e).__name__;


def get_domain_suffix_list():
    url = 'http://data.iana.org/TLD/tlds-alpha-by-domain.txt'
    text = requests.get(url).text
    return list(map(lambda s: s.lower(), text.splitlines()[1:]))


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


def proc(task):
    print("Processing", task[3], "at", task[2])
    price = get_price(task[2], task[3])
    print(price, task[3], "at", task[2])
    return (task[0], task[1], price)


test_domain = '499e55e57a45'
domain_suffix_list = get_domain_suffix_list()
site_list = get_site_list()
print('Total:', len(domain_suffix_list) * len(site_list))
pool = Pool(50)
tasks = [(i, j, site, test_domain + '.' + suffix)
         for i, suffix in enumerate(domain_suffix_list)
         for j, site in enumerate(site_list)]
results = pool.map(proc, tasks)
pool.close()
pool.join()
workbook = xlsxwriter.Workbook('prices.xlsx')
worksheet = workbook.add_worksheet()
for i, site in enumerate(site_list):
    worksheet.write(0, i + 1, site[:site.find('.')] + (site[site.find('/'):] if site.find('/') >= 0 else ''))
for i, suffix in enumerate(domain_suffix_list):
    worksheet.write(i + 1, 0, suffix)
for i, j, price in results:
    worksheet.write(i + 1, j + 1, price)
workbook.close()
