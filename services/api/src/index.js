const dotenv = require('dotenv');
dotenv.config();

const express = require('express');
const cors = require('cors');
const morgan = require('morgan');

const jobsRouter = require('./routes/jobs');
const { connectRedis } = require('./redisClient');

const app = express();
const PORT = process.env.PORT || 8080;
const LOG_LEVEL = process.env.LOG_LEVEL || 'dev';

app.use(cors());
app.use(express.json());
app.use(morgan(LOG_LEVEL));

app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    uptime: process.uptime(),
    timestamp: new Date().toISOString(),
  });
});

app.use('/jobs', jobsRouter);

app.use((err, req, res, _next) => {
  console.error('API error', err);
  res.status(err.status || 500).json({
    error: err.message || 'Internal server error',
  });
});

async function bootstrap() {
  try {
    await connectRedis();
    app.listen(PORT, () => {
      console.log(`API server listening on port ${PORT}`);
    });
  } catch (error) {
    console.error('Failed to start API server', error);
    process.exit(1);
  }
}

bootstrap();

