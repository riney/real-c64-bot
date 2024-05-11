#!/usr/bin/env node
const amqp = require('amqplib');
const masto = require('masto');

const queue = 'messages';
const rabbitmq_host = process.env.RABBITMQ_HOST;
const rabbitmq_user = process.env.RABBITMQ_USER;
const rabbitmq_pass = process.env.RABBITMQ_PASS;

(async () => {
  let connection;
  try {
    console.log(`Connecting to queue at ${rabbitmq_host}`);
    connection = await amqp.connect(`amqp://${rabbitmq_user}:${rabbitmq_pass}@${rabbitmq_host}`);
    const channel = await connection.createChannel();
    await channel.assertQueue(queue, { durable: true });

    // const masto = createRestAPIClient({
    //   url: process.env.URL,
    //   accessToken: process.env.TOKEN,
    // });
    
    // channel.sendToQueue(queue, Buffer.from(text), { persistent: true });
    // console.log(" [x] Sent '%s'", text);
    
    await channel.close();
  }
  catch (err) {
    console.warn(err);
  }
  finally { 
    console.log("Closing.")
    await connection.close();
  };
})();