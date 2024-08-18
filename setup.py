from setuptools import setup

setup(
    name="crel",
    description="fast, templateless html generation",
    keywords="python, html, simple, fast",
    url="https://github.com/null-none/crel",
    packages=[
        "types",
    ],
    namespace_packages=["src"],
    package_dir={"src": "src"},
    classifiers=["Framework :: Django"],
)
