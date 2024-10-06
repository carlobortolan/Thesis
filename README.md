# GoCast Analytics

Analysis of service and error logs of TUMLive's GoCast Microservices.

## Overview

1. **API Error Analysis**

2. **Worker Error Analysis**

3. **gRPC vs REST API Comparison**

## Usage

1. Create and activate the virtual environment

```sh
python -m venv env && source env/bin/activate
```

2. Run the notebook

```sh
jupyter notebook
```

## Build

Run the following command to build the notebook. The build files can be found in the `build` folder:

```sh
make
```

This will execute the Jupyter Notebook and convert it to an HTML file, which will be moved to the `build` directory as `index.html.`

To clean up the build directory, run:

```sh
make clean
```

---

© Carlo Bortolan

> Carlo Bortolan &nbsp;&middot;&nbsp;
> GitHub [carlobortolan](https://github.com/carlobortolan) &nbsp;&middot;&nbsp;
> contact via [carlobortolan@gmail.com](mailto:carlobortolan@gmail.com)
