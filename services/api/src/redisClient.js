const { createClient } = require('redis');

const redisUrl = process.env.REDIS_URL || 'redis://redis:6379';

const redisClient = createClient({ url: redisUrl });

redisClient.on('error', (err) => {
  console.error('Redis client error', err);
});

async function connectRedis() {
  if (!redisClient.isOpen) {
    await redisClient.connect();
    console.log(`Connected to Redis at ${redisUrl}`);
  }
  return redisClient;
}

function getRedis() {
  if (!redisClient.isOpen) {
    throw new Error('Redis client is not connected yet.');
  }
  return redisClient;
}

module.exports = {
  connectRedis,
  getRedis,
};


