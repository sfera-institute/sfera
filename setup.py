import pathlib
import re
import setuptools


root = pathlib.Path(__file__).absolute().parent
name = root.name
package_path = root / name
readme_path = root / 'README.md'
requirements_path = root / 'requirements.txt'
github_url = f'https://github.com/sfera-institute/{name}'


def get_version():
    path = package_path / '__init__.py'
    text = path.read_text()
    return re.search(r"version = '(.*?)'", text).group(1)


def get_documentation():
    return readme_path.read_text()


def get_requirements():
    return requirements_path.read_text().splitlines()


def get_package_configuration():
    config = dict(
        name = name,
        version = get_version(),
        author = 'SFERA Institute',
        author_email = 'hello@sfera.institute',
        description = 'An open-source infrastructure for the 99%.',
        long_description = get_documentation(),
        long_description_content_type = 'text/markdown',
        url = github_url,
        project_urls = {
            'Documentation': github_url,
            'Source': github_url,
            'Tracker': f'{github_url}/issues',
        },
        packages = setuptools.find_packages(),
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
        ],
        python_requires = '>=3.8',
        install_requires = get_requirements(),
    )
    return config


if __name__ == '__main__':
    config = get_package_configuration()
    setuptools.setup(**config)