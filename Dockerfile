FROM nginx:alpine

# Kopiere Website-Dateien
COPY index.html /usr/share/nginx/html/
COPY Logenhaus_blue.jpg /usr/share/nginx/html/
COPY admin.html /usr/share/nginx/html/

# Kopiere nginx-Konfiguration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponiere Port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
