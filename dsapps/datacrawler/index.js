// import { Command } from 'commander';
// import chalk from 'chalk';

import { parseData, dataToTable } from "./query.js";
import * as json from './json/index.js';

(async () => {
    var data = await json.fromFile('./datacrawler/output.json');
    var parsedData = await parseData(data);
    console.log(dataToTable(parsedData).toString())
    json.toFile('raids.json', parsedData);
})();