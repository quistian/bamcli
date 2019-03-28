# bamcli

bamcli is a CLI (Command Line Interface) to
BAM (BlueCat Address Manager). It uses the
BAM Python API.

  DNS data can be created/deleted/changed and viewed
  via this intereface.

  At the present time bulk operations are managed
  by creating a file of bamcli commands and reading
  the file into the shell

Usage:

  $ pip install --editable .
  $ bam view french.utoronto.ca [RR-type] [RR-value] [TTL]
  $ bam view french.utoronto.ca TXT
  $ bam view french.utoronto.ca TXT
