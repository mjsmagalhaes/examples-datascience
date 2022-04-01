import { Command } from 'commander';
// import chalk from 'chalk';

import { parseRaidData, transformRaidDataToTable } from "./wow/raids/query.js";
import * as json from './json/index.js';

import { BNET, queryRaidData } from './wow/raids/query.js';
import { loadAuthData } from './query_source.js';

const program = new Command();
program.version('0.0.1');

program
    .command('raid')
    .description('Get raid info for a character')
    .arguments('<character>')
    .option('-r, --realm <name>', 'character realm', 'azralon')
    .option('--debug', 'output debug files')
    .action(async (character, options, command) => {
        // Source
        var auth = await loadAuthData();
        BNET.params.access_token = auth.access_token;
        // console.log(options)

        var data = await queryRaidData(character, options.realm, BNET);

        if (options.debug)
            json.toFile('datacrawler/output.json', data);

        // Alternate Source for Debugging.
        // var data = json.fromFile('datacrawler/output.json');

        // Transform
        var parsedData = await parseRaidData(data);
        console.log(transformRaidDataToTable(parsedData).toString());

        // Sink
        if (options.debug)
            json.toFile('datacrawler/raids.json', parsedData);
    })


program.parse();