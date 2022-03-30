
import lo from 'lodash';
import Table from 'cli-table3';

import * as R from 'ramda';
import * as wow from './wow/transform.js';

export async function parseData(data) {
    const transform = R.pipe(
        wow.filterInstanceId(1195),
        wow.extractKillsPerDifficulty(),
        wow.transformToKillsPerBoss
    )

    return await transform(data)
}

export function dataToTable(data) {
    var t = new Table({
        head: [
            // chalk.green('ENCOUNTERS'),
            // chalk.green('KILLS')
            'ENCOUNTERS', 'KILLS'
        ]
    });

    lo.forEach(data, (el, key) => {
        t.push([key, JSON.stringify(el)])
    })

    return t;
}

