"""
Script for adding Rfam infoboxes to Wikipedia pages.

Usage:
python pwb.py add_infobox RF03114 RF03115
"""

import sys

import pywikibot

from generate_infobox import get_infobox
from rfam_db import connection


def add_infobox(family):
    site = pywikibot.Site('en', 'wikipedia')
    infobox = get_infobox(family)

    with connection.cursor() as cursor:
        sql = """SELECT title
                 FROM wikitext, family
                 WHERE
                 wikitext.auto_wiki = family.auto_wiki
                 AND family.rfam_acc = '{}'""".format(family)
        cursor.execute(sql)
        result = cursor.fetchone()

    wiki_title = result['title'].decode('utf-8')

    # prevent accidental updating of generic wiki pages
    if 'motif' not in wiki_title or 'motifs' in wiki_title:
        print('Not updating page {}'.format(wiki_title))
        return

    wiki = pywikibot.Page(site, wiki_title)

    if 'Infobox rfam' in wiki.text:
        print('Infobox already exists, not adding a new one')
        return

    wiki.text = infobox + '\n' + wiki.text
    print wiki.text
    wiki.save('Add Rfam infobox', botflag=True)


def main():
    if len(sys.argv) > 1:
        families = sys.argv[1:]
    else:
        print 'Please specify Rfam accession'
        return

    for family in families:
        add_infobox(family)


if __name__ == '__main__':
    main()
