// src/api.js
import { BASE_URL } from './config';

// --------- LOGIN ---------
export const login = (correo, contrasena) => {
  const formData = new FormData();
  formData.append('correo', correo);
  formData.append('contrasena', contrasena);

  return fetch(`${BASE_URL}/login`, {
    method: 'POST',
    body: formData,
    mode: 'cors' // para render
  });
};
// ---------------------- REGISTRO ----------------------
export const registrarUsuario = (formData) =>
  fetch(`${BASE_URL}/registro`, {
    method: 'POST',
    body: formData,
    mode: 'cors'
  });

export async function recuperarContrasena(correo) {
  const formData = new FormData()
  formData.append("correo", correo)
  return fetch(`${BASE_URL}/recuperar-contrasena`, {
    method: 'POST',
    body: formData
  })
}

export async function restablecerContrasena(token, nuevaContrasena) {
  const formData = new FormData()
  formData.append("token", token)
  formData.append("nuevaContrasena", nuevaContrasena)
  return fetch(`${BASE_URL}/restablecer-contrasena`, {
    method: 'POST',
    body: formData
  })
}



//--------------Ver datos a editar-----------
// Obtener datos del perfil
export const obtenerPerfil = async (id) => {
  const res = await fetch(`${BASE_URL}/usuarios/${id}`)
  if (!res.ok) throw new Error()
  return await res.json()
}

// Actualizar perfil
export const actualizarPerfil = async (id, formData) => {
  const res = await fetch(`${BASE_URL}/usuarios/${id}`, {
    method: 'PUT',
    body: formData
  })
  if (!res.ok) throw new Error()
  return await res.json()
}


// CATEGORÍAS
export const fetchCategorias = () => fetch(`${BASE_URL}/categorias`).then(res => res.json())
export const crearNuevaCategoria = (nombre) => {
  const formData = new FormData()
  formData.append('nombre', nombre)
  return fetch(`${BASE_URL}/categorias`, { method: 'POST', body: formData })
}
export const actualizarCategoria = (id, nombre) => {
  const formData = new FormData()
  formData.append('nombre', nombre)
  return fetch(`${BASE_URL}/categorias/${id}`, { method: 'PUT', body: formData })
}
export const eliminarCategoriaPorId = (id) =>
  fetch(`${BASE_URL}/categorias/${id}`, { method: 'DELETE' })

// PRODUCTOS
export const fetchProductos = () => fetch(`${BASE_URL}/productos`).then(res => res.json())
export const crearProducto = (formData) =>
  fetch(`${BASE_URL}/productos`, {
    method: 'POST',
    body: formData,
    mode: 'cors'
  });

export const actualizarProducto = (id, formData) =>
  fetch(`${BASE_URL}/productos/${id}`, { method: 'PUT', body: formData })
export const eliminarProductoPorId = (id) =>
  fetch(`${BASE_URL}/productos/${id}`, { method: 'DELETE' })

export const toggleDisponibilidadProducto = (id) =>
  fetch(`${BASE_URL}/productos/${id}/toggle-disponible`, {
    method: 'PUT',
    mode: 'cors'
  });
// --- ÓRDENES (Cocina) ---
export const fetchOrdenes = () =>
  fetch(`${BASE_URL}/ordenes`, { method: 'GET', mode: 'cors' }).then(res => res.json())

export const marcarOrdenComoEntregada = (id) =>
  fetch(`${BASE_URL}/ordenes/${id}/entregado`, {
    method: 'PUT',
    mode: 'cors'
  }).then(res => res.json())

