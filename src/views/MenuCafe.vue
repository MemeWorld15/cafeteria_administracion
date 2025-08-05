<template>
  <div class="menu-app">
    <!-- Topbar -->
    <header class="menu-topbar">
      <div class="menu-topbar-logo">
        <img :src="logo" alt="Logo" />
        <div>
          <span class="menu-brand">Cafetería</span><br />
          <span class="menu-role">Cliente</span>
        </div>
      </div>
      <div class="top-right">
        <Icon icon="mdi:weather-sunny" @click="toggleDarkMode" class="topbar-icon" />
        <Icon icon="mdi:account" class="topbar-icon" />
        <span class="menu-name">{{ nombreUsuario }}</span>
        <div class="dropdown" @click="toggleDropdown">
          <Icon icon="mdi:chevron-down" class="topbar-icon" />
          <div v-if="mostrarDropdown" class="dropdown-menu">
            <p class="usuario-nombre">{{ nombreUsuario }}</p>
            <hr />
            <button class="logout-btn" @click="cerrarSesion"><Icon icon="mdi:logout" class="mr-1" /> Cerrar sesión</button>
          </div>
        </div>
      </div>
    </header>

    <!-- Tabs -->
    <div class="menu-tabs">
      <button :class="{ active: vista === 'menu' }" @click="vista = 'menu'"><Icon icon="mdi:food" class="mr-1" /> Menú</button>
      <button :class="{ active: vista === 'ordenes' }" @click="vista = 'ordenes'"><Icon icon="mdi:receipt" class="mr-1" /> Órdenes</button>
    </div>

    <!-- Main Body -->
    <div class="menu-main-body">
      <!-- Vista Menú -->
      <template v-if="vista === 'menu'">
        <aside class="menu-sidebar scrollable">
          <h3><Icon icon="mdi:format-list-bulleted" /> Categorías</h3>
          <ul>
            <li v-for="cat in categorias" :key="cat"
                :class="{ active: categoriaSeleccionada === cat }"
                @click="categoriaSeleccionada = cat">
              {{ cat }}
            </li>
            <li :class="{ active: categoriaSeleccionada === 'Todas' }" @click="categoriaSeleccionada = 'Todas'"><Icon icon="mdi:view-list" class="mr-1" />
              Todas
            </li>
          </ul>
        </aside>

        <main class="menu-content">
          <input type="text" placeholder="Buscar..." class="menu-buscar" />
          <Icon icon="mdi:magnify" class="absolute right-3 top-3 text-gray-400" />
          <div class="menu-seccion scrollable">
            <div class="menu-titulo"><Icon icon="mdi:silverware-fork-knife" /> Menú <!--<span class="mesa">Mesa 1</span>--></div>
            <div v-for="categoria in categorias" :key="categoria"
                v-show="categoriaSeleccionada === 'Todas' || categoriaSeleccionada === categoria"
                class="menu-categoria">
              <h2 @click="toggleCategoria(categoria)" style="cursor: pointer;">
                {{ categoria }}
                <Icon :icon="categoriaExpandida[categoria] ? 'mdi:chevron-up' : 'mdi:chevron-down'" class="ml-2" />
              </h2>
              <div v-show="categoriaExpandida[categoria]">
                  </div> <!-- ESTA LÍNEA ES LA QUE FALTABA -->

                <div class="menu-item"
                  v-for="platillo in platillos[categoria]"
                  :key="platillo.nombre"
                  :class="{ 'no-disponible': platillo.disponible === false }">

                <img
                  v-if="platillo.imagen_url"
                  :src="`${BASE_URL}${platillo.imagen_url}`"
                  alt="Imagen de {{ platillo.nombre }}"
                  class="platillo-imagen-item"
                />

                <div class="platillo-detalle">
                  <strong class="platillo-nombre">
                    {{ platillo.nombre }}
                    <span v-if="!platillo.disponible">(No disponible)</span>
                  </strong>
                  <p class="platillo-descripcion">
                    {{ platillo.descripcion }}
                  </p>
                  <p class="platillo-precio">
                    ${{ parseFloat(platillo.precio).toFixed(2) }}
                  </p>
                  <div class="platillo-botones">
                    <button @click="agregarProductoOrden(platillo)" :disabled="!platillo.disponible"><Icon icon="mdi:plus" /></button>
                    <button @click="disminuirProductoOrden(platillo)" :disabled="!platillo.disponible"><Icon icon="mdi:minus" /></button>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </main>

        <aside class="menu-orden scrollable">
          <h3><Icon icon="mdi:cart" /> Orden</h3>
          <!--<p><strong>Mesa</strong> 1</p>-->
          <div class="menu-resumen">
            <div v-if="orden.length === 0"><Icon icon="mdi:cart-remove" class="mr-2" /> Aún no hay productos en la orden.</div>
            <div v-else>
              <p v-for="item in orden" :key="item.nombre">
                - {{ item.cantidad }} x {{ item.nombre }}
                <span>${{ (item.precio * item.cantidad).toFixed(2) }}</span>
                <button @click="eliminarProductoOrden(item)"><Icon icon="mdi:close" /></button>
              </p>
            </div>
          </div>
          <Icon icon="mdi:account" class="absolute left-3 top-3 text-gray-400" />
          <input v-model="nombreCliente" type="text" placeholder="Nombre del cliente" />
          <Icon icon="mdi:note-text" class="absolute left-3 top-3 text-gray-400" />
          <textarea v-model="notaOrden" placeholder="Nota"></textarea>
          <p class="menu-total"><Icon icon="mdi:cash-register" /> Total: <strong>${{ calcularTotal() }}</strong></p>
          <button class="menu-ordenar" @click="enviarOrden"><Icon icon="mdi:send" class="mr-2" /> ORDENAR</button>
          <p v-if="mensajeConfirmacion" style="margin-top: 0.5rem; color: green;"><Icon icon="mdi:check-circle" class="mr-1" />{{ mensajeConfirmacion }}</p>
          
        </aside>
      </template>

      <template v-if="vista === 'ordenes'">
          <Ordenes />
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
//import logo from '../assets/images/LogoCafe.png'
import Ordenes from './Ordenes.vue'
import logo from '../assets/images/Group.svg'
//import '../EstilosCss/menuc.css'
import '../EstilosCss/base.css'
import '../EstilosCss/layout.css'
import '../EstilosCss/topbar.css'
import '../EstilosCss/sidebar.css'
import '../EstilosCss/menu.css'
import '../EstilosCss/components.css'
import '../EstilosCss/dark-mode.css'
import { BASE_URL } from '../config';
import {
  fetchMenu,
  //fetchOrdenesCliente,
  enviarOrden as enviarOrdenAPI,
  //cancelarOrdenPorId
} from '../api'

