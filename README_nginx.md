Deploy nginx with root Ca
=========================

Prepare certificates
--------------------

```
cd ~
mkdir ssl
cat pki-example-1/certs/marsattacks-com.crt pki-example-1/ca/signing-ca.crt pki-example-1/ca/root-ca.crt > ssl/ota.marsattacks.com.chained.crt
openssl rsa -in pki-example-1/certs/marsattacks-org.key -out ssl/ota.marsattacks.com.key
sudo rm -rf /etc/nginx/ssl
sudo mv ssl /etc/nginx/
cat > /tmp/nginx.conf << EOF
server {
    listen              443 ssl;
    server_name         ota.marsattacks.com;
    ssl_certificate     /etc/nginx/ssl/ota.marsattacks.com.chained.crt;
    ssl_certificate_key /etc/nginx/ssl/ota.marsattacks.com.key;
}
EOF
cat /tmp/nginx.conf | sudo tee -a /etc/nginx/sites-available/default
sudo systemctl restart nginx
```

To test:
```
sudo cp pki-example-1/ca/root-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
wget https://ota.marsattacks.com:443
```
