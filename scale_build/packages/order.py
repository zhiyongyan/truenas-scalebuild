import logging

from scale_build.exceptions import CallError
from scale_build.utils.package import get_packages


logger = logging.getLogger(__name__)


def get_initialized_packages(desired_packages=None):
    binary_packages = {}
    desired_packages = desired_packages or []
    packages_list = get_packages()
    packages = {}
    for package in packages_list:
        if not package.exists:
            raise CallError(f'Missing sources for {package.name},  did you forget to run "make checkout" ?')

        packages[package.name] = package
        for binary_package in package.binary_packages:
            binary_packages[binary_package.name] = binary_package

    if desired_packages and not set(desired_packages).issubset(set(packages)):
        raise CallError(f'{", ".join(set(desired_packages) - set(packages))!r} packages not found')

    for pkg_name, package in packages.items():
        for dep in filter(lambda d: d in packages, package.build_time_dependencies(binary_packages)):
            packages[dep].children.add(pkg_name)

    if desired_packages:
        for pkg_name, package in filter(
            lambda i: i[1].name in desired_packages or any(desired in i[1].children for desired in desired_packages),
            packages.items()
        ):
            package.force_build = pkg_name in desired_packages or package.hash_changed
    else:
        for pkg_name, package in filter(lambda i: i[1].hash_changed, packages.items()):
            for child in package.children:
                packages[child].parent_changed = True

    return {package.name: package for package in packages.values()}


def get_to_build_packages(packages=None, desired_packages=None):
    return {
        k: v for k, v in (packages or get_initialized_packages()).items()
        if (v.force_build if desired_packages else v.rebuild)
    }