const vista = ref('menu')
const categorias = ref([])
const platillos = ref({})
const categoriaSeleccionada = ref('Todas')
const categoriaExpandida = ref({})
const orden = ref([])

const nombreCliente = ref(localStorage.getItem("usuario_nombre") || '')
const notaOrden = ref('')
const mensajeConfirmacion = ref('')
//const historialOrdenes = ref([])
const nombreUsuario = ref(localStorage.getItem("usuario_nombre") || "Invitado")
const usuario_id = parseInt(localStorage.getItem("usuario_id") || '0')
const mostrarDropdown = ref(false)
//const ordenExpandida = ref(null)


const toggleCategoria = (cat) => {
  categoriaExpandida.value[cat] = !categoriaExpandida.value[cat]
}

const toggleDarkMode = () => {
  document.body.classList.toggle('dark-mode')
}

const toggleDropdown = () => {
  mostrarDropdown.value = !mostrarDropdown.value
}

// Cierra dropdown al hacer clic fuera
const handleClickOutside = (event) => {
  const dropdown = document.querySelector('.dropdown')
  if (dropdown && !dropdown.contains(event.target)) {
    mostrarDropdown.value = false
  }
}

const handleEscape = (e) => {
  if (e.key === 'Escape' && ordenExpandida.value) {
    ordenExpandida.value = null
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleEscape)
  obtenerMenu()
  //obtenerOrdenes()
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleEscape)
})


