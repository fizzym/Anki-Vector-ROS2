// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vector:srv/VectorSpeak.idl
// generated code does not contain a copyright notice
#include "vector/srv/detail/vector_speak__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

// Include directives for member types
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
vector__srv__VectorSpeak_Request__init(vector__srv__VectorSpeak_Request * msg)
{
  if (!msg) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    vector__srv__VectorSpeak_Request__fini(msg);
    return false;
  }
  return true;
}

void
vector__srv__VectorSpeak_Request__fini(vector__srv__VectorSpeak_Request * msg)
{
  if (!msg) {
    return;
  }
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

vector__srv__VectorSpeak_Request *
vector__srv__VectorSpeak_Request__create()
{
  vector__srv__VectorSpeak_Request * msg = (vector__srv__VectorSpeak_Request *)malloc(sizeof(vector__srv__VectorSpeak_Request));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vector__srv__VectorSpeak_Request));
  bool success = vector__srv__VectorSpeak_Request__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
vector__srv__VectorSpeak_Request__destroy(vector__srv__VectorSpeak_Request * msg)
{
  if (msg) {
    vector__srv__VectorSpeak_Request__fini(msg);
  }
  free(msg);
}


bool
vector__srv__VectorSpeak_Request__Sequence__init(vector__srv__VectorSpeak_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  vector__srv__VectorSpeak_Request * data = NULL;
  if (size) {
    data = (vector__srv__VectorSpeak_Request *)calloc(size, sizeof(vector__srv__VectorSpeak_Request));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vector__srv__VectorSpeak_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vector__srv__VectorSpeak_Request__fini(&data[i - 1]);
      }
      free(data);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
vector__srv__VectorSpeak_Request__Sequence__fini(vector__srv__VectorSpeak_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      vector__srv__VectorSpeak_Request__fini(&array->data[i]);
    }
    free(array->data);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

vector__srv__VectorSpeak_Request__Sequence *
vector__srv__VectorSpeak_Request__Sequence__create(size_t size)
{
  vector__srv__VectorSpeak_Request__Sequence * array = (vector__srv__VectorSpeak_Request__Sequence *)malloc(sizeof(vector__srv__VectorSpeak_Request__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = vector__srv__VectorSpeak_Request__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
vector__srv__VectorSpeak_Request__Sequence__destroy(vector__srv__VectorSpeak_Request__Sequence * array)
{
  if (array) {
    vector__srv__VectorSpeak_Request__Sequence__fini(array);
  }
  free(array);
}


bool
vector__srv__VectorSpeak_Response__init(vector__srv__VectorSpeak_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  return true;
}

void
vector__srv__VectorSpeak_Response__fini(vector__srv__VectorSpeak_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
}

vector__srv__VectorSpeak_Response *
vector__srv__VectorSpeak_Response__create()
{
  vector__srv__VectorSpeak_Response * msg = (vector__srv__VectorSpeak_Response *)malloc(sizeof(vector__srv__VectorSpeak_Response));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vector__srv__VectorSpeak_Response));
  bool success = vector__srv__VectorSpeak_Response__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
vector__srv__VectorSpeak_Response__destroy(vector__srv__VectorSpeak_Response * msg)
{
  if (msg) {
    vector__srv__VectorSpeak_Response__fini(msg);
  }
  free(msg);
}


bool
vector__srv__VectorSpeak_Response__Sequence__init(vector__srv__VectorSpeak_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  vector__srv__VectorSpeak_Response * data = NULL;
  if (size) {
    data = (vector__srv__VectorSpeak_Response *)calloc(size, sizeof(vector__srv__VectorSpeak_Response));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vector__srv__VectorSpeak_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vector__srv__VectorSpeak_Response__fini(&data[i - 1]);
      }
      free(data);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
vector__srv__VectorSpeak_Response__Sequence__fini(vector__srv__VectorSpeak_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      vector__srv__VectorSpeak_Response__fini(&array->data[i]);
    }
    free(array->data);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

vector__srv__VectorSpeak_Response__Sequence *
vector__srv__VectorSpeak_Response__Sequence__create(size_t size)
{
  vector__srv__VectorSpeak_Response__Sequence * array = (vector__srv__VectorSpeak_Response__Sequence *)malloc(sizeof(vector__srv__VectorSpeak_Response__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = vector__srv__VectorSpeak_Response__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
vector__srv__VectorSpeak_Response__Sequence__destroy(vector__srv__VectorSpeak_Response__Sequence * array)
{
  if (array) {
    vector__srv__VectorSpeak_Response__Sequence__fini(array);
  }
  free(array);
}
