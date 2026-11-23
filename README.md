## Cambios de la versión 2026-11-23

- Se mantienen las **20 fotografías en el banco** y las **12 evaluaciones aleatorias por participante**; una fotografía adicional es la práctica y no se repite. No se modificó el tamaño de la tarea sin solicitarlo.
- Slider de 0.00 a 1.00 con once posiciones discretas en incrementos de 0.10, incluida la práctica. Se necesita mover la barra para habilitar **Siguiente** (o **Iniciar experimento** tras la práctica). No hay paso ni botón **Confirmar este valor** en el código fuente entregado: se conserva únicamente el botón de navegación imprescindible para enviar y guardar la respuesta.
- En la exportación general ancha `all_apps_wide`, cada `respuesta_XX` queda asociada con `rostro_id_XX`, que corresponde directamente a `_static/rostros/rostro_XX.png`. Se conserva el `custom_export` en formato largo con `orden_presentacion`, `rostro_id` y `archivo_imagen`, para una fila por evaluación. No se muestran estos IDs al participante.
- Revisar y validar en una **sesión nueva** después de actualizar la aplicación, ya que se agregaron campos al modelo Player. Probar un recorrido y verificar ambos tipos de CSV antes de recolectar datos reales.

# BEERLab — Experimento de percepción racial (oTree)

**Estado:** versión revisada posterior al piloto manual exitoso en GitHub Codespaces con Python 3.11 y a pruebas `otree test` completadas por el equipo. Se requiere volver a probar este ZIP actualizado antes de uso con participantes reales.

## Propósito y flujo
El estudio asigna **una de cuatro formulaciones** a cada participante:
1. negra(o)
2. afromexicana(o)
3. afrodescendiente
4. afromexicana(o), negra(o) o afrodescendiente (frase conjunta INEGI)

Pantallas: bienvenida → consentimiento (>18 años) → datos generales → instrucciones → práctica (no se exporta) → **12 rostros seleccionados aleatoriamente de 20**, sin reemplazo y sin mostrar de nuevo el rostro de práctica → cierre. La misma formulación se mantiene durante todo el recorrido. Cada rostro recibe una puntuación entre 0 y 1.

La práctica utiliza **uno de los 20 rostros** y luego se seleccionan 12 de los **19 restantes**. Por eso nunca se repite el rostro de práctica para ese participante.

## Estructura
- `settings.py` en la raíz: configuraciones oTree.
- `percepcion/__init__.py`: modelos, aleatorización, páginas y exportación.
- `percepcion/*.html`: pantallas responsivas del estudio.
- `percepcion/tests.py`: bot para el recorrido completo y comprobación de no repetición.
- `_static/rostros/`: 20 fotos derivadas del PDF proporcionado por el equipo, sin reconstrucción de facciones.

