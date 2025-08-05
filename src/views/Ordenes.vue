<template>
  <main class="ordenes-historial scrollable">
    <h3>Órdenes previas</h3>
    <ul class="ordenes-lista">
      <li v-for="ord in historialOrdenes" :key="ord.id" class="orden-item">
        <strong>{{ ord.cliente }}</strong><br />
        <span>{{ ord.fecha_mostrada }} a las {{ ord.hora }}</span>

        <p v-if="ord.nota"><strong>Nota:</strong> {{ ord.nota }}</p>

        <ul>
          <li v-for="p in ord.productos" :key="p.nombre_producto">
            {{ p.cantidad }} x {{ p.nombre_producto }} - ${{ (p.cantidad * p.precio_unitario).toFixed(2) }}
          </li>
        </ul>
        <p><strong>Total:</strong> ${{ ord.total }}</p>

        <div class="estado-wrapper">
          <span
            :class="['estado', ord.entregado ? 'entregado' : ord.cancelada ? 'cancelada' : 'no-entregado']"
          >
            {{ ord.entregado ? 'Entregado' : ord.cancelada ? 'Cancelado' : 'En espera' }}
          </span>
          <span v-if="ord.cancelada && ord.motivo_cancelacion" class="motivo-cancelacion">
            {{ ord.motivo_cancelacion }}
          </span>
        </div>

        <button @click="ordenExpandida = ord">Ver Detalle</button>
        <button
          :disabled="!puedeCancelar(ord.fechaDate) || ord.entregado || ord.cancelada"
          :class="['cancelar-btn', { desactivado: !puedeCancelar(ord.fechaDate) || ord.entregado || ord.cancelada }]"
          @click="cancelarOrden(ord.id)"
        >
          Cancelar
        </button>
      </li>
    </ul>

    <transition name="modal-fade">
      <div v-if="ordenExpandida" class="modal-overlay" @click.self="ordenExpandida = null">
        <div class="modal-content">
          <h3>Detalle de Orden</h3>
          <p><strong>Cliente:</strong> {{ ordenExpandida.cliente }}</p>
          <p><strong>Fecha:</strong> {{ ordenExpandida.fecha_mostrada }} a las {{ ordenExpandida.hora }}</p>
          <p v-if="ordenExpandida.nota"><strong>Nota:</strong> {{ ordenExpandida.nota }}</p>
          <ul>
            <li v-for="p in ordenExpandida.productos" :key="p.nombre_producto">
              {{ p.cantidad }} x {{ p.nombre_producto }} - ${{ (p.cantidad * p.precio_unitario).toFixed(2) }}
            </li>
          </ul>
          <p><strong>Total:</strong> ${{ ordenExpandida.total }}</p>

          <div v-if="ordenExpandida.cancelada" class="detalle-cancelado">
            <p><strong>Estado:</strong> Cancelada</p>
            <p v-if="ordenExpandida.motivo_cancelacion"><strong>Motivo:</strong> {{ ordenExpandida.motivo_cancelacion }}</p>
          </div>

          <div v-else-if="ordenExpandida.entregado">
            <p><strong>Estado:</strong> Entregada</p>
          </div>

          <button @click="ordenExpandida = null">Cerrar</button>
        </div>
      </div>
    </transition>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchOrdenesCliente, cancelarOrdenPorCliente } from '../api'

const historialOrdenes = ref([])
const ordenExpandida = ref(null)
const usuario_id = parseInt(localStorage.getItem("usuario_id") || '0')

const obtenerOrdenes = async () => {
  if (!usuario_id) return
  const data = await fetchOrdenesCliente(usuario_id)
  historialOrdenes.value = data.map(ord => ({
    ...ord,
    total: ord.productos.reduce((acc, p) => acc + p.precio_unitario * p.cantidad, 0).toFixed(2),
    fechaDate: new Date(ord.fecha),
    nota: ord.nota || '',
    cancelada: ord.cancelada || false,
    motivo_cancelacion: ord.motivo_cancelacion || ''
  }))
}

const cancelarOrden = async (ordenId) => {
  if (!confirm("¿Seguro que quieres cancelar esta orden?")) return
  try {
    const res = await cancelarOrdenPorCliente(ordenId)
    if (!res.ok) {
      const detail = await res.json()
      alert("Error al cancelar la orden: " + (detail.detail || '')); 
    } else {
      await obtenerOrdenes()
      alert("Orden cancelada correctamente.")
    }
  } catch {
    alert("Error al cancelar la orden.")
  }
}

const puedeCancelar = (fechaReal) => {
  const ahora = new Date()
  const diferenciaMin = (ahora - fechaReal) / 1000 / 60
  return diferenciaMin <= 2
}

onMounted(() => {
  obtenerOrdenes()
})
</script>
