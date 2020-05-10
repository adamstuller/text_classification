class TagBalancer():
    
    def __init__(self, limit):
        self.__limit = limit
        # self.__default_tag = default_tag
    
    def fit(self,y):
        self.__original_tags = list(y.unique())
        self.__tag_mapper = y.value_counts().to_dict()
        for key, value in self.__tag_mapper.items():
            if value < self.__limit: 
                self.__tag_mapper[key] = 'DEFAULT_TAG' #if self.__default_tag is None else self.__default_tag
            else: 
                self.__tag_mapper[key] = key
        print(self.__tag_mapper)
        return self
                
    def transform(self, y):
        return y.apply(lambda tag: self.__tag_mapper[tag])
    
    def fit_transform(self, y):
        self.fit(y)
        return self.transform(y)