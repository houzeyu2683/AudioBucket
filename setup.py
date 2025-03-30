import setuptools
setuptools.find_packages('.')

name = "AudioBucket"
setuptools.setup(
    name=name,
    version="0.1.0",
    packages=setuptools.find_packages('.'),
    install_requires=[
        "moviepy==2.1.2",
        "numpy==2.2.4",
        "pandas==2.2.3",
        "pillow==10.4.0",
        "tqdm==4.67.1",
        "yt-dlp==2025.3.27"
    ],
    author="Greg",
    author_email="houzeyu2683@gmail.com",
    description="",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/houzeyu2683/InstrumentalExtraction",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)