"""Utilities for pulling data."""
import requests
import xml.etree.ElementTree as ET
import re


class Site:
    """Class for representing used sites."""

    def __init__(self, location, user, passw):
        """Create site representation."""
        self.location = location
        self.user = user
        self.passw = passw


def oai_index(target):
    """Pull solr index using oai, return as dictionary."""
    # test request if target is reachable, get entire index after
    query_info = requests.get(target + '?fl=PID&indent=on&q=fedora.model:monograph OR fedora.model:periodical&wt=json')
    query_info_json = query_info.json()
    num_found = query_info_json['response']['numFound']
    index = requests.get(target + 'fl=PID&indent=on&q=fedora.model:monograph OR fedora.model:periodical&wt=json&rows=' + str(num_found))
    indexdict = index.json()
    return indexdict


def fedora_record_identif(target, user, passw, uuid):
    """Request xml object using uuid and attempt to extract system number."""
    r = requests.get(target + uuid + '/objectXML', auth=requests.auth.HTTPBasicAuth(user, passw))
    if r.status_code != 200:
        print("Something went wrong... (error code: ", r.status_code, ")")
    try:
        root = ET.fromstring(r.content)

        for element in root.iter():
            if element.tag == '{http://www.loc.gov/mods/v3}recordIdentifier':
                if re.match(r'\d\d\d\d\d\d\d\d\d', element.text):
                    print("Sysno found: ", element.text)
                    return element.text
    except ET.ParseError as err:
        print("Unable to parse xml...")
        print("Reason: \n", err)
    print("Sysno not found...")
    return None
