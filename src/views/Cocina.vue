<template>
  <div class="cocina-app">
    <!--prueba  Topbar -->
    <header class="cocina-topbar">
      <div class="cocina-logo">
        <img :src="logo" alt="Logo" />
        <span class="cocina-brand">Cafetería</span>
      </div>
      <div class="cocina-user" @click="toggleDropdown">
        <Icon icon="mdi:weather-sunny" @click.stop="toggleDarkMode" class="topbar-icon" />
        <Icon icon="mdi:bell" class="topbar-icon" />
        <img :src="fotoPerfil" alt="Perfil" class="cocina-foto-perfil" />

        <div class="cocina-user-info">
          <span class="cocina-usuario">{{ nombreUsuario }}</span><br />
          <span class="cocina-rol">{{ rolUsuario }}</span>
        </div>
        <Icon icon="mdi:chevron-down" class="topbar-icon" />
        <div v-if="mostrarDropdown" class="dropdown-menu" @click.stop>
          <p>{{ nombreUsuario }}</p>
          <hr />
          <button @click="vista = 'editar-perfil'"><Icon icon="mdi:account-edit" class="mr-1" /> Editar perfil</button>
          <button @click="cerrarSesion"><Icon icon="mdi:logout" class="mr-1" /> Cerrar sesión</button>
        </div>
      </div>
    </header>

    <div class="cocina-main">
      <!-- Sidebar -->
      <aside :class="['cocina-sidebar', { collapsed: sidebarColapsada }]">
        <div class="sidebar-toggle" @click="toggleSidebar">
          <Icon :icon="sidebarColapsada ? 'mdi:chevron-right' : 'mdi:chevron-left'" />
        </div>
        <ul>
          <li :class="{ active: vista === 'menu' }" @click="vista = 'menu'">
            <Icon icon="mdi:silverware-fork-knife" />
            <span v-if="!sidebarColapsada">Menú</span>
          </li>
          <li :class="{ active: vista === 'ordenes' }" @click="vista = 'ordenes'">
            <Icon icon="mdi:receipt" />
            <span v-if="!sidebarColapsada">Órdenes</span>
          </li>
          <li :class="{ active: vista === 'canceladas' }" @click="vista = 'canceladas'">
            <Icon icon="mdi:close-circle" />
            <span v-if="!sidebarColapsada"> Órdenes Canceladas</span>
          </li>
        </ul>
      </aside>


      <!-- Vista Órdenes con separación -->
      <main class="cocina-contenido" v-if="vista === 'ordenes'">
        <h2><Icon icon="mdi:clipboard-list" /> Órdenes - Café</h2>
        <div v-if="!hayOrdenesPendientes">
              <p><Icon icon="mdi:sleep" class="mr-2" /> No hay órdenes pendientes en este momento.</p>
            </div>
        <!-- Órdenes por realizar -->
        <section class="bloque-seccion">
          <h3 class="seccion-title"><Icon icon="mdi:clock-outline" /> Órdenes por realizar</h3>
          <!--<script setu" :key="'pend-' + fecha">-->
            <div v-for="(turnos, fecha) in ordenesAgrupadas" :key="'pend-' + fecha">
            <div v-for="(ordenesTurno, turno) in turnos" :key="'pend-' + turno + fecha">
              <div v-if="ordenesTurno.some(o => !o.entregado)">
                <h4 class="fecha-turno"><Icon icon="mdi:calendar" /> {{ formatFecha(fecha) }} — <Icon icon="mdi:clock" /> {{ turno }}</h4>
                <div class="scroll-tabla">
                  <table class="tabla-ordenes">
                    <thead>
                      <tr>
                        <th>Cliente</th>
                        <th>Productos</th>
                        <th>Notas</th>
                        <th>Hora</th>
                        <th>Status</th>
                        <th>Acción</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="orden in ordenesTurno.filter(o => !o.entregado && !o.cancelada)" :key="orden.id">
                        <td><strong>{{ orden.cliente }}</strong></td>
                        <td>
                          <ul>
                            <li v-for="prod in orden.productos" :key="prod.id">
                              {{ prod.cantidad }} x {{ prod.nombre_producto }}
                            </li>
                          </ul>
                        </td>
                        <td>{{ orden.nota || 'Sin Notas' }}</td>
                        <td>{{ orden.hora }}</td>
                        <td><span class="estado no-entregado">En espera</span></td>
                        <td>
                          <button @click="marcarEntregado(orden.id)" class="btn-entregar"><Icon icon="mdi:check-circle" class="mr-1" /> Marcar como entregado</button>
                          <button @click="cancelarOrdenChef(orden.id)" class="btn-cancelar"><Icon icon="mdi:close-circle" class="mr-1" /> Cancelar</button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Órdenes entregadas -->
        <section class="bloque-seccion">
          <h3 class="seccion-title"><Icon icon="mdi:check-circle" /> Órdenes entregadas</h3>
          <div v-for="(turnos, fecha) in ordenesAgrupadas" :key="'ent-' + fecha">
          
            <div v-for="(ordenesTurno, turno) in turnos" :key="'ent-' + turno + fecha">
              <div v-if="ordenesTurno.some(o => o.entregado)">
                <h4 class="fecha-turno"><Icon icon="mdi:calendar" /> {{ formatFecha(fecha) }} — <Icon icon="mdi:clock" /> {{ turno }}</h4>
                <div class="scroll-tabla">
                  <table class="tabla-ordenes">
                    <thead>
                      <tr>
                        <th>Cliente</th>
                        <th>Productos</th>
                        <th>Nota</th>
                        <th>Hora</th>
                        <th>Status</th>
                        <th>Acción</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="orden in ordenesTurno.filter(o => o.entregado)" :key="orden.id">
                        <td><strong>{{ orden.cliente }}</strong></td>
                        <td>
                          <ul>
                            <li v-for="prod in orden.productos" :key="prod.id">
                              {{ prod.cantidad }} x {{ prod.nombre_producto }}
                            </li>
                          </ul>
                        </td>
                        <td>{{ orden.nota || '-' }}</td>
                        <td>{{ orden.hora }}</td>
                        <td>
                          <span v-if="orden.cancelada" class="estado cancelada"><Icon icon="mdi:close-circle" /> Cancelada</span>
                          <span v-else class="estado entregado"><Icon icon="mdi:check-circle" /> Entregado</span>
                        </td>

                        <td><span class="entregado-msg"><Icon icon="mdi:check" /> Entregado</span></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
            <!-- Vista Órdenes Canceladas -->
      <main class="cocina-contenido" v-if="vista === 'canceladas'">
        <h2><Icon icon="mdi:close-circle" /> Órdenes Canceladas</h2>

        <div v-if="!hayOrdenesCanceladas">
          <p><Icon icon="mdi:emoticon-happy" class="mr-2" /> No hay órdenes canceladas en este momento.</p>
        </div>

        <section class="bloque-seccion">
          <h3 class="seccion-title"><Icon icon="mdi:alert-circle" /> Órdenes Canceladas</h3>
          <div v-for="(turnos, fecha) in ordenesAgrupadasCanceladas" :key="'cancel-' + fecha">
            <div v-for="(ordenesTurno, turno) in turnos" :key="'cancel-' + turno + fecha">
              <div v-if="ordenesTurno.some(o => o.cancelada)">
                <h4 class="fecha-turno"><Icon icon="mdi:calendar" /> {{ formatFecha(fecha) }} — <Icon icon="mdi:clock" /> {{ turno }}</h4>
                <div class="scroll-tabla">
                  <table class="tabla-ordenes">
                    <thead>
                      <tr>
                        <th>Cliente</th>
                        <th>Productos</th>
                        <th>Nota</th>
                        <th>Hora</th>
                        <th>Status</th>
                        <th>Acción</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="orden in ordenesTurno.filter(o => o.cancelada)" :key="orden.id">
                        <td><strong>{{ orden.cliente }}</strong></td>
                        <td>
                          <ul>
                            <li v-for="prod in orden.productos" :key="prod.id">
                              {{ prod.cantidad }} x {{ prod.nombre_producto }}
                            </li>
                          </ul>
                        </td>
                        <td>{{ orden.nota || '-' }}</td>
                        <td>{{ orden.hora }}</td>
                        <td>
                          <span class="estado cancelada"><Icon icon="mdi:close-circle" /> Cancelada</span>
                        </td>
                        <td><span class="cancelada-msg"><Icon icon="mdi:close" /> Cancelada</span></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      <!-- Vista Menú -->
      <main class="cocina-contenido" v-if="vista === 'menu'">
        <h2><Icon icon="mdi:silverware-fork-knife" /> Menú de Productos</h2>

        <h3><Icon icon="mdi:plus-circle" /> Agregar Platillo</h3>
        <form @submit.prevent="crearProductoNuevo" class="form-platillo">
          
          <input v-model="nuevoProducto.nombre" placeholder="Nombre" required />
          <textarea v-model="nuevoProducto.descripcion" placeholder="Descripción" required />
          <input v-model="nuevoProducto.precio" type="number" min="0.01" step="0.01" placeholder="Precio" required />
          <select v-model="nuevoProducto.categoria_id" required>
            <option disabled value="">Seleccionar categoría</option>
            <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
          </select>
          <button type="submit"><Icon icon="mdi:plus" class="mr-1" /> Agregar</button>
        </form>
        <p v-if="mensaje" :style="{ color: mensajeColor }"><Icon :icon="mensajeColor === 'green' ? 'mdi:check-circle' : 'mdi:alert-circle'" class="mr-1" />{{ mensaje }}</p>

        <table class="tabla-ordenes">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Categoría</th>
              <th>Precio</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="prod in productos" :key="prod.id">
              <td>{{ prod.nombre }}</td>
              <td>{{ categoriaNombre(prod.categoria_id) }}</td>
              <td>${{ prod.precio }}</td>
              <td>
                <span :class="prod.disponible ? 'activo' : 'inactivo'">
                  <Icon :icon="prod.disponible ? 'mdi:check-circle' : 'mdi:close-circle'" class="mr-1" />
                  {{ prod.disponible ? 'Disponible' : 'Agotado' }}
                </span>
              </td>
              <td>
                <button @click="abrirEditar(prod)"><Icon icon="mdi:pencil" class="mr-1" /> Editar</button>
                <button @click="toggleDisponible(prod.id)">
                  <Icon :icon="prod.disponible ? 'mdi:eye-off' : 'mdi:eye'" class="mr-1" />
                  {{ prod.disponible ? 'Marcar Agotado' : 'Marcar Disponible' }}
                </button>
                <button @click="eliminarProducto(prod.id)"><Icon icon="mdi:trash-can" class="mr-1" /> Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Modal de edición -->
        <div v-if="editandoProducto" class="modal-overlay" @click.self="cerrarModal">
          <div class="modal">
            <h3><Icon icon="mdi:pencil" /> Editar Platillo</h3>
            <form @submit.prevent="guardarEdicion">
              <input v-model="editandoProducto.nombre" required />
              <textarea v-model="editandoProducto.descripcion" required />
              <input v-model="editandoProducto.precio" type="number" min="0.01" step="0.01" required />
              <select v-model="editandoProducto.categoria_id" required>
                <option disabled value="">Seleccionar categoría</option>
                <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
              </select>
              <div class="modal-buttons">
                <button type="submit">Guardar</button>
                <button type="button" @click="cerrarModal">Cancelar</button>
              </div>
            </form>
          </div>
        </div>
      </main>
      <main class="cocina-contenido" v-if="vista === 'editar-perfil'">
  <EditarPerfil @foto-actualizada="fotoPerfil = $event" />

