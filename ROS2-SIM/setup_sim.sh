#!/bin/bash
# =============================================================================
# setup_sim.sh — Configuración autónoma del entorno de simulación
# Unitree Go2 AIR + MuJoCo + ROS 2 Humble
#
# Ejecutar DENTRO del contenedor Distrobox (Ubuntu 22.04 + ROS 2 Humble):
#   chmod +x setup_sim.sh
#   ./setup_sim.sh
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_DIR="$HOME/unitree_ws"
SDK_DIR="$HOME/unitree_sdk2"
MUJOCO_VERSION="3.2.6"
MUJOCO_ARCH="x86_64"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC}  $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()  { echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"; echo -e "${CYAN}▶ $1${NC}"; echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"; }

# =============================================================================
# PASO 1: Verificar entorno
# =============================================================================
log_step "PASO 1/9: Verificando entorno"

if [ ! -f /opt/ros/humble/setup.bash ]; then
    log_error "ROS 2 Humble no encontrado en /opt/ros/humble/"
    log_error "Instálalo: sudo apt install ros-humble-ros-base"
    exit 1
fi

source /opt/ros/humble/setup.bash

if [ "$ROS_DISTRO" != "humble" ]; then
    log_error "ROS_DISTRO no es humble. Abortando."
    exit 1
fi

log_info "ROS 2 Humble detectado correctamente"
log_info "Arquitectura: $(uname -m)"

# =============================================================================
# PASO 2: Instalar dependencias de sistema
# =============================================================================
log_step "PASO 2/9: Instalando dependencias de sistema (apt)"

sudo apt-get update -qq

PACKAGES=(
    libeigen3-dev
    libboost-all-dev
    libglfw3-dev
    libglfw3
    libyaml-cpp-dev
    libfmt-dev
    cmake
    build-essential
    git
    ros-humble-rosidl-default-generators
    ros-humble-rosidl-default-runtime
    ros-humble-rmw-cyclonedds-cpp
    ros-humble-rosbag2-cpp
    ros-humble-ros2cli
    ros-humble-ros2pkg
    ros-humble-ros2interface
    ros-humble-ros2topic
    ros-humble-ros2node
    ros-humble-ros2action
    ros-humble-ros2service
    ros-humble-ros2param
    python3-pip
    python3-colcon-common-extensions
)

for pkg in "${PACKAGES[@]}"; do
    if dpkg -l | grep -q "^ii.*${pkg} "; then
        log_info "Ya instalado: $pkg"
    else
        log_info "Instalando: $pkg"
        sudo apt-get install -y -qq "$pkg" 2>&1 | tail -1
    fi
done

# =============================================================================
# PASO 3: Clonar repositorios
# =============================================================================
log_step "PASO 3/9: Clonando repositorios Unitree"

mkdir -p "$WS_DIR/src"

# SDK Unitree
if [ ! -d "$SDK_DIR" ]; then
    log_info "Clonando unitree_sdk2..."
    git clone https://github.com/unitreerobotics/unitree_sdk2.git "$SDK_DIR"
else
    log_info "unitree_sdk2 ya existe, omitiendo clonación"
fi

# Interfaces ROS 2
if [ ! -d "$WS_DIR/src/unitree_ros2" ]; then
    log_info "Clonando unitree_ros2..."
    git clone https://github.com/unitreerobotics/unitree_ros2.git "$WS_DIR/src/unitree_ros2"
else
    log_info "unitree_ros2 ya existe, omitiendo clonación"
fi

# Simulador MuJoCo
if [ ! -d "$WS_DIR/src/unitree_mujoco" ]; then
    log_info "Clonando unitree_mujoco..."
    git clone https://github.com/unitreerobotics/unitree_mujoco.git "$WS_DIR/src/unitree_mujoco"
else
    log_info "unitree_mujoco ya existe, omitiendo clonación"
fi

# =============================================================================
# PASO 4: Compilar SDK Unitree
# =============================================================================
log_step "PASO 4/9: Compilando unitree_sdk2"

cd "$SDK_DIR"

if [ -f /usr/local/lib/libunitree_sdk2.a ]; then
    log_info "unitree_sdk2 ya instalado en /usr/local/lib/"
