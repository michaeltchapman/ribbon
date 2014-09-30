
# rpm 4.8 (EL6) Structure.
flags = {
    'ANY'        : 0,
    'LESS'       : (1 << 1),    # <
    'GREATER'    : (1 << 2),    # >
    'EQUAL'      : (1 << 3),    # =
    'PROVIDES'   : (1 << 4),    # internal use only
    'CONFLICTS'  : (1 << 5),    # internal use only
    'PREREQ'     : (1 << 6),    # legacy
    'OBSOLETES'  : (1 << 7),    # internal use only
    'INTERP'     : (1 << 8),    # interpreter for scriptlet
    'SCRIPT_PRE' : (1 << 9),    # preinstall
    'SCRIPT_POST' : (1 << 10),  # postinstall
    'SCRIPT_PREUN' : (1 << 11), # preuninstall
    'SCRIPT_POSTUN' : (1 << 12),# postuninstall
    'SCRIPT_VERIFY' : (1 << 13),# verify
    'FIND_REQUIRES' : (1 << 14),# generated from find_requires
    'FIND_PROVIDES' : (1 << 15),# generated from find_provides

    'TRIGGERIN'  : (1 << 16),   # install trigger
    'TRIGGERUN'  : (1 << 17),   # uninstall trigger
    'TRIGGERPOSTUN' : (1 << 18),# post uninstall trigger
    'MISSINGOK'  : (1 << 19),   # %config(missingok)
    'SCRIPT_PREP' : (1 << 20),   # prep build
    'SCRIPT_BUILD' : (1 << 21),  # actual build
    'SCRIPT_INSTALL' : (1 << 22),# install build
    'SCRIPT_CLEAN' : (1 << 23),  # clean build
    'RPMLIB' : (1 << 24),        # rpm library feature
    'TRIGGERPREIN' : (1 << 25),  # pre install trigger
    'KEYRING'    : (1 << 26),    # ??
    'PATCHES'    : (1 << 27),    # ??
    'CONFIG'     : (1 << 28)     # ??
}
# TODO rpm 4.11 (EL 7) Structure
#ANY        = 0,
#LESS       = (1 << 1),
#GREATER    = (1 << 2),
#EQUAL      = (1 << 3),
#/* bit 4 unused */
#POSTTRANS  = (1 << 5),
#PREREQ     = (1 << 6),
#PRETRANS   = (1 << 7),
#INTERP     = (1 << 8),
#SCRIPT_PRE = (1 << 9),
#SCRIPT_POST = (1 << 10),
#SCRIPT_PREUN = (1 << 11),
#SCRIPT_POSTUN = (1 << 12),
#SCRIPT_VERIFY = (1 << 13),
#FIND_REQUIRES = (1 << 14),
#FIND_PROVIDES = (1 << 15),
#
#TRIGGERIN  = (1 << 16),
#TRIGGERUN  = (1 << 17),
#TRIGGERPOSTUN = (1 << 18),
#MISSINGOK  = (1 << 19),
#/* bits 20-23 unused */
#RPMLIB = (1 << 24),
#TRIGGERPREIN = (1 << 25),
#KEYRING    = (1 << 26),
#/* bit 27 unused */
#CONFIG     = (1 << 28)

def parse_number(n):
    n = int(n)
    return [ f for f, v in flags.items() if n & v]

