
<template>
  <div class="admin-app">
    <!-- Topbar -->
    <header class="admin-topbar">
      <div class="admin-topbar-logo">
        <img :src="logo" alt="Logo" />
        <div>
          <span class="admin-brand">Cafetería</span><br />
          <span class="admin-role">Administrador</span>
        </div>
      </div>
      <div class="top-right">
        <Icon :icon="isDarkMode ? 'mdi:moon-waning-crescent' : 'mdi:weather-sunny'" @click="toggleDarkMode" />
        <Icon icon="mdi:bell" />
        <img :src="fotoActual || defaultFoto" alt="Foto de perfil" class="perfil-imagen" />
        <!--<i class="fas fa-user"></i>-->
        <!-- Nuevo ícono de paleta -->
        <Icon icon="mdi:palette" @click="toggleThemeSettings" />
        
        <span class="admin-name">{{ nombreUsuario }}</span>
        <!--<i class="fas fa-chevron-down"></i>-->
        <div class="dropdown" @click="toggleDropdown">
          <Icon icon="mdi:chevron-down" />
          <div v-if="mostrarDropdown" class="dropdown-menu" @click.stop>
            <p class="usuario-nombre">{{ nombreUsuario }}</p>
            <hr />
            <button @click="editarPerfil">Editar perfil</button>
            <button class="logout-btn" @click="cerrarSesion">Cerrar sesión</button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Body -->
    <div class="admin-main-body">
      <!-- Sidebar -->
      <aside class="admin-sidebar" :class="{ collapsed: isCollapsed }">
        <div class="admin-toggle-btn" @click="toggleSidebar">
          <Icon icon="mdi:menu" />
        </div>
        <nav class="admin-nav">
          <ul>
            <li :class="{ active: vistaActual === 'menu' }" @click="cambiarVista('menu')">
              <Icon icon="mdi:silverware-fork-knife" /><span>Menú</span>
            </li>
            <li :class="{ active: vistaActual === 'graficas' }" @click="cambiarVista('graficas')">
              <Icon icon="mdi:chart-pie" /><span>Ventas</span>
            </li>
            <li :class="{ active: vistaActual === 'ordenes' }" @click="cambiarVista('ordenes')">
              <Icon icon="mdi:receipt" /><span>Órdenes</span>
            </li>
            <li :class="{ active: vistaActual === 'usuarios' }" @click="cambiarVista('usuarios')">
              <Icon icon="mdi:account-group" /><span>Usuarios</span>
            </li>
            <li :class="{ active: vistaActual === 'agregar-empleado' }" @click="cambiarVista('agregar-empleado')">
              <Icon icon="mdi:account-plus" /><span>Agregar Empleados</span>
            </li>
            <li :class="{ active: vistaActual === 'inventario' }" @click="cambiarVista('inventario')">
              <Icon icon="mdi:package-variant" /><span>Inventario</span>
            </li>
            <li :class="{ active: vistaActual === 'caja' }" @click="cambiarVista('caja')">
              <Icon icon="mdi:cash-register" /><span>Caja</span>
            </li>
            <li :class="{ active: vistaActual === 'historial' }" @click="cambiarVista('historial')">
              <Icon icon="mdi:history" /><span>Historial</span>
            </li>
            <li :class="{ active: vistaActual === 'historial-inventario' }" @click="cambiarVista('historial-inventario')">
              <Icon icon="mdi:clipboard-list" /><span>Historial Inventario</span>
            </li>
          </ul>
        </nav>
        <div class="admin-settings">
          <Icon icon="mdi:cog" /><span>Configuración</span>
        </div>
      </aside>

      <!-- Main Content -->
      <div class="admin-content">
        <h2>Bienvenido al Panel de Administración</h2>
        <EditarPerfil v-if="vistaActual === 'editar-perfil'" @foto-actualizada="actualizarFoto" />


        <UsuariosCard v-if="vistaActual === 'usuarios'" />
        <div v-if="vistaActual === 'ordenes'">
  <h3>Órdenes registradas</h3>
  <div style="margin-bottom: 1rem;">
  <label for="filtroEstado"><strong>Filtrar por estado:</strong></label>
  <select v-model="filtroEstado" id="filtroEstado" style="margin-left: 0.5rem;">
    <option value="todos">Todos</option>
    <option value="pendientes">Pendientes</option>
    <option value="entregados">Entregados</option>
    <option value="cancelados">Cancelados</option>
  </select>
