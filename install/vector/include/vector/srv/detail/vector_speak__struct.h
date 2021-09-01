// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vector:srv/VectorSpeak.idl
// generated code does not contain a copyright notice

#ifndef VECTOR__SRV__DETAIL__VECTOR_SPEAK__STRUCT_H_
#define VECTOR__SRV__DETAIL__VECTOR_SPEAK__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

// Struct defined in srv/VectorSpeak in the package vector.
typedef struct vector__srv__VectorSpeak_Request
{
  rosidl_runtime_c__String message;
} vector__srv__VectorSpeak_Request;

// Struct for a sequence of vector__srv__VectorSpeak_Request.
typedef struct vector__srv__VectorSpeak_Request__Sequence
{
  vector__srv__VectorSpeak_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vector__srv__VectorSpeak_Request__Sequence;


// Constants defined in the message

// Struct defined in srv/VectorSpeak in the package vector.
typedef struct vector__srv__VectorSpeak_Response
{
  bool success;
} vector__srv__VectorSpeak_Response;

// Struct for a sequence of vector__srv__VectorSpeak_Response.
typedef struct vector__srv__VectorSpeak_Response__Sequence
{
  vector__srv__VectorSpeak_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vector__srv__VectorSpeak_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VECTOR__SRV__DETAIL__VECTOR_SPEAK__STRUCT_H_
