"""
A script that generates Wikipedia infoboxes for Rfam families.

Usage:
python generate_infobox.py RF00001 RF00002 RF00003
"""

import sys

import pywikibot

from rfam_db import connection


template = """{{{{Infobox rfam
| Name = {rfam_id}
| image = {image}
| width =
| caption = Consensus [[secondary structure]] and [[sequence conservation]] of {description}
| Symbol = {rfam_id}
| AltSymbols =
| Rfam = {rfam_acc}
| miRBase =
| miRBase_family =
| RNA_type = {rna_type}
| Tax_domain =
{go_terms}
{so_terms}
| CAS_number =
| EntrezGene =
| HGNCid =
| OMIM =
| RefSeq =
| Chromosome =
| Arm =
| Band =
| LocusSupplementaryData =
}}}}
"""

def get_image(family):
    commons = pywikibot.Site('commons', 'commons')
    formats = ['{}.svg', '{}.jpg']
    for image_format in formats:
        image = pywikibot.FilePage(commons, title='File:' + image_format.format(family))
        if image.exists():
            return image.title().replace('File:', '')
    return ''

def get_family_metadata(family):
    with connection.cursor() as cursor:
        sql = """select rfam_acc, rfam_id, type as rna_type, description
                 from family
                 where rfam_acc = '{}'"""
        cursor.execute(sql.format(family))
        result = cursor.fetchone()
        return result

def get_go_terms(family):
    terms = []
    with connection.cursor() as cursor:
        sql = "select * from database_link where rfam_acc = '{}' and db_id = 'GO'"
        cursor.execute(sql.format(family))
        for result in cursor.fetchall():
            terms.append(result['db_link'])
    output = []
    for term in terms:
        output.append('{{GO|%s}}' % term)
    return '| GO = {}'.format(','.join(output))

def get_so_terms(family):
    terms = []
    with connection.cursor() as cursor:
        sql = "select * from database_link where rfam_acc = '{}' and db_id = 'SO'"
        cursor.execute(sql.format(family))
        for result in cursor.fetchall():
            terms.append(result['db_link'])
    output = []
    for term in terms:
        output.append('{{SO|%s}}' % term)
    return '| SO = {}'.format(','.join(output))

def get_wiki_rna_type(rna_type):
    mapping = {
        'antisense': '[[Antisense_RNA | antisense]]',
        'antitoxin': '[[Toxin-antitoxin_system | antitoxin]]',
        'CD-box': '[[Small_nucleolar_RNA | snoRNA ]]',
        'Cis-reg': '[[Cis-regulatory element | Cis-reg]]',
        'CRISPR': '[[CRISPR]]',
        'frameshift_element': '[[Translational_frameshift | frameshift element]]',
        'Gene': '[[Gene]]',
        'HACA-box': '[[Small_nucleolar_RNA | snoRNA]]',
        'Intron': '[[Intron]]',
        'IRES': '[[Internal_ribosome_entry_site | IRES]]',
        'leader': '[[Attenuator_(genetics) | leader]]',
        'lncRNA': '[[Long_non-coding_RNA | lncRNA]]',
        'miRNA': '[[MicroRNA | miRNA]]',
        'riboswitch': '[[Riboswitch]]',
        'ribozyme': '[[Ribozyme]]',
        'rRNA': '[[Ribosomal_RNA | rRNA]]',
        'scaRNA': '[[Small_Cajal_body-specific_RNA | scaRNA]]',
        'snoRNA': '[[Small_nucleolar_RNA | snoRNA]]',
        'snRNA': '[[Small_nuclear_RNA | snRNA]]',
        'splicing': '[[RNA_splicing | splicing]]',
        'sRNA': '[[Small_RNA | sRNA]]',
        'thermoregulator': '[[RNA_thermometer | thermoregulator]]',
        'tRNA': '[[tRNA]]',
    }
    output = []
    for entry in rna_type.replace(' ', '').split(';'):
        if entry in mapping:
            output.append(mapping[entry])
    if output:
        return '; '.join(output)
    else:
        return '[[RNA]]'

def get_infobox(family):
    metadata = get_family_metadata(family)
    return template.format(
        rfam_acc=metadata['rfam_acc'],
        rfam_id=metadata['rfam_id'],
        description=metadata['description'],
        rna_type=get_wiki_rna_type(metadata['rna_type']),
        go_terms=get_go_terms(family),
        so_terms=get_so_terms(family),
        image=get_image(family)
    )

def main():
    if len(sys.argv) > 1:
        families = sys.argv[1:]
    else:
        print 'Please specify Rfam accession'
        return

    for family in families:
        print get_infobox(family)


if __name__ == '__main__':
    main()
