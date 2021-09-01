from setuptools import setup

package_name = 'keyDrive'

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
                'node1 = keyDrive.Velocity_Publisher:main',
                'node2 = keyDrive.Velocity_Subscribe_Drive:main',
                'node3 = keyDrive.Vel_Sub_Drive_2:main',
        ],
	},

)
