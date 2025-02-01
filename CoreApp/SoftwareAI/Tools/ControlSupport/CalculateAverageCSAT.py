tools_CalculateAverageCSAT = [
{
    "type": "function",
    "function": {
        "name": "CalculateAverageCSAT",
        "description": "\n**Function Arguments Description**\n\nThe function `CalculateAverageCSAT` takes two arguments:\n\n1. **testeid** (String): This is a unique identifier for a test case, typically a UUID string. It is used to reference a specific ticket within a database.\n\n2. **appfb** (String): This stands for \"application feature\" and is used to specify which reference or setting within the application determines the reference to use. It helps filter or select the relevant data from the database.\n\nThe function processes these inputs to calculate the average CSAT score across all retrieved tickets and returns the result, providing insights into satisfaction levels.",
        "parameters": {
            "type": "object",
            "properties": {
                "testeid": {
                    "type": "string",
                    "description": "Descri\u00e7\u00e3o do argumento testeid."
                },
                "appfb": {
                    "type": "string",
                    "description": "Descri\u00e7\u00e3o do argumento appfb."
                }
            },
            "required": [
                "testeid",
                "appfb"
            ]
        }
    }
}
]
