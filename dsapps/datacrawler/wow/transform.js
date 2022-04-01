import _ from 'lodash';
import lo from 'lodash';
import * as json from '../json/index.js';

export const filterInstanceId = (instanceId, expansionIdx = 7) => {
    return json.transform(
        `expansions[${expansionIdx}].instances[instance.id = ${instanceId}]`
    )
}

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
    result = result || {}
    const process = (el) => lo.update(result, el.name, (el2) => _.assign(el2, { [key]: el.kills }))
    lo.forEach(value, process)
    return result;
}, {})