const express = require('express');
const cors = require('cors');
const path = require('path');
const pool = require('./database');
const jwt = require('jsonwebtoken');

const app = express();
app.use(cors());
app.use(express.json());

const JWT_SECRET = process.env.JWT_SECRET || 'snc_super_secret_key_123';

// JWT Verification Middleware
const verifyJWT = (req, res, next) => {
    const authHeader = req.headers.authorization;
    if (authHeader) {
        const token = authHeader.split(' ')[1];
        jwt.verify(token, JWT_SECRET, (err, user) => {
            if (err) return res.status(403).json({ error: 'Token is invalid or expired' });
            req.user = user;
            next();
        });
    } else {
        res.status(401).json({ error: 'Authorization token required' });
    }
};

// Serve static files (HTML, CSS, JS)
app.use(express.static(__dirname));

// ==================================
// Auth API
// ==================================
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    
    // Hardcoded credentials for prototype
    if (username === 'admin' && password === 'password123') {
        const token = jwt.sign({ username }, JWT_SECRET, { expiresIn: '24h' });
        res.json({ token, status: 'success' });
    } else {
        res.status(401).json({ error: 'Invalid username or password' });
    }
});

// ==================================
// Enquiries API
// ==================================
app.post('/api/enquiries', async (req, res) => { // Public endpoint for website
    const { name, phone, email, message, product } = req.body;
    const timestamp = new Date().toISOString();
    
    try {
        const result = await pool.query(
            `INSERT INTO enquiries (name, phone, email, message, product, timestamp) VALUES ($1, $2, $3, $4, $5, $6) RETURNING id`,
            [name, phone, email, message, product || 'General', timestamp]
        );
        res.json({ id: result.rows[0].id, status: 'success' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.get('/api/enquiries', verifyJWT, async (req, res) => { // Protected
    try {
        const result = await pool.query(`SELECT * FROM enquiries ORDER BY timestamp DESC`);
        res.json(result.rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.delete('/api/enquiries', verifyJWT, async (req, res) => { // Protected
    try {
        await pool.query(`DELETE FROM enquiries`);
        res.json({ status: 'success' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// ==================================
// Products API
// ==================================
app.get('/api/products', async (req, res) => { // Public
    try {
        const result = await pool.query(`SELECT * FROM products`);
        res.json(result.rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/products', verifyJWT, async (req, res) => { // Protected
    const { name, category, price, status } = req.body;
    try {
        const result = await pool.query(
            `INSERT INTO products (name, category, price, status) VALUES ($1, $2, $3, $4) RETURNING id`,
            [name, category, price, status]
        );
        res.json({ id: result.rows[0].id, status: 'success' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.delete('/api/products/:id', verifyJWT, async (req, res) => { // Protected
    try {
        await pool.query(`DELETE FROM products WHERE id = $1`, [req.params.id]);
        res.json({ status: 'success' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// ==================================
// Content API (CMS)
// ==================================
app.get('/api/content', async (req, res) => { // Public (Website reads this)
    try {
        const result = await pool.query(`SELECT * FROM contents`);
        const contentMap = {};
        result.rows.forEach(row => contentMap[row.key] = row.value);
        res.json(contentMap);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/content', verifyJWT, async (req, res) => { // Protected
    const contents = req.body; 
    try {
        for (const [key, value] of Object.entries(contents)) {
            await pool.query(
                `INSERT INTO contents (key, value) VALUES ($1, $2) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value`,
                [key, value]
            );
        }
        res.json({ status: 'success' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// ==================================
// Stats API
// ==================================
app.get('/api/stats', verifyJWT, async (req, res) => { // Protected
    try {
        let stats = { enquiries: 0, products: 0, today: 0 };
        
        const enqResult = await pool.query(`SELECT count(*) as count FROM enquiries`);
        stats.enquiries = parseInt(enqResult.rows[0].count);
        
        const todayStr = new Date().toISOString().split('T')[0];
        const todayResult = await pool.query(`SELECT count(*) as count FROM enquiries WHERE timestamp LIKE $1`, [`${todayStr}%`]);
        stats.today = parseInt(todayResult.rows[0].count);
        
        const prodResult = await pool.query(`SELECT count(*) as count FROM products`);
        stats.products = parseInt(prodResult.rows[0].count);

        res.json(stats);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Start Server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
