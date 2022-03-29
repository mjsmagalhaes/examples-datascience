import { Command } from 'commander';
import chalk from 'chalk';
import lo from 'lodash';
import Table from 'cli-table3';

import * as R from 'ramda';

import * as wow from './wow/transform.js';
import * as json from './json/index.js';

(async () => {
    var data = await json.fromFile('./datacrawler/output.json');

    const transform = R.pipe(
        wow.filterInstanceId(1195),
        wow.extractKillsPerDifficulty(),
        wow.transformToKillsPerBoss,
        json.toFile('raids.json')
    )

    var t = new Table({
        head: [
            chalk.green('ENCOUNTERS'),
            chalk.green('KILLS')
        ]
    });

    lo.forEach(await transform(data), (el, key) => {
        t.push([key, JSON.stringify(el)])
    })

    console.log(t.toString())
})();

