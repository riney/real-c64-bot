const Eris = require('eris');
const Connection = require('rabbitmq-client')

require('dotenv').config()

const BOT_CHANNEL = process.env.channel || 'bot-test'

// Replace TOKEN with your bot account's token
const eris = new Eris.CommandClient(process.env.DISCORD_TOKEN, {}, {
    description: "A test bot made with Eris",
    owner: "somebody",
    prefix: "!",
    intents: [
        "guilds",
        "guildMessages"
    ]
});

eris.on("ready", () => {
    console.log("Discord gateway in startup.");
});

eris.on("error", (err) => {
    console.error(err); // or your preferred logger
});

eris.on("messageCreate", (msg) => { // When a message is created
    mentions = msg.mentions.map(user => user.username);
    if(msg.channel.name === BOT_CHANNEL && mentions.includes('realc64bot')) {
        console.log(`mentioned me! content = ${msg.cleanContent}`);
        eris.createMessage(msg.channel.id, `Pong! msg = ${msg.cleanContent}`);
    }
  });

eris.connect();
