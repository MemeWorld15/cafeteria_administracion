<template>
  <div class="editar-perfil-container">
    <h2>Editar Perfil</h2>
    <div class="perfil-card">
      <div class="perfil-imagen-container" @click="seleccionarImagen">
        <!-- Imagen de perfil que siempre se mantiene visible -->
        <img :src="fotoPreview || fotoActual || defaultFoto" alt="Foto de perfil" class="perfil-imagen" />
        <!-- Capa de superposición para mostrar la previsualización de la nueva foto -->
        <div v-if="fotoPreview" class="overlay">📷 Cambiar foto</div>
      </div>
      <!-- Input de archivo oculto -->
      <input type="file" ref="fileInput" style="display: none;" @change="handleFileChange" accept="image/*" />

      <form @submit.prevent="guardarCambios" class="perfil-form">
        <label>Nombre:</label>
        <input v-model="nombre" type="text" required />

        <label>Correo:</label>
        <input v-model="correo" type="email" required />

        <button type="submit">Guardar Cambios</button>
        <p v-if="mensaje" :style="{ color: mensajeColor, marginTop: '0.5rem' }">{{ mensaje }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { BASE_URL } from '../config'
import { actualizarPerfil, obtenerPerfil } from '../api'

const nombre = ref('')
const correo = ref('')
const fotoActual = ref('')       // Imagen de perfil actual
const fotoPreview = ref('')      // Imagen previsualizada al seleccionar una nueva
const fotoFile = ref(null)       // Archivo de imagen
const mensaje = ref('')
const mensajeColor = ref('green')
const defaultFoto = 'ruta/a/imagen/default.jpg'  // Ruta de la imagen por defecto

// Función para cargar los datos del perfil desde el servidor
const cargarDatos = async () => {
  try {
    const id = localStorage.getItem('usuario_id')
    const datos = await obtenerPerfil(id)
    console.log('Datos del perfil:', datos) // << ESTE LOG
    nombre.value = datos.nombre
    correo.value = datos.correo
    fotoActual.value = datos.foto_url ? new URL(datos.foto_url, BASE_URL).href : ''
    console.log('fotoActual:', fotoActual.value)
  } catch {
    mensaje.value = 'Error al cargar datos.'
    mensajeColor.value = 'red'
  }
}
const emit = defineEmits(['foto-actualizada'])


// Función para abrir el selector de archivos cuando se hace click en la imagen
const seleccionarImagen = () => {
  fileInput.value.click()
}

// Ref para el input de archivo
const fileInput = ref(null)

// Función para manejar la selección de una nueva imagen
const handleFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    fotoFile.value = file
    fotoPreview.value = URL.createObjectURL(file)  // Crear URL temporal para la previsualización
  }
}

// Función para guardar los cambios en el perfil
const guardarCambios = async () => {
  try {
    const id = localStorage.getItem('usuario_id')
    const formData = new FormData()
    formData.append('nombre', nombre.value)
    formData.append('correo', correo.value)
    if (fotoFile.value) {
      formData.append('file', fotoFile.value)  // Adjuntar la nueva imagen
    }

    await actualizarPerfil(id, formData)
    mensaje.value = 'Perfil actualizado correctamente.'
    mensajeColor.value = 'green'
    fotoPreview.value = '' // Limpia la previsualización
    fotoFile.value = null  // Limpia el archivo
    await cargarDatos()    // Vuelve a cargar la foto actual y los datos
    emit('foto-actualizada', fotoActual.value) // Emitir al padre
  } catch {
    mensaje.value = 'Error al actualizar perfil.'
    mensajeColor.value = 'red'
  }
}



// Cargar los datos del perfil cuando se monta el componente
onMounted(() => {
  cargarDatos()
})
</script>


<style scoped>
.editar-perfil-container {
  max-width: 600px;
  margin: auto;
  padding: 2rem;
}

.perfil-card {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 2rem;
  flex-wrap: wrap;
}

.perfil-imagen-container {
  position: relative;
  cursor: pointer;
  width: 180px;
  height: 180px;
}

.perfil-imagen {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
  border: 3px solid #ccc;
  transition: transform 0.3s;
}

.perfil-imagen-container:hover .perfil-imagen {
  transform: scale(1.05);
}

/* La superposición solo se muestra si hay una previsualización */
.overlay {
  position: absolute;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  width: 100%;
  text-align: center;
  border-radius: 0 0 50% 50%;
  padding: 0.3rem;
  font-size: 0.9rem;
}

.perfil-form {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

.perfil-form label {
  font-weight: 500;
}

.perfil-form input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.perfil-form button {
  background: #2d8cf0;
  color: white;
  padding: 0.6rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.perfil-form button:hover {
  background: #1c6dc1;
}
</style>
