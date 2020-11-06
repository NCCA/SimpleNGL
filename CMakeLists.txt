cmake_minimum_required(VERSION 3.12)
# Name of the project
project(SimpleNGLBuild)
# This is the name of the Exe change this and it will change everywhere
set(TargetName SimpleNGL)
# Instruct CMake to run moc automatically when needed (Qt projects only)
set(CMAKE_AUTOMOC ON)
# find Qt libs
find_package(Qt5Widgets)
find_package(glm CONFIG REQUIRED)
find_package(fmt CONFIG REQUIRED)
find_package(OpenImageIO CONFIG REQUIRED)
find_package(freetype CONFIG REQUIRED)

if(UNIX)
    find_package(IlmBase CONFIG REQUIRED)
    find_package(OpenEXR CONFIG REQUIRED)
endif()

# use C++ 17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)
# Set the name of the executable we want to build
add_executable(${TargetName})

# Add NGL include path
include_directories(include $ENV{HOME}/NGL/include)
target_sources(${TargetName} PRIVATE ${PROJECT_SOURCE_DIR}/src/main.cpp  
			${PROJECT_SOURCE_DIR}/src/NGLScene.cpp  
			${PROJECT_SOURCE_DIR}/src/NGLSceneMouseControls.cpp  
			${PROJECT_SOURCE_DIR}/include/NGLScene.h  
)
add_compile_definitions(ADDLARGEMODELS)
add_compile_definitions(GLM_ENABLE_EXPERIMENTAL)

# see what platform we are on and set platform defines
if(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
	message("Mac build")
	find_library(MACGL OpenGL)
	add_definitions(-DGL_SCILENCE_DEPRICATION)
	set ( PROJECT_LINK_LIBS ${MACGL})
elseif(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
	set ( PROJECT_LINK_LIBS -lGL)
elseif(${CMAKE_SYSTEM_NAME} MATCHES "Windows")
	include_directories(include $ENV{HOMEDRIVE}/$ENV{HOMEPATH}/NGL/include)
	link_directories($ENV{HOMEDRIVE}/$ENV{HOMEPATH}/NGL/lib)	
	target_link_libraries(${TargetName} PRIVATE $ENV{HOMEDRIVE}/$ENV{HOMEPATH}/NGL/lib/NGL.lib)
	add_compile_definitions(_USE_MATH_DEFINES)
	add_compile_definitions(NOMINMAX)
	# Need to define this when building shared library or suffer dllimport errors
	add_compile_definitions(BUILDING_DLL)

endif()

# now add NGL specific values
target_link_directories(${TargetName} PRIVATE $ENV{HOME}/NGL/lib )

# add exe and link libs that must be after the other defines
target_link_libraries(${TargetName} PRIVATE OpenImageIO::OpenImageIO OpenImageIO::OpenImageIO_Util)
if(UNIX)
   target_link_libraries(${TargetName} PRIVATE  IlmBase::Iex IlmBase::Half IlmBase::Imath IlmBase::IexMath)
   target_link_libraries(${TargetName} PRIVATE OpenEXR::IlmImf OpenEXR::IlmImfUtil OpenEXR::IlmImfConfig)
endif()
target_link_libraries(${TargetName} PRIVATE ${PROJECT_LINK_LIBS}  Qt5::Widgets fmt::fmt-header-only  )


add_custom_target(CopyShaders ALL
    COMMAND ${CMAKE_COMMAND} -E copy_directory
    ${CMAKE_CURRENT_SOURCE_DIR}/shaders
    $<TARGET_FILE_DIR:${TargetName}>/shaders
    ) 