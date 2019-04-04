## bamcli

bamcli is a CLI (Command Line Interface) to BAM (BlueCat Address Manager). It uses the BAM Python API.

## Installation

Download the source code from Github:

<pre><code>
$ git clone https://github.com/quistian/bamcli.git
</code></pre>

Set up a Python3 virtual environment for bamcli to run in:

<pre><code>
$ cd bamcli
$ python3 -m venv `pwd`/venv
$ . venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install click requests
(venv) $ pip install --editable .
</code></pre>

Customize your Unix shell (this documentation assumes /bin/sh, /bin/bash or /bin/zsh) environment to set the BAM URL, Username and Password.

<pre><code>
(venv) $ cat .example_bamrc
export BAM_USER=fred
export BAM_PW='Flintstones_R_4ever!'
export BAM_API_URL='https://bam.bigcorp.ca/Services/REST/v1/'

(venv) $ mv .example_bamrc .bamrc
(venv) $ vi .bamrc
(venv) $ . .bamrc
</code></pre>

The BAM CLI interface will not work with out these SHELL variables being set which serve as your credentials to the BAM.

When finished with the bamcli session, you can exit the Python virtual environment as follows:

<pre><code>
(venv) $ deactivate
$
</code></pre>


## Description

The CLI operates on one's DNS data Resource Records (RR) using four commands or actions:

* add
* delete
* update
* view

At present the CLI understands four types of DNS Resource Records:

* A records for mapping IP addresses
* CNAME records for creating aliases
* TXT records for adding text based information
* MX records for mail exchanger data

The general bamcli syntax is as follows:

<pre><code>
<b>bamcli</b> <i>action</i> <i>fqdn</i> <i>RR_type</i> <i>value[,value,value]</i> [<i>ttl</i>]
</code></pre>

Where: <br>

<i>action</i> is one of the above mentioned four editing operators:

* add -> adds RRs to the DNS zone. For A records multiple values are permitted.
* delete/remove -> deletes RRs from the DNS zone. Like A records, multiple values are permitted.
* update -> updates the values of a given fqdn. All existing data is effectively deleted
* view/list -> shows the current state of the DNS data

* <i>fqdn</i> is the Fully Qualified Domain Name of the RR.

* <i>RR_type</i> is one of: A, CNAME, TXT, MX
 
* <i>value</i> is the data associated with the respective FQDN and RRtype.

<pre><code>
Note: For TXT records the value must be surrounded by single or double quotes.
      For MX records the priority is optional and should be given after the value, separated by a comma.
      The default priority is 10.
      
      E.g.
      bamcli add txt.zip.bigcorp.ca TXT 'Sam I am!'
      bamcli add mx.zip.bigcorp.ca MX mailer.zip.bigcorp.ca
      bamcli add mx.zip.bigcorp.ca MX secondary.zip.bigcorp.ca:20
</code></pre>

## Examples

<h3> Adding Resource Records</h3>
  
First we shall ADD some data to our zone: zip.bigcorp.ca to our network: 10.10.0.0/24

<pre><code>
(venv) $ bamcli add red.zip.bigcorp.ca  A 10.10.0.100
(venv) $ bamcli add blue.zip.bigcorp.ca A 10.10.10.10
(venv) $ bamcli add blue.zip.bigcorp.ca A 10.10.2.2
(venv) $ bamcli add zip.bigcorp.ca A 10.10.11
(venv) $ bamcli add smtp.zip.bigcorp.ca A 10.10.25.25
(venv) $ bamcli add rouge.zip.bigcorp.ca CNAME red.zip.bigcorp.ca
(venv) $ bamcli add note.zip.bigcorp.ca TXT "Superman and Batman"
(venv) $ bamcli add zip.bigcorp.ca MX 10,smtp.zip.bigcorp.ca
</code></pre>

Records can also be added to the top level:

<pre><code>
(venv) $ bamcli add zip.bigcorp.ca MX 10,smtp.zip.bigcorp.ca
(venv) $ bamcli add zip.bigcorp.ca A 10.10.1.1
</code></pre>

