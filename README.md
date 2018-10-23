MapSnatch
======

Tool for automating light reconaissance of domains and subdomains.


What this tool can do:
1. Find all subdomains of a domain *Using sublist3r*
2. Determine which are alive/reachable
3. Harvest, map, and spider the entireity of the domains site tree
4. Harvest, map, and spider the entireity of all _subdomains_ _*In progress*_


**Usage:** map --domain=example.com --substatus=True

**Installaion:**

>pip install -e .

>sublist3r and a dir containing subbrute need to be within this directory

>sublist3r's requirements.txt 

This tool isnt a finished product by any means, hopefully I get around to adding some more additions to make it a better tool.
The spidering needs adjustments and theres no shortage of simple additions that could be rolled in, such as port scanning.