</div>

  <table class="tabla-ordenes">
  <thead>
    <tr>
      <th>ID</th>
      <th>Cliente</th>
      <th>Fecha</th>
      <th>Hora</th>
      <th>Total</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="orden in ordenesFiltradas" :key="orden.id">
      <td>{{ orden.id }}</td>
      <td>{{ orden.cliente }}</td>
      <td>{{ orden.fecha_mostrada }}</td>
      <td>{{ orden.hora }}</td>
      <td>
        ${{ orden.productos.reduce((acc, p) => acc + p.cantidad * p.precio_unitario, 0).toFixed(2) }}
      </td>
      <td>
        <span :class="orden.cancelada ? 'cancelado' : (orden.entregado ? 'entregado' : 'no-entregado')">
          {{ orden.cancelada ? 'Cancelada' : (orden.entregado ? 'Entregado' : 'Pendiente') }}
        </span>
      </td>
    </tr>
  </tbody>
</table>

</div>

        <Empleado v-if="vistaActual === 'agregar-empleado'" @empleado-creado="obtenerOrdenes" />

        <!-- Formulario para gestionar el menú -->
        <div v-if="vistaActual === 'menu'" class="admin-menu-form">
          <h3>Agregar Categoría</h3>
          <form @submit.prevent="crearCategoria">
            <input v-model="nuevaCategoria" type="text" placeholder="Nombre de categoría" required />
            <button type="submit">Agregar Categoría</button>
          </form>
          <!-- Identar muy bien -->
          <h3 style="margin-top: 2rem;">Categorías Existentes</h3>
          <ul class="lista-categorias">
            <li v-for="cat in categorias" :key="cat.id">
              <input v-if="categoriaEditando?.id === cat.id" v-model="categoriaEditando.nombre" />
              <span v-else>{{ cat.nombre }}</span>

              <button v-if="categoriaEditando?.id === cat.id" @click="guardarEdicionCategoria">Guardar</button>
              <button v-if="categoriaEditando?.id === cat.id" @click="cancelarEdicionCategoria">Cancelar</button>
              
              <button @click="iniciarEdicionCategoria(cat)"><Icon icon="mdi:pencil" /></button>
              <button @click="eliminarCategoria(cat.id)"><Icon icon="mdi:trash-can" /></button>
            </li>
          </ul>


          <h3 style="margin-top: 2rem;">Agregar Producto</h3>
          <form @submit.prevent="crearProductoNuevo">
            <input v-model="nuevoProducto.nombre" type="text" placeholder="Nombre del producto" required />
            <textarea v-model="nuevoProducto.descripcion" placeholder="Descripción" required></textarea>
            <input v-model="nuevoProducto.precio" type="number" placeholder="Precio" required />
            <input type="file" @change="handleFileUpload" accept="image/*" />
            <select v-model="nuevoProducto.categoria_id" required>
              <option disabled value="">Seleccionar categoría</option>
              <option v-for="cat in categorias" :key="cat.id" :value="cat.id">{{ cat.nombre }}</option>
            </select>
            <button type="submit">Agregar Producto</button>
          </form>

          <!-- Productos existentes -->
          <h3 style="margin-top: 3rem;">Productos Existentes</h3>
          <table class="tabla-productos">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Precio</th>
                <th>Categoría</th>
                <th>Foto</th> <!-- 🚩 NUEVA COLUMNA -->
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="prod in productos" :key="prod.id">
                <td>{{ prod.nombre }}</td>
                <td>${{ prod.precio }}</td>
                <td>{{ categorias.find(cat => cat.id === prod.categoria_id)?.nombre || '—' }}</td>
                <!-- 🚩 Mostrar imagen -->
                  <td>
                    <img
                        v-if="prod.imagen_url"
                        :src="getImageUrl(prod.imagen_url)"
                        alt="Producto"
                        style="width: 60px; height: auto; border-radius: 6px; cursor: pointer;"
                        @click="abrirImagenModal(getImageUrl(prod.imagen_url))"
                      />

                    <span v-else style="color: gray;">Sin imagen</span>
                  </td>
                <td>
                  <button @click="editarProducto(prod)"><Icon icon="mdi:pencil" /></button>
                  <button @click="eliminarProducto(prod.id)"><Icon icon="mdi:trash-can" /></button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Formulario edición -->
          <div v-if="productoEditando" class="editar-producto-form">
            <h4>Editar Producto</h4>
            <input v-model="productoEditando.nombre" type="text" placeholder="Nombre" />
            <input v-model="productoEditando.precio" type="number" placeholder="Precio" />
            <textarea v-model="productoEditando.descripcion" placeholder="Descripción" />
            <select v-model="productoEditando.categoria_id">
              <option v-for="cat in categorias" :value="cat.id" :key="cat.id">{{ cat.nombre }}</option>
            </select>
            <input type="file" @change="handleFileUploadEdicion" accept="image/*" />
            <button @click="guardarEdicion">Guardar</button>
            <button @click="productoEditando = null">Cancelar</button>
          </div>

          <p v-if="mensajeMenu" :style="{ color: mensajeColor, marginTop: '1rem' }">{{ mensajeMenu }}</p>
        </div>
        <GraficasTop v-if="vistaActual === 'graficas'" />
        <Inventario v-if="vistaActual === 'inventario'" />
        <Caja v-if="vistaActual === 'caja'" />
        <Historial v-if="vistaActual === 'historial'" />
        <HistorialInventario v-if="vistaActual === 'historial-inventario'" />
      </div>
    </div>
  </div>
  <!-- Modal para vista de imagen -->
