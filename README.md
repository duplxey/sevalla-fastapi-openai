# Real-Time OpenAI Response Streaming with FastAPI

Learn how to integrate OpenAI into your FastAPI project. The repository covers:

1. Synchronous approach (waiting for the entire model response before returning it)
2. Asynchronous approach (streaming the model response chunk by chunk in real time)

Read the [blog post](#).

## How to use?

1. Clone the repository.

2. Create a virtual environment, activate it, and install the requirements:

  ```sh
  $ python3 -m venv venv && source venv/bin/activate
  (venv) $ pip install -r requirements.txt
  ```

3. Copy *.env.example* paste it as *.env* and change it accordingly.

4. Run the development server:

  ```sh
  (venv) $ fastapi dev main.py
  ```

7. Navigate to [http://localhost:8000/](http://localhost:8000/) in your favorite browser.
