
C:

cd C:\service-deploy\apps\std-inv-report-v8


cmd /k "activate python36 && python cleanse_watch.py -i C:\service-deploy\shared\std-inv-report-v8\cleanse\raw -o C:\service-deploy\shared\std-inv-report-v8\cleanse\cleaned -sm -cm"


