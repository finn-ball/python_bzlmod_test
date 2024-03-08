# python_bzlmod_test

A small example to show potential problems and open questions with the `pip` extension.

Both projects simply depend on matplotlib.

The `foo` repository doesn't pin matplotlib and imports `3.8.3`.

The `bar` repository requires matplotlib to be `matplotlib<=3.7.0`.

## Wrong matplotlib version

```sh
cd bar
bazel run //:main
```

Notice that it uses matplotlib `3.8.3`.

Now comment out the dependency on `@foo` in the `BUILD.bazel` file and also fix `main.py` like so:

```python
import matplotlib
import platform

# from foo import print_version

if __name__ == "__main__":
    # print_version()
    print("python version: ", platform.python_version())
    print("matplotlib version: ", matplotlib.__version__)

```

Now `bazel run //:main` which produces matplotlib `3.7.0`.

## Changing python versions

Reset the project back the current commit and make sure you're in the `bar` folder again.

Update the `bar/MODULE.bazel` file to use a different python toolchain:

```starlark
module(
    name = "bar",
)

bazel_dep(name = "foo")
bazel_dep(name = "rules_python", version = "0.31.0")

local_path_override(module_name = "foo", path = "../")

python = use_extension("@rules_python//python/extensions:python.bzl", "python")
python.toolchain(
    is_default = True,
    python_version = "3.10",
)
use_repo(python, "python_3_10", "python_versions")

pip = use_extension("@rules_python//python/extensions:pip.bzl", "pip")
pip.parse(
    hub_name = "bar_pip_deps",
    python_version = "3.10",
    requirements_lock = "@bar//:requirements_lock.txt",
)
use_repo(pip, "bar_pip_deps")

```

Notice when you now do `bazel run //:main`, it will error out with
```
The current build configuration's Python version doesn't match any of the Python
versions available for this wheel. This wheel supports the following Python versions:
    3.9
```

This error goes away if you remove the dependency on `@foo`.

# Fixes for now

This can all be fixed by patching the `foo` repository's `MODULE.bazel` file but it would be good to have a neater solution.
