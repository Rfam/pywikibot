"""
Script for generating Rfam galleries for Wikipedia pages referring to more than
one Rfam family.

Usage:
python pwb.py generate_gallery RT_RNA_motifs
"""

import sys

from rfam_db import connection


def get_gallery(wiki):
    gallery_template = """{{{{Navbox
| name = hide the gallery
| title = Gallery of {gallery_name}
| titlestyle = background:#e7dcc3
| state = autocollapse
| list1  = {{{{Gallery
| lines=5
{families}
}}}}
}}}}"""

    image_line_template = "| Image:{rfam_acc}.svg|'''{rfam_id}''' Secondary structure taken from the [http://rfam.org Rfam] database. Family [http://rfam.org/family/{rfam_acc} {rfam_acc}]"

    with connection.cursor() as cursor:
        sql = """select rfam_acc, rfam_id
                from family t1, wikitext t2
                where t1.`auto_wiki` = t2.`auto_wiki`
                and title = '{}'
                order by rfam_id""".format(wiki)
        cursor.execute(sql)
        results = cursor.fetchall()

    families = []
    for result in results:
        families.append(image_line_template.format(rfam_acc=result['rfam_acc'], rfam_id=result['rfam_id']))

    gallery_name = wiki.replace('_', ' ').replace('-', ' ')
    image_lines = '\n'.join(families)
    return gallery_template.format(gallery_name=gallery_name, families=image_lines)


def main():
    if len(sys.argv) > 1:
        wiki_pages = sys.argv[1:]
    else:
        print 'Please specify a Wiki page'
        return

    for wiki_page in wiki_pages:
        gallery = get_gallery(wiki_page)
        print(gallery)


if __name__ == '__main__':
    main()
