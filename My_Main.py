from fastapi import FastAPI, HTTPException
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import create_extraction_chain
from langchain.document_loaders import PyPDFLoader
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

#Create a FastAPI instance
app = FastAPI()


# Define exception classes
class RequestValidationError(HTTPException): #Exception raised when the data provided in the request does not meet the specified validation criteria.
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail) #  "Bad Request" for 400

class PDFProcessingError(HTTPException): #handle errors specifically related to the processing of PDF file
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail) # "Internal Server Error" erreur coté serveur

class LLMProcessingError(HTTPException): #LLM model processing error exception
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail)

class DataProcessingError(HTTPException): #This exception is raised if no data is extracted from the PDF
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail)


# Endpoint 1
@app.post("/extraire-informations")
async def extraire_informations(pdf_path: str):
    """
    Extracts information from a PDF file.

    **Args**:

        pdf_path (str): Path to the PDF file.

    **Returns**:

        dict: Extracted information from the PDF (JSON format).

    **Raises**:

        RequestValidationError: If the specified PDF file is not found.
        PDFProcessingError: In case of an error processing the PDF file.
    """

    try:
        # We use the gpt-3.5-turbo LLM model from ChatOpenai of the langchain library
        llm = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo",openai_api_key='sk-34bj********************************') # Please provide your openai API secret key
        
        # Define the structure of the information extracted from the paper (title, authors, keywords). "
        schema = {   
            "properties":{
                "title":{"type": "string"},  
                "author": {"type": "array", "items": {"type": "string"}},
                "keywords": {"type": "array", "items": {"type": "string"}}
            }
        }
        
        # Load the paper with PDF format using its path
        doc = PyPDFLoader(pdf_path).load_and_split()

        #Raise exception DataProcessingError
        if not doc:
            raise DataProcessingError(detail="No data extracted from PDF.")
        
        #Create an extraction chain with the defined schema and the LLM model using the create_extraction_chain function 
        chain = create_extraction_chain(schema, llm)
        
        #Run the extraction chain on the loaded document
        metadata= chain.run(doc)
        
        # Return document information in JSON format
        return {"Paper path": pdf_path, "Paper information": metadata}
    
    except FileNotFoundError:
        #raise exception RequestValidationError
        raise RequestValidationError(detail=f"PDF file not found : {pdf_path}")
    
    except Exception as e:
        # raise exception PDFProcessingError
        raise PDFProcessingError(detail=f"PDF processing error: {str(e)}")
    

# Endpoint 2
@app.post("/resumer-papier")
async def resume_paper(pdf_path: str):
    """
    Summarizes the content of a PDF file.

    **Args**:

        pdf_path (str): Path to the PDF file.

    **Returns**:

        dict: Summary of the PDF content (JSON format).

    **Raises**:

        RequestValidationError: If the specified PDF file is not found.
        LLMProcessingError: In case of an error processing the LLM model.
        DataProcessingError: If no data is extracted from the PDF.
    """

    try:
        # We use the gpt-3.5-turbo LLM model from Openai of the langchain library
        llm = OpenAI(temperature=0.2,openai_api_key='sk-34bj********************************') # Please provide your openai API secret key
        
        # Load the paper with PDF format using its path
        doc = PyPDFLoader(pdf_path).load_and_split()

        #Raise exception DataProcessingError
        if not doc:
            raise DataProcessingError(detail="No data extracted from PDF.")
        
        #Create an extraction chain from LLM model using the load_summarize_chain function and the MapReduce approch (used for text summarization).
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        
        #Run the extraction chain on the loaded document
        summary = chain.run(doc)
        
        # Return document summary in JSON format
        return {"Paper path": pdf_path, "Paper resume": summary}
    
    except FileNotFoundError:
        #Raise exception RequestValidationError
        raise RequestValidationError(detail=f"PDF file not found : {pdf_path}")
    
    except Exception as e:
        # Raise exception LLMProcessingError
        raise LLMProcessingError(detail=f"LLM model processing error : {str(e)}")


