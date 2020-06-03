cmake_minimum_required(VERSION 3.2)
# Name of the project
project(SimpleNGLBuild)
#Bring the headers into the project (local ones)
include_directories(include $ENV{HOME}/NGL/include)
# use C++ 14
set(CMAKE_CXX_STANDARD 17)
#the file(GLOB...) allows for wildcard additions of our src dir
set(SOURCES ${PROJECT_SOURCE_DIR}/src/main.cpp  
			${PROJECT_SOURCE_DIR}/src/NGLScene.cpp  
			${PROJECT_SOURCE_DIR}/src/NGLSceneMouseControls.cpp  
			${PROJECT_SOURCE_DIR}/include/NGLScene.h  

)

# see what platform we are on and set platform defines
if(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
	message("Mac build")
	find_library(MACGL OpenGL)
	add_definitions(-DGL_SCILENCE_DEPRICATION)
	set ( PROJECT_LINK_LIBS -lNGL ${MACGL})

elseif(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
	set ( PROJECT_LINK_LIBS -lNGL -lGL)
endif()


#As were using Qt we need to run moc
# define that if you want to include the stanford data sets
# these are very big and make compilation time huge
add_definitions(-DADDLARGEMODELS)

# Find includes in corresponding build directories
set(CMAKE_INCLUDE_CURRENT_DIR ON)
# Instruct CMake to run moc automatically when needed.
set(CMAKE_AUTOMOC ON)


# now add NGL specific values
link_directories( $ENV{HOME}/NGL/lib )
# NGL also needs the OpenGL framework from Qt so add it
find_package(Qt5OpenGL)
find_package(Qt5Widgets)
find_package(Qt5Gui)
find_package(Qt5Core)

# add exe and link libs that must be after the other defines
add_executable(SimpleNGL ${SOURCES})
target_link_libraries(SimpleNGL PRIVATE ${PROJECT_LINK_LIBS}  Qt5::OpenGL Qt5::Core Qt5::Gui Qt5::Widgets )

add_custom_target(CopyShaders ALL
    COMMAND ${CMAKE_COMMAND} -E copy_directory
    ${CMAKE_CURRENT_SOURCE_DIR}/shaders
    ${CMAKE_BINARY_DIR}/shaders
    )