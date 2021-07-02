FROM nikolaik/python-nodejs:python3.9-nodejs16
WORKDIR /home

# Install deps
ADD requirements.txt /home/
ADD package-lock.json /home/
ADD package.json /home/
RUN pip install -r requirements.txt
RUN npm install --save-dev
RUN npm install truffle -g

# Add Files
ADD highwind_st.py /home/
ADD modules /home/modules/
ADD migrations_temp /home/migrations_temp/
ADD contracts_temp /home/contracts_temp/
ADD truffle.js /home/
ADD migrations_temp /home/migrations/

# Make dirs
RUN mkdir -p /home/build
RUN mkdir -p /home/highwind_jsons
RUN mkdir -p /home/highwind_jsons/items/
RUN mkdir -p /home/highwind_jsons/contracts/
RUN mkdir -p /home/migrations

# Expose port
EXPOSE 8501
# Start App
CMD [ "streamlit", "run" ,"highwind_st.py" ]