class Company:
    def __init__(self, url):
        self.url = url
        self.name = ''
        self.tags = []
        self.description = ''
        self.website = ''
        self.linkedin = ''
  
    def set_name(self, name):
        self.name = name
    
    def set_tags(self, tags):
        self.tags = tags
    
    def set_description(self, description):
        self.description = description
    
    def set_website(self, website):
        self.website = website
    
    def set_linkedin(self, linkedin):
        self.linkedin = linkedin

    def get_url(self):
        return self.url
        
    def get_name(self):
        return self.name
    
    def get_tags(self):
        return self.tags
    
    def get_description(self):
        return self.description
    
    def get_website(self):
        return self.website
    
    def get_linkedin(self):
        return self.linkedin