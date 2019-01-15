"""
Example script that identifies old Sanger URLs in all Wikipedia pages linked from
Rfam families.

Usage: python pwb.py update_sanger_urls
"""


import pywikibot

from rfam_db import get_rfam_wiki_pages


def main():
    site = pywikibot.Site('en', 'wikipedia')

    for page in get_rfam_wiki_pages():
        wiki = pywikibot.Page(site, page)
        if 'rfam.sanger.ac.uk' in wiki.text:
            print(page)
            # wiki.text = wiki.text.replace('rfam.sanger.ac.uk', 'rfam.org')
            # wiki.save('Update Rfam URL', botflag=True)

main()
