import lo from 'lodash';
import * as json from '../json/index.js';

export const filterInstanceId = (id) => json.transform(`expansions[7].instances[instance.id = ${id}]`)

const query = `
    modes{
        difficulty.type: progress.encounters.$.{
            "name": encounter.name,
            "kills": completed_count
        }
    }
`
export const extractKillsPerDifficulty = () => json.transform(query)

export const transformToKillsPerBoss = (data) => lo.transform(data, (result, value, key) => {
    const process = (el) => (result[el.name] || (result[el.name] = [])).push({ [key]: el.kills })
    lo.forEach(value, process)
    return result;
}, {})