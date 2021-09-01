// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from vector:srv/VectorSpeak.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "vector/srv/detail/vector_speak__rosidl_typesupport_introspection_c.h"
#include "vector/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "vector/srv/detail/vector_speak__functions.h"
#include "vector/srv/detail/vector_speak__struct.h"


// Include directives for member types
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void VectorSpeak_Request__rosidl_typesupport_introspection_c__VectorSpeak_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  vector__srv__VectorSpeak_Request__init(message_memory);
}

void VectorSpeak_Request__rosidl_typesupport_introspection_c__VectorSpeak_Request_fini_function(void * message_memory)
{
  vector__srv__VectorSpeak_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember VectorSpeak_Request__rosidl_typesupport_introspection_c__VectorSpeak_Request_message_member_array[1] = {
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vector__srv__VectorSpeak_Request, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers VectorSpeak_Request__rosidl_typesupport_introspection_c__VectorSpeak_Request_message_members = {
  "vector__srv",  // message namespace
  "VectorSpeak_Request",  // message name
  1,  // number of fields
  sizeof(vector__srv__VectorSpeak_Request),
  VectorSpeak_Request__rosidl_typesupport_introspection_c__VectorSpeak_Request_message_member_array,  // message members
  VectorSpeak_Request__rosidl_typesupport_introspection_c__VectorSpeak_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  VectorSpeak_Request__rosidl_typesupport_introspection_c__VectorSpeak_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t VectorSpeak_Request__rosidl_typesupport_introspection_c__VectorSpeak_Request_message_type_support_handle = {
  0,
  &VectorSpeak_Request__rosidl_typesupport_introspection_c__VectorSpeak_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_vector
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vector, srv, VectorSpeak_Request)() {
  if (!VectorSpeak_Request__rosidl_typesupport_introspection_c__VectorSpeak_Request_message_type_support_handle.typesupport_identifier) {
    VectorSpeak_Request__rosidl_typesupport_introspection_c__VectorSpeak_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &VectorSpeak_Request__rosidl_typesupport_introspection_c__VectorSpeak_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "vector/srv/detail/vector_speak__rosidl_typesupport_introspection_c.h"
// already included above
// #include "vector/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "vector/srv/detail/vector_speak__functions.h"
// already included above
// #include "vector/srv/detail/vector_speak__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void VectorSpeak_Response__rosidl_typesupport_introspection_c__VectorSpeak_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  vector__srv__VectorSpeak_Response__init(message_memory);
}

void VectorSpeak_Response__rosidl_typesupport_introspection_c__VectorSpeak_Response_fini_function(void * message_memory)
{
  vector__srv__VectorSpeak_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember VectorSpeak_Response__rosidl_typesupport_introspection_c__VectorSpeak_Response_message_member_array[1] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vector__srv__VectorSpeak_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers VectorSpeak_Response__rosidl_typesupport_introspection_c__VectorSpeak_Response_message_members = {
  "vector__srv",  // message namespace
  "VectorSpeak_Response",  // message name
  1,  // number of fields
  sizeof(vector__srv__VectorSpeak_Response),
  VectorSpeak_Response__rosidl_typesupport_introspection_c__VectorSpeak_Response_message_member_array,  // message members
  VectorSpeak_Response__rosidl_typesupport_introspection_c__VectorSpeak_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  VectorSpeak_Response__rosidl_typesupport_introspection_c__VectorSpeak_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t VectorSpeak_Response__rosidl_typesupport_introspection_c__VectorSpeak_Response_message_type_support_handle = {
  0,
  &VectorSpeak_Response__rosidl_typesupport_introspection_c__VectorSpeak_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_vector
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vector, srv, VectorSpeak_Response)() {
  if (!VectorSpeak_Response__rosidl_typesupport_introspection_c__VectorSpeak_Response_message_type_support_handle.typesupport_identifier) {
    VectorSpeak_Response__rosidl_typesupport_introspection_c__VectorSpeak_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &VectorSpeak_Response__rosidl_typesupport_introspection_c__VectorSpeak_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "vector/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "vector/srv/detail/vector_speak__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers vector__srv__detail__vector_speak__rosidl_typesupport_introspection_c__VectorSpeak_service_members = {
  "vector__srv",  // service namespace
  "VectorSpeak",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // vector__srv__detail__vector_speak__rosidl_typesupport_introspection_c__VectorSpeak_Request_message_type_support_handle,
  NULL  // response message
  // vector__srv__detail__vector_speak__rosidl_typesupport_introspection_c__VectorSpeak_Response_message_type_support_handle
};

static rosidl_service_type_support_t vector__srv__detail__vector_speak__rosidl_typesupport_introspection_c__VectorSpeak_service_type_support_handle = {
  0,
  &vector__srv__detail__vector_speak__rosidl_typesupport_introspection_c__VectorSpeak_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vector, srv, VectorSpeak_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vector, srv, VectorSpeak_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_vector
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vector, srv, VectorSpeak)() {
  if (!vector__srv__detail__vector_speak__rosidl_typesupport_introspection_c__VectorSpeak_service_type_support_handle.typesupport_identifier) {
    vector__srv__detail__vector_speak__rosidl_typesupport_introspection_c__VectorSpeak_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)vector__srv__detail__vector_speak__rosidl_typesupport_introspection_c__VectorSpeak_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vector, srv, VectorSpeak_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vector, srv, VectorSpeak_Response)()->data;
  }

  return &vector__srv__detail__vector_speak__rosidl_typesupport_introspection_c__VectorSpeak_service_type_support_handle;
}
