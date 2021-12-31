call build.bat

call publish.bat

call upgrade.bat
:: It almost always can't find the "new" version at first try
call upgrade.bat
