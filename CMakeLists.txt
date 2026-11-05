cmake_minimum_required(VERSION 3.8)
project(rfid_simulator_test)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rfid_sensor REQUIRED)
find_package(gazebo REQUIRED)

add_executable(collect_data_node src/collect_data.cpp)
ament_target_dependencies(collect_data_node rclcpp rfid_sensor)

add_library(move_antenna SHARED src/moveAntenna.cpp)
target_include_directories(move_antenna SYSTEM PRIVATE ${GAZEBO_INCLUDE_DIRS})
target_link_libraries(move_antenna ${GAZEBO_LIBRARIES})
separate_arguments(gazebo_cxx_flags NATIVE_COMMAND "${GAZEBO_CXX_FLAGS}")
target_compile_options(move_antenna PRIVATE ${gazebo_cxx_flags})

install(TARGETS collect_data_node DESTINATION lib/${PROJECT_NAME})
install(TARGETS move_antenna LIBRARY DESTINATION lib)
install(DIRECTORY launch urdf meshes config DESTINATION share/${PROJECT_NAME})

ament_package()
