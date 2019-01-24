Pywikibot for Rfam
==================

This is an Rfam fork of the [Pywikibot](https://github.com/wikimedia/pywikibot)
framework with new scripts for managing [Rfam](http://rfam.org) data on Wikipedia
and Wikimedia Commons.

The Pywikibot framework is a Python library that interfaces with the
`MediaWiki API <https://www.mediawiki.org/wiki/API:Main_page>`_
version 1.14 or higher.

Also included are various general function scripts that can be adapted for
different tasks.

For further information about the library excluding scripts see
the full `code documentation <https://doc.wikimedia.org/pywikibot/>`_.

Quick start
-----------

::

    git clone https://github.com/Rfam/pywikibot.git
    cd core
    git submodule update --init
    python pwb.py script_name

Or to install using PyPI (excluding scripts)
::

    pip install -U setuptools
    pip install pywikibot

Our `installation
guide <https://www.mediawiki.org/wiki/Manual:Pywikibot/Installation>`_
has more details for advanced usage.

Basic Usage
-----------

If you wish to write your own script it's very easy to get started:

::

    import pywikibot
    site = pywikibot.Site('en', 'wikipedia')  # The site we want to run our bot on
    page = pywikibot.Page(site, 'Wikipedia:Sandbox')
    page.text = page.text.replace('foo', 'bar')
    page.save('Replacing "foo" with "bar"')  # Saves the page

Rfam-specific Tasks
-------------------

1. **Upload Rfam secondary structure diagram** to Wikimedia Commons. Note: sharing
the images on Wikimedia Commons makes the files available to Wikipedia projects
in different languages (make sure `upload_to_commons = True` in `user-conf.py`).

::

    python pwb.py upload_image RF03114 RF03115

2. **Create Rfam infobox** to get the code that can be manually added to Wikipedia.

::

    python pwb.py generate_infobox RF03114 RF03115

3. **Add Rfam infobox** to a Wikipedia page (only if it has no infobox already).

::

    python pwb.py add_infobox RF03114 RF03115

4. **Generate Rfam infobox** for a Wikipedia page (need to add to Wikipedia manually).

::

    python pwb.py generate_gallery RT_RNA_motifs

-------------------------------------------------------------------------------------------

For more documentation on pywikibot see `docs <https://doc.wikimedia.org/pywikibot/>`_.

Required external programs
---------------------------

It may require the following programs to function properly:

* `7za`: To extract 7z files
