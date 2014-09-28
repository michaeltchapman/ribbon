"""
Methods for parsing and writing rpm spec files 
"""
import re
import subprocess
import ribbon.build

log = ribbon.build.log

def load(path):
    try:
        with open(path) as f:
            return f.read()
    except EnvironmentError:
        log.error('Exception opening file at: %s', path) 

# Against src rpm or bin rpm?
# tags = rpm -qp --querytags  openstack-keystone-2014.1.2.1-1.el6.src.rpm 2>/dev/null
# rpm -qp --queryformat "[%{$tag} ]" openstack-keystone-2014.1.2.1-1.el6.src.rpm 2>/dev/null
def load_tags(path):
    tags = {}
    log.debug("running tags = rpm -qp --querytags %s 2>/dev/null", path)
    taglist = subprocess.call(['rpm', '-qp', '--querytags', path, '2>/dev/null']).split('\n')
    log.debug("loading tags : %s", str(taglist))
    for tag in taglist:
        tags[tag] = subprocess.call['rpm', '-qp', '--queryformat', ''.join('"[%{' + tag + '}'), ']"', path, '2>/dev/null'].split(' ')
        log.debug("loaded tag : %s", (tag, tags[tag]))
    return tags
   
# rpm -qp --scripts openstack-keystone-2014.1.2.1-1.el6.noarch.rpm
def load_scripts(path):
    scripts = {}
    scriptlines = subprocess.call(['rpm', '-qp', '--scripts', path, '2>/dev/null']).split('\n')
    scriptlist = []
    for i, line in enumerate(scriptlines):
        res = re.match('(\S*)\s*\S*\s*\(using\s*(\S*)\):', line)
        if res:
            scriptlist.append((res.groups(), i))
    for i, script in enumerate(scriptlist):
        if (i+1 < len(scriptlist)):
            scripts[script[0][0]] = '\n'.join(scriptlines[script[1] + 1:scriptlist[i+1][1]])
        else:
            scripts[script[0][0]] = '\n'.join(scriptlines[script[1] + 1:])
    return scripts

def load_macros():
    raise NotImplementedError

# rpm -qp --filesbypkg openstack-keystone-2014.1.2.1-1.el6.src.rpm 2>/dev/null
def load_files():
    raise NotImplementedError

def load_directives():
    raise NotImplementedError

def load_conditionals():
    raise NotImplementedError

