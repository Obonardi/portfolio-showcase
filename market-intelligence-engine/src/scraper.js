const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const { Parser } = require('json2csv');

async function aggregateData() {
    console.log("Starting data aggregation...");
    
    // Target: A tech news site
    const url = 'https://news.ycombinator.com/';
    
    try {
        const { data } = await axios.get(url);
        const $ = cheerio.load(data);
        const results = [];

        // Selecting titles and links
        $('.titleline > a').each((i, el) => {
            results.push({
                title: $(el).text(),
                link: $(el).attr('href'),
                scrapedAt: new Date().toISOString()
            });
        });

        // Save to CSV
        const parser = new Parser();
        const csv = parser.parse(results);
        
        if (!fs.existsSync('./data')){
            fs.mkdirSync('./data');
        }
        
        fs.writeFileSync('./data/output.csv', csv);
        console.log('Success! Data saved to ./data/output.csv');
        
    } catch (error) {
        console.error('Error fetching the data:', error);
    }
}

aggregateData();