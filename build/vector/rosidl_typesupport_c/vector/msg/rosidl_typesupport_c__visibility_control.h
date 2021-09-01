// generated from
// rosidl_typesupport_c/resource/rosidl_typesupport_c__visibility_control.h.in
// generated code does not contain a copyright notice

#ifndef VECTOR__MSG__ROSIDL_TYPESUPPORT_C__VISIBILITY_CONTROL_H_
#define VECTOR__MSG__ROSIDL_TYPESUPPORT_C__VISIBILITY_CONTROL_H_

#ifdef __cplusplus
extern "C"
{
#endif

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__
  #ifdef __GNUC__
    #define ROSIDL_TYPESUPPORT_C_EXPORT_vector __attribute__ ((dllexport))
    #define ROSIDL_TYPESUPPORT_C_IMPORT_vector __attribute__ ((dllimport))
  #else
    #define ROSIDL_TYPESUPPORT_C_EXPORT_vector __declspec(dllexport)
    #define ROSIDL_TYPESUPPORT_C_IMPORT_vector __declspec(dllimport)
  #endif
  #ifdef ROSIDL_TYPESUPPORT_C_BUILDING_DLL_vector
    #define ROSIDL_TYPESUPPORT_C_PUBLIC_vector ROSIDL_TYPESUPPORT_C_EXPORT_vector
  #else
    #define ROSIDL_TYPESUPPORT_C_PUBLIC_vector ROSIDL_TYPESUPPORT_C_IMPORT_vector
  #endif
#else
  #define ROSIDL_TYPESUPPORT_C_EXPORT_vector __attribute__ ((visibility("default")))
  #define ROSIDL_TYPESUPPORT_C_IMPORT_vector
  #if __GNUC__ >= 4
    #define ROSIDL_TYPESUPPORT_C_PUBLIC_vector __attribute__ ((visibility("default")))
  #else
    #define ROSIDL_TYPESUPPORT_C_PUBLIC_vector
  #endif
#endif

#ifdef __cplusplus
}
#endif

#endif  // VECTOR__MSG__ROSIDL_TYPESUPPORT_C__VISIBILITY_CONTROL_H_
