

option(CONFIG_SERVER "Build and install server" OFF)


if(PYTHON_EXECUTABLE)
	get_filename_component(tmp ${PYTHON_EXECUTABLE} PATH)
	get_filename_component(PYTHON_MY_BASE_DIR ${tmp} PATH)
	message("Python base dir ->${PYTHON_MY_BASE_DIR}<--")
else()
	message("Python undefined")
endif()

if(CONFIG_SERVER)
	message("configuring server from source dir to build dir")
endif()

file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/python DESTINATION ${CMAKE_INSTALL_PREFIX}/bin ) 