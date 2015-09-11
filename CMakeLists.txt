cmake_minimum_required(VERSION 2.8.11)
# Name of the project
project(SimpleNGL)
#Bring the headers into the project (local ones)
include_directories(include $ENV{HOME}/NGL/include)

#the file(GLOB...) allows for wildcard additions of our src dir
set(SOURCES src/main.cpp  src/NGLScene.cpp  src/OpenGLWindow.cpp
			include/NGLScene.h  include/OpenGLWindow.h

)

# see what platform we are on and set platform defines
if(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
	add_definitions(-DDARWIN)

elif(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
	add_definitions(-DLINUX)
endif()


#As were using Qt we need to run moc
#disable -rdynamic
SET(CMAKE_SHARED_LIBRARY_LINK_CXX_FLAGS "")
SET(CMAKE_SHARED_LIBRARY_LINK_C_FLAGS "")

# Find includes in corresponding build directories
set(CMAKE_INCLUDE_CURRENT_DIR ON)
# Instruct CMake to run moc automatically when needed.
set(CMAKE_AUTOMOC ON)

add_definitions(-O2 -D_FILE_OFFSET_BITS=64 -fPIC) 


# now add NGL specific values
set ( PROJECT_LINK_LIBS -lNGL -lGL)
link_directories( ~/NGL/lib )
include_directories(~/NGL/include/)
# as NGL uses Qt we need to define this flag
add_definitions(-DQT5BUILD)
# NGL also needs the OpenGL framework from Qt so add it
find_package(Qt5OpenGL)
find_package(Qt5Widgets)
find_package(Qt5Gui)
find_package(Qt5Core)


# add exe and link libs this must be after the other defines
add_executable(SimpleNGL ${SOURCES})
target_link_libraries(SimpleNGL Qt5::OpenGL Qt5::Core Qt5::Gui Qt5::Widgets )
target_link_libraries(SimpleNGL ${PROJECT_LINK_LIBS} )

