pushd "%~dp0../"

py -3.8 -m twine upload --repository testpypi --skip-existing -u=__token__ dist/*

popd