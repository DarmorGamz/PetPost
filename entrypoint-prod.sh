#!/bin/sh
sed -i "s/petpost.localhost/$DOMAIN/g" /usr/share/nginx/html/index.html
exec nginx -g 'daemon off;'