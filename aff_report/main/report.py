import json
import requests
from .responser import pull_response


def sub_start(date_from, date_to, API_LIST):
    'return sorted json by aff_sub'
    result = {}
    response = {"name": {}}
    try:
        for name, key in API_LIST.items():
            url = f"https://api.hasoffers.com/Apiv3/json?api_key={key}&Target=Affiliate_Report&Method=getConversions&fields[]=Stat.affiliate_info1&fields[]=OfferUrl.name&fields[]=Goal.name&filters[Stat.date][conditional]=BETWEEN&filters[Stat.date][values][]={date_from}&filters[Stat.date][values][]={date_to}&data_start=2021-01-01&hour_offset=-1&limit=50000"
            result[name] = sub_report(url)
            response["name"][name] = {"sourceid": {}}
            for source, aff_sub in result[name].items():
                response["name"][name]["sourceid"][source] = {"affsub": aff_sub}
        return pull_response(True,1,response)
    except:
        return pull_response(False,0,"Bad request (sub_start)")


def sub_report(url):
    'return sorted dict by aff_sub'
    try:
        r = requests.get(url)
        text = json.loads(r.text)
        source = {}
        result = {}
        mostwanted = ["Default", "Deposit", "TestAccount"]  # leads without these statuses will be skip
    except:
        return "Connection to report service lost"

    try:
        for el in text['response']["data"]["data"]:  # sort all leads
            if el["Goal"]["name"] in mostwanted:
                goal = el["Goal"]["name"]
                aff_sub = el["Stat"]["affiliate_info1"]
                offer_url = el["OfferUrl"]["name"][-8:]
                if offer_url not in source:
                    source[offer_url] = {aff_sub: {"Default": 0, "Deposit": 0, "TestAccount": 0}}
                if aff_sub not in source[offer_url]:
                    source[offer_url][aff_sub] = {"Default": 0, "Deposit": 0, "TestAccount": 0}
                if goal not in source[offer_url][aff_sub]:
                    source[offer_url][aff_sub][goal] = 1
                else:
                    source[offer_url][aff_sub][goal] += 1

        for key in source:  # delete all tests
            for i in source[key]:
                test = source[key][i].pop("TestAccount")
                source[key][i]["Default"] -= test
                result[key] = dict(source[key])
                if source[key][i]["Default"] < 1 and source[key][i]["Deposit"] < 1:
                    result[key].pop(i)
    except:
        return pull_response(False,0,"Bad request (sub_report)")
    return result


def geo_start(date_from, date_to, API_LIST):
    'return sorted json by geo '
    result = {}
    response = {"name": {}}
    try:
        for name, key in API_LIST.items():
            url = f"https://api.hasoffers.com/Apiv3/json?api_key={key}&Target=Affiliate_Report&Method=getConversions&fields[]=Country.name&fields[]=Goal.name&filters[Stat.date][conditional]=BETWEEN&filters[Stat.date][values][]={date_from}&filters[Stat.date][values][]={date_to}&data_start=2021-01-01&hour_offset=-1&limit=50000"
            result[name] = geo_report(url)
            response["name"][name] = {"geo": {}}
            for geo, status in result[name].items():
                response["name"][name]["geo"][geo] = status
        return pull_response(True,1,response)
    except:
        return pull_response(False,0,"Bad request (geo_start)")


def geo_report(url):
    'return sorted dict'
    try:
        r = requests.get(url)
        text = json.loads(r.text)
        geo_list = {}
        result = {}
        mostwanted = ["Default", "Deposit", "TestAccount"]  # leads without these statuses will be skip
    except:
        return "Connection to report service lost"

    try:
        for el in text['response']["data"]["data"]:  # sort all leads by geo
            if el["Goal"]["name"] in mostwanted:
                goal = el["Goal"]["name"]
                geo = el["Country"]["name"]
                if geo not in geo_list:
                    geo_list[geo] = {"Default": 0, "Deposit": 0, "TestAccount": 0}
                if goal not in geo_list[geo]:
                    geo_list[geo][goal] = 1
                else:
                    geo_list[geo][goal] += 1

        for key in geo_list:  # delete all tests
            test = geo_list[key].pop("TestAccount")
            geo_list[key]["Default"] -= test
            result[key] = dict(geo_list[key])
            if geo_list[key]["Default"] < 1 and geo_list[key]["Deposit"] < 1:
                result.pop(key)
    except:
        return pull_response(False,0,"Bad request (geo_report)")
    return result