<div v-if="imagenModalVisible" class="modal-overlay" @click="cerrarImagenModal">
  <div class="modal-content" @click.stop>
    <img :src="imagenModalUrl" alt="Vista de Imagen" class="imagen-ampliada" />
    <button @click="cerrarImagenModal" class="cerrar-btn">Cerrar</button>
  </div>
</div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import Empleado from './Empleado.vue'
import logo from '../assets/images/Group.svg'
import UsuariosCard from './UsuariosCard.vue'
import Caja from './Caja.vue'
import EditarPerfil from './EditarPerfil.vue';
import { BASE_URL } from '../config';
//import '../EstilosCss/AdminStylo.css's
import '../EstilosCss/base.css'
import '../EstilosCss/layout.css'
import '../EstilosCss/topbar.css'
import '../EstilosCss/sidebar.css'
import '../EstilosCss/admins.css'
import '../EstilosCss/components.css'
import '../EstilosCss/dark-mode.css'
import GraficasTop from './GraficasTop.vue'
import Inventario from './Inventario.vue'
import Historial from './Historial.vue'
import HistorialInventario from './HistorialInventario.vue'

import {
  fetchCategorias,
  fetchProductos,
  obtenerPerfil,
  fetchOrdenes,
  crearNuevaCategoria,
  actualizarCategoria,
  eliminarCategoriaPorId,
  crearProducto,
  actualizarProducto,
  eliminarProductoPorId,
  //crearEmpleado as crearEmpleadoAPI
} from '../api'



const fotoActual = ref('')       // Aquí guardamos la foto del perfil
const defaultFoto = 'ruta/a/imagen/default.jpg'  // Ruta de la imagen por defecto

const isCollapsed = ref(false)
const vistaActual = ref('menu')
const cambiarVista = (vista) => { vistaActual.value = vista }
const toggleSidebar = () => { isCollapsed.value = !isCollapsed.value }

