call build.bat

pushd "%~dp0../"

py -3.8 -m twine upload --repository pypi --skip-existing -u=__token__ dist/*

popd

py -3.8 -m pip install --upgrade --no-deps g3-config
py -3.8 -m pip install --upgrade --no-deps g3-config

