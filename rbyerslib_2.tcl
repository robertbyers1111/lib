
#   +-----------------+
#---| SHOW_expect_out |---------------------------------------------------------
#   +-----------------+

proc SHOW_expect_out {SEVERITY index} {
  global expect_out
  foreach line [split $expect_out($index) \r\n] {
    set line [string trim $line]
    if {$line != "" } {
      logMsg $SEVERITY $line
    }
  }
}

#   +------------+
#---| showBoxMsg |--------------------------------------------------------------
#   +------------+

proc showBoxMsg {msg {longtail {0}}} {

  set now [clock format [clock seconds]]

  set L1 [string length $msg]
  set L2 [expr $L1 + 2]

  append border1 "+" [string repeat - $L2] "+"

  set border2 "---|"

  if {$longtail == 1 || \
   [regexp -nocase {^\s*long\s*$} $longtail] || \
   [regexp -nocase {^\s*true\s*$} $longtail] } {

      set border3 "|----------------------------------------------------------------"

  } else {
      set border3 "|------------"
  }

  puts ""
  logMsg INFO "   $border1"
  logMsg INFO "$border2 $msg $border3"
  logMsg INFO "   $border1\n"
}

#   +------------------+
#---| CREATE_unxObject |--------------------------------------------------------
#   +------------------+

proc CREATE_unxObject {unxObjectID_VARNAME name} {

  global spawn_id
  global prev_spawn_id
  global PROMPTS
  global expect_out
  global unxObject
  upvar  $unxObjectID_VARNAME unxObjectID

  log_user 0
  set timeout 8
  set shell /bin/bash

  INIT_PROMPTS

  set NOW [clock clicks -milliseconds] ; after 1

  if {[info exists spawn_id]} {
    set prev_spawn_id $spawn_id
  } else {
    set prev_spawn_id ""
  }

  #   +-----------------------+
  #---| Spawn a shell session |---
  #   +-----------------------+

      if {[catch {spawn $shell} msg]} {
        logMsg ERROR $msg
        exit
      } else {
        logMsg INFO "Spawned $shell using pid $msg and spawn_id $spawn_id"
      }

      expect {
        -re $PROMPTS {
          logMsg INFO "Got initial $shell prompt '$expect_out(0,string)'"
        }
        timeout {
          logMsg ERROR "Timeout waiting for initial $shell prompt"
          exit
        }
      }

  #   +---------------------------+
  #---| Set the object properties |---
  #   +---------------------------+

      set unxObjectID $NOW
      set unxObject($unxObjectID,name) $name
      set unxObject($unxObjectID,spawn_id) $spawn_id
      set unxObject($unxObjectID,prev_spawn_id) $prev_spawn_id

  #   +---------------------+
  #---| Display useful info |---
  #   +---------------------+

      puts ""
      logMsg DEBUG "---- CREATING UNIX OBJECT -----------------"
      logMsg DEBUG "              ID: $unxObjectID"
      logMsg DEBUG "            name: $unxObject($unxObjectID,name)"
      logMsg DEBUG "        spawn_id: $unxObject($unxObjectID,spawn_id)"

      if {[info exists unxObject($unxObjectID,prev_spawn_id)] \
      && $unxObject($unxObjectID,prev_spawn_id) != ""} {
        logMsg DEBUG "   prev_spawn_id: $unxObject($unxObjectID,prev_spawn_id)"
      }

      logMsg DEBUG "-------------------------------------------"

  #   +---------------------+
  #---| That is all for now |---
  #   +---------------------+

      return $unxObjectID

}

#   +-----------------+
#---| LOGIN_unxRemote |---------------------------------------------------------
#   +-----------------+

proc LOGIN_unxRemote {unxObjectID remhost remuser} {

  global CURR_USERNAME

  set METHOD ssh
  set METHODOPTS "-A -o ConnectTimeout=8"
  set CURR_USERNAME $remuser

  puts ""

  logMsg DEBUG "---- LOGGING INTO A UNIX SYSTEM -----------"
  logMsg DEBUG "            IP Addr: $remhost"
  logMsg DEBUG "        unxObjectID: $unxObjectID"
  logMsg DEBUG "            remuser: $remuser"

  SEND_unxCmd $unxObjectID "/home/rbyers/etc/ssh-agent-check.sh"
  SEND_unxCmd $unxObjectID "$METHOD $METHODOPTS $remuser@$remhost"

  logMsg DEBUG "-------------------------------------------"

}

#   +---------------------------+
#---| LOGIN_unxRemoteWithPasswd |-----------------------------------------------
#   +---------------------------+

proc LOGIN_unxRemoteWithPasswd {unxObjectID ipaddr username {password {abc123}}} {

  global CURR_USERNAME
  global CURR_PASSWORD

  set METHOD "ssh -A -o ConnectTimeout=8 -i /home/rbyers/.ssh/rbyers_2017-0522_internal.ppk"
  set CURR_USERNAME $username
  set CURR_PASSWORD $password

  puts ""

  logMsg DEBUG "---- LOGGING INTO A UNIX SYSTEM -----------"
  logMsg DEBUG "            IP Addr: $ipaddr"
  logMsg DEBUG "        unxObjectID: $unxObjectID"
  logMsg DEBUG "           username: $username"
  logMsg DEBUG "           password: $password"


  SEND_unxCmd $unxObjectID "$METHOD $username@$ipaddr"

  logMsg DEBUG "-------------------------------------------"

}

#   +--------------+
#---| INIT_PROMPTS |------------------------------------------------------------
#   +--------------+

