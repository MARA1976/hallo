import runpod  # Required

def process_data(input_data):
    # Exemple de traitement : retourne un message avec le nom
    name = input_data.get("name", "RunPod")
    return {"message": f"Hello, {name}!"}

def handler(event):
    # Extract input data from the request
    input_data = event["input"]
    
    # Process the input (replace this with your own code)
    result = process_data(input_data)
    
    # Return the result
    return result

runpod.serverless.start({"handler": handler})  # Required
