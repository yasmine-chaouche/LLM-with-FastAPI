
This code represents an API built with FastAPI, incorporating a Large Language Model (LLM) through the langchain library. It facilitates the extraction of information and the generation of automatic summaries for research papers.



#### Explications:
    Run the API in terminal: uvicorn My_Main:app --reload
    Test the API with the http://localhost:8000/docs URL
        
   ###### Documentation
        By using docstrings comments, FastAPI can automatically extract the necessary information from the code.
        When running FastAPI application, we can access the automatically generated documentation by the URL http://localhost:8000/docs or http://localhost:8000/redoc
        
        Model: we use the gpt-3.5-turbo model from openai of the langchain library
    
  ###### hyperparameters:
        temperature:parameter for controlling the creativity or variability of model predictions. In this case it is =0.2 makes the model's predictions more focused and deterministic with a high precision.
        


#### Test case:
    for the provided paper: we use "./Papers/MyPaper.pdf" as input:
        Endpoint1 output: 
            {
         "paper path": "./Papers/MyPaper.pdf",
         "paper information": [
             {
             "title": "WEKA-based Real-Time Attack Detection for V ANET Simulations",
             "author": [
                 "Yasmine CHAOUCHE",
                 "Eric RENAULT",
                 "Ryma BOUSSAHA"
             ],
              "keywords": [
                  "V ANET",
                 "WEKA",
                 "Attack Detection",
                 "Real-Time"
             ]
             }
         ]
         }
        
        
        
        endpoint2 output:
         {
         "Paper path": "./Papers/MyPaper.pdf",
         "Paper resume": " This paper presents an enhanced version of the Framework for Misbehavior Detection (F2MD) 
         which uses the Waikato Environment for Knowledge Analysis (WEKA) and the Support Vector Machine (SVM) algorithm 
         for real-time attack detection in Vehicular Ad Hoc Networks (VANETs). It also discusses the use of machine learning 
         techniques in Intrusion Detection Systems (IDS) and the advantages of using simulators such as VEINS for testing. 
         This solution facilitates real-time detection evaluations, model comparisons, and result visualization, enhancing 
         the overall effectiveness of the framework."
         }

#### Conclusion:
     the summary result is quite precise, and the information extracted from the paper are correct :))
