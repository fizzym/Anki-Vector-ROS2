// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vector:srv/VectorConnect.idl
// generated code does not contain a copyright notice

#ifndef VECTOR__SRV__DETAIL__VECTOR_CONNECT__BUILDER_HPP_
#define VECTOR__SRV__DETAIL__VECTOR_CONNECT__BUILDER_HPP_

#include "vector/srv/detail/vector_connect__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace vector
{

namespace srv
{

namespace builder
{

class Init_VectorConnect_Request_serial
{
public:
  Init_VectorConnect_Request_serial()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::vector::srv::VectorConnect_Request serial(::vector::srv::VectorConnect_Request::_serial_type arg)
  {
    msg_.serial = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vector::srv::VectorConnect_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vector::srv::VectorConnect_Request>()
{
  return vector::srv::builder::Init_VectorConnect_Request_serial();
}

}  // namespace vector


namespace vector
{

namespace srv
{

namespace builder
{

class Init_VectorConnect_Response_message
{
public:
  explicit Init_VectorConnect_Response_message(::vector::srv::VectorConnect_Response & msg)
  : msg_(msg)
  {}
  ::vector::srv::VectorConnect_Response message(::vector::srv::VectorConnect_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vector::srv::VectorConnect_Response msg_;
};

class Init_VectorConnect_Response_success
{
public:
  Init_VectorConnect_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VectorConnect_Response_message success(::vector::srv::VectorConnect_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_VectorConnect_Response_message(msg_);
  }

private:
  ::vector::srv::VectorConnect_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vector::srv::VectorConnect_Response>()
{
  return vector::srv::builder::Init_VectorConnect_Response_success();
}

}  // namespace vector

#endif  // VECTOR__SRV__DETAIL__VECTOR_CONNECT__BUILDER_HPP_
