
if [ "x$RBYERSLIB_SH_BEENHERE" = "x" ]; then

#   +-----------------------+
#---| Stuff to do only once |---
#   +-----------------------+

#-- Make sure we know who I am

    export ME=$LOGNAME

    if [ "x$ME" = "x" ]; then
      echo WTF LOGNAME UNDEFINED
      exit
    fi

#-- Various locations relative to user's home directory

    if [ "$SUDO_USER" = "" ]; then
      export MYHOME=/home/$ME
    else
      export HOME=/root
      export MYHOME=/home/$SUDO_USER
    fi

    export BIN=$HOME/bin
    export ETC=$HOME/etc
    export LOG=$HOME/logs
    export PUB=$HOME/public_html
    export VAR=$HOME/var

#-- Some folks don't have their own tmp directory :(

    if [ -d $HOME/tmp ]
    then
      export TMP=$HOME/tmp
    else
      export TMP=/tmp
    fi

#-- Various locations relative to rmbjr60' home directory

    export BHOME=/home/rmbjr60

    export BBIN=$BHOME/bin
    export BETC=$BHOME/etc
    export BLOG=$BHOME/logs
    export BPUB=$BHOME/public_html
    export BSRC=$BHOME/src
    export BTMP=$BHOME/tmp
    export BVAR=$BHOME/var

    export COMMIFY=$BBIN/commify

#-- Shorthands that are useful for sed and egrep.

    # (use double quotes (") surrounding sed expression)

#-- Match date and time

    export DATE="20[0-3][0-9]-[0-1][0-9]-[0-3][0-9]"
    export TIME="[0-2][0-9]:[0-5][0-9]:[0-5][0-9]"

#-- Match Numbers, Alphas, Alphanumeric, Spaces and IP Addresses

    export NUM="[0-9]"
    export NUMS="${NUM}${NUM}*"
    export ZNUMS="${NUM}*"

    export ALPHA="[a-zA-Z]"
    export ALPHAS="${ALPHA}${ALPHA}*"
    export ZALPHAS="${ALPHA}*"

    export ALPHANUM="[a-zA-Z0-9]"
    export ALPHANUMS="${ALPHANUM}${ALPHANUM}*"
    export ZALPHANUMS="${ALPHANUM}*"

    export HEXDIGIT="[a-fA-F0-9]"
    export HEXDIGITS="${ALPHANUM}${ALPHANUM}*"
    export ZHEXDIGITS="${ALPHANUM}*"

    export SPACE="[ 	]"
    export SPACES="${SPACE}${SPACE}*"
    export ZSPACES="${SPACE}*"
    export NOTSPACES="[^ 	][^ 	]*"

    export NUMSPACE="[ 0-9	]"
    export NUMSPACES="${NUMSPACE}${NUMSPACE}*"
    export ZNUMSPACES="${NUMSPACE}*"

#-- Matches an IPv4 Address

    export GREPIPADDR="$NUMS\.$NUMS\.$NUMS\.$NUMS"

#-- Match the permisions field from 'ls -l'

    export PERMS="[-dlstcb][-rwx][-rwx][-rwx][-rwx][-rwx][-rwx][-rwx][-rwx][-rwx]"

fi

#   +---------------------------------------+
#---| Stuff to redo EVERY time we come here |---
#   +---------------------------------------+

    export NOW=`$BBIN/NOW`
    export TMPF1=$TMP/atempfile_01-$NOW.tmp
    export TMPF2=$TMP/atempfile_02-$NOW.tmp
    export TMPF3=$TMP/atempfile_03-$NOW.tmp
    export TMPF4=$TMP/atempfile_04-$NOW.tmp
    export TMPF5=$TMP/atempfile_05-$NOW.tmp
    export TMPF6=$TMP/atempfile_06-$NOW.tmp
    export TMPF7=$TMP/atempfile_07-$NOW.tmp
    export TMPF8=$TMP/atempfile_08-$NOW.tmp
    export TMPF9=$TMP/atempfile_09-$NOW.tmp
    export TMPF=$TMPF1

#-- For detecting if we've been here before

    export RBYERSLIB_SH_BEENHERE=1

