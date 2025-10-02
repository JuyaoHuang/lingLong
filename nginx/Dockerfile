# nginx/Dockerfile

# 使用官方 Nginx 镜像
FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/