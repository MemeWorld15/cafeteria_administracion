<!-- src/components/Empleado.vue -->
<template>
  <div class="form-empleado">
    <h3>Agregar Nuevo Empleado</h3>
    <form @submit.prevent="crearEmpleado">
      <input v-model="empleado.nombre" type="text" placeholder="Nombre completo" required />
      <input v-model="empleado.correo" type="email" placeholder="Correo" required />
      <select v-model="empleado.ocupacion" required>
        <option disabled value="">Seleccionar ocupación</option>
        <option value="chef">Chef</option>
      </select>
      <input v-model="empleado.rendimiento" type="text" placeholder="Teléfono" required />
      <input v-model="empleado.contrasena" type="text" placeholder="Contraseña" required />

      <button type="button" @click="generarContrasena">Generar Contraseña Aleatoria</button>
      <button type="submit">Registrar</button>
      <p v-if="mensaje" :style="{ color: mensajeColor }">{{ mensaje }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { crearEmpleado as crearEmpleadoAPI } from '../api'

const emit = defineEmits(['empleado-creado'])

const empleado = ref({
  nombre: '',
  correo: '',
  ocupacion: '',
  rendimiento: '',
  contrasena: ''
})

const mensaje = ref('')
const mensajeColor = ref('green')

const crearEmpleado = async () => {
  mensaje.value = ''
  try {
    const creadorId = parseInt(localStorage.getItem('usuario_id') || '0')
    if (!creadorId) {
      mensaje.value = 'Error: usuario no autenticado.'
      mensajeColor.value = 'red'
      return
    }

    const formData = new FormData()
    Object.entries(empleado.value).forEach(([key, val]) => formData.append(key, val))
    formData.append('creado_por', creadorId)

    const res = await crearEmpleadoAPI(formData)
    if (!res.ok) throw new Error()

    mensaje.value = 'Empleado creado exitosamente.'
    mensajeColor.value = 'green'
    emit('empleado-creado')  // Para notificar al componente padre

    empleado.value = {
      nombre: '',
      correo: '',
      ocupacion: '',
      rendimiento: '',
      contrasena: ''
    }
  } catch {
    mensaje.value = 'Error al registrar empleado.'
    mensajeColor.value = 'red'
  }
}

const generarContrasena = () => {
  const caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
  let password = ""
  for (let i = 0; i < 8; i++) {
    password += caracteres.charAt(Math.floor(Math.random() * caracteres.length))
  }
  empleado.value.contrasena = password
}
</script>

