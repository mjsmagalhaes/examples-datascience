// import { Command } from 'commander';
// import chalk from 'chalk';

// import { parseRaidData, transformRaidDataToTable } from "./wow/raids/query.js";
import * as json from './json/index.js';

import { BNET, queryRaidData } from './wow/raids/query.js';
import { loadAuthData } from './query_source.js';

(async () => {
    // Source
    // var data = await json.fromFile('./datacrawler/output.json');
    var auth = await loadAuthData();

    BNET.params.access_token = auth.access_token;
    var data = await queryRaidData('yapriesty', 'azralon', BNET);

    //     // Transform
    //     var parsedData = await parseRaidData(data);
    //     console.log(transformRaidDataToTable(parsedData).toString())

    //     // Sink
    // json.toFile('raids.json', parsedData);
    json.toFile('./raids.json', data);
})();