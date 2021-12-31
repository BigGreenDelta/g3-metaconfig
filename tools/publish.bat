pushd "%~dp0../"

py -3.8 -m twine upload --repository pypi --skip-existing --config-file=Tools/.pypirc dist/*

popd