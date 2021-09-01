// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vector:srv/VectorConnect.idl
// generated code does not contain a copyright notice

#ifndef VECTOR__SRV__DETAIL__VECTOR_CONNECT__STRUCT_HPP_
#define VECTOR__SRV__DETAIL__VECTOR_CONNECT__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__vector__srv__VectorConnect_Request __attribute__((deprecated))
#else
# define DEPRECATED__vector__srv__VectorConnect_Request __declspec(deprecated)
#endif

namespace vector
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct VectorConnect_Request_
{
  using Type = VectorConnect_Request_<ContainerAllocator>;

  explicit VectorConnect_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->serial = "";
    }
  }

  explicit VectorConnect_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : serial(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->serial = "";
    }
  }

  // field types and members
  using _serial_type =
    std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other>;
  _serial_type serial;

  // setters for named parameter idiom
  Type & set__serial(
    const std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other> & _arg)
  {
    this->serial = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vector::srv::VectorConnect_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const vector::srv::VectorConnect_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vector::srv::VectorConnect_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vector::srv::VectorConnect_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vector::srv::VectorConnect_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vector::srv::VectorConnect_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vector::srv::VectorConnect_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vector::srv::VectorConnect_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vector::srv::VectorConnect_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vector::srv::VectorConnect_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vector__srv__VectorConnect_Request
    std::shared_ptr<vector::srv::VectorConnect_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vector__srv__VectorConnect_Request
    std::shared_ptr<vector::srv::VectorConnect_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VectorConnect_Request_ & other) const
  {
    if (this->serial != other.serial) {
      return false;
    }
    return true;
  }
  bool operator!=(const VectorConnect_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VectorConnect_Request_

// alias to use template instance with default allocator
using VectorConnect_Request =
  vector::srv::VectorConnect_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace vector


#ifndef _WIN32
# define DEPRECATED__vector__srv__VectorConnect_Response __attribute__((deprecated))
#else
# define DEPRECATED__vector__srv__VectorConnect_Response __declspec(deprecated)
#endif

namespace vector
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct VectorConnect_Response_
{
  using Type = VectorConnect_Response_<ContainerAllocator>;

  explicit VectorConnect_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit VectorConnect_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vector::srv::VectorConnect_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const vector::srv::VectorConnect_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vector::srv::VectorConnect_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vector::srv::VectorConnect_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vector::srv::VectorConnect_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vector::srv::VectorConnect_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vector::srv::VectorConnect_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vector::srv::VectorConnect_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vector::srv::VectorConnect_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vector::srv::VectorConnect_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vector__srv__VectorConnect_Response
    std::shared_ptr<vector::srv::VectorConnect_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vector__srv__VectorConnect_Response
    std::shared_ptr<vector::srv::VectorConnect_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VectorConnect_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const VectorConnect_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VectorConnect_Response_

// alias to use template instance with default allocator
using VectorConnect_Response =
  vector::srv::VectorConnect_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace vector

namespace vector
{

namespace srv
{

struct VectorConnect
{
  using Request = vector::srv::VectorConnect_Request;
  using Response = vector::srv::VectorConnect_Response;
};

}  // namespace srv

}  // namespace vector

#endif  // VECTOR__SRV__DETAIL__VECTOR_CONNECT__STRUCT_HPP_
