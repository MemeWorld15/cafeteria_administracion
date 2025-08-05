const fs = require('fs');
const path = require('path');
const pool = require('./db'); // tu archivo de conexión a PostgreSQL

async function ejecutarSetup() {
  try {
    const sql = fs.readFileSync(path.join(__dirname, 'setup.sql')).toString();
    await pool.query(sql);
    console.log('✅ Tablas creadas correctamente.');
    process.exit(0);
  } catch (error) {
    console.error('❌ Error al crear las tablas:', error);
    process.exit(1);
  }
}

ejecutarSetup();
