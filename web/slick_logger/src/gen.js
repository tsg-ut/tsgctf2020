const users = require('../dist/data/users.json');
const fs = require('fs');

const text = `
[2020-01-21 16:51:38] hakatashi: Ta-da!
[2020-01-21 16:52:15] hakatashi: Today we are here to make creative, brand-new, and fun web challenge
[2020-01-21 16:52:41] hakatashi: for TSG CTF 2020!
[2020-01-21 16:53:20] kcz: fmm
[2020-01-21 16:56:19] lmt_swallow: sg
[2020-01-21 16:56:38] lmt_swallow: then what is the idea for that?
[2020-01-21 16:56:59] hakatashi: nope!
[2020-01-21 16:57:26] lmt_swallow: huh?
[2020-01-21 16:58:10] kcz: huh?
[2020-01-21 16:59:48] hakatashi: No worries. We have about half year for preparation.

[2020-03-16 23:06:37] lmt_swallow: any ideas?

[2020-03-17 13:11:07] hakatashi: No
[2020-03-17 13:11:19] hakatashi: But I think we can make the flag first
[2020-03-17 13:14:17] hakatashi: This is the essential part of ctf, right?
[2020-03-17 15:30:03] kcz: That's way too far away from essential
[2020-03-17 15:30:49] kcz: Even random string is accetable
[2020-03-17 15:31:19] kcz: for any challenges
[2020-03-17 15:31:21] hakatashi: But we want to be fun, right?
[2020-03-17 15:31:40] kcz: :thinking_face:

[2020-03-18 18:01:18] kcz: Can we have VC now?
[2020-03-18 18:03:28] lmt_swallow: :+1:
[2020-03-18 18:03:45] hakatashi: okay.
[2020-03-18 18:05:09] kcz: https://meet.google.com/xxx-xxxx-xxx
[2020-03-18 20:30:11] hakatashi: okay, we took a quick chat and determined our direction
[2020-03-18 20:32:02] hakatashi: basically I'm responsible for making decisions about how we can make challenge, so I will create the document about core concept of the challenge sooner or later
[2020-03-18 20:32:41] kcz: waiwai
[2020-03-18 20:32:45] hakatashi: we also determined what our flag to be
[2020-03-18 20:33:18] hakatashi: I set reminder about that in secret channel
[2020-03-18 20:33:39] kcz: reminder?
[2020-03-18 20:33:53] hakatashi: y
[2020-03-18 20:34:41] hakatashi: The flag should be super-secret and also simultaneously, operated properly. I can use that as the vault that automatically opens before CTF begins, right?
[2020-03-18 20:34:48] hakatashi: smart enough
[2020-03-18 20:35:31] kcz: that makes sense

[2020-05-12 21:40:31] lmt_swallow: I attended the virtual security conference and one session about organizing ctf inspired me a lot.
[2020-05-12 21:40:44] lmt_swallow: Maybe we can learn from that

[2020-07-03 07:00:25] lmt_swallow: Well, it's already one week before the ctf
[2020-07-03 07:08:07] lmt_swallow: Maybe we should conceive what idea can be good challenge asap

[2020-02-10 16:57:08] hakatashi: @lmt_swallow I was very impressed by the blog post you published yesterday!
[2020-02-10 16:58:56] hakatashi: definitely it has brought a new wind in these areas.
[2020-02-10 17:03:28] lmt_swallow: thx
[2020-02-10 17:03:51] lmt_swallow: The most challenging part was English :)
[2020-02-10 17:05:17] hakatashi: then what is your advice to mitigate them?
[2020-02-10 17:05:42] hakatashi: Just use rust or golang?
[2020-02-10 17:06:04] lmt_swallow: yes
[2020-02-10 17:07:10] lmt_swallow: As I said there, Rust and Go have pretty nice mechanism for that
[2020-02-10 17:07:50] lmt_swallow: Principally, I recommend using Go.
[2020-02-10 17:08:38] lmt_swallow: It's much suitable for web development
[2020-02-10 17:10:10] hakatashi: Cool

[2020-04-29 17:02:08] lmt_swallow: How are you going?
[2020-04-29 17:05:34] hakatashi: we all have hard time to survive
[2020-04-29 17:09:19] lmt_swallow: yeah, very true
[2020-04-29 17:09:51] lmt_swallow: there are also many security events/conferences that was cancelled because of that
[2020-04-29 17:10:24] lmt_swallow: ppl around me is such depressed
[2020-04-29 17:10:57] hakatashi: I feel you
[2020-04-29 17:11:12] hakatashi: then, what can we do?
[2020-04-29 17:11:31] hakatashi: should we postpone our event too?
[2020-04-29 17:12:19] kcz: No. There should be in-house entertainment such like this even in hard times
[2020-04-29 17:12:41] hakatashi: for sure
[2020-04-29 17:13:36] hakatashi: we should be entertainers
[2020-04-29 17:15:09] lmt_swallow: yes, like always
`;

const files = new Map();
let cnt = 708;

for (const line of text.split('\n')) {
  let match;
  if ((match = line.match(/^\[(.+?)\] (.+?): (.+?)$/))) {
    const [, date, username, message] = match;
    const time = new Date(date + '+0900');
    const ts = (time.getTime() / 1000) + '.' + cnt.toString().padStart(4, '0') + '00';
    const user = users.find(({name}) => name === username).id;
    const filename = `${date.split(' ')[0]}.json`;
    if (!files.has(filename)) {
      files.set(filename, []);
    }
    files.get(filename).push({
      type: 'message',
      text: message,
      user,
      ts,
    });

    cnt += 3 + Math.floor(Math.random() * 3);
  }
}

for (const [key, value] of files) {
  fs.writeFileSync(key, JSON.stringify(value, null, '    '));
}
