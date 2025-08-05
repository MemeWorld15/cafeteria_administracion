
-- Tabla de usuarios
CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100),
  correo VARCHAR(100) UNIQUE,
  contraseña VARCHAR(100),
  grado VARCHAR(50),
  carrera VARCHAR(50),
  rol TEXT CHECK (rol IN ('admin', 'cliente', 'empleado', 'chef')) DEFAULT 'cliente',
  ocupacion VARCHAR(50)
);

-- Tabla de empleados
CREATE TABLE empleados (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100),
  correo VARCHAR(100) UNIQUE,
  ocupacion VARCHAR(100),
  rendimiento VARCHAR(100),
  foto TEXT,
  contraseña VARCHAR(255),
  creado_por INT,
  FOREIGN KEY (creado_por) REFERENCES usuarios(id)
);

-- Tabla de categorías
CREATE TABLE categorias (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla de productos
CREATE TABLE productos (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT,
  precio NUMERIC(10, 2),
  categoria_id INT,
  disponible BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Tabla de órdenes
CREATE TABLE ordenes (
  id SERIAL PRIMARY KEY,
  cliente VARCHAR(100) NOT NULL,
  nota TEXT,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  entregado BOOLEAN DEFAULT FALSE,
  usuario_id INT,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- Tabla intermedia: productos por orden
CREATE TABLE orden_productos (
  id SERIAL PRIMARY KEY,
  orden_id INT,
  nombre_producto VARCHAR(100),
  cantidad INT,
  precio_unitario NUMERIC(10,2),
  FOREIGN KEY (orden_id) REFERENCES ordenes(id) ON DELETE CASCADE
);

-- Tabla de inventario
CREATE TABLE inventario (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  cantidad FLOAT NOT NULL,
  unidad VARCHAR(20) NOT NULL
);

-- Insertar usuario administrador
INSERT INTO usuarios (nombre, correo, contraseña, rol)
VALUES ('Admin', 'admin@cafe.com', 'admin123', 'admin');
