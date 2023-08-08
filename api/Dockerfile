FROM python:3.10

# Copy stuff
WORKDIR "/app"
COPY . .

# Install dependencies
RUN pip install chalice==1.29.0 boto3==1.28.1
RUN pip install -r requirements.txt

# Run your app
CMD [ "chalice", "local", "--host", "0.0.0.0" ]
