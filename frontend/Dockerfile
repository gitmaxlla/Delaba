FROM node:20-alpine as static-build

WORKDIR /frontend

COPY ./ ./
RUN npm install
RUN npm run build

FROM nginx
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=static-build /frontend/build/client /usr/share/nginx/html
