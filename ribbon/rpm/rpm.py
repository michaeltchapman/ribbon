"""
Methods for parsing and writing rpm spec files 
"""
import re
import subprocess
import logging
import flags
import os

log = logging.getLogger('build')

# list of tags that are arrays
other_arrays = [
  'SOURCE',
  'SOURCEPACKAGE'
  'SOURCEPCKGID'
  'SOURCERPM'
  'PATCH',
  'PATCHESFLAGS',
  'PATCHESNAME',
  'PATCHESVERSION',
  'PROVIDES',
  'PROVIDENAME',
  'PROVIDEVERSION',
  'PROVIDEFLAGS',
  'NOSOURCE',
  'NOPATCH',
  'CONFLICTS',
  'CONFLICTFLAGS',
  'CONFLICTNAME',
  'CONFLICTVERSION',
  'EXCLUDEARCH',
  'EXCLUDEOS',
  'EXCLUSIVEARCH',
  'EXCLUSIVEOS',
]
require_arrays = [
  'REQUIRES',
  'REQUIREFLAGS',
  'REQUIRENAME',
  'REQUIREVERSION',
]
file_arrays = [
  'FILENAMES',
  'FILESTATES',
  'FILEMODES',
  #'FILEUIDS',
  #'FILEGIDS',
  'FILEMTIMES',
  'FILERDEVS',
  'FILEINODES',
  'FILECAPS',
  'FILECLASS',
  'FILECOLORS',
  'FILECONTEXTS',
  'FILEDEPENDSN',
  'FILEDEPENDSX',
  'FILEDEVICES',
  'FILEDIGESTS',
  'FILELANGS',
  'FILEPROVIDE',
  'FILEREQUIRE',
  'FILESIZES',
  'FILEUSERNAME',
  'FILEMD5S',
  'FILELINKTOS',
  'FILEFLAGS',
  'FILEGROUPNAME',
  'FILEVERIFYFLAGS',
]

FNULL = open(os.devnull, 'w')

def load(path):
    try:
        with open(path) as f:
            return f.read()
    except EnvironmentError:
        log.error('Exception opening file at: %s', path) 

# Against src rpm or bin rpm?
# rpm -qp --queryformat "[%{$tag} ]" openstack-keystone-2014.1.2.1-1.el6.src.rpm 2>/dev/null
def load_tags(path):
    tags = {}
    taglist = load_taglist(path)
    log.debug("loading tags : %s", str(taglist))
    arrays = file_arrays + require_arrays + other_arrays
    for tag in taglist:
        if tag in arrays:
            command = ['rpm', '-qp', '--queryformat', '[%{' + tag.strip(' ') + '}\\n]', path]
        else:
            command = ['rpm', '-qp', '--queryformat', '%{' + tag.strip(' ') + '}', path]
        log.debug("running : %s", ' '.join(command))
        if tag in arrays:
            tags[tag] = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=FNULL).communicate()[0].split('\n')
        else:
            tags[tag] = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=FNULL).communicate()[0]
    for tag, value in sorted(tags.items()):
        value = None if (value == [] or value == ['']) else value
        tags[tag] = value
        log.debug("loaded tag {0}: {1}".format(tag, value))
    requires = format_requires(tags)
    files = format_files(tags)
    rpm = { 'requires' :  requires, 'tags': tags, 'files': files}
    return rpm

def format_requires(tags):
    requires = {}
    for i, req in enumerate(tags['REQUIRES']):
        if req != '':
            res = {}
            res['flags'] = flags.parse_flags(tags['REQUIREFLAGS'][i], 'require_flags')
            res['version'] = tags['REQUIREVERSION'][i]
            requires[req] = res
            log.debug("requirement: {0}: {1} {2}".format(req, ' '.join(res['flags']), res['version']))
    return requires

def format_files(tags):
    files = {}

    for i, req in enumerate(tags['FILENAMES']):
        if req != '':
            res = {}
            res['flags'] = flags.parse_flags(tags['FILEFLAGS'][i], 'file_flags')
            for tag in file_arrays:
                if tags[tag] and tags[tag][i] != '':
                    value = tags[tag][i]
                else:
                    value = None
                if tag[-1] == 'S' and tag != 'FILECLASS':
                    tag = tag[:-1]
                res[tag.lower()[4:]] = value
                files[req] = res
            for k, v in res.items():
                log.debug("file: {0}, {1} = {2}".format(req, k, str(res[k])))

    return files

# rpm -qp --querytags openstack-keystone-2014.1.2.1-1.el6.noarch.rpm
def load_taglist(path):
    log.debug("rpm -qp --querytags %s 2>/dev/null" % path)
    return filter(None, subprocess.Popen(['rpm', '-qp', '--querytags', path, '2>/dev/null'], stdout=subprocess.PIPE, stderr=FNULL).communicate()[0].split('\n'))

# rpm -qp --scripts openstack-keystone-2014.1.2.1-1.el6.noarch.rpm
def load_scripts(path):
    scripts = {}
    scriptlines = subprocess.Popen(['rpm', '-qp', '--scripts', path, '2>/dev/null'], stdout=subprocess.PIPE, stderr=FNULL).communicate()[0].split('\n')
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
