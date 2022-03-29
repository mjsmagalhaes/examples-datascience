import * as R from 'ramda';

import * as wow from './wow/transform.js';
import * as json from './json/index.js';

// --experimental - specifier - resolution=node
// Source >> Transformation >> Sink

// https://develop.battle.net/documentation/guides/using-oauth/authorization-code-flow
// https://github.com/diogosouza/oauth2-with-node-js

(async () => {
    var data = await json.fromFile('./datacrawler/output.json');

    const transform = R.pipe(
        wow.filterInstanceId(1195),
        wow.extractKillsPerDifficulty(),
        wow.transformToKillsPerBoss,
        json.toFile('raids.json')
    )

    console.log(transform(data))
})();

