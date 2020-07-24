const fs = require('fs');
const {cubes2buffer} = require('../dist/utils.js');
const Cube = require('../dist/node_modules/cubejs');
const {chunk} = require('../dist/node_modules/lodash');

const pow = (a, n) => {
  let r = new Cube();
  let x = a.clone();
  while (n !== 0n) {
    if (n % 2n === 1n) {
      r.multiply(x);
    }
    x.multiply(x);
    n /= 2n;
  }
  return r;
};

Cube.initSolver();

const lines = fs.readFileSync('../dist/output.txt').toString().split('\n');
const cubes = [];

for (const cubeInfo of chunk(lines, 6)) {
  if (cubeInfo.length < 6) {
    break;
  }

  const {g, h, c1, c2} = eval(`(${cubeInfo.join('')})`);
  const rh = Cube.inverse(h);

  let x = 0;
  const cube = new Cube();

  while (true) {
    x++;
    cube.move(g);

    if (cube.clone().move(rh).isSolved()) {
      break;
    }
  }

  const c1Cube = new Cube().move(c1);
  const c2Cube = new Cube().move(c2);

  const poweredCube = pow(c1Cube, BigInt(x))
  const m = c2Cube.move(poweredCube.solve());

  cubes.push(m);
}

console.log(cubes2buffer(cubes).toString());

