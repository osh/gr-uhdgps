INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_UHDGPS uhdgps)

FIND_PATH(
    UHDGPS_INCLUDE_DIRS
    NAMES uhdgps/api.h
    HINTS $ENV{UHDGPS_DIR}/include
        ${PC_UHDGPS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    UHDGPS_LIBRARIES
    NAMES gnuradio-uhdgps
    HINTS $ENV{UHDGPS_DIR}/lib
        ${PC_UHDGPS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(UHDGPS DEFAULT_MSG UHDGPS_LIBRARIES UHDGPS_INCLUDE_DIRS)
MARK_AS_ADVANCED(UHDGPS_LIBRARIES UHDGPS_INCLUDE_DIRS)

