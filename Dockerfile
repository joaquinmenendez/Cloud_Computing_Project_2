FROM python:3.7.3-stretch

# Working Directory
WORKDIR /describer

# Copy source code to working directory
COPY . app.py /describer/

# Install packages from requirements.txt
RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

#Espose a port
EXPOSE 8080

CMD flask run --host=0.0.0.0