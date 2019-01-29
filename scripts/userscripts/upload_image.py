"""
Script for uploading Rfam secondary structure images from Rfam website
to Wikimedia Commons.

Usage:
python pwb.py upload_image RF02925
"""

import os
import sys

from datetime import date


def generate_desc_file(family):
    template = """{{{{Information
|Description=Secondary structure of {rfam_acc} RNA family
|Date={date}
|Source=Rfam
|Author=Rfam
|Permission={{{{PD-because|This image is taken from the [http://rfam.org Rfam database], which is completely in the [ftp://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT/COPYING public domain].}}}}
}}}}
[[Category:Non-coding RNA]]"""
    filename = '{}.desc'.format(family)
    with open(filename, 'w') as f:
        f.write(template.format(rfam_acc=family, date=str(date.today())))
    return filename


def preprocess_image(family):
    svg_web = '{}-web.svg'.format(family)
    svg_final = '{}.svg'.format(family)
    cmd = 'wget -q -O {0} http://rfam.xfam.org/family/{1}/image/rscape'
    os.system(cmd.format(svg_web, family))
    with open(svg_web, 'r') as f_in:
        with open(svg_final, 'w') as f_out:
            flag = 0
            for line in f_in.readlines():
                if 'text1000' in line or 'text1001' in line:
                    continue
                if flag == 0 and '</text>' in line:
                    flag = 1
                    continue
                f_out.write(line)
    os.remove(svg_web)
    return svg_final


def upload_image(family):
    cmd_template = ('python pwb.py upload -abortonwarn -keep -noverify '
                    '-descfile:{desc} -filename:{family}.svg {image}')
    descfile = generate_desc_file(family)
    image = preprocess_image(family)
    cmd = cmd_template.format(desc=descfile, family=family, image=image)
    try:
        print cmd
        os.system(cmd)
    finally:
        os.remove(descfile)
        os.remove(image)


def main():
    if len(sys.argv) > 1:
        families = sys.argv[1:]
    else:
        print 'Please specify Rfam accession'
        return

    for family in families:
        upload_image(family)


if __name__ == '__main__':
    main()
