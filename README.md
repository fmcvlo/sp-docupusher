# SP Docupusher

Este repositorio contiene un script diseñado para automatizar el manejo de Stored Procedures (SP), incluyendo su registro, documentación y control de versiones en un entorno de desarrollo estructurado.

## Funcionalidades

- **Registro de SP**: Registra y mueve automáticamente los SP a un directorio organizado.
- **Documentación**: Actualiza automáticamente el archivo de documentación de SP con las descripciones y tickets asociados.
- **Control de versiones**: Realiza commits automáticos al repositorio Git, manteniendo un historial de cambios actualizado.
- **Validación de archivos**: Verifica si los SP están creados o deben generarse, evitando conflictos con archivos duplicados.

## Requisitos

- Python 3.9 o superior.
- Sistema operativo Windows.
- Git instalado y configurado.
- Acceso a un repositorio Git para almacenar los cambios.

## Estructura del Proyecto

📂 sps-vbolsa
├── 📂 Ejecuciones
│ ├── 📂 v11.1.6
│ ├── 📂 v11.1.7
│ └── SP_Registro.md
├── 📂 Sps
│ ├── ejemplo_sp.sql
└── SP_Documentation.md

## Uso

### 1. Configuración Inicial

1. Clona este repositorio en tu sistema local.

   ```bash
   git clone <URL_DEL_REPOSITORIO>

   ```

2. Asegúrate de que las rutas definidas en el script (`BASE_PATH`, `REPO_BASE_PATH`) coincidan con tu entorno local.

### 2. Ejecución del Script

1. Navega al directorio donde está el script.

   cd C:/Users/fmachiavello/script

2. Ejecuta el script:

   python script.py

### 3. Interacción con el Script

El script te hará una serie de preguntas:

1. **Versión del SP**: Ingresa la versión del directorio donde se registrará el SP (por ejemplo, `11.1.7`).
2. **SP Creado**: Indica si el SP ya está creado (`s/n`):
   - Si seleccionas `s`, el script buscará el SP en el directorio `sps`.
   - Si seleccionas `n`, deberás proporcionar el contenido del SP para que se cree un archivo nuevo.
3. **Estado de Ejecución**: Especifica si el SP se ejecutó con éxito (`e`) o falló (`f`).
4. **Notas**: Ingresa cualquier nota adicional para el registro.
5. **Descripción del SP**: Proporciona una descripción breve del SP.
6. **Número de Ticket**: Indica el número del ticket asociado al SP.

### 4. Actualización Automática

El script realizará las siguientes acciones:

1. Moverá el archivo del SP al directorio correspondiente.
2. Actualizará el archivo de registro (`SP_Registro.md`).
3. Actualizará la documentación (`SP_Documentation.md`).
4. Hará un commit y push al repositorio Git.

## Ejemplo de Salida

Ingresa la versión de la carpeta de ejecuciones (por ejemplo, 11.1.7): v11.1.7
¿El SP ya está creado? (s/n): s
Estado de ejecución (e/f): e
Notas adicionales (opcional): Fix aplicado en validación de cuentas
Descripción del SP: Validación de cuentas duplicadas
Número de ticket asociado: SDP-12345
Registro actualizado en: C:/Users/fmachiavello/sps-vbolsa/Ejecuciones/v11.1.7/SP_Registro.md
Documentación actualizada correctamente, con doble tabulación en las nuevas entradas.
Cambios subidos al repositorio.

## Contribuciones

Si deseas contribuir, por favor abre un issue o crea un pull request con tus sugerencias.

## Licencia

Este proyecto está licenciado bajo los términos de la [MIT License](LICENSE).

**Desarrollado por**: Franco Machiavello
