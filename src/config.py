class BaseConfig(object): 
    'Base config class' 
    DEBUG = True 
    TESTING = False 
 
class ProductionConfig(BaseConfig): 
    'Production specific config' 
    DEBUG = False 
 
class StagingConfig(BaseConfig): 
    'Staging specific config' 
    DEBUG = True 
 
class DevelopmentConfig(BaseConfig): 
    'Development environment specific config' 
    DEBUG = True 
    TESTING = True 
 

