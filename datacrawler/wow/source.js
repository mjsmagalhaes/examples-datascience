import { JSONSource } from "../json/source.js";

export class WoWSource extends JSONSource {
    constructor() {
        super()
        this.base_url = 'https://us.api.blizzard.com/profile/wow';
    }

    async initialize() {
        try {
            var authData = await this.loadAuthData();
            this.token = authData.access_token;
            console.log(authData)
            console.log(new Date(authData.expiration))
        } catch (e) {

        }

        // if (!authData) {
        //     return
        // }
    }

    async getProfileRaids(char, realm) {
        var url = `${this.base_url}/character/${realm}/${char}/encounters/raids?namespace=profile-us&locale=en_US&access_token=${this.token}`;
        return await this.get_data(url)
    }
}