Time to Live values can be assigned on a per RR basis (the default being 86400 seconds/1 day) by adding a numeric value as the last argument:

<pre><code>
(venv) $ bamcli add tmp.zip.bigcorp.ca A 10.10.7.7 3600
</code></pre>

<h3> Updating DNS data </h3>

The <i>update</i> action is similar in function to deleting all values associated with a FQDN of a given RRtype and then replacing them with the new ones given.

E.g.

<pre><code>
(venv) $ bamcli update zip.bigcorp.ca. A 10.10.10.1,10.10.10.2
Updated RR as follows:
zip.bigcorp.ca  IN  A  10.10.10.1
zip.bigcorp.ca  IN  A  10.10.10.2
</code></pre>

Will remove any and all A records associated with zip.bigcorp.ca and add two new one. The result will be:

<pre><code>
(venv) $ bamcli view zip.bigcorp.ca A
zip.bigcorp.ca  IN  A  10.10.10.1
zip.bigcorp.ca  IN  A  10.10.10.2
</code></pre>

The update action can be used to change the Time To Live (TTL) value for a given RR.

E.g.

<pre><code>
(venv) $ bamcli view zip.bigcorp.ca A
zip.bigcorp.ca  IN  A  10.10.10.1

(venv) $ bamcli update zip.bigcorp.ca A 10.10.10.1 3600
Updated RR as follows:
zip.bigcorp.ca  IN  3600 A  10.10.10.1
(venv) $ bamcli view zip.bigcorp.ca A
zip.bigcorp.ca  IN  3600 A  10.10.10.1
</code></pre>

<h3> Viewing DNS data </h3>

Now we can VIEW the data we have added. To see the entire zone use the top level domain name followed by a dot. (The output is in BIND format).



<pre><code>
(venv) $ bamcli view zip.bigcorp.ca<b>.</b>
zip.bigcorp.ca       IN       A      10.10.1.1
zip.bigcorp.ca       IN       MX     10 smtp.zip.bigcorp.ca
blue.zip.bigcorp.ca  IN       A      10.10.10.10
blue.zip.bigcorp.ca  IN       A      10.10.2.2
red.zip.bigcorp.ca   IN       A      10.10.0.100
tmp.zip.bigcorp.ca   IN  3600 A      10.10.7.7
rouge.zip.bigcorp.ca IN       CNAME  red.zip.bigcorp.ca
note.zip.bigcorp.ca  IN       TXT    "Superman and Batman"
</code></pre>

To see only the data at the top of the zone drop the trailing dot:

<pre><code>
(venv) $ bamcli view zip.bigcorp.ca
zip.bigcorp.ca       IN   A      10.10.1.1
zip.bigcorp.ca       IN   MX     10 smtp.zip.bigcorp.ca
</code></pre>

To see all data of the same RR type the value can be dropped from the argument list:



<pre><code>
(venv) $ bamcli view blue.zip.bigcorp.ca A
blue.zip.bigcorp.ca       IN   A    10.10.10.10
blue.zip.bigcorp.ca       IN   A    10.10.2.2
</code></pre>

<h3> Deleting DNS data </h3>

Deleting DNS RRs are done in the same manner in which they were added. The general syntax is:

<pre><code>
(venv) $ bamcli delete fqdn RR_type value
</code></pre>

Here are some examples:

<pre><code>
(venv) $ bamcli delete zip.bigcorp.ca A 10.10.1.1
(venv) $ bamcli delete blue.zip.bigcorp.ca A 10.10.10.10,10.10.2.2
(venv) $ bamcli delete rouge.zip.bigcorp.ca CNAME

Note: CNAME records can be deleted with or without the value as there can only be one record per fqdn.
</code></pre>

## Batch operations

At the present time bulk operations are managed by creating a file of bamcli commands using file as input to the shell.

<pre><code>
(venv) $cat cli-cmds | sh
</code></pre>
