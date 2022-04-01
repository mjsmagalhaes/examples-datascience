import fs from 'fs';
import got from 'got';

import * as json from './json/index.js'
import { credentials } from './keys.js'

export async function loadAuthData() {
    var data = await json.fromFile('datacrawler/credentials.json');

    if (data === undefined || (data.expiration * 1000) < Date.now()) {
        console.log('Obtaining new token ...')
        data = await getAuthToken()
    } else {
        console.log('Authentication Data Found.')
    }

    return data
}

async function getAuthToken() {
    const data = await got.post(`https://us.battle.net/oauth/token`, {
        form: credentials
    }).json()

    data.expiration = (Date.now() + (data.expires_in * 1000)) / 1000;

    json.toFile("datacrawler/credentials.json", JSON.stringify(data))
    return data
}
