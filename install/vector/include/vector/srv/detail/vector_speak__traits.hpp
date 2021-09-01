// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vector:srv/VectorSpeak.idl
// generated code does not contain a copyright notice

#ifndef VECTOR__SRV__DETAIL__VECTOR_SPEAK__TRAITS_HPP_
#define VECTOR__SRV__DETAIL__VECTOR_SPEAK__TRAITS_HPP_

#include "vector/srv/detail/vector_speak__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<vector::srv::VectorSpeak_Request>()
{
  return "vector::srv::VectorSpeak_Request";
}

template<>
inline const char * name<vector::srv::VectorSpeak_Request>()
{
  return "vector/srv/VectorSpeak_Request";
}

template<>
struct has_fixed_size<vector::srv::VectorSpeak_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<vector::srv::VectorSpeak_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<vector::srv::VectorSpeak_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<vector::srv::VectorSpeak_Response>()
{
  return "vector::srv::VectorSpeak_Response";
}

template<>
inline const char * name<vector::srv::VectorSpeak_Response>()
{
  return "vector/srv/VectorSpeak_Response";
}

template<>
struct has_fixed_size<vector::srv::VectorSpeak_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<vector::srv::VectorSpeak_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<vector::srv::VectorSpeak_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<vector::srv::VectorSpeak>()
{
  return "vector::srv::VectorSpeak";
}

template<>
inline const char * name<vector::srv::VectorSpeak>()
{
  return "vector/srv/VectorSpeak";
}

template<>
struct has_fixed_size<vector::srv::VectorSpeak>
  : std::integral_constant<
    bool,
    has_fixed_size<vector::srv::VectorSpeak_Request>::value &&
    has_fixed_size<vector::srv::VectorSpeak_Response>::value
  >
{
};

template<>
struct has_bounded_size<vector::srv::VectorSpeak>
  : std::integral_constant<
    bool,
    has_bounded_size<vector::srv::VectorSpeak_Request>::value &&
    has_bounded_size<vector::srv::VectorSpeak_Response>::value
  >
{
};

template<>
struct is_service<vector::srv::VectorSpeak>
  : std::true_type
{
};

template<>
struct is_service_request<vector::srv::VectorSpeak_Request>
  : std::true_type
{
};

template<>
struct is_service_response<vector::srv::VectorSpeak_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // VECTOR__SRV__DETAIL__VECTOR_SPEAK__TRAITS_HPP_
