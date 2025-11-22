
// index.js
const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Health check
app.get('/health', (_req, res) => {
    res.json({ ok: true, service: 'jurassic-spark-backend' });
});

// Root route
app.get('/', (_req, res) => {
    res.send('🦖 Jurassic Spark backend is running!');
});

// Start server
app.listen(PORT, () => {
    console.log(`[server] Listening on http://localhost:${PORT}`);
});
