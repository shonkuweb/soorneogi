const usePostgres = !!process.env.DATABASE_URL;

let pool;

if (usePostgres) {
    const { Pool } = require('pg');
    pool = new Pool({
        connectionString: process.env.DATABASE_URL
    });

    pool.initDB = async function() {
        try {
            await pool.query(`
                CREATE TABLE IF NOT EXISTS enquiries (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    email TEXT,
                    message TEXT,
                    product TEXT,
                    timestamp TEXT
                )
            `);
            await pool.query(`
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    category TEXT,
                    price TEXT,
                    status TEXT
                )
            `);
            await pool.query(`
                CREATE TABLE IF NOT EXISTS contents (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            `);
            const res = await pool.query(`SELECT count(*) as count FROM contents`);
            if (parseInt(res.rows[0].count) === 0) {
                await pool.query(
                    `INSERT INTO contents (key, value) VALUES 
                    ($1, $2), ($3, $4), ($5, $6)`,
                    [
                        'home_hero_title', 'A Century of Quality & Reliability',
                        'home_hero_subtitle', 'Precision engineered industrial pipe solutions for global infrastructure and heavy manufacturing sectors.',
                        'about_mission_title', 'Transforming Tradition into Modern Excellence'
                    ]
                );
            }
            console.log('Connected to PostgreSQL database and initialized tables.');
        } catch (err) {
            console.error('Error initializing PostgreSQL database', err);
        }
    };
} else {
    const sqlite3 = require('sqlite3').verbose();
    const path = require('path');
    
    const dbPath = path.resolve(__dirname, 'snc_database.sqlite');
    const db = new sqlite3.Database(dbPath);

    pool = {
        query: function(sql, params = []) {
            return new Promise((resolve, reject) => {
                // Convert $1, $2... to ? for sqlite
                const sqliteSql = sql.replace(/\$\d+/g, '?');
                
                // If it's a SELECT or returning query, we use db.all
                if (sqliteSql.trim().toUpperCase().startsWith('SELECT') || sqliteSql.toUpperCase().includes('RETURNING')) {
                    db.all(sqliteSql, params, function(err, rows) {
                        if (err) reject(err);
                        else resolve({ rows: rows || [] });
                    });
                } else {
                    db.run(sqliteSql, params, function(err) {
                        if (err) reject(err);
                        else resolve({ rows: [], insertId: this.lastID });
                    });
                }
            });
        },
        initDB: async function() {
            try {
                await pool.query(`
                    CREATE TABLE IF NOT EXISTS enquiries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        phone TEXT,
                        email TEXT,
                        message TEXT,
                        product TEXT,
                        timestamp TEXT
                    )
                `);
                await pool.query(`
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        category TEXT,
                        price TEXT,
                        status TEXT
                    )
                `);
                await pool.query(`
                    CREATE TABLE IF NOT EXISTS contents (
                        key TEXT PRIMARY KEY,
                        value TEXT
                    )
                `);
                const res = await pool.query(`SELECT count(*) as count FROM contents`);
                if (parseInt(res.rows[0].count) === 0) {
                    await pool.query(
                        `INSERT INTO contents (key, value) VALUES 
                        ($1, $2), ($3, $4), ($5, $6)`,
                        [
                            'home_hero_title', 'A Century of Quality & Reliability',
                            'home_hero_subtitle', 'Precision engineered industrial pipe solutions for global infrastructure and heavy manufacturing sectors.',
                            'about_mission_title', 'Transforming Tradition into Modern Excellence'
                        ]
                    );
                }
                console.log('Connected to local SQLite database and initialized tables.');
            } catch (err) {
                console.error('Error initializing SQLite database', err);
            }
        }
    };
}

pool.initDB();

module.exports = pool;
