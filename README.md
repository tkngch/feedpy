feedpy
------


USAGE
=====
> feedpy [-h] [--version] [--crawl] [--build] [--serve]

> optional arguments:
>   -h, --help  show this help message and exit
>   --version   show program's version number and exit
>   --crawl     update the RSS feeds
>   --build     build static pages
>   --serve     crawl and build


DESCRIPTION
===========
**feedpy** is a minimalistic feed aggregator. It aggregates RSS feeds and
generate static html pages. The execution requires a 'feedpy' directory
containing 'feedpy.conf' and 'subscription' in $XDG _ CONFIG _ HOME (often
/home/ _ username _ /.config).
