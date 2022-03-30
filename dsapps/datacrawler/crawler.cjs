//index.js
const rp = require('request-promise')
const cheerio = require('cheerio')
const fs = require('fs');
const path = require('path');
var https = require('https');

const { Command } = require('commander');
const chalk = require('chalk');
const Table = require('cli-table')
const { snakeCase } = require('change-case')
const diacritics = require('remove-accents')
const string = require('string-sanitizer')

const program = new Command();
program.version('0.0.1');

program
    .command('save')
    .description('save a website to a local html file')
    .arguments('<url>')
    .option('-o, --output <file>','name of the output file', 'index.html')
    .action((url, options, command) => {
        // console.log(`cheese: ${program.opts().cheese}`);
        console.log(chalk.blue('== Running Command: Save =='));
        console.log(chalk.yellow('url:', url));
        console.log(chalk.yellow('file:', options.output));

        create_request(url);
        save_file(options.output)
    });

program
    .command('parse')
    .description('parse a local file to extract data')
    .arguments('<file>')
    .action((file, options, command) => {
        console.log(chalk.blue('== Running Command: Parse =='));
        console.log(chalk.yellow('file:', file));

        let $ = load_file(file)
        parse($, file)
    });

program.parse();

function create_request(url) {
    return options = {
        uri: url,
        transform: function (body) {
            return cheerio.load(body)
        }
    }
}

function save_file(file) {
    rp(options)
    .then(($) => {
        fs.writeFileSync(path.join(process.cwd(), file), $.html(), {'encoding': 'utf-8'});
    })
    .catch((err) => {
        console.log(err);
    })
}

function load_file(file) {
    var $ = cheerio.load(fs.readFileSync(path.join(process.cwd(), file)));
    return $
}

function parse($, file) {
    let data = {};
    
    // let arr = file.split('\')
    // let pictures_dir = arr[arr.length - 1];
    let input_file = path.parse(file)
    pictures_dir = path.join(process.cwd(), input_file.dir, input_file.name)

    if(!fs.existsSync(pictures_dir))
        fs.mkdirSync(pictures_dir);
    

    // --- Images ---
    let promises = []
    $('li > img').each((index, el) => {
        let url = el.attribs.src
        console.log(url)

        if(!url.startsWith('http')) return

        let arr = url.split('/')
        let filename = arr[arr.length - 1];
        
        var download = function(url, dest, cb) {
            var stream = fs.createWriteStream(dest);
            return https.get(url, function(response) {
                response.pipe(stream);
                stream.on('finish', function() {
                    stream.close(cb);
                });
            });
        }

        setTimeout(() => {
            promises.push(download(url, path.join(pictures_dir, filename)))
        }, 2000);
    })
    
    
    // --- Nome da Suíte ---
    data.title = $.text($('h1.entry-title'))
    const cli_table = new Table({
        head: [chalk.green('Título')]
    });
    
    cli_table.push([chalk`{cyan ${data.title}}`])
    console.log(cli_table.toString())

    let json_name = `${ snakeCase(string.sanitize.keepSpace(diacritics(data.title))) }`;

    // --- Tabela de Horários - Preço
    data.table = [];
    let table = $('tbody', 'table.table')

    table.children().each((index, el) => {
        let horario = $.text(el.children[0].children)
        let preço = $.text(el.children[1].children)        
        data.table.push({ horario, preço })
    })

    const cli_table_1 = new Table({
        head: [chalk.green('Horário'), chalk.green('Preço')]
    });

    data.table.forEach((el) => {
        cli_table_1.push([chalk.cyan(el.horario), chalk.cyan(el.preço)])
    })
    console.log(cli_table_1.toString())


    // --- Informações: Features ---
    let info = $('div.col-md-12', 'div.entry-content').contents().toArray()
        .map(element => {
            if (element.type === 'text')
                return $(element).text().trim()
            
            if (element.tagName === 'strong')
                return $(element.children).text().trim()
                
            return null
        })
        .filter(text => text)
    
    data.features = info[0].split(' - ')

    const cli_table_2 = new Table({
        head: [chalk.green('Features')]
    });

    data.features.forEach(element => {
        cli_table_2.push([element])
    });
    
    console.log(cli_table_2.toString())
    
    // --- Informações: Extras ---
    data.info = info.filter((el, idx) => idx > 0)
    
    const cli_table_3 = new Table({
        head: [chalk.green('Informações Adicionais')]
    });
    
    data.info.forEach(element => {
        cli_table_3.push([element])
    });
    console.log(cli_table_3.toString())

    fs.writeFileSync(json_name + '.json', JSON.stringify(data, null, 2))

    Promise.all(promises)
}