else
    mkdir -p build && cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release
    make -j$(nproc)
    sudo make install
    log_info "unitree_sdk2 compilado e instalado"
fi

# =============================================================================
# PASO 5: Descargar MuJoCo 3.2.6
# =============================================================================
log_step "PASO 5/9: Descargando MuJoCo ${MUJOCO_VERSION}"

MUJOCO_DIR="$WS_DIR/src/unitree_mujoco/simulate/mujoco"

if [ -f "$MUJOCO_DIR/lib/libmujoco.so" ]; then
    log_info "MuJoCo ya existe en $MUJOCO_DIR"
else
    MUJOCO_TARBALL="/tmp/mujoco-${MUJOCO_VERSION}.tar.gz"
    MUJOCO_URL="https://github.com/google-deepmind/mujoco/releases/download/${MUJOCO_VERSION}/mujoco-${MUJOCO_VERSION}-linux-${MUJOCO_ARCH}.tar.gz"

    if [ ! -f "$MUJOCO_TARBALL" ]; then
        log_info "Descargando MuJoCo desde GitHub..."
        curl -fsSL -o "$MUJOCO_TARBALL" "$MUJOCO_URL"
    fi

    log_info "Extrayendo MuJoCo..."
    cd /tmp
    tar xzf "$MUJOCO_TARBALL"
    mv "mujoco-${MUJOCO_VERSION}" "$MUJOCO_DIR"
    log_info "MuJoCo instalado en $MUJOCO_DIR"
fi

# =============================================================================
# PASO 6: Limpiar workspace
# =============================================================================
log_step "PASO 6/9: Limpiando workspace"

cd "$WS_DIR"
rm -rf build install log
log_info "Workspace limpio"

# =============================================================================
# PASO 7: Aplicar parches
# =============================================================================
log_step "PASO 7/9: Aplicando parches de código"

PATCH_DIR="$SCRIPT_DIR/patches"

# 7a: Eliminar Connext DDS IDL de los CMakeLists.txt de interfaces
for pkg in unitree_api unitree_go unitree_hg; do
    CMAKEFILE="$WS_DIR/src/unitree_ros2/cyclonedds_ws/src/unitree/$pkg/CMakeLists.txt"
    if [ -f "$CMAKEFILE" ]; then
        # Eliminar find_package(rosidl_generator_dds_idl REQUIRED)
        sed -i '/find_package(rosidl_generator_dds_idl REQUIRED)/d' "$CMAKEFILE"
        # Eliminar bloque rosidl_generate_dds_interfaces + add_dependencies (3 líneas después)
        sed -i '/rosidl_generate_dds_interfaces(/,/)/d' "$CMAKEFILE"
        sed -i '/add_dependencies(/,/)/d' "$CMAKEFILE"
        log_info "Parche aplicado: $pkg/CMakeLists.txt"
    fi
done

# 7b: Corregir hack #define private public en main.cc
MAIN_CC="$WS_DIR/src/unitree_mujoco/simulate/src/main.cc"
GLFW_H="$WS_DIR/src/unitree_mujoco/simulate/mujoco/simulate/glfw_adapter.h"

if [ -f "$MAIN_CC" ]; then
    # Eliminar líneas 15-18 (el hack)
    sed -i '\|// !!! hack code: make glfw_adapter.window_ public|d' "$MAIN_CC"
    sed -i '|#define private public|d' "$MAIN_CC"
    sed -i '|#include "glfw_adapter.h"|{ N; s|#include "glfw_adapter.h"\n#undef private|#include "glfw_adapter.h"|; }' "$MAIN_CC"
    # Cambiar window_ por window()
    sed -i 's|->window_,user_key_cb|->window(), user_key_cb|g' "$MAIN_CC"
    log_info "Parche aplicado: main.cc (hack #define private public eliminado)"
fi

# 7c: Añadir accessor window() en glfw_adapter.h
if [ -f "$GLFW_H" ]; then
    if ! grep -q "GLFWwindow\* window()" "$GLFW_H"; then
        sed -i '/mjtButton TranslateMouseButton(int button) const override;/a\  GLFWwindow* window() const { return window_; }' "$GLFW_H"
        log_info "Parche aplicado: glfw_adapter.h (accessor window() añadido)"
    fi
