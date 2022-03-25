const fs = require('fs');
const jp = require('jsonpath');
const R = require('ramda');
const keys = require('./keys')

var client_id = keys.client_id;
var client_secret = keys.client_secret;

// var url = `https://us.api.blizzard.com/profile/wow/character/azralon/yapriesty/statistics?namespace=profile-us&locale=en_US&access_token=${token}`;

async function getAuthToken() {
    const got = await import('got');
    const data = await got.got(`https://us.battle.net/oauth/token`, {
        method: 'POST',
        form: { client_id, client_secret, grant_type: 'client_credentials' }
    }).json()

    data.expiration = Date.now() + (data.expires_in * 1000)

    fs.writeFile("credential.json", JSON.stringify(data), 'utf8', (err) => {
        if (err) { console.log(err) }
    });
    return data
}

async function get_data(url) {
    const got = await import('got');
    const response = await got.got(url).json();

    fs.writeFile("output.json", JSON.stringify(response), 'utf8', (err) => console.log(err));

    return response;
}

async function load_data(file) {
    if (!fs.existsSync(file)) {
        return
    }

    return new Promise((resolve, reject) => {
        fs.readFile(file, 'utf8', (err, data) => {
            if (err) {
                console.error(err)
                return
            }
            // console.log(data)
            resolve(JSON.parse(data))
        });
    })
}

async function loadAuthData() {
    var data = await load_data('credential.json');

    if (data === undefined || data.expiration < Date.now()) {
        console.log('Obtaining new token ...')
        data = await getAuthToken()
    }

    return data
}

class WoW {
    constructor(token) {
        this.token = token;
    }

    async getProfileRaids(char, realm) {
        console.log(this.token)
        var url = `https://us.api.blizzard.com/profile/wow/character/${realm}/${char}/encounters/raids?namespace=profile-us&locale=en_US&access_token=${this.token}`;
        return await get_data(url)
    }
}

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

    var authData = null;

    try {
        authData = await loadAuthData();
        console.log(authData)
        console.log(new Date(authData.expiration))
    } catch (e) {

    }

    if (!authData) {
        return
    }

    var wow = new WoW(authData.access_token);

    // const data = await wow.getProfileRaids('yapriesty', 'azralon');

    var data = await load_data('output.json')
    var d2 = jp.query(data, '$.expansions[7].instances[*]')
    // console.log(d2)
    // console.log(jp.query(d2, '$..instance'))
    // console.log(jp.query(d2, '$..modes'))

    console.log(jp.query(d2, '$..[?(@.instance.id == 1190)]'))

})();