</main>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
//import '../EstilosCss/cocinastyle.css'
import logo from '../assets/images/Group.svg'
import EditarPerfil from './EditarPerfil.vue' // Ajusta la ruta si está en otra carpeta
import { BASE_URL } from '../config';
import '../EstilosCss/base.css'
import '../EstilosCss/layout.css'
import '../EstilosCss/topbar.css'
import '../EstilosCss/sidebar.css'
import '../EstilosCss/cocina.css'
import '../EstilosCss/components.css'
import '../EstilosCss/dark-mode.css'
//import logo from '../assets/images/LogoCafe.png'
import {
  fetchOrdenes,
  fetchProductos,
  obtenerPerfil,
  fetchCategorias,
  toggleDisponibilidadProducto,
  eliminarProductoPorId,
  marcarOrdenComoEntregada,
  crearProducto,
  actualizarProducto,
  cancelarOrdenCocina
} from '../api'

const fotoPerfil = ref('') // foto del usuario
const sidebarColapsada = ref(false)
const toggleSidebar = () => (sidebarColapsada.value = !sidebarColapsada.value)

const vista = ref('ordenes')
const ordenes = ref([])
const productos = ref([])
const categorias = ref([])
const nuevoProducto = ref({ nombre: '', descripcion: '', precio: '', categoria_id: '' })
const editandoProducto = ref(null)
const nombreUsuario = ref('')
const rolUsuario = ref('')
const mostrarDropdown = ref(false)
const mensaje = ref('')
const mensajeColor = ref('green')
const cancelarOrdenChef = async (id) => {
  if (!confirm("¿Seguro que deseas cancelar esta orden?")) return;
  try {
    const res = await cancelarOrdenCocina(id);
    if (res.success) {
      alert(res.message || "✅ Orden cancelada correctamente.");
      await cargarOrdenes();
    } else if (res.detail) {
      alert("❌ " + res.detail); // Mostrar el mensaje de error del backend
    } else {
      alert("❌ Error al cancelar la orden.");
    }
  } catch (error) {
    alert("❌ Error al cancelar la orden.");
    console.error(error);
  }
};


