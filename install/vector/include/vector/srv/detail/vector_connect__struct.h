// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vector:srv/VectorConnect.idl
// generated code does not contain a copyright notice

#ifndef VECTOR__SRV__DETAIL__VECTOR_CONNECT__STRUCT_H_
#define VECTOR__SRV__DETAIL__VECTOR_CONNECT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'serial'
#include "rosidl_runtime_c/string.h"

// Struct defined in srv/VectorConnect in the package vector.
typedef struct vector__srv__VectorConnect_Request
{
  rosidl_runtime_c__String serial;
} vector__srv__VectorConnect_Request;

// Struct for a sequence of vector__srv__VectorConnect_Request.
typedef struct vector__srv__VectorConnect_Request__Sequence
{
  vector__srv__VectorConnect_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vector__srv__VectorConnect_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

// Struct defined in srv/VectorConnect in the package vector.
typedef struct vector__srv__VectorConnect_Response
{
  bool success;
  rosidl_runtime_c__String message;
} vector__srv__VectorConnect_Response;

// Struct for a sequence of vector__srv__VectorConnect_Response.
typedef struct vector__srv__VectorConnect_Response__Sequence
{
  vector__srv__VectorConnect_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vector__srv__VectorConnect_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VECTOR__SRV__DETAIL__VECTOR_CONNECT__STRUCT_H_
