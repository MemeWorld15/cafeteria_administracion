<template>
  <div class="p-4">
    <h3 class="text-xl font-semibold mb-4"><Icon icon="mdi:history" class="mr-2" /> Historial de movimientos</h3>

    <!-- Filtros -->
    <div class="filtros flex gap-4 mb-6 items-center flex-wrap">
      <div class="flex flex-col">
        <label for="filtro" class="text-sm font-medium"><Icon icon="mdi:filter" class="mr-1" /> Filtrar por:</label>
        <select id="filtro" v-model="filtroTipo" class="border rounded px-2 py-1">
          <option value="">Todos</option>
          <option value="Entrada">Entrada</option>
          <option value="Salida">Salida</option>
        </select>
      </div>

      <div class="flex flex-col">
        <label class="text-sm font-medium"><Icon icon="mdi:search" class="mr-1" /> Buscar insumo:</label>
        <input
          type="text"
          placeholder="Buscar insumo..."
          v-model="busqueda"
          class="border rounded px-2 py-1"
        />
      </div>

      <div class="pt-5">
        <button @click="limpiarFiltros" class="bg-gray-200 px-4 py-2 rounded hover:bg-gray-300"><Icon icon="mdi:filter-remove" class="mr-1" />
          Limpiar filtros
        </button>
      </div>
    </div>

    <!-- Tabla -->
    <div class="overflow-x-auto">
      <table class="tabla-inventario w-full border-collapse">
        <thead>
          <tr class="bg-gray-100">
            <th class="border px-3 py-2 text-left">Fecha</th>
            <th class="border px-3 py-2 text-left">Insumo</th>
            <th class="border px-3 py-2 text-left">Movimiento</th>
            <th class="border px-3 py-2 text-right">Cantidad</th>
            <th class="border px-3 py-2 text-left">Unidad</th>
            <th class="border px-3 py-2 text-center">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="m in historialFiltrado"
            :key="m.id"
            class="hover:bg-gray-50"
          >
            <td class="border px-3 py-2">{{ formatearFecha(m.fecha) }}</td>
            <td class="border px-3 py-2">{{ m.insumo }}</td>
            <td
              class="border px-3 py-2 font-medium"
              :class="{
                'text-green-700': esEntrada(m.tipo_movimiento),
                'text-red-700': esSalida(m.tipo_movimiento)
              }"
            >
              <Icon v-if="esEntrada(m.tipo_movimiento)" icon="mdi:arrow-up" class="mr-1" />
              <Icon v-else-if="esSalida(m.tipo_movimiento)" icon="mdi:arrow-down" class="mr-1" />
              {{ m.tipo_movimiento }}
            </td>
            <td class="border px-3 py-2 text-right">
              {{ m.cantidad !== null ? Number(m.cantidad).toFixed(2) : '-' }}
            </td>
            <td class="border px-3 py-2">{{ m.unidad }}</td>
            <td class="border px-3 py-2 text-center">
              <button
                class="px-3 py-1 rounded shadow-sm hover:opacity-90 disabled:opacity-40"
                :disabled="!puedeDeshacer(m.tipo_movimiento)"
                @click="deshacer(m.insumo_id)"
                :title="puedeDeshacer(m.tipo_movimiento) ? 'Revertir este movimiento' : 'Solo se puede deshacer consumo o reabastecimiento'"
              >
                <Icon icon="mdi:undo" class="mr-1" /> Deshacer
              </button>
            </td>
          </tr>

          <tr v-if="historialFiltrado.length === 0">
            <td colspan="6" class="text-center py-6">
              No hay movimientos que mostrar.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Toast -->
    <div
      v-if="toastMsg"
      :class="['toast', toastTipo === 'error' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800']"
      class="fixed bottom-4 right-4 border rounded px-4 py-2 shadow"
    >
      <Icon v-if="toastTipo === 'error'" icon="mdi:alert-circle" class="mr-2" />
      <Icon v-else icon="mdi:check-circle" class="mr-2" />
      {{ toastMsg }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import '../EstilosCss/layout.css'
import '../EstilosCss/components.css'
import '../EstilosCss/base.css'
import {
  obtenerHistorialInventario,
  deshacerUltimoMovimiento
} from '../api'

// Estados
const historial = ref([])
const filtroTipo = ref('')
const busqueda = ref('')
const toastMsg = ref('')
const toastTipo = ref('')

// Cargar historial
async function cargarHistorial() {
  try {
    historial.value = await obtenerHistorialInventario()
  } catch (e) {
    console.error('Error cargando historial:', e)
    toast('No se pudo cargar el historial', 'error')
  }
}

// Al montar
onMounted(() => {
  cargarHistorial()
})

// Funciones de ayuda (entrada/salida)
const esEntrada = (tipo) => {
  return ['reabastecimiento', 'agregado'].includes(tipo) || tipo.startsWith('revertir_')
}
const esSalida = (tipo) => {
  return ['consumo', 'eliminacion'].includes(tipo)
}
const puedeDeshacer = (tipo) => {
  // Solo permitir deshacer estos dos (el backend también valida)
  return ['consumo', 'reabastecimiento'].includes(tipo)
}

// Computado con filtros, mapeando Entrada/Salida
const historialFiltrado = computed(() => {
  let resultado = historial.value

  if (filtroTipo.value) {
    if (filtroTipo.value === 'Entrada') {
      resultado = resultado.filter(m => esEntrada(m.tipo_movimiento))
    } else if (filtroTipo.value === 'Salida') {
      resultado = resultado.filter(m => esSalida(m.tipo_movimiento))
    }
  }

  if (busqueda.value) {
    resultado = resultado.filter(m =>
      m.insumo.toLowerCase().includes(busqueda.value.toLowerCase())
    )
  }

  return resultado
})

// Limpiar filtros
function limpiarFiltros() {
  filtroTipo.value = ''
  busqueda.value = ''
}

// Formatear fecha (más legible)
function formatearFecha(raw) {
  try {
    return new Date(raw).toLocaleString()
  } catch {
    return raw
  }
}

// Función para revertir movimiento
const deshacer = async (id) => {
  if (!id) {
    toast('ID inválido para deshacer movimiento', 'error')
    return
  }

  if (!confirm('¿Revertir el último movimiento para este insumo?')) {
    return
  }

  try {
    const res = await deshacerUltimoMovimiento(id)
    let data
    try {
      data = await res.json()
    } catch {
      data = {}
    }

    if (res.ok) {
      toast('Movimiento revertido con éxito.') 
      await cargarHistorial()
    } else {
      const msg = typeof data.detail === 'string'
        ? data.detail
        : JSON.stringify(data.detail || 'Desconocido')
      toast('Error: ' + msg, 'error')
    }
  } catch (e) {
    console.error('🔴 Error de red:', e)
    toast('Error de conexión', 'error')
  }
}

// Mostrar toast
function toast(mensaje, tipo = 'exito') {
  toastMsg.value = mensaje
  toastTipo.value = tipo
  setTimeout(() => {
    toastMsg.value = ''
  }, 3000)
}
</script>
<style scoped>
.filtros {
  margin-bottom: 1rem;
  display: flex;
  gap: 1rem;
  align-items: center;
}


.toast {
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 5px;
  color: white;
}

.toast.exito {
  background-color: #4caf50;
}

.toast.error {
  background-color: #f44336;
}
</style>
