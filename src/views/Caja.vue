<template>
  <div class="caja-container">
    <div class="main-grid">
      <!-- Header Principal -->
      <div class="header-card">
        <div class="header-content">
          <div class="header-icon"><Icon icon="mdi:cash-register" /></div>
          <div class="header-text">
            <h1>Sistema de Caja</h1>
            <p>Control integral de ventas y arqueo</p>
          </div>
        </div>
        <div class="header-stats">
          <div class="stat-item">
            <div class="stat-value">${{ totalVentas.toFixed(2) }}</div>
            <div class="stat-label">Total Ventas</div>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <div class="stat-value">${{ totalGastos.toFixed(2) }}</div>
            <div class="stat-label">Total Gastos</div>
          </div>
        </div>
      </div>

      <!-- Configuración del Corte -->
      <div class="config-card">
        <div class="card-header">
          <h3><Icon icon="mdi:cog" /> Configuración</h3>
        </div>
        <div class="config-content">
          <div class="config-row">
            <div class="input-container">
              <label><Icon icon="mdi:calendar" /> Fecha</label>
              <input type="date" v-model="fechaSeleccionada" @change="calcularCorte" class="modern-input" />
            </div>
            <div class="input-container">
              <label><Icon icon="mdi:clock-outline" /> Turno</label>
              <select v-model="turnoSeleccionado" @change="calcularCorte" class="modern-select">
                <option value="matutino">🌅 Matutino</option>
                <option value="vespertino">🌆 Vespertino</option>
                <option value="nocturno">🌙 Nocturno</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Arqueo de Caja -->
      <div class="arqueo-card">
        <div class="card-header">
          <h3><Icon icon="mdi:target" /> Arqueo de Caja</h3>
        </div>
        <div class="arqueo-content">
          <div class="arqueo-input-section">
            <div class="money-input-wrapper">
              <label><Icon icon="mdi:cash" /> Monto en Caja </label>
              <div class="money-input">
                <span class="currency">$</span>
                <input type="number" v-model.number="montoEnCaja" placeholder="0.00" class="amount-field" />
              </div>
            </div>
            <button @click="realizarArqueo" class="btn-arqueo">
              <span class="btn-icon"><Icon icon="mdi:magnify" /></span>
              Realizar Arqueo
            </button>
          </div>

          <div v-if="resultadoArqueo !== null" class="arqueo-result">
            <div v-if="resultadoArqueo === 0" class="result-perfect">
              <div class="result-icon"><Icon icon="mdi:party-popper" /> ¡Perfecto!</div>
              <div class="result-content">
                <p>La caja está completamente cuadrada</p>
              </div>
            </div>
            <div v-else-if="resultadoArqueo > 0" class="result-excess">
              <div class="result-icon"><Icon icon="mdi:trending-up" /></div>
              <div class="result-content">
                <h4>Exceso de ${{ resultadoArqueo.toFixed(2) }}</h4>
                <p>Hay dinero adicional en la caja</p>
              </div>
            </div>
            <div v-else class="result-deficit">
              <div class="result-icon"><Icon icon="mdi:trending-down" /></div>
              <div class="result-content">
                <h4>Déficit de ${{ Math.abs(resultadoArqueo).toFixed(2) }}</h4>
                <p>Falta dinero en la caja</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Gastos de Caja -->
      <div class="gastos-card">
        <div class="card-header">
          <h3><Icon icon="mdi:clipboard-list" /> Gastos de Caja</h3>
          <div class="gastos-summary">
            <span class="total-gastos-badge">${{ totalGastos.toFixed(2) }}</span>
          </div>
        </div>

        <div class="gastos-content">
          <div class="add-gasto-section">
            <div class="add-gasto-form">
              <div class="form-row">
                <div class="input-container flex-2">
                  <input v-model="nuevoGasto.descripcion" placeholder="Descripción del gasto..." class="modern-input" />
                </div>
                <div class="input-container flex-1">
                  <div class="money-input">
                    <span class="currency">$</span>
                    <input type="number" v-model.number="nuevoGasto.monto" placeholder="0.00" class="amount-field" />
                  </div>
                </div>
                <button @click="agregarGasto" class="btn-add-gasto">
                  <span class="btn-icon"><Icon icon="mdi:plus" /> Agregar</span>
                </button>
              </div>
            </div>
          </div>

          <div class="gastos-list" v-if="gastos.length > 0">
            <div class="gastos-header">
              <span>Detalle de Gastos</span>
              <span>{{ gastos.length }} {{ gastos.length === 1 ? 'gasto' : 'gastos' }}</span>
            </div>
            <div class="gastos-items">
              <div v-for="(gasto, index) in gastos" :key="index" class="gasto-item">
                <div class="gasto-icon"><Icon icon="mdi:credit-card" /></div>
                <div class="gasto-details">
                  <div class="gasto-descripcion">{{ gasto.descripcion }}</div>
                  <div class="gasto-timestamp">{{ new Date().toLocaleTimeString() }}</div>
                </div>
                <div class="gasto-amount">${{ gasto.monto.toFixed(2) }}</div>
                <button @click="eliminarGasto(index)" class="btn-delete-gasto">
                  <span><Icon icon="mdi:trash-can" /> Eliminar</span>
                </button>
              </div>
            </div>
          </div>

          <div v-else class="no-gastos">
            <div class="no-gastos-icon"><Icon icon="mdi:note-text" /></div>
            <p>No hay gastos registrados para este turno</p>
          </div>
        </div>
      </div>

      <!-- Resumen y Acciones (contenido a exportar) -->
      <div id="corte-pdf">
        <div class="summary-card">
          <div class="summary-content">
            <div class="summary-row">
              <div class="summary-item">
                <div class="summary-label">Ventas Totales</div>
                <div class="summary-value positive">${{ totalVentas.toFixed(2) }}</div>
              </div>
              <div class="summary-item">
                <div class="summary-label">Gastos Totales</div>
                <div class="summary-value negative">-${{ totalGastos.toFixed(2) }}</div>
              </div>
              <div class="summary-item highlight">
                <div class="summary-label">Total Esperado</div>
                <div class="summary-value">${{ (totalVentas - totalGastos).toFixed(2) }}</div>
              </div>
            </div>

            <div class="arqueo-info">
              <p><strong>Monto en Caja:</strong> ${{ montoEnCaja.toFixed(2) }}</p>
              <p><strong>Resultado:</strong> 
                <span v-if="resultadoArqueo === 0">Caja Cuadrada</span>
                <span v-else-if="resultadoArqueo > 0">Exceso de ${{ resultadoArqueo.toFixed(2) }}</span>
                <span v-else>Déficit de ${{ Math.abs(resultadoArqueo).toFixed(2) }}</span>
              </p>
              <p><strong>Fecha:</strong> {{ fechaSeleccionada }} | <strong>Turno:</strong> {{ turnoSeleccionado }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Botones -->
      <div class="action-buttons">
        <button @click="guardarCorte" class="btn-save-corte">
          <span class="btn-icon"><Icon icon="mdi:content-save" /></span>
          Guardar Corte de Caja
        </button>
        <button @click="generarPDF" class="btn-report">
          <span class="btn-icon"><Icon icon="mdi:file-pdf" /></span>
          Generar PDF
        </button>
        <button @click="generarCSV" class="btn-report">
          <span class="btn-icon"><Icon icon="mdi:file-excel" /></span>
          Exportar CSV
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import '../EstilosCss/base.css'
import '../EstilosCss/layout.css'
import '../EstilosCss/caja.css'
import '../EstilosCss/dark-mode.css'
import '../EstilosCss/components.css'
import html2pdf from 'html2pdf.js'
import { fetchOrdenes,guardarCorteCaja  } from '../api'

const fechaSeleccionada = ref(new Date().toISOString().slice(0, 10))
const turnoSeleccionado = ref('matutino')
const totalVentas = ref(0)
const montoEnCaja = ref(0)
const resultadoArqueo = ref(null)

const gastos = ref([])
const nuevoGasto = ref({ descripcion: '', monto: 0 })

const calcularCorte = async () => {
  const todasOrdenes = await fetchOrdenes()
  const ordenesDelDia = todasOrdenes.filter(o =>
    o.fecha.startsWith(fechaSeleccionada.value) &&
    o.turno === turnoSeleccionado.value
  )
  totalVentas.value = ordenesDelDia.reduce((total, orden) => {
    const totalOrden = orden.productos.reduce((suma, p) => suma + p.cantidad * p.precio_unitario, 0)
    return total + totalOrden
  }, 0)
  resultadoArqueo.value = null
}

const totalGastos = computed(() => gastos.value.reduce((sum, g) => sum + g.monto, 0))

const realizarArqueo = () => {
  const totalEsperado = totalVentas.value - totalGastos.value
  resultadoArqueo.value = montoEnCaja.value - totalEsperado
}

const agregarGasto = () => {
  if (nuevoGasto.value.descripcion.trim() && nuevoGasto.value.monto > 0) {
    gastos.value.push({ 
      ...nuevoGasto.value,
      timestamp: new Date().toISOString()
    })
    nuevoGasto.value = { descripcion: '', monto: 0 }
  }
}

const eliminarGasto = (index) => {
  gastos.value.splice(index, 1)
}

const guardarCorte = async () => {
  const corte = {
    fecha: fechaSeleccionada.value,
    turno: turnoSeleccionado.value,
    totalVentas: totalVentas.value,
    gastos: gastos.value,
    totalGastos: totalGastos.value,
    montoCaja: montoEnCaja.value,
    resultado: resultadoArqueo.value
  }

  try {
    const response = await guardarCorteCaja(corte)

    if (response.ok) {
      alert('✅ Corte guardado exitosamente.')
    } else {
      const error = await response.json()
      alert('❌ Error al guardar corte: ' + error.detail)
    }
  } catch (error) {
    alert('❌ Error en conexión con backend: ' + error.message)
  }
}

const generarPDF = () => {
  const element = document.getElementById('corte-pdf')
  html2pdf().set({
    margin: 10,
    filename: `corte_caja_${fechaSeleccionada.value}_${turnoSeleccionado.value}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
  }).from(element).save()
}

const generarCSV = () => {
  let csvContent = `Descripción,Monto\n`
  gastos.value.forEach(g => {
    csvContent += `"${g.descripcion}",${g.monto.toFixed(2)}\n`
  })

  csvContent += `\nTotal Ventas,${totalVentas.value.toFixed(2)}\n`
  csvContent += `Total Gastos,${totalGastos.value.toFixed(2)}\n`
  csvContent += `Monto en Caja,${montoEnCaja.value.toFixed(2)}\n`
  csvContent += `Resultado Arqueo,${resultadoArqueo.value?.toFixed(2) || 0}\n`

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', `corte_caja_${fechaSeleccionada.value}_${turnoSeleccionado.value}.csv`)
  link.click()
}

onMounted(() => {
  calcularCorte()
})
</script>

