#!/usr/bin/python

from xml.etree import ElementTree
import xml.etree.cElementTree as ET
from xml.dom import minidom
import os

def check_file_exits(path):
    return os.path.isfile(path)

def diff_lists(a,b):
    return [[x for x in a if x not in b], [x for x in b if x not in a]]

def read_ipset_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    ipset = []
    for element in root:
        ipset.append(element.text)
    return ipset

def parse_acl(filename,keyword):
    with open (filename,"r") as acl_dump:
        lines = acl_dump.read()
    delimiter = "EOF"
    iplist = lines.split(delimiter)[1].split('\n')
    processed_acl = []
    for ipset in iplist:
        if ipset != '':
            if keyword.lower() in ipset.split(',')[1].lower():
                processed_acl.append(ipset.split(',')[0])
    return processed_acl

def generate_ipset_xml(acl,filename):
    root = ET.Element("ipset",type="hash:ip")
    for ip in acl:
        ET.SubElement(root, "entry").text = ip
    tree = ET.ElementTree(root)
    tree.write(filename,encoding='utf-8',xml_declaration=True)

def read_ipset_xml(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    ipset = []
    for c in root:
        ipset.append(c.text)
    return ipset

def main():
    # defaults
    acl_file = "/usr/share/firewall-check/adminhosts/file.conf"
    firewalld_ipset_dir = "/etc/firewalld/ipsets"
    managed_groups = {"nagios":["nagios"],"backuppc":["backuppc"],"placeholderadmins":["secure servers","farpoint","placeholder office"]}
    
    firewalld_reload = False
    for group in managed_groups:
	ipset_file = os.path.join(firewalld_ipset_dir,group + ".xml")
        rpm_acl = []
        for keyword in managed_groups[group]:
            rpm_acl += (parse_acl(placeholder_acl_file,keyword))
        if not check_file_exits(ipset_file):
            generate_ipset_xml(rpm_acl,ipset_file)
	    firewalld_reload = True
        else:
            firewalld_acl = read_ipset_xml(ipset_file)
            c = diff_lists(rpm_acl,firewalld_acl)
            if len(c[0]) != 0 or len(c[1]) != 0:
                generate_ipset_xml(rpm_acl,ipset_file)
		firewalld_reload = True
	
    if firewalld_reload == True:
	os.system("firewall-cmd --reload")	

if __name__ == '__main__':
    main()
