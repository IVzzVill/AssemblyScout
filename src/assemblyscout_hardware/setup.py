from setuptools import find_packages, setup

package_name = 'assemblyscout_hardware'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/physical_base.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zadrac',
    maintainer_email='ivanvazquezv@icloud.com',
    description='Puente ROS 2 para la base física de AssemblyScout.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'esp32_bridge = assemblyscout_hardware.esp32_bridge:main',
        ],
    },
)
