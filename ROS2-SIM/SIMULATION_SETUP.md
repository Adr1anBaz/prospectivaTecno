# Unitree Go2 AIR — Simulación MuJoCo + ROS 2 Humble

## Guía Completa de Configuración del Entorno de Simulación

---

## Tabla de Contenidos

1. [Arquitectura del Sistema](#1-arquitectura-del-sistema)
2. [Pre-requisitos](#2-pre-requisitos)
3. [Instalación de Dependencias del Sistema](#3-instalación-de-dependencias-del-sistema)
4. [Obtención de MuJoCo 3.2.6](#4-obtención-de-mujoco-326)
5. [Compilación del SDK Unitree (unitree_sdk2)](#5-compilación-del-sdk-unitree-unitree_sdk2)
6. [Estructura del Workspace](#6-estructura-del-workspace)
7. [Limpieza de Artefactos Previos](#7-limpieza-de-artefactos-previos)
8. [Corrección de los CMakeLists.txt de Interfaces ROS 2](#8-corrección-de-los-cmakeliststxt-de-interfaces-ros-2)
9. [Corrección del Hack `#define private public` en main.cc](#9-corrección-del-hack-define-private-public-en-maincc)
10. [Configuración de CycloneDDS](#10-configuración-de-cyclonedds)
11. [Compilación del Workspace Completo](#11-compilación-del-workspace-completo)
12. [Resolución de Archivos de Modelo (scene.xml)](#12-resolución-de-archivos-de-modelo-scenexml)
13. [Ejecución del Simulador](#13-ejecución-del-simulador)
14. [Problemas Comunes y Soluciones](#14-problemas-comunes-y-soluciones)
15. [Resumen de Comandos](#15-resumen-de-comandos)

---

## 1. Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────┐
│  Distrobox Container (Ubuntu 22.04)                 │
│  ROS 2 Humble + CycloneDDS                          │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │  ~/unitree_ws/                               │   │
│  │  ├── src/                                    │   │
│  │  │   ├── unitree_ros2/  (interfaces ROS 2)   │   │
│  │  │   │   ├── unitree_api/  (8 mensajes)      │   │
│  │  │   │   ├── unitree_go/   (23 mensajes Go2) │   │
│  │  │   │   └── unitree_hg/   (11 mensajes H1)  │   │
│  │  │   └── unitree_mujoco/  (simulador MuJoCo) │   │
│  │  ├── build/  (artefactos de compilación)     │   │
│  │  └── install/ (paquetes instalados)          │   │
│  └──────────────────────────────────────────────┘   │
│                                                     │
│  Dependencias externas:                             │
│  ├── /opt/ros/humble/          (ROS 2 Humble)       │
│  ├── /usr/local/lib/libunitree_sdk2.a (SDK nativo) │
│  ├── ~/unitree_sdk2/thirdparty/ (CycloneDDS 0.10.2)│
│  └── MuJoCo 3.2.6 (vendored en simulate/mujoco/)   │
└─────────────────────────────────────────────────────┘
```

### Flujo de comunicación

```
MuJoCo (física) ──► unitree_mujoco ──► unitree_sdk2 ──► CycloneDDS ──► ROS 2
       ▲                  ▲                  ▲
   simulación       renderizado        puente DDS
   Go2 AIR          GLFW+MuJoCo        (mensajes)
```

---

## 2. Pre-requisitos

### 2.1 Entorno contenedor

El desarrollo se realiza dentro de un contenedor **Distrobox** con Ubuntu 22.04:

```bash
# Verificar que estamos dentro del contenedor
cat /etc/os-release
# PRETTY_NAME="Ubuntu 22.04.5 LTS"

# Verificar ROS 2 Humble
echo $ROS_DISTRO
# humble
```

### 2.2 ROS 2 Humble base

```bash
# Si no está instalado:
sudo apt update
sudo apt install ros-humble-ros-base

# Paquetes adicionales necesarios:
sudo apt install \
  ros-humble-rosidl-default-generators \
  ros-humble-rosidl-default-runtime \
  ros-humble-rmw-cyclonedds-cpp \
  ros-humble-rosbag2-cpp \
  ros-humble-ros2cli \
  ros-humble-ros2pkg \
  ros-humble-ros2interface \
  ros-humble-ros2topic \
  ros-humble-ros2node \
  ros-humble-ros2action \
  ros-humble-ros2service \
  ros-humble-ros2param
```

### 2.3 Dependencias de sistema

```bash
sudo apt install \
  libeigen3-dev \
  libboost-all-dev \
  libglfw3-dev \
  libglfw3 \
  libyaml-cpp-dev \
  libfmt-dev \
  cmake \
  build-essential \
  git
```

### 2.4 SDK Unitree (unitree_sdk2)

El SDK debe estar clonado y compilado en `~/unitree_sdk2/`. El repositorio contiene:

- **Biblioteca estática precompilada**: `lib/x86_64/libunitree_sdk2.a`
- **CycloneDDS empaquetado**: `thirdparty/lib/x86_64/libddsc.so` y `libddscxx.so`
- **Headers**: `include/`
- **Ejemplos**: `example/`

```bash
cd ~
git clone https://github.com/unitreerobotics/unitree_sdk2.git
cd unitree_sdk2
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
sudo make install
```

> **IMPORTANTE**: El SDK empaqueta CycloneDDS **0.10.2 compilado sin shared memory (`noshm`)**. Esta versión es crucial — ver sección 10.

### 2.5 Repositorios del workspace

```bash
mkdir -p ~/unitree_ws/src
cd ~/unitree_ws/src

# Interfaces ROS 2 de Unitree
git clone https://github.com/unitreerobotics/unitree_ros2.git

# Simulador MuJoCo de Unitree
git clone https://github.com/unitreerobotics/unitree_mujoco.git
```

---

## 3. Instalación de Dependencias del Sistema

```bash
sudo apt-get update

# GLFW3 — ventana de simulación
sudo apt-get install -y libglfw3-dev libglfw3

# Herramientas ROS 2 CLI
sudo apt-get install -y \
  ros-humble-ros2cli \
  ros-humble-ros2pkg \
  ros-humble-ros2interface \
  ros-humble-ros2topic \
  ros-humble-ros2node \
  ros-humble-ros2action \
  ros-humble-ros2service \
  ros-humble-ros2param

# RMW CycloneDDS (necesario en build-time para find_package(rclcpp))
sudo apt-get install -y ros-humble-rmw-cyclonedds-cpp
```

> **Nota**: `ros-humble-rmw-cyclonedds-cpp` instala también `ros-humble-cyclonedds` (v0.10.5) y `ros-humble-iceoryx-*` como dependencias. Estos NO serán usados por el simulador (usamos la versión empaquetada 0.10.2), pero son necesarios para compilar los paquetes ROS 2 (`stand_go2`, `unitree_ros2_example`).

---

## 4. Obtención de MuJoCo 3.2.6

El simulador compila los fuentes de la UI de MuJoCo directamente (`glfw_adapter.cc`, `simulate.cc`, etc.). Por tanto, necesitamos el **binario precompilado** de MuJoCo que incluye tanto las bibliotecas como el código fuente del simulador.

### 4.1 Descarga

```bash
MUJOCO_VERSION="3.2.6"
ARCH="x86_64"

cd /tmp
curl -fsSL -o mujoco-bin.tar.gz \
  "https://github.com/google-deepmind/mujoco/releases/download/${MUJOCO_VERSION}/mujoco-${MUJOCO_VERSION}-linux-${ARCH}.tar.gz"
```

### 4.2 Verificar contenido

El tarball debe contener:

```
mujoco-3.2.6/
├── include/          # Headers públicos de MuJoCo
├── lib/
│   └── libmujoco.so  # Biblioteca compartida
├── simulate/         # Código fuente de la UI (glfw_adapter.{h,cc}, simulate.{h,cc}, etc.)
├── model/            # Modelos de ejemplo
├── bin/              # Binarios de utilidad
└── sample/           # Ejemplos
```

### 4.3 Instalación en el árbol de fuentes

El `CMakeLists.txt` de `unitree_mujoco` espera MuJoCo en un subdirectorio `mujoco/` relativo a `simulate/`:

```bash
MUJOCO_SIM_DIR=~/unitree_ws/src/unitree_mujoco/simulate
cd /tmp
tar xzf mujoco-bin.tar.gz
mv mujoco-${MUJOCO_VERSION} ${MUJOCO_SIM_DIR}/mujoco
```

Estructura resultante:

```
unitree_ws/src/unitree_mujoco/simulate/
├── CMakeLists.txt
├── config.yaml
├── src/
│   ├── main.cc
│   └── ...
└── mujoco/              ← MuJoCo 3.2.6
    ├── include/
    ├── lib/libmujoco.so
    └── simulate/
        ├── glfw_adapter.h
        ├── glfw_adapter.cc
        ├── simulate.cc
        └── ...
```

---

## 5. Compilación del SDK Unitree (unitree_sdk2)

El SDK debe estar compilado e instalado en `/usr/local/`:

```bash
cd ~/unitree_sdk2
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
sudo make install
```

Verificar:

```bash
# Biblioteca estática
ls /usr/local/lib/libunitree_sdk2.a   # Debe existir

# Config CMake
ls /usr/local/lib/cmake/unitree_sdk2/unitree_sdk2Config.cmake  # Debe existir

# Headers
ls /usr/local/include/unitree/        # Debe existir
```

---

## 6. Estructura del Workspace

```
~/unitree_ws/
├── src/
│   ├── unitree_ros2/
│   │   ├── cyclonedds_ws/src/unitree/
│   │   │   ├── unitree_api/      (ROS 2: mensajes de API genérica)
│   │   │   ├── unitree_go/       (ROS 2: mensajes específicos Go2)
│   │   │   └── unitree_hg/       (ROS 2: mensajes H1/G1)
│   │   └── example/src/          (ROS 2: ejemplos para todos los robots)
│   └── unitree_mujoco/
│       ├── simulate/             (CMake: simulador MuJoCo standalone)
│       │   ├── CMakeLists.txt
│       │   ├── config.yaml
│       │   ├── mujoco/           (MuJoCo 3.2.6)
│       │   └── src/main.cc
│       ├── unitree_robots/       (Modelos XML de robots)
│       └── example/ros2/         (ROS 2: ejemplo stand_go2)
├── build/                        (creado por colcon)
├── install/                      (creado por colcon)
└── log/                          (creado por colcon)
```

---

## 7. Limpieza de Artefactos Previos

Antes de compilar, eliminar cualquier artefacto de compilaciones anteriores:

```bash
cd ~/unitree_ws
rm -rf build install log
```

> **Razón**: Los directorios `build/`, `install/`, y `log/` son regenerados por `colcon build`. Artefactos viejos pueden causar errores de caché CMake o archivos `COLCON_IGNORE` residuales que impiden que colcon descubra paquetes.

---

## 8. Corrección de los CMakeLists.txt de Interfaces ROS 2

### 8.1 Problema

Los tres paquetes de interfaces (`unitree_api`, `unitree_go`, `unitree_hg`) contienen código heredado de ROS 2 Foxy que genera DDS IDL para **RTI Connext**:

```cmake
find_package(rosidl_generator_dds_idl REQUIRED)   # ← innecesario para CycloneDDS

rosidl_generate_dds_interfaces(
  ${rosidl_generate_interfaces_TARGET}__dds_connext_idl
  IDL_TUPLES ${rosidl_generate_interfaces_IDL_TUPLES}
  OUTPUT_SUBFOLDERS "dds_connext"
)
add_dependencies(
  ${PROJECT_NAME}
  ${PROJECT_NAME}__dds_connext_idl
)
```

Dado que usamos **CycloneDDS**, que utiliza el sistema de type support por introspección de ROS 2, este código genera IDL para un RMW que nunca usaremos.

### 8.2 Solución

Eliminar el bloque de generación de DDS IDL **de los tres archivos**:

**Archivos a modificar:**
- `src/unitree_ros2/cyclonedds_ws/src/unitree/unitree_api/CMakeLists.txt`
- `src/unitree_ros2/cyclonedds_ws/src/unitree/unitree_go/CMakeLists.txt`
- `src/unitree_ros2/cyclonedds_ws/src/unitree/unitree_hg/CMakeLists.txt`

**Quitar:**
1. `find_package(rosidl_generator_dds_idl REQUIRED)` (línea ~26)
2. El bloque completo `rosidl_generate_dds_interfaces(...)` + `add_dependencies(...)` (líneas ~44-52)

**Resultado**: Los tres paquetes pasan de ~64-79 líneas a ~50-55 líneas. La generación de interfaces ROS 2 estándar (`rosidl_generate_interfaces()`) no se modifica.

### 8.3 ¿Por qué funciona sin Connext IDL?

CycloneDDS utiliza **ROS 2 introspection type support** — un mecanismo que serializa/deserializa mensajes usando información de tipos en runtime, sin necesidad de IDL pre-generado específico del vendor. La llamada `rosidl_generate_interfaces()` ya genera todo lo necesario.

---

## 9. Corrección del Hack `#define private public` en main.cc

### 9.1 Problema

En `src/unitree_mujoco/simulate/src/main.cc:15-18`:

```cpp
// !!! hack code: make glfw_adapter.window_ public
#define private public
#include "glfw_adapter.h"
#undef private
```

Este hack:
1. Viola la **One Definition Rule (ODR)** de C++ — diferentes unidades de traducción ven diferentes definiciones de la clase `GlfwAdapter`
2. Expone miembros privados de `std::optional`, `std::pair`, y otras clases de la STL incluidas transitivamente
3. Causa comportamiento indefinido y potencial corrupción de heap

El acceso concreto que necesita el hack es `glfw_adapter.window_` (el puntero `GLFWwindow*`) en la línea 691 para registrar un callback de teclado.

### 9.2 Solución

**Paso 1**: Añadir un accessor público en `glfw_adapter.h`:

```cpp
// En simulate/mujoco/simulate/glfw_adapter.h, dentro de la sección public:
GLFWwindow* window() const { return window_; }
```

**Paso 2**: Reemplazar el hack en `main.cc`:

```cpp
// ANTES:
// !!! hack code: make glfw_adapter.window_ public
#define private public
#include "glfw_adapter.h"
#undef private

// DESPUÉS:
#include "glfw_adapter.h"
```

**Paso 3**: Actualizar el uso:

```cpp
// ANTES:
glfwSetKeyCallback(static_cast<mj::GlfwAdapter*>(sim->platform_ui.get())->window_, user_key_cb);

// DESPUÉS:
glfwSetKeyCallback(static_cast<mj::GlfwAdapter*>(sim->platform_ui.get())->window(), user_key_cb);
```

---

## 10. Configuración de CycloneDDS

### 10.1 El problema de las dos versiones

Existen **dos versiones diferentes de CycloneDDS** en el sistema:

| Fuente | Versión | Shared Memory | Ruta |
|--------|---------|---------------|------|
| Sistema (apt) | **0.10.5** | Sí (iceoryx) | `/opt/ros/humble/lib/x86_64-linux-gnu/libddsc.so` |
| SDK Unitree | **0.10.2** | No (`noshm`) | `~/unitree_sdk2/thirdparty/lib/x86_64/libddsc.so` |

La biblioteca estática `libunitree_sdk2.a` fue **precompilada** contra CycloneDDS 0.10.2-noshm. Si en runtime se carga la versión 0.10.5 con shared memory, las estructuras internas de datos no coinciden, causando:

```
dds_writecdr_impl_common: Assertion `(wr->m_iox_pub == NULL) == (d->a.iox_chunk == NULL)' failed.
corrupted size vs. prev_size
free(): invalid pointer
Aborted (core dumped)
```

### 10.2 ¿Por qué se carga la versión incorrecta?

ROS 2 Humble modifica el entorno al hacer `source /opt/ros/humble/setup.bash`, estableciendo:

```bash
LD_LIBRARY_PATH=/opt/ros/humble/lib/x86_64-linux-gnu:/opt/ros/humble/lib:...
```

`LD_LIBRARY_PATH` tiene **mayor prioridad** que `RUNPATH` (el mecanismo por defecto de CMake). Por tanto, la CycloneDDS del sistema (0.10.5) siempre prevalece sobre la empaquetada (0.10.2), incluso si configuramos RPATH en el binario.

### 10.3 Solución: RPATH con `--disable-new-dtags`

Cambiar de `RUNPATH` (sobreescribible por `LD_LIBRARY_PATH`) a `RPATH` (tiene prioridad sobre `LD_LIBRARY_PATH`):

### 10.4 Modificación del CMakeLists.txt de unitree_mujoco

Actualizar `src/unitree_mujoco/simulate/CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.16)
project(unitree_mujoco)

if (CMAKE_BUILD_TYPE MATCHES "Debug")
  message("Debug mode")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -g -O0 -fPIC")
else()
  message("Release mode")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -O3 -DNDEBUG -fPIC")
endif()

list(APPEND CMAKE_PREFIX_PATH "/opt/unitree_robotics/lib/cmake")
find_package(unitree_sdk2 REQUIRED)
find_package(Boost REQUIRED COMPONENTS program_options)

# Usar CycloneDDS EMPAQUETADO (0.10.2-noshm) — NO el del sistema (0.10.5+shm)
set(DDSC_LIB "/home/rimuru/unitree_sdk2/thirdparty/lib/x86_64/libddsc.so")
set(DDSCXX_LIB "/home/rimuru/unitree_sdk2/thirdparty/lib/x86_64/libddscxx.so")

include_directories(
  /usr/local/include/iceoryx/v2.0.2
  mujoco/include
  mujoco/simulate
  src/lodepng
)
link_directories(mujoco/lib)

file(GLOB SIM_SRC
  src/joystick/joystick.cc
  mujoco/simulate/glfw_*.cc
  mujoco/simulate/platform_*.cc
  mujoco/simulate/simulate.cc
  src/lodepng/lodepng.cpp
)

link_libraries(
  pthread
  mujoco
  glfw
  yaml-cpp
  unitree_sdk2
  ${DDSC_LIB}
  ${DDSCXX_LIB}
  boost_program_options
  fmt
)

add_executable(unitree_mujoco ${SIM_SRC} src/main.cc)
add_executable(jstest src/joystick/jstest.cc src/joystick/joystick.cc)
```

### 10.5 Compilación con RPATH

El flag crítico es `-Wl,--disable-new-dtags`, que fuerza `RPATH` (prioritario) en vez de `RUNPATH`:

```bash
cd ~/unitree_ws
colcon build --packages-select unitree_mujoco \
  --cmake-args \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_BUILD_RPATH="/home/rimuru/unitree_sdk2/thirdparty/lib/x86_64" \
    -DCMAKE_INSTALL_RPATH="/home/rimuru/unitree_sdk2/thirdparty/lib/x86_64" \
    -DCMAKE_EXE_LINKER_FLAGS="-Wl,--disable-new-dtags"
```

### 10.6 Verificación

```bash
# Verificar que es RPATH (no RUNPATH)
readelf -d ~/unitree_ws/build/unitree_mujoco/unitree_mujoco | grep -i rpath
# Debe mostrar: (RPATH) Library rpath: [.../thirdparty/lib/x86_64...]

# Verificar que ambas bibliotecas CycloneDDS vienen del bundle
ldd ~/unitree_ws/build/unitree_mujoco/unitree_mujoco | grep ddsc
# libddsc.so.0 => .../unitree_sdk2/thirdparty/lib/x86_64/libddsc.so.0
# libddscxx.so.0 => .../unitree_sdk2/thirdparty/lib/x86_64/libddscxx.so.0
```

Ambas deben apuntar a `~/unitree_sdk2/thirdparty/lib/x86_64/`. Si `libddsc.so.0` apunta a `/opt/ros/humble/...`, el RPATH no se aplicó correctamente.

### 10.7 Configuración XML de CycloneDDS

Actualizar `src/unitree_ros2/cyclonedds_ws/src/cyclonedds.xml`:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<CycloneDDS>
    <Domain Id="any">
        <SharedMemory>
            <Enable>false</Enable>
        </SharedMemory>
        <General>
            <Interfaces>
                <NetworkInterface name="lo" priority="default" multicast="default" />
            </Interfaces>
        </General>
    </Domain>
</CycloneDDS>
```

> **Nota**: La interfaz `lo` (loopback) es para pruebas locales. Para el robot real, usar la interfaz de red Wi-Fi (ej. `enp3s0` o `wlan0`). Shared memory se deshabilita explícitamente ya que el CycloneDDS empaquetado se compiló sin soporte (`noshm`).

---

## 11. Compilación del Workspace Completo

### 11.1 Orden de compilación

Colcon resuelve automáticamente las dependencias, pero el orden lógico es:

1. `unitree_api` → Independiente, solo depende de `geometry_msgs`
2. `unitree_hg` → Independiente, solo depende de `geometry_msgs`
3. `unitree_go` → Depende de `unitree_api`
4. `unitree_mujoco` → Depende de `unitree_sdk2`, MuJoCo, GLFW
5. `stand_go2` → Depende de `unitree_go`, `unitree_api`
6. `unitree_ros2_example` → Depende de `unitree_go`, `unitree_hg`, `unitree_api`

### 11.2 Compilación

```bash
cd ~/unitree_ws

source /opt/ros/humble/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Compilar todo con RPATH para unitree_mujoco
colcon build \
  --cmake-args \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_BUILD_RPATH="/home/rimuru/unitree_sdk2/thirdparty/lib/x86_64" \
    -DCMAKE_INSTALL_RPATH="/home/rimuru/unitree_sdk2/thirdparty/lib/x86_64" \
    -DCMAKE_EXE_LINKER_FLAGS="-Wl,--disable-new-dtags"
```

### 11.3 Resultado esperado

```
Summary: 6 packages finished
  unitree_api        [OK]
  unitree_go         [OK]
  unitree_hg         [OK]
  unitree_mujoco     [OK] (warning: no install target — normal, es cmake puro)
  stand_go2          [OK]
  unitree_ros2_example [OK]
```

### 11.4 Verificación

```bash
source ~/unitree_ws/install/setup.bash

# Paquetes ROS 2 disponibles
ros2 pkg list | grep unitree
# unitree_api
# unitree_go
# unitree_hg
# unitree_ros2_example
# stand_go2

# Interfaces disponibles (43 en total)
ros2 interface list | grep unitree_go | head -5
# unitree_go/msg/AudioData
# unitree_go/msg/BmsCmd
# unitree_go/msg/BmsState
# unitree_go/msg/Error
# unitree_go/msg/Go2FrontVideoData
```

---

## 12. Resolución de Archivos de Modelo (scene.xml)

### 12.1 Problema

El binario `unitree_mujoco` resuelve rutas relativas basándose en la ubicación del ejecutable:

```cpp
// main.cc:674
std::filesystem::path proj_dir = std::filesystem::path(getExecutableDir()).parent_path();

// config.yaml se busca en: proj_dir / "config.yaml"
//                          = build/ / "config.yaml"

// scene.xml se busca en:   proj_dir.parent_path() / "unitree_robots" / robot / scene.xml
//                          = unitree_ws/ / "unitree_robots" / go2 / "scene.xml"
```

Ejecutable en `build/unitree_mujoco/unitree_mujoco`:
- `proj_dir` = `build/`
- `proj_dir.parent_path()` = `~/unitree_ws/`

### 12.2 Solución: Enlaces simbólicos

Crear symlinks en las ubicaciones esperadas apuntando a los archivos fuente:

```bash
# config.yaml
ln -sf ~/unitree_ws/src/unitree_mujoco/simulate/config.yaml \
       ~/unitree_ws/build/config.yaml

# Modelos de robots
ln -sfn ~/unitree_ws/src/unitree_mujoco/unitree_robots \
        ~/unitree_ws/unitree_robots
```

Verificar:

```bash
ls ~/unitree_ws/build/config.yaml       # Debe existir
ls ~/unitree_ws/unitree_robots/go2/     # Debe mostrar scene.xml, go2.xml, etc.
```

---

## 13. Ejecución del Simulador

### 13.1 Lanzamiento básico

```bash
~/unitree_ws/build/unitree_mujoco/unitree_mujoco
```

Salida esperada:

```
MuJoCo version 3.2.6
Mujoco data is prepared
1780355230.052295 [1] unitree_mu: selected interface "lo" is not multicast-capable: disabling multicast
<<------------- Link ------------->>
Link_index: 0, name: world
Link_index: 1, name: base_link
... (18 links del Go2)
<<------------- Joint ------------->>
... (12 joints)
<<------------- Actuator ------------->>
... (12 actuadores)
<<------------- Sensor ------------->>
... (50 sensores: posiciones, velocidades, torques, IMU)
```

> **Nota**: El warning `selected interface "lo" is not multicast-capable` es benigno. CycloneDDS usa unicast en loopback, lo cual es correcto para pruebas locales.

### 13.2 Configuración del robot

Editar `src/unitree_mujoco/simulate/config.yaml`:

```yaml
robot: "go2"                # Robot a simular
robot_scene: "scene.xml"    # Escena MuJoCo
domain_id: 1                # DDS domain ID
interface: "lo"             # Interfaz de red (lo=local, wlan0=WiFi)
use_joystick: 0             # 0=sin gamepad, 1=con gamepad
enable_elastic_band: 0      # Banda elástica virtual (para H1)
```

> **Importante**: Después de cambiar `config.yaml`, NO es necesario recompilar. El simulador lee el archivo en cada ejecución.

### 13.3 Controles del teclado en simulación

| Tecla | Acción |
|-------|--------|
| `Backspace` | Resetear simulación |
| Ratón + arrastrar | Rotar cámara |
| `Shift` + ratón | Mover cámara |
| Rueda ratón | Zoom |
| `Tab` | Cambiar modo de cámara |
| `Espacio` | Pausar/Reanudar física |

---

## 14. Problemas Comunes y Soluciones

### 14.1 `CMake Error: Could not find rosidl_generator_dds_idl`

**Causa**: Entorno ROS 2 no sourced o el paquete no instalado.

**Solución**:
```bash
source /opt/ros/humble/setup.bash
sudo apt install ros-humble-rosidl-generator-dds-idl
```

> **Nota**: Después de nuestras correcciones en la sección 8, este paquete ya no es necesario para compilar.

### 14.2 `Could not find ROS middleware implementation 'rmw_cyclonedds_cpp'`

**Causa**: El paquete `ros-humble-rmw-cyclonedds-cpp` no está instalado. CMake lo busca cuando algún paquete hace `find_package(rclcpp REQUIRED)`.

**Solución**:
```bash
sudo apt install ros-humble-rmw-cyclonedds-cpp
```

### 14.3 `fatal error: glfw_adapter.h: No such file or directory`

**Causa**: MuJoCo no está instalado en la ubicación esperada (`simulate/mujoco/simulate/`).

**Solución**: Ver sección 4 — descargar y extraer MuJoCo 3.2.6.

### 14.4 `cannot find -lmujoco` / `cannot find -lglfw`

**Causa**: Falta MuJoCo (`libmujoco.so`) o GLFW (`libglfw3.so`).

**Solución**:
```bash
# GLFW
sudo apt install libglfw3-dev

# MuJoCo — ver sección 4
```

### 14.5 `ParseXML: Error opening file '.../scene.xml'`

**Causa**: Los symlinks de la sección 12 no están creados.

**Solución**: Ejecutar los comandos de la sección 12.2.

### 14.6 `free(): invalid pointer` / `corrupted size vs. prev_size` / `Aborted`

**Causa probable**: CycloneDDS del sistema (0.10.5+shm) prevalece sobre el empaquetado (0.10.2-noshm). Ver sección 10.

**Verificación**:
```bash
ldd ~/unitree_ws/build/unitree_mujoco/unitree_mujoco | grep ddsc
# Ambas líneas deben apuntar a ~/unitree_sdk2/thirdparty/lib/x86_64/
```

Si `libddsc.so.0` apunta a `/opt/ros/humble/lib/`, el RPATH no está funcionando. Recompilar con los flags de la sección 10.5.

### 14.7 `dds_writecdr_impl_common: Assertion ... failed`

**Causa**: Inconsistencia en el estado de iceoryx/shared memory de CycloneDDS. La versión del sistema tiene soporte de shared memory pero la del SDK no.

**Solución**: Asegurar que se usa la CycloneDDS empaquetada (sección 10).

### 14.8 Pantalla azul en MuJoCo

Esto es **normal**. La pantalla azul es el color de fondo por defecto de MuJoCo cuando no hay terreno cargado. El robot Go2 debería aparecer renderizado en la escena. Si toda la ventana es azul sin robot visible:

- Verificar que `scene.xml` se cargó correctamente (sin errores `ParseXML`)
- La cámara puede estar apuntando a una posición vacía — usar ratón para rotar

### 14.9 `selected interface "lo" is not multicast-capable: disabling multicast`

**No es un error.** CycloneDDS detecta que la interfaz loopback no soporta multicast y automáticamente cambia a unicast. El simulador funciona correctamente.

### 14.10 `ros2: command not found`

**Causa**: Las herramientas CLI de ROS 2 no están instaladas.

**Solución**:
```bash
sudo apt install ros-humble-ros2cli ros-humble-ros2pkg ros-humble-ros2interface
```

---

## 15. Resumen de Comandos

### Instalación completa desde cero

```bash
# === 1. Dependencias del sistema ===
sudo apt update
sudo apt install -y \
  libeigen3-dev libboost-all-dev libglfw3-dev libglfw3 \
  libyaml-cpp-dev libfmt-dev cmake build-essential git \
  ros-humble-rosidl-default-generators ros-humble-rosidl-default-runtime \
  ros-humble-rmw-cyclonedds-cpp ros-humble-rosbag2-cpp \
  ros-humble-ros2cli ros-humble-ros2pkg ros-humble-ros2interface \
  ros-humble-ros2topic ros-humble-ros2node

# === 2. Clonar repositorios ===
mkdir -p ~/unitree_ws/src
cd ~/unitree_ws/src
git clone https://github.com/unitreerobotics/unitree_ros2.git
git clone https://github.com/unitreerobotics/unitree_mujoco.git
cd ~
git clone https://github.com/unitreerobotics/unitree_sdk2.git

# === 3. Compilar SDK ===
cd ~/unitree_sdk2 && mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
sudo make install

# === 4. Descargar MuJoCo 3.2.6 ===
cd /tmp
curl -fsSL -o mujoco.tar.gz \
  "https://github.com/google-deepmind/mujoco/releases/download/3.2.6/mujoco-3.2.6-linux-x86_64.tar.gz"
tar xzf mujoco.tar.gz
mv mujoco-3.2.6 ~/unitree_ws/src/unitree_mujoco/simulate/mujoco

# === 5. Limpiar workspace ===
cd ~/unitree_ws && rm -rf build install log

# === 6. Aplicar correcciones ===
# (Ver secciones 8, 9, 10, 12 de este documento)

# === 7. Compilar ===
source /opt/ros/humble/setup.bash
cd ~/unitree_ws
colcon build \
  --cmake-args \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_BUILD_RPATH="$HOME/unitree_sdk2/thirdparty/lib/x86_64" \
    -DCMAKE_INSTALL_RPATH="$HOME/unitree_sdk2/thirdparty/lib/x86_64" \
    -DCMAKE_EXE_LINKER_FLAGS="-Wl,--disable-new-dtags"

# === 8. Crear symlinks para runtime ===
ln -sf ~/unitree_ws/src/unitree_mujoco/simulate/config.yaml ~/unitree_ws/build/config.yaml
ln -sfn ~/unitree_ws/src/unitree_mujoco/unitree_robots ~/unitree_ws/unitree_robots

# === 9. Ejecutar ===
~/unitree_ws/build/unitree_mujoco/unitree_mujoco
```

---

## Notas Finales

### Estado del workspace tras la configuración

| Componente | Estado |
|-----------|--------|
| `unitree_api` (8 mensajes) | Compilado e instalado |
| `unitree_go` (23 mensajes Go2) | Compilado e instalado |
| `unitree_hg` (11 mensajes H1) | Compilado e instalado |
| `unitree_mujoco` (simulador) | Compilado (binario en build/) |
| `stand_go2` (ejemplo) | Compilado e instalado |
| `unitree_ros2_example` (ejemplos) | Compilado e instalado |
| MuJoCo 3.2.6 | Vendored en simulate/mujoco/ |
| CycloneDDS 0.10.2-noshm | Empaquetado con SDK |
| Go2 scene.xml | Resuelto vía symlink |

### Archivos modificados respecto al upstream

1. `unitree_api/CMakeLists.txt` — Eliminado bloque `rosidl_generate_dds_interfaces`
2. `unitree_go/CMakeLists.txt` — Eliminado bloque `rosidl_generate_dds_interfaces`
3. `unitree_hg/CMakeLists.txt` — Eliminado bloque `rosidl_generate_dds_interfaces`
4. `unitree_mujoco/simulate/CMakeLists.txt` — Añadido enlace explícito a CycloneDDS empaquetado
5. `unitree_mujoco/simulate/mujoco/simulate/glfw_adapter.h` — Añadido accessor `window()`
6. `unitree_mujoco/simulate/src/main.cc` — Eliminado hack `#define private public`, usa `window()`
7. `cyclonedds.xml` — Deshabilitado SharedMemory, interfaz `lo`

### Siguiente paso: Navegación Autónoma

Con la simulación funcionando, el siguiente paso es integrar el stack Nav2 (SLAM, localización AMCL, planificación de rutas) usando los tópicos ROS 2 expuestos por `unitree_mujoco` a través de CycloneDDS.
