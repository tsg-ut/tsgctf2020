# Slick Logger Writeup

## Solution

Go's strconv.Unquote error mishandling + Blind Regex Injection on re2.

This is an advanced challenge of Blind Regex Injection. If you are unfamiliar with this concept, I would recommend to first read [A Rough Idea of Blind Regular Expression Injection Attack](https://diary.shift-js.info/blind-regular-expression-injection/).

As noted in that blogpost, the regex parser of Go is using non-backtracking engines and the "classic" exploit of Blind Regex Injection such like the following not works here.

`^(?=(some regexp here))((.*)*)*salt$`

Instead, we can invent new attacking method like the following.

`^some regexp here(.?){1000}(.?){1000}(.?){1000}(.?){1000}⋯⋯(.?){1000}(.?){1000}salt$`

The trick used here is related to how Go's regex engine, [re2](https://github.com/google/re2) traces the string. RE2 is a non-backtracking regular expression engine, so it is guaranteed not to require an exponential amount of computation for the length of a character. However, as it processes all possible states of the automaton simultaneously RE2 requires a computational complexity proportional to the number of states of the automaton.

So the basic idea is to use a regular expression such that the number of states of the automaton explodes, and we can use such a regular expression as an indicator of whether or not the string matches in the middle.

RE2 has default limitation of repetition `{n}` with `n <= 1000`, but since Go's implementation of RE2 has no total limitation of DFA state, we can repeat `(.?){1000}` as often as we like, and this allows us to make the regular expression process as heavy as possible.

So, as we observed the execution time of CGI is limited to 1 second in httpd.conf, we can adjust repetition count of `(.?){1000}` so that we tell if a regular expression matches a particular pattern by the HTTP status code returned, 200 or 504.

Then, we can apply a normal Blind Regex Injection method here and get flag. Our expected solver is placed in [solver/solve.js](solver/solve.js).

Translated with www.DeepL.com/Translator (free version)

## Flag

`TSGCTF{Y0URETH3W1NNNER202OH}`
