import fs from 'fs';
import got from 'got';


// JSONSource / HTMLSource / GraphQLSource ?
export class Source {
    async getAuthToken() {
        const data = await got.got(`https://us.battle.net/oauth/token`, {
            method: 'POST',
            form: { client_id, client_secret, grant_type: 'client_credentials' }
        }).json()

        data.expiration = Date.now() + (data.expires_in * 1000)

        fs.writeFile("credentials.json", JSON.stringify(data), 'utf8', (err) => {
            if (err) { console.log(err) }
        });
        return data
    }

    async loadAuthData() {
        var data = await load_data('credentials.json');

        if (data === undefined || data.expiration < Date.now()) {
            console.log('Obtaining new token ...')
            data = await getAuthToken()
        }

        return data
    }

    async getData(url) {
        const response = await got.got(url).json();

        fs.writeFile("output.json", JSON.stringify(response), 'utf8', (err) => console.log(err));

        return response;
    }
}