## Requisitos y prueba local
Python **3.11** sobre Linux (requisito de BEERLab). Versiones declaradas: `otree==6.0.15`, `psycopg2-binary==2.9.10`.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export ADMIN_PASSWORD="$(python -c 'import secrets; print(secrets.token_urlsafe(16))')"
otree test
otree devserver 8000
```

En Windows: `.venv\Scripts\activate`. Ejecuta desde la raíz de este repositorio.

Para probar bots:
```bash
otree test
```

Prueba las configuraciones `percepcion` y las cuatro `piloto_*` en dos navegadores independientes. En la sesión general, los grupos se distribuyen de forma aleatoria y aproximadamente equilibrada. Cada configuración piloto fuerza una sola condición para facilitar revisión. **No usar pilotos para reclutamiento real.**

## Datos y exportación
En el panel administrativo de oTree, exporta `all_apps_wide`, el CSV personalizado de la aplicación y `PageTimes` si se requieren tiempos. El `custom_export` de este proyecto genera **12 filas por participante completo**, con códigos seudónimos de participante y sesión, condición (número y texto), ID de rostro, **nombre exacto de archivo (`rostro_XX.png`)**, orden de presentación, respuesta 0–1 y datos generales. **No exporta** respuestas de práctica ni participantes con alguna de las 12 respuestas faltantes; estos últimos permanecen en los datos brutos de oTree. El ID de participante usado en la exportación es `p.participant.code` (no el ID interno del jugador, que puede repetirse entre sesiones). Almacena los datos únicamente en la base de datos configurada por el laboratorio; no escribe datos al disco del contenedor.

Los códigos de participante no contienen nombres, pero son identificadores seudónimos. Dar acceso exclusivamente al equipo autorizado y docente, según el consentimiento aprobado. El laboratorio administra las copias nocturnas; el equipo investigador realiza y resguarda las exportaciones.

## Variables de entorno
`ADMIN_PASSWORD` y `SECRET_KEY`, configuradas por el laboratorio. `DATABASE_URL` es configurada por el laboratorio y nunca aparece escrita en `settings.py`. No se necesitan variables `OTREE_` propias. No hay Rooms (`ROOMS = []`); se usan enlaces individuales de sesión.

## Ficha técnica para BEERLab
- Subdominio propuesto: `percepcion` (sujeto a disponibilidad).
- Versión de entrega: `0.1.1-azul-candidato` (identificar después tag Git y commit real).
- Configuración en producción: `percepcion`.
- Piloto: cuatro `piloto_*`.
- Participantes simultáneos y fechas: **por acordar con el equipo y el laboratorio**.
- Acceso administrativo: persona autorizada a definir por el equipo.
- Sin pagos ni materiales subidos por los participantes.
- El proyecto no incluye `Procfile`, `runtime.txt` ni Dockerfile.

## Pruebas antes del despliegue
- Ejecutar `otree devserver` y `otree test` bajo Python 3.11 y oTree instalado.
- Revisar visualmente cada formulario, textos y fotos, en escritorio y móvil.
- Verificar condiciones 1–4, datos exportados, tamaño de muestra y que práctica no reaparezca.
- Confirmar enlace administrativo y acceso, probar con dos navegadores, ejecutar prueba de producción y clonar el ZIP en una máquina limpia.
- Validar textos de consentimiento final con el expediente aprobado antes de reclutar.

**Validación:** el equipo confirmó previamente `Bots completed session` para cinco configuraciones y completó un piloto manual en Codespaces, con respuestas almacenadas en SQLite y vinculadas al orden de rostros. Estos resultados corresponden a la copia probada antes de la revisión de la exportación; vuelve a correr `otree test` y un piloto completo con este paquete. Antes de producción, BEERLab debe validar los textos de consentimiento, la configuración segura y la exportación real.

## Actualización desde Codespaces / GitHub

El ZIP incluye **la estructura completa del proyecto** (`settings.py` y `requirements.txt` en la raíz; HTML y Python en `percepcion/`; fotografías en `_static/rostros/`). Para sustituir la versión anterior, extrae el contenido y reemplaza los archivos correspondientes manteniendo las rutas. No arrastres todos los archivos a una sola carpeta.

Si haces pruebas en Codespaces, el puerto 8000 se abre desde la pestaña *Puertos* (dirección `.app.github.dev`); no abras `localhost` desde tu computadora. Los enlaces `/demo/...` y `/InitializeParticipant/...` que genere oTree con `localhost` pueden conservar la ruta pero sustituir el origen por la dirección de Codespaces.

## Exportar CSV desde oTree

En la consola administrativa, entra en **Data** y busca la descarga CSV específica de la app `percepcion` (*custom export*). En vez de interpretar la tabla ancha (que contiene `orden_rostros` y `respuesta_01` a `respuesta_12` por separado), usa este CSV para análisis: una fila = una fotografía evaluada. Este archivo se produce bajo demanda; no necesitas ejecutar el script temporal usado para revisar la base SQLite.

La columna `archivo_imagen` identifica el archivo de las fotografías; la práctica se excluye. Los pilotos son exclusivamente para pruebas, no para reclutamiento definitivo.

## Estilo azul (actualización del 18 de noviembre de 2026)

Se sustituyó la paleta naranja por azul en las siete pantallas (botones, encabezados, resaltados, control deslizante, fondo y etiquetas). No se modificaron los modelos, la aleatorización ni los datos registrados. Azul principal: `#2563B8`; fondo: `#F3F7FC`. Este cambio visual requiere una revisión rápida en escritorio y móvil.

**Antes de entregar al laboratorio:** generar commit/tag de esta versión; ejecutar `otree test` y recorrido manual tras actualizar; validar las cuatro condiciones y el CSV personalizado con 12 filas por participante completo; revisar consentimiento con el expediente aprobado; probar en una instalación limpia y coordinar con BEERLab fecha, capacidad simultánea, subdominio, persona responsable y credenciales/variables de entorno por vía segura. No incluir datos de prueba ni contraseñas en el repositorio.

Nota de interfaz: en Practica.html y Rostro.html se eliminan también, en caso de inyección por una plantilla anterior, elementos interactivos cuyo texto sea «Confirmar este valor». Solo queda Siguiente / Iniciar experimento. Para ver el cambio en una sesión desplegada hay que actualizar el código servido y refrescar la página.
