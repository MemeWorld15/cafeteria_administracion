<template>
  <div class="restablecer-container">
    <div class="restablecer-card">
      <h2 class="titulo">Restablecer Contraseña</h2>
      <form @submit.prevent="enviar" class="formulario">
        <input
          v-model="nuevaContrasena"
          type="password"
          placeholder="Nueva contraseña"
          required
          class="input"
        />
        <input
          v-model="confirmar"
          type="password"
          placeholder="Confirmar contraseña"
          required
          class="input"
        />
        <button type="submit" class="boton">Actualizar contraseña</button>
      </form>
      <p v-if="mensaje" :style="{ color: mensajeColor, marginTop: '10px' }">
        {{ mensaje }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { restablecerContrasena } from '../api'

const route = useRoute()
const router = useRouter()
const token = ref('')
const nuevaContrasena = ref('')
const confirmar = ref('')
const mensaje = ref('')
const mensajeColor = ref('green')

onMounted(() => {
  token.value = route.query.token
})

const enviar = async () => {
  if (nuevaContrasena.value !== confirmar.value) {
    mensaje.value = 'Las contraseñas no coinciden.'
    mensajeColor.value = 'red'
    return
  }

  try {
    const res = await restablecerContrasena(token.value, nuevaContrasena.value)
    if (!res.ok) throw new Error()
    mensaje.value = 'Contraseña actualizada correctamente.'
    mensajeColor.value = 'green'
    setTimeout(() => router.push('/login'), 2000)
  } catch (e) {
    mensaje.value = 'Token inválido o expirado.'
    mensajeColor.value = 'red'
  }
}
</script>

<style scoped>
.restablecer-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #1e3d34; /* Igual que el fondo de login y recuperar */
  padding: 1rem;
}

.restablecer-card {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.titulo {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #1e3d34;
}

.formulario {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input {
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
}

.input:focus {
  border-color: #1e3d34;
}

.boton {
  padding: 0.75rem;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.boton:hover {
  background-color: #333;
}
</style>
