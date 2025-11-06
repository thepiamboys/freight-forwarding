from setuptools import setup, find_packages
import os

# Read README if exists
long_description = ""
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="freight_forwarding",
    version="1.0.0",
    description="Freight Forwarding add-on for ERPNext v15",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="PT Kurhanz Trans",
    author_email="dev@kurhanz.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "frappe>=15.0.0,<16.0.0",
        "gunicorn @ git+https://github.com/frappe/gunicorn@bb554053bb87218120d76ab6676af7015680e8b6",
    ],
)

