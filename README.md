
This project provides a secure API service built with Flask that enables users to submit and run custom Python scripts on a server. To ensure safe execution, it leverages nsjail for sandboxing. The API returns the output of the script’s main() function along with any standard output generated.


## Setup Execution


1.  **Build the Docker Image:**
    This builds the image. Replace `<your-image-tag>`
    ```bash
    docker build -t <your-image-tag> .
    ```

2.  **Run the Docker Container Locally:**
    This maps host port 8080 to the container's port 8080. Replace `<your-image-tag>` with the tag used in the build step.
    ```bash
    docker run -p 8080:8080 --rm <your-image-tag>
    ```

3.  **Test Locally:**

        ```bash
            curl -X POST https://localhost:8080/execute \
            -H "Content-Type: application/json" \
            -d '{
                "script": "import json, numpy as np\ndef main():\n    return {\"sum\": int(np.sum([1, 2, 3]))}"
            }'
        ```

## Deployment to Google Cloud Run

## Testing Deployed Service Examples

The following examples assume the service has been deployed and is accessible at the URL:
`https://python-app-10467047585.northamerica-northeast1.run.app` .


    ```bash
        curl -X POST https://python-app-10467047585.northamerica-northeast1.run.app/execute \
        -H "Content-Type: application/json" \
        -d '{
            "script": "import json, numpy as np\ndef main():\n    return {\"sum\": int(np.sum([1, 2, 3]))}"
        }'
    ```
