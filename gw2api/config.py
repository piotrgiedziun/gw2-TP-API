class Config( object ):
  
  EMAIL = ""
  PASSWORD = ""
  
  def getData( self ):
    return {
      'email': self.getEmail(),
      'password': self.getPassword()
    }
  
  def getEmail( self ):
    return self.EMAIL
    
  def getPassword( self ):
    return self.PASSWORD