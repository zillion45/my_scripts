# -*- coding: utf-8 -*-

import sys
import urllib2
import xml.etree.cElementTree as ET

xml_url = 'http://dict-co.iciba.com/api/dictionary.php?type=xml&key=YOURKEY&w=%s' % sys.argv[1]
tree = ET.ElementTree(file=urllib2.urlopen(xml_url))

root = tree.getroot()
print "查询单词：" + root[0].text
n = sum(1 for x in tree.iter(tag='ps'))
if n:
    print "英音：".decode('utf-8') + root[1].text
    print "美音：".decode('utf-8') + root[3].text
try:
    for i, j in zip(tree.iter(tag='pos'), tree.iter(tag='acceptation')):
        print i.text + ' ' + j.text.rstrip('\n')
    for elem in tree.iter(tag='sent'):
        print elem[0].text.rstrip('\n') + elem[1].text.rstrip('\n')
except:
    pass
