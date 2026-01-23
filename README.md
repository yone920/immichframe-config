# ImmichFrame Config                                                                                                                                      
                                                                                                                                                            
  A lightweight web app for editing ImmichFrame settings from your phone or desktop.                                                                        
                                                                                                                                                            
  ## Features                                                                                                                                               
  - Mobile-friendly interface                                                                                                                               
  - Edit display, appearance, and weather settings                                                                                                          
  - No authentication needed (local network use)                                                                                                            
                                                                                                                                                            
  ## Deploy                                                                                                                                                 
                                                                                                                                                            
  ```bash                                                                                                                                                   
  docker compose up -d --build                                                                                                                              
                                                                                                                                                            
  Access at http://your-server-ip:5050                                                                                                                      
                                                                                                                                                            
  Configuration                                                                                                                                             
                                                                                                                                                            
  Mount your ImmichFrame settings directory to /config:                                                                                                     
                                                                                                                                                            
  volumes:                                                                                                                                                  
    - /opt/immichframe:/config   