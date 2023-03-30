
#   +---------+
#---| SET_ENV |-----------------------------------------------------------------
#   +---------+
#
# Set some default global variables, taken from user's environment

proc SET_ENV {} {

  global env
  global USER LOGNAME HOME ANVILRC

  if {[info exists env(USER)]} {
    set USER $env(USER)
    set LOGNAME $env(USER)
  } elseif {[info exists env(LOGNAME)} {
    set USER $env(LOGNAME)
    set LOGNAME $env(LOGNAME)
  } else {
    puts stderr "WTF: unable to determin who you are"
    exit
  }

  if {[info exists env(HOME)]} {
    set HOME $env(HOME)
  } else {
    puts stderr "WTF: unable to determin your home directory"
    exit
  }

  set ANVILRC $HOME/.anvilrc
  if { ! [file exists $ANVILRC]} {
    set ANVILRC ANVILRC_NOT_EXIST
  }

}

#   +-----+
#---| NOW |---------------------------------------------------------------------
#   +-----+
#
# Returns the current date and time in various formats as follows:
#
# -----     ------------   ---------------
# Param     Set to         Format returned
# -----     ------------   ---------------
#
#   fmt     ymd            Y-M-D
#           ymdhms         Y-M-D_H:M:S
#           (all others)   H:M:S
#
# -----     ------------   -------
# Param     Set to         Meaning
# -----     ------------   -------
#
#   nc      1, nc or NC    Supresses any '-', '_' or ':' character.
#           (all others)   Disables the supression
#
#-------------------------------------------------------------------------------

proc NOW {{fmt {HMS}} {nc {0}}} {

  set fmt [string tolower $fmt]
  regsub -all {[-_]} $fmt {} fmt

  switch -- [string tolower $nc] {
    1 -
    nc {
      set nc 1
    }
    default {
      set nc 0
    }
  }

  switch -- $fmt {
    ymd {
      if {$nc} {
        set fmtString "%y%m%d"
      } else {
        set fmtString "%y-%m-%d"
      }
    }
    ymdhms {
      if {$nc} {
        set fmtString "%y%m%d_%H%M%S"
      } else {
        set fmtString "%y-%m-%d_%H:%M:%S"
      }
    }
    hms -
    default {
      if {$nc} {
        set fmtString "%H%M%S"
      } else {
        set fmtString "%H:%M:%S"
      }
    }
  }

  return [clock format [clock seconds] -format $fmtString]
}

#   +--------+
#---| MYPUTS |------------------------------------------------------------------
#   +--------+

proc MYPUTS {dest severity msg} {
  set LABEL [format "\[%-5s %s\]" $severity [NOW]]
  puts $dest "$LABEL $msg"
}

#   +--------+
#---| logMsg |------------------------------------------------------------------
#   +--------+
#
# A simplified version of anvil's logMsg. Appears here so that this lib can be
# used by non-anvil scripts.

if {[info proc logMsg] == ""} {
proc logMsg {severity msg} {
    switch -- $severity {
      INFO2 -
      ERROR -
      USAGE -
      WARNING -
      FAIL {
        set dest stderr
      }
      default {
        set dest stdout
      }
    }
    MYPUTS $dest $severity $msg
}
}

#   +-------+
#---| DEBUG |-------------------------------------------------------------------
#   +-------+

proc DEBUG {msgList} {
    global DEBUGSTATE
    if {[info exists DEBUGSTATE] && $DEBUGSTATE != 0} {
        set msg $msgList
        foreach line [split $msg \n] {
          if {$line == ""} {
            puts ""
          } else {
            logMsg DEBUG $line
          }
        }
    }
}

#   +------+
#---| INFO |--------------------------------------------------------------------
#   +------+
#
# (this version sends output to stdout)

proc INFO {msgList} {
    set msg $msgList
    foreach line [split $msg \n] {
      if {$line == ""} {
        puts ""
      } else {
        logMsg INFO $line
      }
    }
}

#   +-------+
#---| INFO2 |-------------------------------------------------------------------
#   +-------+
#
# (this version sends output to stderr)

proc INFO2 {msgList} {
    set msg $msgList
    foreach line [split $msg \n] {
      if {$line == ""} {
        puts ""
      } else {
        logMsg INFO2 $line
      }
    }
}

#   +------+
#---| WARN |--------------------------------------------------------------------
#   +------+

if {[info proc WARN] == ""} {
proc WARN {msgList} {
    set msg $msgList
    foreach line [split $msg \n] {
      if {$line == ""} {
        puts ""
      } else {
        logMsg WARN $line
      }
    }
}
}

#   +-----+
#---| WTF |---------------------------------------------------------------------
#   +-----+

if {[info proc WTF] == ""} {
proc WTF {msgList} {
    set msg $msgList
    foreach line [split $msg \n] {
      if {$line == ""} {
        puts ""
      } else {
        logMsg WARN "WTF? $line"
      }
    }
}
}

#   +-------+
#---| ERROR |-------------------------------------------------------------------
#   +-------+

if {[info proc ERROR] == ""} {
proc ERROR {msgList} {
    set msg $msgList
    foreach line [split $msg \n] {
      if {$line == ""} {
        puts ""
      } else {
        logMsg ERROR $line
      }
    }
}
}

#   +--------+
#---| BUMMER |------------------------------------------------------------------
#   +--------+

if {[info proc BUMMER] == ""} {
proc BUMMER {msgList} {
    set msg $msgList
    foreach line [split $msg \n] {
      if {$line == ""} {
        puts ""
      } else {
        logMsg BUMMER $line
      }
    }
}
}

#   +-------+
#---| USAGE |-------------------------------------------------------------------
#   +-------+

if {[info proc USAGE] == ""} {
proc USAGE {msgList} {
    set msg $msgList
    foreach line [split $msg \n] {
      if {$line == ""} {
        puts ""
      } else {
        puts stderr ""
        logMsg USAGE "          [file tail [info script]] $line"
        puts stderr ""
      }
    }
    exit
}
}

#   +--------------+
#---| PROC: sleepy |------------------------------------------------------------
#   +--------------+

proc sleepy {seconds} {

  puts ""
  set wait $seconds

  logMsg INFO "Pausing $wait seconds"

  while {$wait} {

    if {$wait <= 10} {
      set afterval 1000
      set decrval -1
    } elseif {$wait <= 60} {
      set afterval 5000
      set decrval -5
    } else {
      set afterval 30000
      set decrval -30
    }

    after $afterval

    logMsg INFO $wait
    incr wait $decrval
  }
}

#   +-----------------+
#---| Getclock_YMDHMS |---------------------------------------------------------
#   +-----------------+
#
# Returns the current year, month, day, hour, minute and second as a string (YYMMDD_HHMMSS)

proc Getclock_YMDHMS {} {
  return [clock format [clock seconds] -format %y%m%d_%H%M%S]
}

#   +--------------+
#---| Getclock_HMS |------------------------------------------------------------
#   +--------------+
#
# Returns the current hour minute and second as a string (HHMMSS)

proc Getclock_HMS {} {
  return [clock format [clock seconds] -format %H%M%S]
}

#   +-------------------+
#---| Getclock_HH:MM:SS |-------------------------------------------------------
#   +-------------------+
#
# Returns the current hour minute and second as a string (HH:MM:SS)

proc Getclock_HH:MM:SS {} {
  return [clock format [clock seconds] -format %H:%M:%S]
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

#   +---------------+
#---| UTY_open_file |-----------------------------------------------------------
#   +---------------+
#
# Opens a file. Name of file can be passed in, or, if filename is an integer,
# the filename is taken from the user's command line arguments.
#
# ARGs:
#
#   filename:    Which of the cmd line args to use (0, 1, 2, etc.)
#   access_type: Open the file as read only ('r') or writeable ('w'). Any
#                tcl open code (r, w, a, etc.) works.
#
# RETURNs:
#
#   Returns a two element list. First elem is file handle, second is filename
#
# SUGGESTED CALLING EXAMPLE:
#
#
#          foreach {fhandle fname} [UTY_open_file 0] break
#
#
#-------------------------------------------------------------------------------

proc UTY_open_file {filename {access_type {r}}} {

  global argc
  global argv

  if {[regexp {^\d+$} $filename]} {

     set argindex $filename

     INFO "Taking filename from command line argument #$argindex"

     if {$argc < 1} {
       ERROR "No command line arguments found"
       exit
     }

     if {$argindex >= $argc} {
       ERROR "At least [expr $argindex + 1] command line arguments required"
       exit
     }

     set filename [lindex $argv $argindex]
  }

  INFO "Opening '$filename' with permissions '$access_type'"

  if {[catch {open $filename $access_type} fid]} {
    ERROR $fid
    exit
  } else {
    INFO "Opened '$filename' on channel '$fid' using permissions '$access_type'"
  }

  return [list $fid $filename]

}

#   +-------------------+
#---| cmdline_open_file |-------------------------------------------------------
#   +-------------------+
#
#zzz#   EXAMPLE:
#zzz#
#zzz#      set fid1 [cmdline_open_file 0]
#zzz#      set fid2 [cmdline_open_file 1 r]
#zzz#      set fid3 [cmdline_open_file 2 w]
#zzz#    
#zzz#      while {![eof $fid1]} {
#zzz#        gets $fid1 line
#zzz#        puts $fid3 "LINE from fid1: $line" }
#zzz#    
#zzz#      while {![eof $fid2]} {
#zzz#        gets $fid2 line
#zzz#        puts $fid3 "LINE from fid2: $line" }
#zzz#    

proc cmdline_open_file {argindex1_filename {access_type {r}}} {

  global argc
  global argv

  if {$argc < 1} {
    puts stderr "USER CMDLINE ERROR: At least one command line argument required"
    exit
  }

  if {$argindex1_filename >= $argc} {
    puts stderr "USER CMDLINE ERROR: At least [expr $argindex1_filename + 1] command line arguments required"
    exit
  }

  set FILENAME [lindex $argv $argindex1_filename]

  if {[catch {open $FILENAME $access_type} fid]} {
    puts stderr "ERROR: $fid"
    exit
  } else {
    puts "Opened $FILENAME on channel $fid using permissions $access_type"
  }

  return $fid

}

#   +--------------+
#---| INIT_PROMPTS |------------------------------------------------------------
#   +--------------+

proc INIT_PROMPTS {} {
  global PROMPTS
  if { ! [info exists PROMPTS]} {
    set PROMPTS [format "\\$ \$\|> \$\|# \$\|Password:\\s*\$\|Connected\\s+to\\s+.*(\r|\n)220\\s+\\S+\\s+FTP\\s+.*ready.*(\r|\n)Name .*:"]
  }
}

#   +---------------------+
#---| START_shell_session |-----------------------------------------------------
#   +---------------------+
#
# Now using another shell because so I can use a simple prompt string. This makes the
# expect operations work much more reliably (no ctrl chars in the prompt string)

proc START_shell_session {{shell {/bin/dash}}} {

  global spawn_id
  global PROMPTS
  global expect_out
  set timeout 6

  INIT_PROMPTS

  if {[catch {spawn $shell} msg]} {
    ERROR $msg
    exit
  } else {
    DEBUG "Spawned $shell using pid $msg and spawn_id $spawn_id"
  }

  expect {
    -re $PROMPTS {
      DEBUG "Got initial $shell prompt '[string trim $expect_out(0,string)]'"
    }
    timeout {
      ERROR "Timeout waiting for initial $shell prompt"
      exit
    }
  }

}

#   +----------+
#---| SEND_cmd |----------------------------------------------------------------
#   +----------+

proc SEND_cmd {cmd {extraCR {}}} {

  global PROMPTS
  global spawn_id
  global expect_out

  set ORIG_log_user [log_user]

  INIT_PROMPTS

  DEBUG "Send command '$cmd' to spawn_id $spawn_id"
  send $cmd\r

  if {[info exists extraCR]} {
    if {$extraCR == "extraCR"} {
      DEBUG "Send extra CR.."
      after 250
      send \r
    }
  }

  #-- Initialize timeout and max iterations to their defaults

      set timeout 1
      set MAX_TRIES 30

  #-- Override timeout and max iterations, if either global exists

      global rbyerslib__SEND_cmd__timeout
      if {[info exists rbyerslib__SEND_cmd__timeout]} {
        set timeout $rbyerslib__SEND_cmd__timeout
      }

      global rbyerslib__SEND_cmd__MAX_TRIES
      if {[info exists rbyerslib__SEND_cmd__MAX_TRIES]} {
        set MAX_TRIES $rbyerslib__SEND_cmd__MAX_TRIES
      }

  set NUM_TRIES 0
  set STILL_LOOKING 1
  set t0 [clock seconds]

  while {$STILL_LOOKING} {

    incr NUM_TRIES

    expect {

      -re {Connected\s+to\s+.*220\s+\S+\s+FTP\s+server\s+.*\s+ready.*Name\s+\S+\s*:\s*$} {
        if {$ORIG_log_user} {puts ""}
        DEBUG "GOT username prompt for FTP connection"
        set STILL_LOOKING 0
        break
      }

      -re {(?:331)\s+Password\s+required\s+for\s+\S+.*Password\s*:\s*$} {

        #----------------------------------------------------------------------------
        #
        # NOTE: Had to enclose '331' in (?:...) because otherwise I kept getting:
        #
        #    couldn't compile regular expression pattern: invalid repetition count(s)
        #
        #----------------------------------------------------------------------------

        if {$ORIG_log_user} {puts ""}
        DEBUG "GOT password prompt for FTP connection"
        set STILL_LOOKING 0
        break
      }

      -re {Are you sure you want to continue connecting .yes/no} {
        if {$ORIG_log_user} {puts ""}
        DEBUG "GOT 'Are you sure..' PROMPT, sending 'yes'"
        send yes\r
      }

      -re {Save Changes .y/n..: $} {
        if {$ORIG_log_user} {puts ""}
        DEBUG "GOT 'Save Changes' PROMPT, sending 'y'"
        send y\r
      }

      -re {Changes could affect service, continue .y/n..: $} {
        if {$ORIG_log_user} {puts ""}
        DEBUG "GOT 'save changes' QUESTION PROMPT, sending 'y'"
        send y\r
      }

      -re {@.*'s password:\s*} {
        if {$ORIG_log_user} {puts ""}
        DEBUG "GOT password prompt for ssh/sftp connection"
        set STILL_LOOKING 0
        break
      }

      -re {sftp>\s*$} {
        if {$ORIG_log_user} {puts ""}
        DEBUG "successfuly logged on via sftp"
        set STILL_LOOKING 0
        break
      }

      -re $PROMPTS {
        if {$ORIG_log_user} {puts ""}
        DEBUG "GOT prompt '$expect_out(0,string)'"
        set STILL_LOOKING 0
        break
      }

      eof {
        if {$ORIG_log_user} {puts ""}
        DEBUG "GOT eof"
        set STILL_LOOKING 0
        break
      }
    }

    if {$NUM_TRIES >= $MAX_TRIES} {
      BUMMER "Giving up after $NUM_TRIES"
      exit
    }

    #after 1000
    set t1 [clock seconds]
    set elapsed [expr $t1 - $t0]
    if {[expr $MAX_TRIES - $NUM_TRIES] < 5} {
      INFO "Still looking after $elapsed seconds and $NUM_TRIES attempts"
    } else {
      DEBUG "Still looking after $elapsed seconds and $NUM_TRIES attempts"
    }
  }
}

#   +-----------+
#---| SEND_cmd2 |---------------------------------------------------------------
#   +-----------+
#
# This version allows you to pass named attributes. EXAMPLE:
#
#        SEND_cmd2 nextprompt="(config)# " timeout=50 cmd="show running"
#
# Only 'cmd' is required, the others are optional.
#
#-------------------------------------------------------------------------------

proc SEND_cmd2 {args} {

  global PROMPTS
  global spawn_id
  global expect_out
  global timeout

  if {![info exists args]} {
    WTF "At least one argument must be passed to SEND_cmd2"
    exit
  }

  catch {unset extraCR}
  catch {unset PROMPTS}
  INIT_PROMPTS

  set MAX_TRIES 30

  foreach arg $args {
    INFO "               arg: '$arg'"
    if {[regexp {^([^=]+)\s*=\s*(.*)} $arg junk argName argVal]} {
      #NFO "           argName: '$argName'"
      #NFO "            argVal: '$argVal'"
      switch -nocase -- $argName {
        cmd {
          set cmd $argVal
          #NFO "               cmd: '$cmd'"
        }
        nextprompt {
          set nextprompt $argVal
          set PROMPTS $nextprompt
          #NFO "        nextprompt: '$nextprompt'"
        }
        timeout {
          set timeout $argVal
          set MAX_TRIES $timeout
          #NFO "           timeout: $timeout"
        }
        extraCR {
          set extraCR $argVal
          #NFO "           extraCR: $extraCR"
        }
        default {
          WTF "arg '$argName' not supported by this proc (SEND_cmd2)"
          exit
        }
      }
    } else {
      WTF "Unable to parse arg '$arg' in this proc (SEND_cmd2)"
      exit
    }
  }

  if {![info exists cmd]} {
    WTF "Command not found in args passed to proc SEND_cmd2"
  }

  puts "                            ----------------------------------------------------"

  INFO "           SENDING: '$cmd' (spawn_id=$spawn_id)"
  send $cmd\r

  if {[info exists extraCR]} {
    if {$extraCR == "extraCR"} {
      INFO "       SENDING: (extra CR)"
      after 250
      send \r
    }
  }

  set NUM_TRIES 0
  set STILL_LOOKING 1
  set timeout 1

  set t0 [clock seconds]

  while {$STILL_LOOKING} {
    incr NUM_TRIES

    expect {

      -re {Changes could affect service, continue .y/n..: $} {
        puts ""
        INFO "GOT 'changes could affect service' PROMPT, sending 'y'"
        send y\r
      }

      -re {Save Changes .y/n..: $} {
        puts ""
        INFO "GOT 'Save Changes' PROMPT, sending 'y'"
        send y\r
      }

      -re {Connected\s+to\s+.*220\s+\S+\s+FTP\s+server\s+.*\s+ready.*Name\s+\S+\s*:\s*$} {
        puts ""
        INFO "GOT FTP username prompt"
        set STILL_LOOKING 0
        break
      }

      -re {331\s+Password\s+required\s+for\s+\S+.*Password\s*:\s*$} {
        puts ""
        INFO "GOT FTP password prompt"
        set STILL_LOOKING 0
        break
      }

      -re $PROMPTS {
        puts ""

        catch {unset lastline}
        foreach line [split [string trim $expect_out(0,string)] \r\n] {
          if {[string trim $line] != ""} {
            set lastline $line
          }
        }
        if {![info exists lastline]} {
          set lastline [string trim $expect_out(0,string)]
        }

        INFO "        GOT prompt: '$lastline'"
        set STILL_LOOKING 0
        break
      }

      eof {
        puts ""
        INFO "GOT eof"
        set STILL_LOOKING 0
        break
      }
    }

    if {$NUM_TRIES >= $MAX_TRIES} {
      ERROR "Giving up after $NUM_TRIES"
      exit
    }

    #after 1000
    set t1 [clock seconds]
    set elapsed [expr $t1 - $t0]
    INFO "     Still looking: $elapsed seconds / $NUM_TRIES attempts of $MAX_TRIES max"
  }
  INIT_PROMPTS
}

#   +-----------------------+
#---| TELNET_to_loginPrompt |---------------------------------------------------
#   +-----------------------+

proc TELNET_to_loginPrompt {ip} {

  global spawn_id

  if {[catch {spawn telnet $ip} msg]} {
    ERROR $msg
    exit
  } else {
    INFO ""
    INFO "             Spawn: OK"
    INFO "                ip: $ip"
    INFO "               pid: $msg"
    INFO "          spawn_id: $spawn_id"
  }

  expect {
    -re login: {
      INFO "      Login prompt: OK"
      INFO ""
    }
    timeout {
      ERROR "Timeout waiting for login prompt"
      exit
    }
  }
}

#   +-------------------+
#---| compareToExpected |-------------------------------------------------------
#   +-------------------+
#
# Compare a variable to its expected lower and upper bounds. Fail the test
# if it doesn't lie withing the expected range.
#
# ARGs:
#   VARNAME		Name of variable, in caller's scope, to be checked
#   expectedLowerBound	Expected lower bound, inclusive
#   expectedUpperBound	Expected upper bound, inclusive
#
# Note if expectedUpperBound is omitted, an exact match is
# required, using the lower bound as the expected exact value.
#
#-------------------------------------------------------------------------------

proc compareToExpected {VARNAME expectedLowerBound {expectedUpperBound {N/A}}} {

    upvar $VARNAME testVar

    if {[regexp ^N/A$ $expectedUpperBound]} {

      if {$testVar == $expectedLowerBound} {
        logMsg INFO "OK: $VARNAME ($testVar) == $expectedLowerBound"
      } else {
        logResult FAIL "$VARNAME ($testVar) != $expectedLowerBound"
      }

    } else {

      if {$testVar >= $expectedLowerBound && $testVar <= $expectedUpperBound} {

        logMsg INFO "OK: $VARNAME ($testVar) is between $expectedLowerBound *AND* $expectedUpperBound (inclusive)"

      } else {

        if {$testVar < $expectedLowerBound} {
          logResult FAIL "$VARNAME ($testVar) is less than expected lower bound ($expectedLowerBound)"
        } elseif {$testVar > $expectedUpperBound} {
          logResult FAIL "$VARNAME ($testVar) is greater than expected upper bound ($expectedUpperBound)"
        } else {
          logResult FAIL "WTF should never get here!"
        }

      }

    }

}

#   +--------------------+
#---| waitForNoPauseFile |------------------------------------------------------
#   +--------------------+
#
# This procedure will pause the script if a file 'PAUSE.now' exists.
# Once the file is removed this script will continue normal processing.
#
# (use this as a development or debugging tool)
#
# Variables: none
# Return Value: none
#-------------------------------------------------------------------------------

proc waitForNoPauseFile {} {
  if {[file exists "PAUSE.now"]} {
    logMsg INFO "Now pausing until pause file is removed.."
    while {[file exists "PAUSE.now"]} {
      logMsg INFO "(pause file still exists)"
      after 10000
    }
    if {[file exists "PAUSE.now"]} {
      logMsg ERROR "WTF? Fell out of loop yet pause file still exists!"
    } else {
      logMsg INFO "Yay! pause file has be removed!"
      logMsg INFO "Now continue with normal testing..."
    }
  }
}

