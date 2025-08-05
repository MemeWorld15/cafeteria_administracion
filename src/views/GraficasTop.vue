<template>
  <div class="graficas-top">
    <div class="graf-grid">
      <div class="graf-item">
        <h3><Icon icon="mdi:chart-bar" /> Productos más pedidos</h3>
        <canvas ref="chartProductos"></canvas>
      </div>

      <div class="graf-item">
        <h3><Icon icon="mdi:account-group" /> Clientes con más órdenes</h3>
        <canvas ref="chartClientes"></canvas>
      </div>

      <div class="graf-item">
        <div class="ranking-header">
          <h3><Icon icon="mdi:chart-line" /> Ranking de productos vendidos hoy</h3>
          <button @click="toggleOrden">
           <Icon :icon="ordenAscendente ? 'mdi:sort-ascending' : 'mdi:sort-descending'" class="mr-1" />
            Orden: {{ ordenAscendente ? 'Menor → Mayor' : 'Mayor → Menor' }}
          </button>
        </div>
        <canvas ref="chartRanking"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Chart, registerables } from 'chart.js'
import {
  fetchTopProductos,
  fetchTopClientes
} from '../api'

Chart.register(...registerables)

const chartProductos = ref(null)
const chartClientes = ref(null)
const chartRanking = ref(null)

const topProductos = ref([])
const ordenAscendente = ref(true)
let chartRankingInstance = null

const renderRankingChart = () => {
  if (chartRankingInstance) {
    chartRankingInstance.destroy()
  }

  const productosOrdenados = [...topProductos.value].sort((a, b) =>
    ordenAscendente.value ? a.total_pedidos - b.total_pedidos : b.total_pedidos - a.total_pedidos
  )

  chartRankingInstance = new Chart(chartRanking.value, {
    type: 'bar',
    data: {
      labels: productosOrdenados.map(p => p.nombre_producto),
      datasets: [{
        label: 'Veces vendido',
        data: productosOrdenados.map(p => p.total_pedidos),
        backgroundColor: '#2196F3'
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: false }
      }
    }
  })
}

const toggleOrden = () => {
  ordenAscendente.value = !ordenAscendente.value
  renderRankingChart()
}

const cargarGraficas = async () => {
  try {
    const productos = await fetchTopProductos()
    const clientes = await fetchTopClientes()

    topProductos.value = productos

    new Chart(chartProductos.value, {
      type: 'bar',
      data: {
        labels: productos.map(p => p.nombre_producto),
        datasets: [{
          label: 'Cantidad total pedida',
          data: productos.map(p => p.total_pedidos),
          backgroundColor: '#4CAF50'
        }]
      }
    })

    new Chart(chartClientes.value, {
      type: 'doughnut',
      data: {
        labels: clientes.map(c => c.cliente),
        datasets: [{
          label: 'Órdenes',
          data: clientes.map(c => c.total_ordenes),
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#7E57C2']
        }]
      }
    })

    renderRankingChart()

  } catch (err) {
    console.error('Error al cargar gráficas:', err)
  }
}

onMounted(cargarGraficas)
</script>

<style scoped>
.graficas-top {
  padding: 2rem;
  max-width: 1200px;
  margin: auto;
}

.graf-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

.graf-item {
  background: #fff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.graf-item:hover {
  transform: translateY(-4px);
}

.graf-item h3 {
  font-size: 1.2rem;
  color: #333;
  margin: 0;
}

canvas {
  width: 100% !important;
  height: 300px !important;
}

.ranking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.ranking-header button {
  background-color: #2196F3;
  color: #fff;
  border: none;
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
}

.ranking-header button:hover {
  background-color: #1976D2;
}
</style>
