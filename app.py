from flask import Flask, render_template, request, jsonify                                                                                                
  import json                                                                                                                                               
  import os                                                                                                                                                 
                                                                                                                                                            
  app = Flask(__name__)                                                                                                                                     
                                                                                                                                                            
  SETTINGS_FILE = "/config/Settings.json"                                                                                                                   
                                                                                                                                                            
  def load_settings():                                                                                                                                      
      with open(SETTINGS_FILE, "r") as f:                                                                                                                   
          return json.load(f)                                                                                                                               
                                                                                                                                                            
  def save_settings(settings):                                                                                                                              
      with open(SETTINGS_FILE, "w") as f:                                                                                                                   
          json.dump(settings, f, indent=2)                                                                                                                  
                                                                                                                                                            
  @app.route("/")                                                                                                                                           
  def index():                                                                                                                                              
      settings = load_settings()                                                                                                                            
      return render_template("index.html", settings=settings)                                                                                               
                                                                                                                                                            
  @app.route("/api/settings", methods=["GET"])                                                                                                              
  def get_settings():                                                                                                                                       
      return jsonify(load_settings())                                                                                                                       
                                                                                                                                                            
  @app.route("/api/settings", methods=["POST"])                                                                                                             
  def update_settings():                                                                                                                                    
      try:                                                                                                                                                  
          new_settings = request.json                                                                                                                       
          save_settings(new_settings)                                                                                                                       
          return jsonify({"status": "success"})                                                                                                             
      except Exception as e:                                                                                                                                
          return jsonify({"status": "error", "message": str(e)}), 500                                                                                       
                                                                                                                                                            
  if __name__ == "__main__":                                                                                                                                
      app.run(host="0.0.0.0", port=5000)   