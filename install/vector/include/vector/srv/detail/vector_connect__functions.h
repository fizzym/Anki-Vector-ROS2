// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from vector:srv/VectorConnect.idl
// generated code does not contain a copyright notice

#ifndef VECTOR__SRV__DETAIL__VECTOR_CONNECT__FUNCTIONS_H_
#define VECTOR__SRV__DETAIL__VECTOR_CONNECT__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "vector/msg/rosidl_generator_c__visibility_control.h"

#include "vector/srv/detail/vector_connect__struct.h"

/// Initialize srv/VectorConnect message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * vector__srv__VectorConnect_Request
 * )) before or use
 * vector__srv__VectorConnect_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
bool
vector__srv__VectorConnect_Request__init(vector__srv__VectorConnect_Request * msg);

/// Finalize srv/VectorConnect message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
void
vector__srv__VectorConnect_Request__fini(vector__srv__VectorConnect_Request * msg);

/// Create srv/VectorConnect message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * vector__srv__VectorConnect_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
vector__srv__VectorConnect_Request *
vector__srv__VectorConnect_Request__create();

/// Destroy srv/VectorConnect message.
/**
 * It calls
 * vector__srv__VectorConnect_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
void
vector__srv__VectorConnect_Request__destroy(vector__srv__VectorConnect_Request * msg);


/// Initialize array of srv/VectorConnect messages.
/**
 * It allocates the memory for the number of elements and calls
 * vector__srv__VectorConnect_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
bool
vector__srv__VectorConnect_Request__Sequence__init(vector__srv__VectorConnect_Request__Sequence * array, size_t size);

/// Finalize array of srv/VectorConnect messages.
/**
 * It calls
 * vector__srv__VectorConnect_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
void
vector__srv__VectorConnect_Request__Sequence__fini(vector__srv__VectorConnect_Request__Sequence * array);

/// Create array of srv/VectorConnect messages.
/**
 * It allocates the memory for the array and calls
 * vector__srv__VectorConnect_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
vector__srv__VectorConnect_Request__Sequence *
vector__srv__VectorConnect_Request__Sequence__create(size_t size);

/// Destroy array of srv/VectorConnect messages.
/**
 * It calls
 * vector__srv__VectorConnect_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
void
vector__srv__VectorConnect_Request__Sequence__destroy(vector__srv__VectorConnect_Request__Sequence * array);

/// Initialize srv/VectorConnect message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * vector__srv__VectorConnect_Response
 * )) before or use
 * vector__srv__VectorConnect_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
bool
vector__srv__VectorConnect_Response__init(vector__srv__VectorConnect_Response * msg);

/// Finalize srv/VectorConnect message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
void
vector__srv__VectorConnect_Response__fini(vector__srv__VectorConnect_Response * msg);

/// Create srv/VectorConnect message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * vector__srv__VectorConnect_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
vector__srv__VectorConnect_Response *
vector__srv__VectorConnect_Response__create();

/// Destroy srv/VectorConnect message.
/**
 * It calls
 * vector__srv__VectorConnect_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
void
vector__srv__VectorConnect_Response__destroy(vector__srv__VectorConnect_Response * msg);


/// Initialize array of srv/VectorConnect messages.
/**
 * It allocates the memory for the number of elements and calls
 * vector__srv__VectorConnect_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
bool
vector__srv__VectorConnect_Response__Sequence__init(vector__srv__VectorConnect_Response__Sequence * array, size_t size);

/// Finalize array of srv/VectorConnect messages.
/**
 * It calls
 * vector__srv__VectorConnect_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
void
vector__srv__VectorConnect_Response__Sequence__fini(vector__srv__VectorConnect_Response__Sequence * array);

/// Create array of srv/VectorConnect messages.
/**
 * It allocates the memory for the array and calls
 * vector__srv__VectorConnect_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
vector__srv__VectorConnect_Response__Sequence *
vector__srv__VectorConnect_Response__Sequence__create(size_t size);

/// Destroy array of srv/VectorConnect messages.
/**
 * It calls
 * vector__srv__VectorConnect_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vector
void
vector__srv__VectorConnect_Response__Sequence__destroy(vector__srv__VectorConnect_Response__Sequence * array);

#ifdef __cplusplus
}
#endif

#endif  // VECTOR__SRV__DETAIL__VECTOR_CONNECT__FUNCTIONS_H_
