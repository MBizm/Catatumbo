#
# Builder image
#
# base image
FROM node:12.16 as builder



WORKDIR /home/node
#USER node

#COPY --chown=node:node ./package.json .
#COPY --chown=node:node ./package-lock.json .
ARG API_HOST=127.0.0.1:8081

ENV API_URL=$API_HOST

RUN echo ${API_URL}

COPY  ./package.json .
COPY  ./package-lock.json .

RUN npm install

#COPY --chown=node:node . ./
COPY . ./

RUN npm install -g envsub
RUN envsub ./src/assets/env.template.js  ./src/assets/env.js
RUN npm remove -g envsub

RUN npm run build

# Removing development dependencies
RUN rm -r node_modules
# Install using production dependencies
RUN npm install --production; exit 0

# base image
FROM alpine:3.11.6



RUN apk add --no-cache nginx=1.16.1-r6 && \
    rm -rf /var/cache/apk/*

# implement changes required to run NGINX as an unprivileged user
## Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# copy nginx configuration
COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf

RUN rm /etc/nginx/nginx.conf
COPY docker/nginx/nginx.conf /etc/nginx/nginx.conf


# copy artifact build from the 'build environment'
COPY  --from=builder /home/node/dist/CatatumboApp3 /usr/share/nginx/html

#USER nginx
RUN mkdir /tmp/nginx

# expose port 3000
EXPOSE 3000

# run nginx
CMD ["nginx", "-g", "daemon off;"]
