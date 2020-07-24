const Redis = require('ioredis');
const request = require('request-promise');
const connection = new Redis(6379, 'redis');

const mackerelToken = process.env.MACKEREL_TOKEN || null;
const mackerelHostID = process.env.MACKEREL_HOST_ID || null;

// init
connection.set('queued_count', 0);
connection.set('proceeded_count', 0);

// publish tasks to workers
(async () => {
    const app = require('express')();
    const port = 8080;

    var bodyParser = require('body-parser');
    app.use(bodyParser());
    
    app.post('/query', (req, res) => {
        try {
            if (req.body.url !== undefined && req.body.url != ''){
                connection.rpush('query', req.body.url).then(() => {
                    connection.incr('queued_count')
                }).then(() => {
                    console.log(`[*] Queried: ${req.body.url}`);
                });
                res.send('Okay! I got it :-)');
            } else {
                res.send('Umm, there is something wrong ...');
            }
        } catch (e){
            res.send('Umm, there is something wrong ...');
        }
    });
    
    app.listen(port, () => {
        console.log(`Publisher is listening on port ${port}!`);
    });
})();

const report = async () => {
    const queued_count = await connection.get('queued_count');
    const proceeded_count = await connection.get('proceeded_count');

    if(mackerelToken && mackerelHostID) {
        request({
            method: 'POST',
            headers: {
                'X-Api-Key': mackerelToken,
            },
            url: 'https://api.mackerelio.com/api/v0/tsdb',
            json: [
                {
                    hostId: mackerelHostID,
                    name: 'ctfchal.note.queued-count',
                    time: 0|(Date.now() / 1000),
                    value: 0|queued_count,
                },
                {
                    hostId: mackerelHostID,
                    name: 'ctfchal.note.proceeded-count',
                    time: 0|(Date.now() / 1000),
                    value: 0|proceeded_count,
                },
            ],
        })
    }

    console.error(`[-] metrics: ${queued_count}, ${proceeded_count}`);
    setTimeout(report, 1000 * 15);
};
setTimeout(report, 1000 * 15);
