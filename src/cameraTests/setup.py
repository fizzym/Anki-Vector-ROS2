from setuptools import setup

package_name = 'cameraTests'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fizzer',
    maintainer_email='fizzer@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'cam_pub = cameraTests.publish_camera_feed:main',
            'cam_sub = cameraTests.subscribe_camera_feed:main',
            'cam_pub_2 = cameraTests.publish_camera_feed_2:main',
            'cam_sub_2 = cameraTests.subscribe_camera_feed_2:main',
        ],
    },
)