const isDarkMode = ref(false)
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  document.body.classList.toggle('dark-mode', isDarkMode.value)
  localStorage.setItem('modo_oscuro', isDarkMode.value ? 'true' : 'false')
}
//Cerrar sesion
const mostrarDropdown = ref(false)

const toggleDropdown = () => {
  mostrarDropdown.value = !mostrarDropdown.value
}

const cerrarSesion = () => {
  localStorage.clear()
  window.location.href = '/' 
}


// ----------- MENU Y PRODUCTOS -----------
const nuevaCategoria = ref('')
const nuevoProducto = ref({ nombre: '', descripcion: '', precio: '', categoria_id: '' })
const categorias = ref([])
const productos = ref([])
const ordenes = ref([])
// Filtro de estado
const filtroEstado = ref('todos'); // El valor inicial será 'todos' para no filtrar

// Propiedad computada para filtrar las órdenes
const ordenesFiltradas = computed(() => {
  // Si el filtro es 'todos', no aplicar filtro
  if (filtroEstado.value === 'todos') {
    return ordenes.value;
  }
  
  // Filtrar las órdenes basándonos en el estado
  return ordenes.value.filter(orden => {
    if (filtroEstado.value === 'pendientes') {
      return !orden.entregado && !orden.cancelada; // O sea, pendientes
    }
    if (filtroEstado.value === 'entregados') {
      return orden.entregado; // Solo las entregadas
    }
    if (filtroEstado.value === 'cancelados') {
      return orden.cancelada; // Solo las canceladas
    }
  });
});
const mensajeMenu = ref('')
const mensajeColorMenu = ref('green')
const productoEditando = ref(null)
const categoriaEditando = ref(null)
const nombreUsuario = ref('')
const imagenProducto = ref(null)
const imagenProductoEdicion = ref(null) // para edición


const handleFileUpload = (event) => {
  imagenProducto.value = event.target.files[0]
}
const handleFileUploadEdicion = (event) => {
  imagenProductoEdicion.value = event.target.files[0]
}



const crearCategoria = async () => {
  mensajeMenu.value = ''
  try {
    await crearNuevaCategoria(nuevaCategoria.value)
    mensajeMenu.value = 'Categoría agregada.'
    mensajeColorMenu.value = 'green'
    nuevaCategoria.value = ''
    await obtenerCategorias()
  } catch {
    mensajeMenu.value = 'Error al agregar categoría.'
    mensajeColorMenu.value = 'red'
  }
}

const obtenerCategorias = async () => {
  categorias.value = await fetchCategorias()
}

const eliminarCategoria = async (id) => {
  if (!confirm("¿Eliminar esta categoría?")) return
  await eliminarCategoriaPorId(id)
  mensajeMenu.value = 'Categoría eliminada.'
  mensajeColorMenu.value = 'green'
  await obtenerCategorias()
}

const iniciarEdicionCategoria = (cat) => {
  categoriaEditando.value = { ...cat }
}

const cancelarEdicionCategoria = () => {
  categoriaEditando.value = null
}

const guardarEdicionCategoria = async () => {
  try {
    await actualizarCategoria(categoriaEditando.value.id, categoriaEditando.value.nombre)
    mensajeMenu.value = 'Categoría actualizada.'
    mensajeColorMenu.value = 'green'
    categoriaEditando.value = null
    await obtenerCategorias()
  } catch {
    mensajeMenu.value = 'Error al actualizar categoría.'
    mensajeColorMenu.value = 'red'
  }
}

