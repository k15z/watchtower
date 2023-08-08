FROM node:19

# Copy stuff
WORKDIR "/app"
COPY . .

RUN npm install
CMD ["npm", "run", "dev", "--host", "0.0.0.0" ]
