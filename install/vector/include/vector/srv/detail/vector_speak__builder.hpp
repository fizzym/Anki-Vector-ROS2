// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vector:srv/VectorSpeak.idl
// generated code does not contain a copyright notice

#ifndef VECTOR__SRV__DETAIL__VECTOR_SPEAK__BUILDER_HPP_
#define VECTOR__SRV__DETAIL__VECTOR_SPEAK__BUILDER_HPP_

#include "vector/srv/detail/vector_speak__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace vector
{

namespace srv
{

namespace builder
{

class Init_VectorSpeak_Request_message
{
public:
  Init_VectorSpeak_Request_message()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::vector::srv::VectorSpeak_Request message(::vector::srv::VectorSpeak_Request::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vector::srv::VectorSpeak_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vector::srv::VectorSpeak_Request>()
{
  return vector::srv::builder::Init_VectorSpeak_Request_message();
}

}  // namespace vector


namespace vector
{

namespace srv
{

namespace builder
{

class Init_VectorSpeak_Response_success
{
public:
  Init_VectorSpeak_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::vector::srv::VectorSpeak_Response success(::vector::srv::VectorSpeak_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vector::srv::VectorSpeak_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vector::srv::VectorSpeak_Response>()
{
  return vector::srv::builder::Init_VectorSpeak_Response_success();
}

}  // namespace vector

#endif  // VECTOR__SRV__DETAIL__VECTOR_SPEAK__BUILDER_HPP_
