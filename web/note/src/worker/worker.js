const puppeteer = require('puppeteer');
const Redis = require('ioredis');
const connection = new Redis(6379, 'redis');

const browser_option = {
    product: 'firefox',
    headless: true,
};

const crawl = async (url) => {
    console.log(`[*] started: ${url}`)
    
    const browser = await puppeteer.launch(browser_option);
    const page = await browser.newPage();
    await page.setCookie({
        name: 'rack.session',
        value: process.env.COOKIE_VALUE,
        domain: process.env.DOMAIN,
        expires: Date.now() / 1000 + 10,
    });
    try {
        const resp = await page.goto(url, {
            waitUntil: 'load',
            timeout: 3000,
        });
    } catch (err){
        console.log(err);
    }
    await page.close();
    await browser.close();
    console.log(`[*] finished: ${url}`)
};

// handle the whole
function handle(){
    console.log("[*] waiting new query ...")
    connection.blpop("query", 0, async function(err, message) {
        const url = message[1];
        await crawl(url);
        await connection.incr("proceeded_count");
        setTimeout(handle, 10);
    });
}
handle();