export const cancelarOrdenCocina = async (id) => {
  const res = await fetch(`${BASE_URL}/ordenes/${id}/cancelar-por-cocina`, {
    method: 'PATCH',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  if (res.ok) {
    return { success: true, ...(await res.json()) }
  } else {
    const err = await res.json().catch(() => ({}))
    return { success: false, detail: err.detail || 'Error al cancelar desde cocina' }
  }
}



// EMPLEADOS
export const crearEmpleado = (formData) =>
  fetch(`${BASE_URL}/empleados`, { method: 'POST', body: formData })

export const fetchEmpleados = () =>
  fetch(`${BASE_URL}/empleados`).then(res => res.json())

export const actualizarEmpleadoPorId = (id, formData) =>
  fetch(`${BASE_URL}/empleados/${id}`, {
    method: 'PUT',
    body: formData
  })


export const eliminarEmpleadoPorId = (id) =>
  fetch(`${BASE_URL}/empleados/${id}`, { method: 'DELETE' })

// --------- MENÚ ---------
export const fetchMenu = () =>
  fetch(`${BASE_URL}/menu`, { method: 'GET', mode: 'cors' }).then(res => res.json())

// --- ÓRDENES (Cliente) ---
export const fetchOrdenesCliente = (usuario_id) =>
  fetch(`${BASE_URL}/ordenes/cliente/${usuario_id}`, { method: 'GET', mode: 'cors' }).then(res => res.json())

export const enviarOrden = (payload) =>
  fetch(`${BASE_URL}/ordenar`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    mode: 'cors'
  }).then(res => res.json())

export const cancelarOrdenPorCliente = (id) =>
  fetch(`${BASE_URL}/ordenes/${id}/cancelar-por-cliente`, {
    method: 'PATCH',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    }
  })



// INVENTARIO
export const fetchInventario = () =>
  fetch(`${BASE_URL}/inventario`).then(res => res.json());

export const agregarInsumo = (formData) =>
  fetch(`${BASE_URL}/inventario`, {
    method: 'POST',
    body: formData,
    mode: 'cors'
  });

export const actualizarCantidadInsumo = (id, formData) =>
  fetch(`${BASE_URL}/inventario/${id}`, {
    method: 'PUT',
    body: formData
  });

export const editarNombreUnidadInsumo = (id, formData) =>
  fetch(`${BASE_URL}/inventario/${id}/editar`, {
    method: 'PUT',
    body: formData
  });

export const eliminarInsumoPorId = (id) =>
  fetch(`${BASE_URL}/inventario/${id}`, { method: 'DELETE' });

export const consumirInsumo = (id, formData) =>
  fetch(`${BASE_URL}/inventario/${id}/consumir`, {
    method: 'POST',
    body: formData
  });

//  NUEVA función para reabastecer insumo
export const reabastecerInsumo = (id, formData) =>
  fetch(`${BASE_URL}/inventario/${id}/reabastecer`, {
    method: 'POST',
    body: formData
  });
  
export const obtenerHistorialInventario = () =>
  fetch(`${BASE_URL}/inventario/historial`).then(res => res.json());

export const deshacerUltimoMovimiento = (id) =>
  fetch(`${BASE_URL}/inventario/${id}/deshacer_ultimo`, {
    method: 'POST',
    mode: 'cors'  // Asegura que Vite pueda hablar con FastAPI
  });



export const descargarInventarioPDF = () =>
  window.open(`${BASE_URL}/inventario/pdf`, "_blank");
// ---------------------- CAJA ----------------------

export const guardarCorteCaja = (corte) =>
  fetch(`${BASE_URL}/caja`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(corte),
    mode: 'cors'
  });

export const fetchCortesCaja = () =>
  fetch(`${BASE_URL}/caja`, { method: 'GET', mode: 'cors' }).then(res => res.json());
// GRAFICAS
export const fetchTopProductos = () =>
  fetch(`${BASE_URL}/graficas/top-productos`).then(res => res.json())

export const fetchTopClientes = () =>
  fetch(`${BASE_URL}/graficas/top-clientes`).then(res => res.json())

export const fetchProductoMenosPedido = () =>
  fetch(`${BASE_URL}/productos/menos-pedido`).then(res => res.json())


