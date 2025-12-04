#!/usr/bin/env python
try:
    # from distutils.core import setup
    # from distutils.extension import Extension
    from setuptools import setup, Extension
    from Cython.Build import cythonize

    import numpy as np

except ImportError:
    raise ImportError('Numpy needs to be installed or updated.')

extensions = [
    Extension(
        name="LayerModel.rfmini",  # 扩展模块的名称
        sources=[
            "src/extensions/rfmini/rfmini.pyx",  # Cython 文件
            "src/extensions/rfmini/greens.cpp",  # C++ 源文件
            "src/extensions/rfmini/model.cpp",
            "src/extensions/rfmini/pd.cpp",
            "src/extensions/rfmini/synrf.cpp",
            "src/extensions/rfmini/wrap.cpp",
            "src/extensions/rfmini/fork.cpp"
        ],
        include_dirs=[np.get_include()],  # 包含 numpy 的头文件路径
        # language="c++",  # 指定语言为 C++
        #extra_compile_args=["-std=c++17"],  # 添加 C++17 标准支持
    )
]


# 使用 setuptools 的 setup
setup(
    name="LayerModel",
    version="2.0",
    author="unknown",
    description="Calculate layered model ground response",
    install_requires=["numpy", "cython"],  # 指定依赖
    packages=['LayerModel'],  # 包含的 Python 包
    package_dir={'LayerModel': 'src'},  # Python 包的源码目录
    ext_modules=cythonize(extensions),  # 使用 Cython 编译扩展
    # zip_safe=False  # 关闭 zip 压缩，避免加载问题
)
