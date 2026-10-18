OTA Certificates
================

Based on https://pki-tutorial.readthedocs.io/en/latest/simple/index.html

Usage
-----

```
cd ~
git clone https://bitbucket.org/stefanholek/pki-example-1 
cd pki-example-1
sed -i "s/simple/marsattacks/" etc/root-ca.conf
sed -i "s/marsattacks.org/marsattacks.com/" etc/root-ca.conf
sed -i "s/\"org/\"com/" etc/root-ca.conf
sed -i "s/simple/marsattacks/" etc/signing-ca.conf
sed -i "s/marsattacks.org/marsattacks.com/" etc/signing-ca.conf
sed -i "s/\"org/\"com/" etc/signing-ca.conf
mkdir -p ca/root-ca/private ca/root-ca/db crl certs
chmod 700 ca/root-ca/private
cp /dev/null ca/root-ca/db/root-ca.db
echo 01 > ca/root-ca/db/root-ca.crt.srl
echo 01 > ca/root-ca/db/root-ca.crl.srl
```

```
openssl req -new \
    -config etc/root-ca.conf \
    -out ca/root-ca.csr \
    -keyout ca/root-ca/private/root-ca.key
```

Enter 'test' as PEM pass phrase

```
openssl ca -selfsign \
    -config etc/root-ca.conf \
    -in ca/root-ca.csr \
    -out ca/root-ca.crt \
    -extensions root_ca_ext
```

Sign and commit the certificate request

```
mkdir -p ca/signing-ca/private ca/signing-ca/db crl certs
chmod 700 ca/signing-ca/private
cp /dev/null ca/signing-ca/db/signing-ca.db
echo 01 > ca/signing-ca/db/signing-ca.crt.srl
echo 01 > ca/signing-ca/db/signing-ca.crl.srl

openssl req -new \
    -config etc/signing-ca.conf \
    -out ca/signing-ca.csr \
    -keyout ca/signing-ca/private/signing-ca.key
```

Enter 'test' as PEM pass phrase

```
openssl ca \
    -config etc/root-ca.conf \
    -in ca/signing-ca.csr \
    -out ca/signing-ca.crt \
    -extensions signing_ca_ext
```

Sign and commit the certificate request

```
SAN=DNS:ota.marsattacks.com \
openssl req -new \
    -config etc/server.conf \
    -out certs/marsattacks-com.csr \
    -keyout certs/marsattacks-org.key
```

Enter:
1. Domain Component: com
2. Domain Component: marsattacks
3. Domain Component:
4. Organization Name: Simple Inc
5. Organizational Unit Name:
6. Common Name: ota.marsattacks.com

```
openssl ca \
    -config etc/signing-ca.conf \
    -in certs/marsattacks-com.csr \
    -out certs/marsattacks-com.crt \
    -extensions server_ext
```

Sign and commit the certificate request