fi

# 7d: Actualizar CMakeLists.txt de unitree_mujoco para usar CycloneDDS empaquetado
SIM_CMAKE="$WS_DIR/src/unitree_mujoco/simulate/CMakeLists.txt"
if [ -f "$SIM_CMAKE" ]; then
    cat > "$SIM_CMAKE" << 'CMAKE_EOF'
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
set(DDSC_LIB "$ENV{HOME}/unitree_sdk2/thirdparty/lib/x86_64/libddsc.so")
set(DDSCXX_LIB "$ENV{HOME}/unitree_sdk2/thirdparty/lib/x86_64/libddscxx.so")

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
CMAKE_EOF
    log_info "Parche aplicado: unitree_mujoco/CMakeLists.txt"
fi

# 7e: Config CycloneDDS
CYCLONE_XML="$WS_DIR/src/unitree_ros2/cyclonedds_ws/src/cyclonedds.xml"
cat > "$CYCLONE_XML" << 'XML_EOF'
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
XML_EOF
log_info "Parche aplicado: cyclonedds.xml"

# =============================================================================
# PASO 8: Compilar workspace
# =============================================================================
log_step "PASO 8/9: Compilando workspace con colcon"

cd "$WS_DIR"
source /opt/ros/humble/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

colcon build \
    --cmake-args \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_BUILD_RPATH="$HOME/unitree_sdk2/thirdparty/lib/x86_64" \
        -DCMAKE_INSTALL_RPATH="$HOME/unitree_sdk2/thirdparty/lib/x86_64" \
        -DCMAKE_EXE_LINKER_FLAGS="-Wl,--disable-new-dtags"

# =============================================================================
# PASO 9: Crear symlinks para runtime
# =============================================================================
log_step "PASO 9/9: Creando symlinks para archivos de modelo"

ln -sf "$WS_DIR/src/unitree_mujoco/simulate/config.yaml" "$WS_DIR/build/config.yaml"
ln -sfn "$WS_DIR/src/unitree_mujoco/unitree_robots" "$WS_DIR/unitree_robots"

log_info "Symlinks creados:"
log_info "  config.yaml → build/config.yaml"
log_info "  unitree_robots/ → unidad_ws/unitree_robots"

# =============================================================================
# Verificación final
# =============================================================================
log_step "VERIFICACIÓN FINAL"

echo ""
echo "  ✅ ROS 2 Humble:     $(source /opt/ros/humble/setup.bash && echo $ROS_DISTRO)"
echo "  ✅ MuJoCo:           $(strings $WS_DIR/src/unitree_mujoco/simulate/mujoco/lib/libmujoco.so 2>/dev/null | grep -m1 'MuJoCo version' || echo 'instalado')"
echo "  ✅ unitree_sdk2:     $([ -f /usr/local/lib/libunitree_sdk2.a ] && echo 'instalado' || echo 'FALTA')"
echo "  ✅ unitree_mujoco:   $([ -f $WS_DIR/build/unitree_mujoco/unitree_mujoco ] && echo 'compilado' || echo 'FALTA')"
echo "  ✅ Paquetes ROS 2:   $(source $WS_DIR/install/setup.bash 2>/dev/null && ros2 pkg list 2>/dev/null | grep unitree | wc -l) encontrados"
echo "  ✅ Simulador RPATH:  $(readelf -d $WS_DIR/build/unitree_mujoco/unitree_mujoco 2>/dev/null | grep -q RPATH && echo 'RPATH (prioritario)' || echo 'RUNPATH (revisar)')"
echo ""

log_info "¡Configuración completada!"
echo ""
echo "  Para ejecutar la simulación:"
echo "    ~/unitree_ws/build/unitree_mujoco/unitree_mujoco"
echo ""
echo "  Para usar el controlador por voz en simulación:"
echo "    cd ~/proyectoProspectiva/ROS2-SIM"
echo "    python3 sim_robot_controller.py"
echo ""
echo "  Consulta la guía completa en:"
echo "    ~/proyectoProspectiva/ROS2-SIM/SIMULATION_SETUP.md"
echo "    ~/proyectoProspectiva/ROS2-SIM/GUIA_SIMULACION.md"
echo ""
