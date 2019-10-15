from setuptools import setup

setup(
    name="python-webhook-server",
    version="0.1",
    description="A simple but powerful webhook server",
    url="",
    author="Vangelis Kostalas",
    author_email="kostalas.v@gmail.com",
    license="MIT",
    packages=["webhookserver"],
    entry_points={
        "console_scripts": ["webhookserver = webhookserver.cli:main [SERVE]"]
    },
    extras_require={"SERVE": ["gunicorn>=19.9, <20"], "CLI": ["gunicorn>=19.9, <20"]},
    zip_safe=False,
)
