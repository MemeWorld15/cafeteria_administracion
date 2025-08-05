<template>
  <div class="historial-container">
    <div class="main-grid">
      <!-- Header -->
      <div class="header-card">
        <div class="header-content">
          <div class="header-icon"><Icon icon="mdi:history" /></div>
          <div class="header-text">
            <h1>Historial de Cortes de Caja</h1>
            <p>Consulta de registros guardados</p>
          </div>
        </div>
      </div>

      <!-- Filtros -->
      <div class="filter-card">
        <div class="card-header">
          <h3><Icon icon="mdi:filter" /> Filtros</h3>
        </div>
        <div class="filter-content">
          <div class="filter-row">
            <div class="input-container">
              <label><Icon icon="mdi:calendar" /> Fecha</label>
              <input type="date" v-model="filtroFecha" class="modern-input" />
            </div>
            <div class="input-container">
              <label><Icon icon="mdi:clock-outline" /> Turno</label>
              <select v-model="filtroTurno" class="modern-select">
                <option value="">Todos</option>
                <option value="matutino"><Icon icon="mdi:weather-sunset" /> Matutino</option>
                <option value="vespertino"><Icon icon="mdi:weather-sunny" /> Vespertino</option>
                <option value="nocturno"><Icon icon="mdi:weather-night" /> Nocturno</option>
              </select>
            </div>
            <button @click="filtrarCortes" class="btn-filtrar">
              <span class="btn-icon"><Icon icon="mdi:magnify" /></span> Filtrar
            </button>
          </div>
        </div>
      </div>

      <!-- Tabla de Historial -->
      <div class="tabla-card">
        <div class="card-header">
          <h3><Icon icon="mdi:table" /> Registros</h3>
        </div>
        <div class="tabla-content">
          <table class="tabla-historial">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Turno</th>
                <th>Total Ventas</th>
                <th>Total Gastos</th>
                <th>Monto Caja</th>
                <th>Resultado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(corte, index) in cortesFiltrados" :key="index">
                <td>{{ corte.fecha }}</td>
                <td>{{ corte.turno }}</td>
                <td>${{ corte.total_ventas.toFixed(2) }}</td>
                <td>-${{ corte.total_gastos.toFixed(2) }}</td>
                <td>${{ corte.monto_caja.toFixed(2) }}</td>
                <td>
                  <span v-if="corte.resultado === 0"><Icon icon="mdi:check-circle" class="text-green-500" /> Cuadrada</span>
                  <span v-else-if="corte.resultado > 0"><Icon icon="mdi:trending-up" class="text-blue-500" /> Exceso ${{ corte.resultado.toFixed(2) }}</span>
                  <span v-else><Icon icon="mdi:trending-down" class="text-red-500" /> Déficit ${{ Math.abs(corte.resultado).toFixed(2) }}</span>
                </td>
              </tr>
              <tr v-if="cortesFiltrados.length === 0">
                <td colspan="6" style="text-align: center;">Sin registros encontrados</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { fetchCortesCaja } from '../api'

import '../EstilosCss/components.css'
import '../EstilosCss/base.css'
import '../EstilosCss/layout.css'

const cortesGuardados = ref([])
const filtroFecha = ref('')
const filtroTurno = ref('')

const cortesFiltrados = computed(() => {
  return cortesGuardados.value.filter(corte => {
    const coincideFecha = filtroFecha.value ? corte.fecha === filtroFecha.value : true
    const coincideTurno = filtroTurno.value ? corte.turno === filtroTurno.value : true
    return coincideFecha && coincideTurno
  })
})

const filtrarCortes = () => {
  // El filtrado lo hace automáticamente el computed
}

onMounted(async () => {
  try {
    const cortes = await fetchCortesCaja()
    cortesGuardados.value = cortes
  } catch (error) {
    console.error('Error al obtener cortes:', error)
    alert('Ocurrió un error al cargar el historial de cortes')
  }
})
</script>

<style scoped>
.tabla-historial {
  width: 100%;
  border-collapse: collapse;
}

.tabla-historial th,
.tabla-historial td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.tabla-historial th {
  background-color: #f5f5f5;
  font-weight: bold;
}
.main-grid {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  margin-top: 1rem;
  align-items: start;
}

/* Filtros */
.filter-card {
  background-color: #fff;
  border: 1px solid #e2e2e2;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.filter-row {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-container {
  display: flex;
  flex-direction: column;
}

.modern-input,
.modern-select {
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

/* Botón */
.btn-filtrar {
  background-color: #1e8e3e;
  color: white;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s;
}

.btn-filtrar:hover {
  background-color: #166c2f;
}

/* Tabla */
.tabla-card {
  background-color: #fff;
  border-radius: 8px;
  border: 1px solid #ddd;
  padding: 1rem;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

</style>
