import fs from 'fs';
import * as R from 'ramda';

export async function fromFile(file) {
    if (!fs.existsSync(file)) {
        console.log(`ERROR: Couldn't find ${file}.`)
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

export const toFile = R.curry(async (file, json_data) => {
    fs.writeFile(file, JSON.stringify(json_data), 'utf8', (err) => {
        if (err) {
            console.error(err)
            return
        }
    })
    return json_data;
});