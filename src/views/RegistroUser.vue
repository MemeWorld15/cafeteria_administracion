<template>
  <div class="registro-page">
    <div class="registro-container">
      <!-- Lado Izquierdo -->
      <div class="left-side">
        <img :src="logo" alt="Logo Cafetería" class="logo" />
      </div>

      <!-- Lado Derecho -->
      <div class="right-side">
        <h2>CREAR CUENTA</h2>
        <h3>Regístrate con tus datos</h3>
        <form @submit.prevent="registrarUsuario">
          <input v-model="nombre" type="text" placeholder="Nombre Completo" class="input-field" required />
          <input v-model="correo" type="email" placeholder="Correo Electrónico" class="input-field" required />

          <select v-model="grado" class="input-field" required>
            <option disabled value="">Selecciona tu grado</option>
            <option v-for="n in 9" :key="n" :value="n">{{ n }}</option>
          </select>

          <select v-model="carrera" class="input-field" required>
            <option disabled value="">Selecciona tu carrera</option>
            <option>Ingeniería en Software</option>
            <option>Lengua</option>
            <option>Administración</option>
          </select>

          <!-- Campo de contraseña con ojito -->
          <div class="password-wrapper" style="position: relative;">
            <input
              :type="mostrarContrasena ? 'text' : 'password'"
              v-model="contrasena"
              placeholder="Contraseña"
              class="input-field"
              required
            />
            <i
              class="fas"
              :class="mostrarContrasena ? 'fa-eye-slash' : 'fa-eye'"
              @click="mostrarContrasena = !mostrarContrasena"
              style="position: absolute; right: 10px; top: 12px; cursor: pointer;"
            ></i>
          </div>

          <!-- Campo de confirmar contraseña con ojito -->
          <div class="password-wrapper" style="position: relative;">
            <input
              :type="mostrarConfirmar ? 'text' : 'password'"
              v-model="confirmar"
              placeholder="Confirmar Contraseña"
              class="input-field"
              required
            />
            <i
              class="fas"
              :class="mostrarConfirmar ? 'fa-eye-slash' : 'fa-eye'"
              @click="mostrarConfirmar = !mostrarConfirmar"
              style="position: absolute; right: 10px; top: 12px; cursor: pointer;"
            ></i>
          </div>

          <button type="submit" class="register-button">REGISTRARSE</button>
        </form>

        <p class="login-text">
          ¿Ya tienes una cuenta?
          <router-link to="/login" class="login-link">Inicia sesión aquí</router-link>
        </p>

        <p v-if="mensaje" :style="{ color: mensajeColor, marginTop: '10px' }">{{ mensaje }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import '../EstilosCss/registro.css'
import logo from '../assets/images/LogoCafe.png'
import { registrarUsuario as apiRegistro } from '../api'

const router = useRouter()

const nombre = ref('')
const correo = ref('')
const grado = ref('')
const carrera = ref('')
const contrasena = ref('')
const confirmar = ref('')
const mensaje = ref('')
const mensajeColor = ref('green')

// Estado para mostrar/ocultar contraseña
const mostrarContrasena = ref(false)
const mostrarConfirmar = ref(false)

function validarCorreo(correo) {
  return correo.endsWith('@gmail.com') || correo.endsWith('@unach.mx')
}

async function registrarUsuario() {
  mensaje.value = ''

  if (!nombre.value || !correo.value || !grado.value || !carrera.value || !contrasena.value || !confirmar.value) {
    mensaje.value = 'Todos los campos son obligatorios.'
    mensajeColor.value = 'red'
    return
  }

  if (!validarCorreo(correo.value)) {
    mensaje.value = 'El correo debe ser @gmail.com o @unach.mx.'
    mensajeColor.value = 'red'
    return
  }

  if (contrasena.value !== confirmar.value) {
    mensaje.value = 'Las contraseñas no coinciden.'
    mensajeColor.value = 'red'
    return
  }

  try {
    const formData = new FormData()
    formData.append('nombre', nombre.value)
    formData.append('correo', correo.value)
    formData.append('grado', grado.value)
    formData.append('carrera', carrera.value)
    formData.append('contrasena', contrasena.value)

    const res = await apiRegistro(formData)

    if (!res.ok) {
      const data = await res.json()
      throw new Error(data?.detail || 'Error al registrar.')
    }

    mensaje.value = 'Registro exitoso. Redirigiendo...'
    mensajeColor.value = 'green'

    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err) {
    mensaje.value = err.message === 'Failed to fetch'
      ? 'No se pudo conectar al servidor.'
      : err.message
    mensajeColor.value = 'red'
  }
}
</script>
