

option(CONFIG_SERVER "Build and install server" OFF)


if(PYTHON_EXECUTABLE)
	get_filename_component(tmp ${PYTHON_EXECUTABLE} PATH)
	get_filename_component(PYTHON_MY_BASE_DIR ${tmp} PATH)
	message("Python base dir ->${PYTHON_MY_BASE_DIR}<--")
else()
	message("Python undefined")
endif()

if(CONFIG_SERVER)
	message("configuring server from ${CMAKE_CURRENT_SOURCE_DIR} to
${CMAKE_INSTALL_PREFIX} ")
endif()

file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/server DESTINATION ${CMAKE_INSTALL_PREFIX}/bin ) 
set(RCM_SERVER_DIR ${CMAKE_INSTALL_PREFIX}/bin/python)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/python/Desktop_setup/paraview3.14.desktop
${RCM_SERVER_DIR}/Desktop_setup/paraview3.14.desktop @ONLY)

