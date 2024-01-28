import os
import shutil
import setuptools
from setuptools.extension import Extension
from Cython.Build import cythonize, build_ext


def need_compiler(file, file_path):
    return (
        '__init__' not in file
        and 'build' not in file_path
        and 'dist' not in file_path
        and 'output' not in file_path
        and 'setup' not in file
    )


def find_compiler_files(root_path=os.getcwd()):
    result, white_pys = [], []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            path = os.path.join(root, file)
            if file.endswith('.py') and 'setup' not in file:
                if need_compiler(file, path) and '__init__.py' not in path:
                    result.append(path)
                else:
                    white_pys.append(path)
    result = [
        Extension(str(f).replace('.py', '').replace(os.path.sep, '.'),
                  sources=[str(f)])
        for f in result
    ]
    white_pys = [str(f).replace('.py', '').replace(os.path.sep, '.') for f in white_pys]
    return result, white_pys


if __name__ == '__main__':
    _src_files, _white_pys = find_compiler_files('toolboxes')
    requirements = [i.strip() for i in open('requirements.txt').readlines()]

    with open(r"README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    version = '0.0.1'
    name = 'toolboxes'
    setuptools.setup(
        name=name,
        version=version,
        description='工程开发、性能调优常用方法',
        long_description=long_description,
        long_description_content_type="text/markdown",
        author='陈霁皓',
        python_requires=">=3.8",
        py_modules=_white_pys,
        ext_modules=cythonize(
            _src_files,
            compiler_directives={'language_level': '3'}
        ),
        install_requires=requirements,
        packages=['toolboxes'],
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )

    for _root, _, _files in os.walk(os.getcwd()):
        for _file in _files:
            if _file.endswith('.c'):
                os.remove(os.path.join(_root, _file))