const crearProductoNuevo = async () => {
  try {
    const formData = new FormData()
    Object.entries(nuevoProducto.value).forEach(([key, val]) => formData.append(key, val))
    
    if (imagenProducto.value) {
      formData.append('file', imagenProducto.value)
    }

    await crearProducto(formData)
    mensajeMenu.value = 'Producto agregado.'
    mensajeColorMenu.value = 'green'

    nuevoProducto.value = { nombre: '', descripcion: '', precio: '', categoria_id: '' }
    imagenProducto.value = null // limpia la imagen después de cargar
    await obtenerProductos()
  } catch {
    mensajeMenu.value = 'Error al agregar producto.'
    mensajeColorMenu.value = 'red'
  }
}
//Editar perfil
const editarPerfil = () => {
  vistaActual.value = 'editar-perfil' // Cambiar la vista a "editar perfil"
}


const obtenerProductos = async () => {
  productos.value = await fetchProductos()
}

const getImageUrl = (path) => {
  // Si ya recibes la URL absoluta desde el backend, puedes devolver path directamente.
  // Si recibes "/assets/food/imagen.jpg", asegúrate que tu Vite pueda resolverlo:
  return `${BASE_URL}${path}`;
};

const imagenModalVisible = ref(false);
const imagenModalUrl = ref('');

const abrirImagenModal = (url) => {
  imagenModalUrl.value = url;
  imagenModalVisible.value = true;
};

const cerrarImagenModal = () => {
  imagenModalVisible.value = false;
  imagenModalUrl.value = '';
};


const eliminarProducto = async (id) => {
  if (!confirm("¿Eliminar este producto?")) return
  try {
    await eliminarProductoPorId(id)
    mensajeMenu.value = 'Producto eliminado.'
    mensajeColorMenu.value = 'green'
    await obtenerProductos()
  } catch {
    mensajeMenu.value = 'Error al eliminar producto.'
    mensajeColorMenu.value = 'red'
  }
}

const editarProducto = (prod) => {
  productoEditando.value = { ...prod }
}

const guardarEdicion = async () => {
  try {
    const formData = new FormData()
    Object.entries(productoEditando.value).forEach(([key, val]) => formData.append(key, val))

    if (imagenProductoEdicion.value) {
      formData.append('file', imagenProductoEdicion.value)
    }

    await actualizarProducto(productoEditando.value.id, formData)
    mensajeMenu.value = 'Producto actualizado.'
    mensajeColorMenu.value = 'green'
    productoEditando.value = null
    imagenProductoEdicion.value = null // limpia la imagen de edición
    await obtenerProductos()
  } catch {
    mensajeMenu.value = 'Error al actualizar producto.'
    mensajeColorMenu.value = 'red'
  }
}



const obtenerOrdenes = async () => {
  const data = await fetchOrdenes()
  ordenes.value = data.map(ord => {
    const fechaObj = new Date(ord.fecha)
    return {
      ...ord,
      fecha_mostrada: fechaObj.toLocaleDateString('es-ES', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      }),
      hora: fechaObj.toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    }
  })
}
const actualizarFoto = (nuevaFoto) => {
  fotoActual.value = nuevaFoto
}



onMounted(async () => {
  const rol = localStorage.getItem('usuario_rol')
  if (rol !== 'admin') {
    router.push('/login')
    return
  }
  
  // Cargar el nombre del usuario
  nombreUsuario.value = localStorage.getItem('usuario_nombre') || 'Usuario'

  // Cargar las categorías, productos y órdenes
  
  obtenerCategorias()
  obtenerProductos()
  obtenerOrdenes()

  // Cargar la imagen del perfil
  try {
    const id = localStorage.getItem('usuario_id') // Asegúrate de que el ID esté en localStorage
    const datos = await obtenerPerfil(id) // Obtén los datos del perfil desde la API
    fotoActual.value = datos.foto_url ? new URL(datos.foto_url, BASE_URL).href : defaultFoto
  } catch {
    fotoActual.value = defaultFoto  // Si ocurre un error, mostrar la imagen por defecto
  }

  // Configurar el modo oscuro si se ha guardado en localStorage
  if (localStorage.getItem('modo_oscuro') === 'true') {
    isDarkMode.value = true
    document.body.classList.add('dark-mode')
  }
})
</script>


