import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import RegistroUser from '../views/RegistroUser.vue'
import Administrador from '../views/Administrador.vue'
import ClienteCompra from '../views/ClienteCompra.vue'
import MenuCafe from '../views/MenuCafe.vue'
import UsuariosCard from '../views/UsuariosCard.vue'
import Cocina from '../views/Cocina.vue'
import RecuperarContrasena from '../views/RecuperarContrasena.vue'
import RestablecerContrasena from '../views/RestablecerContrasena.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/registro',
    name: 'registro',
    component: RegistroUser
  },
   {
    path: '/recuperar-contrasena',
    name: 'recuperar-contrasena',
    component: RecuperarContrasena
  },
  {
    path: '/restablecer-contrasena',
    name: 'restablecer-contrasena',
    component: RestablecerContrasena
  },
  {
    path: '/administrador',
    name: 'administrador',
    component: Administrador,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/cliente',
    name: 'cliente',
    component: ClienteCompra,
    meta: { requiresAuth: true, role: 'cliente' }
  },
  {
    path: '/menu',
    name: 'menu',
    component: MenuCafe,
    meta: { requiresAuth: true, role: 'cliente' }
  },
  {
    path: '/empleados',
    name: 'empleados',
    component: UsuariosCard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/cocina',
    name: 'cocina',
    component: Cocina,
    meta: { requiresAuth: true, role: 'chef' }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

//  Protección de rutas basada en el rol
router.beforeEach((to, from, next) => {
  const userRole = localStorage.getItem('usuario_rol')
  const requiresAuth = to.meta.requiresAuth
  const allowedRole = to.meta.role

  if (requiresAuth) {
    if (!userRole) {
      // No hay sesión
      return next('/login')
    }

    if (userRole !== allowedRole) {
      alert('⛔ Acceso no autorizado.')
      return next('/login')
    }
  }

  next()
})

export default router
