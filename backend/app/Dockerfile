FROM python:latest 


#working dir
WORKDIR /code

RUN apt-get update && \
     apt-get install -y netcat-openbsd
# Install dependencies
COPY requirements.txt .

# Install netcat

RUN pip install  -r requirements.txt

# Copy entire project directory to working directory
COPY . .

COPY wait-for.sh .
EXPOSE 8000
#CMD python3 -m uvicorn app:app --reload --host 0.0.0.0 --port 80
# Command to run the FastAPI application
#RUN python3 -m uvicorn main:app --reload
# CMD [ "python", "-m", "uvicorn", "index:app", ,"--reload", "--host", "0.0.0.0", "--port", "8000"]
RUN chmod +x wait-for.sh

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]