const cerrarSesion = () => {
  localStorage.clear()
  window.location.href = '/'  
}

const obtenerMenu = async () => {
  platillos.value = await fetchMenu()
  categorias.value = Object.keys(platillos.value)
  categoriaSeleccionada.value = 'Todas'
  const expanded = {}
  categorias.value.forEach(cat => (expanded[cat] = true))
  categoriaExpandida.value = expanded
}

const agregarProductoOrden = (producto) => {
  const existe = orden.value.find(p => p.nombre === producto.nombre)
  if (existe) {
    existe.cantidad++
  } else {
    orden.value.push({ ...producto, cantidad: 1, precio: parseFloat(producto.precio) })
  }
}

const disminuirProductoOrden = (producto) => {
  const index = orden.value.findIndex(p => p.nombre === producto.nombre)
  if (index !== -1) {
    if (orden.value[index].cantidad > 1) {
      orden.value[index].cantidad--
    } else {
      orden.value.splice(index, 1)
    }
  }
}

const eliminarProductoOrden = (producto) => {
  orden.value = orden.value.filter(p => p.nombre !== producto.nombre)
}

const calcularTotal = () => {
  return orden.value.reduce((acc, prod) => acc + prod.precio * prod.cantidad, 0).toFixed(2)
}

const obtenerTurnoActual = () => {
  const hora = new Date().getHours();
  if (hora >= 6 && hora < 14) return 'matutino';
  if (hora >= 14 && hora < 22) return 'vespertino';
  return 'nocturno';
}

const enviarOrden = async () => {
  if (!nombreCliente.value.trim() || orden.value.length === 0) {
    alert("Por favor ingresa el nombre del cliente y al menos un producto.")
    return
  }
  const payload = {
    cliente: nombreCliente.value,
    nota: notaOrden.value,
    usuario_id,
    turno: obtenerTurnoActual(),
    productos: orden.value.map(p => ({
      nombre: p.nombre,
      cantidad: p.cantidad,
      precio: p.precio
    }))
  }
  const res = await enviarOrdenAPI(payload)
  if (res.ok) {
    mensajeConfirmacion.value = 'Orden enviada correctamente.'
    orden.value = []
    notaOrden.value = ''
    obtenerOrdenes()
    setTimeout(() => mensajeConfirmacion.value = '', 4000)
  } else {
    alert('Error al enviar la orden.')
  }
}

//const cancelarOrden = async (ordenId) => {
  //if (!confirm("¿Seguro que quieres cancelar esta orden?")) return
  //const res = await cancelarOrdenPorId(ordenId)
  //if (!res.ok) {
    //alert("Error al cancelar la orden.")
  //} else {
    //await obtenerOrdenes()
  //  alert("Orden cancelada correctamente.")
//  }
//}

//const puedeCancelar = (fechaReal) => {
  //const ahora = new Date()
  //const diferenciaMin = (ahora - fechaReal) / 1000 / 60
  //return diferenciaMin <= 2
//}

//const obtenerOrdenes = async () => {
  //if (!usuario_id) return
  //const data = await fetchOrdenesCliente(usuario_id)
  //historialOrdenes.value = data.map(ord => ({
  //...ord,
  //total: ord.productos.reduce((acc, p) => acc + p.precio_unitario * p.cantidad, 0).toFixed(2),
  //fechaDate: new Date(ord.fecha),
  //nota: ord.nota || ''
//}))

//}
</script>
