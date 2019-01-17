"""
A script that retrieves all Rfam infoboxes from Wikipedia.

Usage:
python get_all_infoboxes.py
"""


import pywikibot

from rfam_db import get_rfam_wiki_pages


def main():
    site = pywikibot.Site('en', 'wikipedia')

    for page in get_rfam_wiki_pages():
    # for page in ['RsaOG']:
        wiki = pywikibot.Page(site, page)
        flag = 0
        for line in wiki.text.split('\n'):
            if '{{Infobox rfam' in line:
                flag = 1
                print line
            elif line.endswith('LocusSupplementaryData = }}'):
                print line
                flag = 0
                break
            elif flag == 1 and line.startswith('}}'):
                flag = 0
                print '}}'
                break
            elif flag == 1:
                try:
                    print(line)
                except:
                    print('ERROR')


main()
