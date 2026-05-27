const fs = require('fs');
const path = require('path');

const p = path.resolve(__dirname, '..', 'Sony-Web', 'games.json');
if (!fs.existsSync(p)) {
  console.error('games.json not found at', p);
  process.exit(2);
}
const data = JSON.parse(fs.readFileSync(p, 'utf8'));
const games = data.games || {};
const ps5Ids = Object.keys(games).filter(id => games[id] && games[id].platform === 'PS5');
// Preserve existing order if already included; otherwise append new IDs
const existingAll = (data.platforms && data.platforms.PS5 && data.platforms.PS5.sections && data.platforms.PS5.sections.all && data.platforms.PS5.sections.all.games) || [];
const unique = Array.from(new Set([...existingAll, ...ps5Ids]));

if (!data.platforms) data.platforms = {};
if (!data.platforms.PS5) data.platforms.PS5 = { sections: { all: { games: unique } } };
else {
  if (!data.platforms.PS5.sections) data.platforms.PS5.sections = {};
  if (!data.platforms.PS5.sections.all) data.platforms.PS5.sections.all = { games: unique };
  else data.platforms.PS5.sections.all.games = unique;
}

fs.writeFileSync(p, JSON.stringify(data, null, 2), 'utf8');
console.log('Updated PS5 all.games with', unique.length, 'IDs');
