# Usuarios Predefinidos - Generador de Personas

## 🔐 Sistema de Acceso Restringido

El sistema está configurado para usar **SOLO** usuarios predefinidos:


## ⚠️ Características del Sistema:

- ✅ **Registro deshabilitado** - No se pueden crear nuevos usuarios
- ✅ **Solo usuarios predefinidos** - Acceso limitado a los dos usuarios
- ✅ **Contraseñas encriptadas** - Seguridad con bcrypt
- ✅ **Panel de administración** - Solo lectura (sin eliminación)

## 🚀 Para crear el archivo de usuarios:

Ejecuta el script:
```bash
python create_predefined_users.py
```

## 📋 Para Streamlit Cloud:

1. Ejecuta el script para generar `users.xlsx`
2. Convierte a JSON usando `convert_to_secrets.py`
3. Copia el JSON en Streamlit Cloud > Settings > Secrets

## 🔒 Seguridad:

- Las contraseñas están hasheadas con bcrypt
- No se almacenan en texto plano
- El archivo Excel está protegido por `.gitignore`
- Solo lectura en producción
