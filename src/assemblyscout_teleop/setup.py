from setuptools import find_packages, setup

package_name = 'assemblyscout_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name + '/launch',
            ['launch/ps4_turtlesim.launch.py']),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zadrac',
    maintainer_email='ivanvazquezv@icloud.com',
    description='Teleoperación de AssemblyScout con control PS4 para ROS 2',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'ps4_teleop = assemblyscout_teleop.ps4_teleop:main',
        ],
    },
)
