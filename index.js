require('dotenv').config();
const express = require('express');
const { MongoClient, ObjectId } = require('mongodb');

const app = express();
app.use(express.json());

const port = process.env.PORT || 8000;
const mongoUri = process.env.MONGODB_URI;
const dbName = process.env.MONGODB_DB_NAME;
const collectionName = process.env.MONGODB_COLLECTION_NAME || 'items';

if (!mongoUri || !dbName) {
  console.error('Missing MONGODB_URI or MONGODB_DB_NAME in .env');
  process.exit(1);
}

const mongoClient = new MongoClient(mongoUri);
let collection;

async function getCollection() {
  if (!collection) {
    await mongoClient.connect();
    collection = mongoClient.db(dbName).collection(collectionName);
  }
  return collection;
}

app.get('/', (req, res) => {
  res.send('Hello, world! With db');
});

app.get('/api/items', async (req, res) => {
  try {
    const limit = Math.min(Number(req.query.limit) || 20, 100);
    const dbCollection = await getCollection();
    const items = await dbCollection.find({}).limit(limit).toArray();
    res.json(items);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch items' });
  }
});

app.get('/api/items/:id', async (req, res) => {
  try {
    const { id } = req.params;

    if (!ObjectId.isValid(id)) {
      return res.status(400).json({ error: 'Invalid id format' });
    }

    const dbCollection = await getCollection();
    const item = await dbCollection.findOne({ _id: new ObjectId(id) });

    if (!item) {
      return res.status(404).json({ error: 'Item not found' });
    }

    return res.json(item);
  } catch (error) {
    return res.status(500).json({ error: 'Failed to fetch item' });
  }
});

app.post('/api/items', async (req, res) => {
  try {
    const payload = req.body;

    if (!payload || typeof payload !== 'object' || Array.isArray(payload) || Object.keys(payload).length === 0) {
      return res.status(400).json({ error: 'Request body must be a non-empty JSON object' });
    }

    const { _id, ...itemData } = payload;
    const dbCollection = await getCollection();
    const result = await dbCollection.insertOne(itemData);
    const createdItem = await dbCollection.findOne({ _id: result.insertedId });

    return res.status(201).json(createdItem || { _id: result.insertedId, ...itemData });
  } catch (error) {
    return res.status(500).json({ error: 'Failed to create item' });
  }
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port} with db`);
});

process.on('SIGINT', async () => {
  await mongoClient.close();
  process.exit(0);
});
