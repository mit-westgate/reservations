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
   RewriteBase /
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
	tar -C lib -xzf lib/MarkupSafe-0.19.tar.gz
	tar -C lib -xzf lib/flup-1.0.2.tar.gz
	tar -C lib -xzf lib/itsdangerous-0.23.tar.gz
	tar -C lib -xzf lib/Flask-0.10.1.tar.gz
	tar -C lib -xzf lib/Jinja2-2.7.2.tar.gz
	tar -C lib -xzf lib/Werkzeug-0.9.4.tar.gz
	rm lib/MarkupSafe-0.19.tar.gz
	rm lib/flup-1.0.2.tar.gz
	rm lib/itsdangerous-0.23.tar.gz
	rm lib/Flask-0.10.1.tar.gz
	rm lib/Jinja2-2.7.2.tar.gz
	rm lib/Werkzeug-0.9.4.tar.gz

clean:
	rm -f .htaccess
	rm -f `find . -name "*fcgi" | grep -v app.fcgi`