proc INIT_PROMPTS {} {
  global PROMPTS
  if { ! [info exists PROMPTS]} {
    set PROMPTS [format "\\$ \$\|> \$\|# \$\|Password:\\s*\$\|.sudo.\\s+password\\s+for\\s+\\S+:\|Connected\\s+to\\s+.*(\r|\n)220\\s+\\S+\\s+FTP\\s+.*ready.*(\r|\n)Name .*:"]
  }
}

#   +-------------+
#---| SEND_unxCmd |-------------------------------------------------------------
#   +-------------+

proc SEND_unxCmd {unxObjectID cmd} {

  set DEFAULT_TIMEOUT_SECS 15
  set DEFAULT_CURR_USERNAME acme
  set DEFAULT_CURR_PASSWORD abc123

  global expect_out
  global spawn_id
  global unxObject
  global TIMEOUT_SECS
  global CURR_USERNAME
  global CURR_PASSWORD
  global PROMPTS

  set spawn_id $unxObject($unxObjectID,spawn_id)

  INIT_PROMPTS

  if { ! [info exists TIMEOUT_SECS]} {
    set TIMEOUT_SECS $DEFAULT_TIMEOUT_SECS
  }

  if { ! [info exists CURR_USERNAME]} {
    set CURR_USERNAME $DEFAULT_CURR_USERNAME
  }

  if { ! [info exists CURR_PASSWORD]} {
    set CURR_PASSWORD $DEFAULT_CURR_PASSWORD
  }

  puts ""
  logMsg DEBUG "SENDING UNIX COMMAND '$cmd'"
  logMsg DEBUG "unxObjectID: $unxObjectID"
  logMsg DEBUG "spawn_id: $spawn_id"

  set expect_out(buffer) "_o0O------------- UN-INITIALIZED -------------O0o_"
  send $cmd\r

  set elapsed 0
  set FLAG_timedOut 1
  set FLAG_DENIED 0
  set t0 [clock seconds]

  while {$elapsed <= $TIMEOUT_SECS} {

    expect {

      -re {Permission denied .publickey.} {
        logMsg DEBUG "..."
        logMsg DEBUG "... PERMISSION DENIED! ('publickey')"
        logMsg DEBUG "..."
        set FLAG_DENIED 1
        break
      }

      -re {The authenticity of host .*Are you sure you want to continue connecting .yes/no} {
        logMsg DEBUG "GOT 'Are you sure..' PROMPT, sending 'yes'"
        send yes\r
      }

      -re {Connected\s+to\s+.*220\s+\S+\s+FTP\s+server\s+.*\s+ready.*Name\s+\S+\s*:\s*$} {
        logMsg DEBUG "GOT username prompt for FTP connection"
        set FLAG_timedOut 0
        break
      }

      -re {Save Changes .y/n..: $} {
        logMsg DEBUG "GOT 'Save Changes' PROMPT, sending 'y'"
        send y\r
      }

      -re {Changes could affect service, continue .y/n..: $} {
        logMsg DEBUG "GOT 'save changes' QUESTION PROMPT, sending 'y'"
        send y\r
      }

      -re {ssh: connect to host .* port .*: Connection timed out} {
        logMsg DEBUG "Connection timeout detected"
        set FLAG_timedOut 1
        break
      }

      -re {[\r\n]+login:\s*$} {
        logMsg DEBUG "GOT login prompt"
        logMsg DEBUG "SENDING '$CURR_USERNAME'"
        send $CURR_USERNAME\r
        set t0 [clock seconds]
        set elapsed 0
      }

      -re {331\s+Password\s+required\s+for\s+\S+.*Password\s*:\s*$} {
        logMsg DEBUG "GOT FTP password prompt"
        set FLAG_timedOut 0
        break
      }

      -re {sudo.\s+password\s+for\s+\S+:} {
        logMsg DEBUG "GOT SUDO PASSWORD prompt"
        logMsg DEBUG "SENDING '$CURR_PASSWORD'"
        send $CURR_PASSWORD\r
        set t0 [clock seconds]
        set elapsed 0
      }

      -re {[Pp]assword:\s*$} {
        logMsg DEBUG "GOT generic PASSWORD prompt '($expect_out(0,string))'"
        logMsg DEBUG "SENDING '$CURR_PASSWORD'"
        send $CURR_PASSWORD\r
        set t0 [clock seconds]
        set elapsed 0
      }

      -re {\s+\d\d:\d\d:\d\d.\[m(>|##)\s+.\[K\s*$} {
         # \s+\d\d:\d\d:\d\d.\[m##\s+.\[K\s*$
        logMsg DEBUG "GOT PROMPT WITH BASH ESCAPES'($expect_out(0,string))'"
        set FLAG_timedOut 0
        break
      }

      -re $PROMPTS {
        logMsg DEBUG "GOT generic prompt '$expect_out(0,string)'"
        set FLAG_timedOut 0
        break
      }

      eof {
        logMsg DEBUG "GOT eof"
        set FLAG_timedOut 0
        break
      }
    }

    after 1000
    set elapsed [expr [clock seconds] - $t0]

  }

  if {$FLAG_DENIED} {
    logMsg WARN "unabled to open ssh session due to publickey auth failure"
    set unxObject($unxObjectID,status) "BOGUS"
  } elseif {$FLAG_timedOut} {
    logMsg WARN "TIMEOUT experienced while running command '$cmd'"
    set unxObject($unxObjectID,status) "BOGUS"
  }

}

