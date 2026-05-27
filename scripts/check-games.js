const fs = require('fs');
const path = require('path');

const p = path.resolve(__dirname, '..', 'Sony-Web', 'games.json');
if (!fs.existsSync(p)) {
  console.error('games.json not found at', p);
  process.exit(2);
}
const data = JSON.parse(fs.readFileSync(p, 'utf8'));
const ps5Sections = (data.platforms && data.platforms.PS5 && data.platforms.PS5.sections) || {};
const refs = [];
Object.keys(ps5Sections).forEach(sec => {
  const arr = ps5Sections[sec].games || [];
  arr.forEach(id => refs.push(id));
});
const duplicates = refs.filter((v,i,a) => a.indexOf(v) !== i);
const missing = refs.filter(id => !(data.games && Object.prototype.hasOwnProperty.call(data.games, id)));
const result = {
  totalGames: Object.keys(data.games || {}).length,
  ps5Sections: Object.keys(ps5Sections).reduce((acc,k)=>{acc[k]=(ps5Sections[k].games||[]);return acc;},{}),
  referencedIDs: refs,
  duplicates: Array.from(new Set(duplicates)),
  missing: Array.from(new Set(missing))
};
console.log(JSON.stringify(result, null, 2));
