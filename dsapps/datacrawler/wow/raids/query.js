
import lo from 'lodash';
import Table from 'cli-table3';
import axios from 'axios';

import * as R from 'ramda';
import * as wow from '../transform.js';

export const DSAPPS = {
    url: './data',
    // params: {}
}

export const BNET = {
    'url': 'https://us.api.blizzard.com/profile/wow/character',
    params: {
        namespace: 'profile-us',
        locale: 'en_US'
    }
}

export async function queryRaidData(character, realm, profile = DSAPPS) {
    var _realm = realm.trim().toLowerCase();
    var _character = character.trim().toLowerCase();
    var url = `${profile.url}/${_realm}/${_character}/encounters/raids`

    // console.log(profile)
    var r = await axios.get(url, { params: profile.params });

    return r.data
}

export async function parseRaidData(data) {
    const transform = R.pipe(
        wow.filterInstanceId(1195),
        wow.extractKillsPerDifficulty(),
        wow.transformToKillsPerBoss
    )

    return await transform(data)
}

export function transformRaidDataToTable(data) {
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