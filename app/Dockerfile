FROM node:19

# Copy stuff
WORKDIR "/app"
COPY . .

RUN npm install -g @ionic/cli
RUN npm install
CMD ["ionic", "serve", "--host", "0.0.0.0" ]
