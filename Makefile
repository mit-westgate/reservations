FCGI_NAME:=$(shell awk 'BEGIN{srand();printf("%d", 65536*rand())}')

define HTACCESS
<IfModule mod_fcgid.c>
   AddHandler fcgid-script .fcgi
   <Files ~ (\.fcgi)>
       SetHandler fcgid-script
       Options +FollowSymLinks +ExecCGI
   </Files>
</IfModule>

<IfModule mod_rewrite.c>
   Options +FollowSymlinks
   RewriteEngine On
   RewriteBase /reservations
   RewriteRule ^admin$$ admin.py [L]
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteRule ^(.*)$$ $(FCGI_NAME).fcgi/$$1 [QSA,L]
</IfModule>
endef
export HTACCESS

default:
	cp app.fcgi $(FCGI_NAME).fcgi
	echo "$$HTACCESS" > .htaccess

lib:
	mkdir -p lib
	wget -P lib https://pypi.python.org/packages/source/M/MarkupSafe/MarkupSafe-0.19.tar.gz
	wget -P lib https://pypi.python.org/packages/source/f/flup/flup-1.0.2.tar.gz
	wget -P lib https://pypi.python.org/packages/source/i/itsdangerous/itsdangerous-0.23.tar.gz
	wget -P lib https://pypi.python.org/packages/source/F/Flask/Flask-0.10.1.tar.gz
	wget -P lib https://pypi.python.org/packages/source/J/Jinja2/Jinja2-2.7.2.tar.gz
	wget -P lib https://pypi.python.org/packages/source/W/Werkzeug/Werkzeug-0.9.4.tar.gz
	wget -P lib https://files.pythonhosted.org/packages/ca/a9/62f96decb1e309d6300ebe7eee9acfd7bccaeedd693794437005b9067b44/pytz-2018.5.tar.gz
	wget -P lib https://files.pythonhosted.org/packages/50/30/f89a4fc014a03e180840d432e73ffb96da422f2a8094ff3539f0f0c46661/oauth2client-4.1.2.tar.gz
	wget -P lib https://files.pythonhosted.org/packages/fd/ce/aa4a385e3e9fd351737fd2b07edaa56e7a730448465aceda6b35086a0d9b/httplib2-0.11.3.tar.gz
	wget -P lib https://files.pythonhosted.org/packages/4e/92/e4746e646585c8c359781c19984fe8b6b8794a6cfe382cd481329d5252ac/google-api-python-client-1.7.4.tar.gz
	wget -P lib https://files.pythonhosted.org/packages/9b/7c/ee600b2a9304d260d96044ab5c5e57aa489755b92bbeb4c0803f9504f480/pyOpenSSL-18.0.0.tar.gz
	wget -P lib https://files.pythonhosted.org/packages/16/d8/bc6316cf98419719bd59c91742194c111b6f2e85abac88e496adefaf7afe/six-1.11.0.tar.gz
	wget -P lib https://files.pythonhosted.org/packages/10/46/059775dc8e50f722d205452bced4b3cc965d27e8c3389156acd3b1123ae3/pyasn1-0.4.4.tar.gz
	wget -P lib https://files.pythonhosted.org/packages/37/33/74ebdc52be534e683dc91faf263931bc00ae05c6073909fde53999088541/pyasn1-modules-0.2.2.tar.gz
	wget -P lib https://files.pythonhosted.org/packages/14/89/adf8b72371e37f3ca69c6cb8ab6319d009c4a24b04a31399e5bd77d9bb57/rsa-3.4.2.tar.gz
	wget -P lib https://files.pythonhosted.org/packages/cd/db/f7b98cdc3f81513fb25d3cbe2501d621882ee81150b745cdd1363278c10a/uritemplate-3.0.0.tar.gz
	tar -C lib -xzf lib/MarkupSafe-0.19.tar.gz
	tar -C lib -xzf lib/flup-1.0.2.tar.gz
	tar -C lib -xzf lib/itsdangerous-0.23.tar.gz
	tar -C lib -xzf lib/Flask-0.10.1.tar.gz
	tar -C lib -xzf lib/Jinja2-2.7.2.tar.gz
	tar -C lib -xzf lib/Werkzeug-0.9.4.tar.gz
	tar -C lib -xzf lib/pytz-2018.5.tar.gz
	tar -C lib -xzf lib/oauth2client-4.1.2.tar.gz
	tar -C lib -xzf lib/httplib2-0.11.3.tar.gz
	tar -C lib -xzf lib/google-api-python-client-1.7.4.tar.gz
	tar -C lib -xzf lib/pyOpenSSL-18.0.0.tar.gz
	tar -C lib -xzf lib/six-1.11.0.tar.gz
	tar -C lib -xzf lib/pyasn1-0.4.4.tar.gz
	tar -C lib -xzf lib/pyasn1-modules-0.2.2.tar.gz
	tar -C lib -xzf lib/rsa-3.4.2.tar.gz
	tar -C lib -xzf lib/uritemplate-3.0.0.tar.gz
	rm lib/MarkupSafe-0.19.tar.gz
	rm lib/flup-1.0.2.tar.gz
	rm lib/itsdangerous-0.23.tar.gz
	rm lib/Flask-0.10.1.tar.gz
	rm lib/Jinja2-2.7.2.tar.gz
	rm lib/Werkzeug-0.9.4.tar.gz
	rm lib/pytz-2018.5.tar.gz
	rm lib/oauth2client-4.1.2.tar.gz
	rm lib/httplib2-0.11.3.tar.gz
	rm lib/google-api-python-client-1.7.4.tar.gz
	rm lib/pyOpenSSL-18.0.0.tar.gz
	rm lib/six-1.11.0.tar.gz
	rm lib/pyasn1-0.4.4.tar.gz
	rm lib/rsa-3.4.2.tar.gz
	rm lib/pyasn1-modules-0.2.2.tar.gz
	rm lib/uritemplate-3.0.0.tar.gz
clean:
	rm -f .htaccess
	rm -f `find . -name "*fcgi" | grep -v app.fcgi`
