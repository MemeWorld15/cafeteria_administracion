<template>
  <div class="usuarios-card">
    <h3>Empleados Registrados</h3>

    <!-- Mensaje de eliminación -->
    <p v-if="mensaje" :class="['alerta', mensajeColor]">{{ mensaje }}</p>

    <table v-if="empleados.length > 0">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Ocupación</th>
          <th>Correo</th>
          <th>Rendimiento</th>
          <th>Contraseña</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="emp in empleados" :key="emp.id">
          <td>
            <img :src="emp.foto || defaultAvatar" class="avatar" />
            {{ emp.nombre }}
          </td>
          <td>{{ emp.ocupacion }}</td>
          <td>{{ emp.correo }}</td>
          <td class="tel-verde">{{ emp.rendimiento }}</td>
          <td>
            <span>
              {{ mostrarContrasenas[emp.id] ? emp.contrasena : '••••••' }}
            </span>
            <Icon
              :icon="mostrarContrasenas[emp.id] ? 'mdi:eye-off' : 'mdi:eye'"
              @click="toggleContrasena(emp.id)"
              style="margin-left: 0.5rem; cursor: pointer;"
              class="icon-eye"
            />
          </td>
          <td>
            <Icon icon="mdi:pencil" class="edit-icon" @click="editarEmpleado(emp)" />
            <Icon icon="mdi:trash-can" class="trash-icon" @click="eliminarEmpleado(emp.id)" />
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else style="margin-top: 1rem; color: #888;">No hay empleados registrados aún.</p>
    <div v-if="empleadoEditando" class="modal-editar">
      <h4>Editar Empleado</h4>
      <form @submit.prevent="guardarEdicion">
        <label>Nombre: <input v-model="empleadoEditando.nombre" required /></label><br />
        <label>Correo: <input v-model="empleadoEditando.correo" required /></label><br />
        <label>Ocupación: <input v-model="empleadoEditando.ocupacion" required /></label><br />
        <label>Rendimiento: <input v-model="empleadoEditando.rendimiento" required /></label><br />
        <label>Contraseña: <input v-model="empleadoEditando.contrasena" required /></label><br />
        <button type="submit">Guardar</button>
        <button type="button" @click="cancelarEdicion">Cancelar</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import '../EstilosCss/usercard.css'
import { BASE_URL } from '../config'
import { fetchEmpleados,  actualizarEmpleadoPorId, eliminarEmpleadoPorId } from '../api'

const props = defineProps({
  fotoActual: {
    type: String,
    default: ''
  }
})

const empleados = ref([])
const defaultAvatar = 'https://i.pravatar.cc/50?img=11'
const mensaje = ref('')
const mensajeColor = ref('success')
const mostrarContrasenas = ref({})

const toggleContrasena = (id) => {
  mostrarContrasenas.value[id] = !mostrarContrasenas.value[id]
}

const cargarEmpleados = async () => {
  try {
    const data = await fetchEmpleados()
    const adminId = parseInt(localStorage.getItem('usuario_id') || '0')

    empleados.value = data.map(emp => ({
      ...emp,
      foto: emp.foto ? new URL(emp.foto, BASE_URL).href : ''
    }))
  } catch (err) {
    mensaje.value = 'Error al cargar empleados.'
    mensajeColor.value = 'error'
  }
}
//Editar empleado
const empleadoEditando = ref(null)

const editarEmpleado = (emp) => {
  empleadoEditando.value = { ...emp } // Copia para evitar modificar directamente
}

const cancelarEdicion = () => {
  empleadoEditando.value = null
}

const guardarEdicion = async () => {
  try {
    const id = empleadoEditando.value.id
    const formData = new FormData()
    formData.append('nombre', empleadoEditando.value.nombre)
    formData.append('correo', empleadoEditando.value.correo)
    formData.append('ocupacion', empleadoEditando.value.ocupacion)
    formData.append('rendimiento', empleadoEditando.value.rendimiento)
    formData.append('contrasena', empleadoEditando.value.contrasena)

    const res = await actualizarEmpleadoPorId(id, formData)
    if (!res.ok) throw new Error()

    mensaje.value = 'Empleado actualizado correctamente.'
    mensajeColor.value = 'success'
    empleadoEditando.value = null
    await cargarEmpleados()
  } catch {
    mensaje.value = 'Error al actualizar empleado.'
    mensajeColor.value = 'error'
  }

  setTimeout(() => (mensaje.value = ''), 3000)
}

const eliminarEmpleado = async (id) => {
  if (!confirm('¿Estás seguro de eliminar este empleado?')) return

  try {
    const res = await eliminarEmpleadoPorId(id)
    if (!res.ok) throw new Error()

    mensaje.value = 'El empleado ha sido eliminado.'
    mensajeColor.value = 'success'
    await cargarEmpleados()
  } catch {
    mensaje.value = 'Error al eliminar empleado.'
    mensajeColor.value = 'error'
  }

  setTimeout(() => (mensaje.value = ''), 3000)
}

onMounted(() => {
  cargarEmpleados()
})

</script>


