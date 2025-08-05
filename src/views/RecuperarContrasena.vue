<template>
  <div class="recuperar-container">
    <div class="recuperar-card">
      <h2 class="titulo">Recuperar Contraseña</h2>
      <form @submit.prevent="enviarCorreo" class="formulario">
        <input
          v-model="correo"
          type="email"
          placeholder="Correo electrónico registrado"
          required
          class="input"
        />
        <button type="submit" class="boton">Enviar enlace</button>
      </form>
      <p v-if="mensaje" :style="{ color: mensajeColor, marginTop: '10px' }">
        {{ mensaje }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { recuperarContrasena } from '../api'

const correo = ref('')
const mensaje = ref('')
const mensajeColor = ref('green')

const enviarCorreo = async () => {
  try {
    const res = await recuperarContrasena(correo.value)
    if (!res.ok) throw new Error()
    mensaje.value = 'Hemos enviado un enlace a tu correo.'
    mensajeColor.value = 'green'
  } catch (e) {
    mensaje.value = 'Error: ¿El correo existe?'
    mensajeColor.value = 'red'
  }
}
</script>

<style scoped>
.recuperar-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #1e3d34; /* Verde oscuro como el login */
  padding: 1rem;
}

.recuperar-card {
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
