#!/bin/bash
echo "Build dependence for scrapy"
echo "———————————————————————————"
yum groupinstall -y "Development Tools"
#yum groupinstall -y "Development Libraries"
yum install -y screen
yum install -y python-requests 
yum install -y python-memcached
yum install -y wget
echo "Build python2.7 & modules..."
echo "———————————————————————————"
rm -fr Python-2.7.11*
wget https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz -O Python-2.7.11.tgz
tar xvf Python-2.7.11.tgz
cd Python-2.7.11
./configure && make && make install
cd ..
wget --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-1.4.2.tar.gz
tar -xvf setuptools-1.4.2.tar.gz
cd setuptools-1.4.2
python2.7 setup.py install
easy_install-2.7 pip
/usr/local/bin/pip2.7 install scrapy==1.1.2
/usr/local/bin/pip2.7 install scrapyd==1.1.0
/usr/local/bin/pip2.7 install scrapyd-client==1.0.1
/usr/local/bin/pip2.7 install python-Levenshtein==0.12.0
/usr/local/bin/pip2.7 install python-memcached
/usr/local/bin/pip2.7 install redis==2.10.5
/usr/local/bin/pip2.7 install requests
/usr/local/bin/pip2.7 install bs4
/usr/local/bin/pip2.7 install hashlib
/usr/local/bin/pip2.7 install MySQLdb==0.2.0

echo "PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/local/sbin" >> /etc/profile
source /etc/profile
echo "finished scrapy dependence"
echo "Build dependence for claw&handler"
rsync ./lib/* /usr/lib
echo "/usr/lib" >> /etc/ld.so.conf
ldconfig
rpm -ivh --nodeps ./rpms/*
echo "Do some clean job..."
echo "———————————————————————————"

