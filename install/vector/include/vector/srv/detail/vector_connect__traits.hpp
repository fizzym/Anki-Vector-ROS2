// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vector:srv/VectorConnect.idl
// generated code does not contain a copyright notice

#ifndef VECTOR__SRV__DETAIL__VECTOR_CONNECT__TRAITS_HPP_
#define VECTOR__SRV__DETAIL__VECTOR_CONNECT__TRAITS_HPP_

#include "vector/srv/detail/vector_connect__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<vector::srv::VectorConnect_Request>()
{
  return "vector::srv::VectorConnect_Request";
}

template<>
inline const char * name<vector::srv::VectorConnect_Request>()
{
  return "vector/srv/VectorConnect_Request";
}

template<>
struct has_fixed_size<vector::srv::VectorConnect_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<vector::srv::VectorConnect_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<vector::srv::VectorConnect_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<vector::srv::VectorConnect_Response>()
{
  return "vector::srv::VectorConnect_Response";
}

template<>
inline const char * name<vector::srv::VectorConnect_Response>()
{
  return "vector/srv/VectorConnect_Response";
}

template<>
struct has_fixed_size<vector::srv::VectorConnect_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<vector::srv::VectorConnect_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<vector::srv::VectorConnect_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<vector::srv::VectorConnect>()
{
  return "vector::srv::VectorConnect";
}

template<>
inline const char * name<vector::srv::VectorConnect>()
{
  return "vector/srv/VectorConnect";
}

template<>
struct has_fixed_size<vector::srv::VectorConnect>
  : std::integral_constant<
    bool,
    has_fixed_size<vector::srv::VectorConnect_Request>::value &&
    has_fixed_size<vector::srv::VectorConnect_Response>::value
  >
{
};

template<>
struct has_bounded_size<vector::srv::VectorConnect>
  : std::integral_constant<
    bool,
    has_bounded_size<vector::srv::VectorConnect_Request>::value &&
    has_bounded_size<vector::srv::VectorConnect_Response>::value
  >
{
};

template<>
struct is_service<vector::srv::VectorConnect>
  : std::true_type
{
};

template<>
struct is_service_request<vector::srv::VectorConnect_Request>
  : std::true_type
{
};

template<>
struct is_service_response<vector::srv::VectorConnect_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // VECTOR__SRV__DETAIL__VECTOR_CONNECT__TRAITS_HPP_
