const express = require('express');
const { v4: uuid } = require('uuid');
const { getRedis } = require('../redisClient');

const router = express.Router();

const JOB_QUEUE_KEY = process.env.JOB_QUEUE_KEY || 'cloud:jobs';
const JOB_HASH_PREFIX = process.env.JOB_HASH_PREFIX || 'cloud:job:';
const JOB_INDEX_KEY = `${JOB_QUEUE_KEY}:index`;
const MAX_JOBS_RETURNED = 20;
const MAX_JOB_HISTORY = 100;

const jobKey = (id) => `${JOB_HASH_PREFIX}${id}`;

const parseJson = (value) => {
  if (!value) return null;
  try {
    return JSON.parse(value);
  } catch (_err) {
    return value;
  }
};

const presentJob = (id, raw) => ({
  jobId: id,
  status: raw.status,
  payload: parseJson(raw.payload),
  result: parseJson(raw.result),
  error: raw.error || null,
  createdAt: raw.createdAt,
  startedAt: raw.startedAt || null,
  completedAt: raw.completedAt || null,
});

router.post('/', async (req, res, next) => {
  try {
    const { text } = req.body || {};
    if (!text || typeof text !== 'string') {
      return res.status(400).json({ error: '`text` (string) is required' });
    }
    if (text.length > 1000) {
      return res.status(400).json({ error: 'text must be 1000 characters or fewer' });
    }

    const jobId = uuid();
    const now = new Date().toISOString();

    const redis = getRedis();
    await redis.hSet(jobKey(jobId), {
      status: 'queued',
      createdAt: now,
      payload: JSON.stringify({ text }),
    });
    await redis.zAdd(JOB_INDEX_KEY, [{ score: Date.now(), value: jobId }]);
    const totalJobs = await redis.zCard(JOB_INDEX_KEY);
    if (totalJobs > MAX_JOB_HISTORY) {
      await redis.zRemRangeByRank(JOB_INDEX_KEY, 0, totalJobs - MAX_JOB_HISTORY - 1);
    }
    await redis.rPush(JOB_QUEUE_KEY, JSON.stringify({ jobId, payload: { text } }));

    return res.status(202).json({ jobId, status: 'queued' });
  } catch (error) {
    return next(error);
  }
});

router.get('/', async (_req, res, next) => {
  try {
    const redis = getRedis();
    const ids = (await redis.zRange(JOB_INDEX_KEY, -MAX_JOBS_RETURNED, -1)).reverse();
    const jobsRaw = await Promise.all(ids.map((id) => redis.hGetAll(jobKey(id))));
    const jobs = ids.map((id, idx) => presentJob(id, jobsRaw[idx] || {}));

    return res.json({ jobs });
  } catch (error) {
    return next(error);
  }
});

router.get('/:id', async (req, res, next) => {
  try {
    const { id } = req.params;
    const redis = getRedis();
    const raw = await redis.hGetAll(jobKey(id));

    if (!raw || Object.keys(raw).length === 0) {
      return res.status(404).json({ error: `Job ${id} not found` });
    }

    return res.json(presentJob(id, raw));
  } catch (error) {
    return next(error);
  }
});

module.exports = router;

