import sys
sys.path.insert(0, '/var/www/scylla/')
sys.path.insert(0, '/var/www/scylla/scyllaenv/lib/python3.8/site-packages')
print(sys.path)

from scylla import app as application
application.root_path = '/var/www/scylla'