import fs from 'fs';
import jp from 'jsonpath';
import * as R from 'ramda';
import keys from './keys.js';
import got from 'got';

var client_id = keys.client_id;
var client_secret = keys.client_secret;

// Source >> Transformation >> Sink

import { WoWSource } from './wow/source.js';

// https://develop.battle.net/documentation/guides/using-oauth/authorization-code-flow
// https://github.com/diogosouza/oauth2-with-node-js

(async () => {
    // var d = await load_data('output.json');
    // console.log(jp.query(d, '$.character'))

    // var getInfo = R.pipe(
    //     R.prop('body'),
    //     JSON.parse,
    //     console.log
    // )


    var wow = new WoWSource();
    // await wow.initialize();
    // const data = await wow.getProfileRaids('yapriesty', 'azralon');

    var data = await wow.loadData('./datacrawler/output.json')

    const json_transform = (query_string, json_data) => jp.query(json_data, query_string)

    const json_sink = (file, json_data) => {
        fs.writeFile(file, JSON.stringify(json_data), 'utf8', (err) => console.log(err))
        return json_data;
    };

    const transform = R.pipe(
        R.curry(json_transform)('$.expansions[7].instances[*]'),
        R.curry(json_transform)('$..[?(@.instance.id == 1190)]'),
        R.curry(json_sink)('raids.json')
    )

    console.log(transform(data))



})();