//ver si hay ordenes 
const hayOrdenesPendientes = computed(() => {
  for (const fecha in ordenesAgrupadas.value) {
    for (const turno in ordenesAgrupadas.value[fecha]) {
      if (ordenesAgrupadas.value[fecha][turno].some(o => !o.entregado && !o.cancelada)) {
        return true;
      }
    }
  }
  return false;
});


const ordenesAgrupadas = computed(() => {
  const agrupadas = {}
  ordenes.value.forEach(o => {
    // Filtrar las órdenes que no están canceladas
    if (!o.cancelada) {
      const fecha = o.fecha
      const hora = parseInt(o.hora.split(':')[0])
      let turno = ''
      if (hora >= 6 && hora < 14) turno = 'Mañana'
      else if (hora >= 14 && hora < 22) turno = 'Tarde'
      else turno = 'Noche'

      if (!agrupadas[fecha]) agrupadas[fecha] = {}
      if (!agrupadas[fecha][turno]) agrupadas[fecha][turno] = []
      agrupadas[fecha][turno].push(o)
    }
  })
  return agrupadas
})


const toggleDarkMode = () => document.body.classList.toggle('dark-mode')
const toggleDropdown = () => (mostrarDropdown.value = !mostrarDropdown.value)
const cerrarSesion = () => {
  localStorage.clear()
  window.location.href = '/'
}

