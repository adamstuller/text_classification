curl http://0.0.0.0:5000/api/v1/topics -X POST \
-F 'name=banks'  \
-F 'dataset=@/Users/adamstuller/Desktop/temp.csv'  \
-F 'description=Topic for banks comment classification'