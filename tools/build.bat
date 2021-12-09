pushd "%~dp0../"

rd /S /Q dist

py -3.8 -m build

popd