const cargarOrdenes = async () => {
  const data = await fetchOrdenes()
  ordenes.value = data.map(ord => {
    const fechaObj = new Date(ord.fecha)
    return {
      ...ord,
      hora: fechaObj.toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    }
  })
}

const formatFecha = fechaStr => {
  const fechaObj = new Date(fechaStr)
  return fechaObj.toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const obtenerProductos = async () => {
  productos.value = await fetchProductos()
}
const obtenerCategorias = async () => {
  categorias.value = await fetchCategorias()
}
const categoriaNombre = id => categorias.value.find(c => c.id === id)?.nombre || '—'

const crearProductoNuevo = async () => {
  mensaje.value = ''
  const p = parseFloat(nuevoProducto.value.precio)
  if (isNaN(p) || p <= 0) {
    mensaje.value = 'Precio debe ser > 0'
    mensajeColor.value = 'red'
    setTimeout(() => (mensaje.value = ''), 3000)
    return
  }
  try {
    const fd = new FormData()
    Object.entries(nuevoProducto.value).forEach(([k, v]) => fd.append(k, v))
    await crearProducto(fd)
    mensaje.value = '✅ Agregado'
    mensajeColor.value = 'green'
    Object.assign(nuevoProducto.value, { nombre: '', descripcion: '', precio: '', categoria_id: '' })
    await obtenerProductos()
  } catch {
    mensaje.value = '❌ Error al agregar'
    mensajeColor.value = 'red'
  }
  setTimeout(() => (mensaje.value = ''), 3000)
}

const toggleDisponible = async id => {
  await toggleDisponibilidadProducto(id)
  await obtenerProductos()
}

const eliminarProducto = async id => {
  if (!confirm('¿Eliminar este platillo?')) return
  await eliminarProductoPorId(id)
  await obtenerProductos()
}

const abrirEditar = prod => (editandoProducto.value = { ...prod })
const cerrarModal = () => (editandoProducto.value = null)

const guardarEdicion = async () => {
  const p = editandoProducto.value
  const price = parseFloat(p.precio)
  if (isNaN(price) || price <= 0) {
    mensaje.value = 'Precio debe ser > 0'
    mensajeColor.value = 'red'
    setTimeout(() => (mensaje.value = ''), 3000)
    return
  }
  try {
    const fd = new FormData()
    Object.entries(p).forEach(([k, v]) => fd.append(k, v))
    await actualizarProducto(p.id, fd)
    mensaje.value = '✅ Actualizado'
    mensajeColor.value = 'green'
    await obtenerProductos()
    cerrarModal()
  } catch {
    mensaje.value = '❌ Error al actualizar'
    mensajeColor.value = 'red'
  }
  setTimeout(() => (mensaje.value = ''), 3000)
}

const marcarEntregado = async id => {
  try {
    const res = await marcarOrdenComoEntregada(id)
    if (res.ok) {
      await cargarOrdenes()
      alert('✅ Orden entregada')
    } else alert('❌ Error al entregar')
  } catch {
    alert('❌ Error al entregar')
  }
}
const ordenesAgrupadasCanceladas = computed(() => {
  const agrupadas = {}
  ordenes.value.forEach(o => {
    if (o.cancelada) { // Solo agrupamos las canceladas
      const fecha = o.fecha
      const hora = parseInt(o.hora.split(':')[0])
      let turno = ''
      if (hora >= 6 && hora < 14) turno = 'Mañana'
      else if (hora >= 14 && hora < 22) turno = 'Tarde'
      else turno = 'Noche'

      if (!agrupadas[fecha]) agrupadas[fecha] = {}
      if (!agrupadas[fecha][turno]) agrupadas[fecha][turno] = []
      agrupadas[fecha][turno].push(o)
    }
  })
  return agrupadas
})


const hayOrdenesCanceladas = computed(() => {
  for (const fecha in ordenesAgrupadasCanceladas.value) {
    for (const turno in ordenesAgrupadasCanceladas.value[fecha]) {
      if (ordenesAgrupadasCanceladas.value[fecha][turno].some(o => o.cancelada)) {
        return true
      }
    }
  }
  return false
})
//Agrupar ordenes Canceladas

const cargarPerfil = async () => {
  try {
    const id = localStorage.getItem('usuario_id')
    const perfil = await obtenerPerfil(id)
    fotoPerfil.value = perfil.foto_url ? new URL(perfil.foto_url, BASE_URL).href : '' // misma lógica que EditarPerfil
  } catch (e) {
    console.error("Error cargando perfil", e)
  }
}

onMounted(() => {
  if (localStorage.getItem('usuario_rol') !== 'chef') {
    window.location.href = '/login'
    return
  }
  nombreUsuario.value = localStorage.getItem('usuario_nombre') || 'Usuario'
  rolUsuario.value = 'Chef'
  cargarOrdenes()
  obtenerProductos()
  obtenerCategorias()
  // Actualización automática de órdenes cada 5 segundos
  cargarPerfil()
setInterval(() => {
  cargarOrdenes()
}, 5000)

})
</script>

