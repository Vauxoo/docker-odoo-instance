FROM vauxoo/odoo-80-image
MAINTAINER Leonardo Astros <leonardo@vauxoo.com>
RUN adduser --home=/home/runbot --disabled-password --gecos "" --shell=/bin/bash runbot

RUN apt-get update && apt-get install nginx python-matplotlib python-pandas -q
RUN echo 'root:runbot' |chpasswd
RUN mkdir /home/runbot/.ssh
RUN chown runbot:runbot -R /home/runbot
ADD files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN ln -s /usr/sbin/nginx /usr/bin/nginx

RUN wget -qO- https://deb.nodesource.com/setup | sudo bash - \
    && apt-get install nodejs \
    && npm install -g less \
    && npm install -g less-plugin-clean-css

USER runbot
ENV HOME /home/runbot
ENV ODOO_USER runbot
ENV ODOO_CONFIG_FILE /home/runbot/odoo_runbot.conf
ENV ODOO_FILESTORE_PATH /home/runbot/.local/share/Odoo/filestore
RUN ssh-keyscan github.com > /home/runbot/.ssh/known_hosts \
    && ssh-keyscan launchpad.net >> /home/runbot/.ssh/known_hosts \
    && ssh-keyscan bitbucket.org >> /home/runbot/.ssh/known_hosts \
    && ssh-keyscan gitlab.com >> /home/runbot/.ssh/known_hosts
RUN git config --global user.email "runbot@vauxoo.com"
RUN git config --global user.name "Runbot Vauxoo"
RUN /bin/bash -c "mkdir -p /home/runbot/instance/{config,extra_addons}"
RUN cd /home/runbot/instance && git clone -b 8.0 https://github.com/odoo/odoo.git odoo
RUN cd /home/runbot/instance/extra_addons \
    && git clone -b 8.0-vauxoo --depth=1 --single-branch https://github.com/Vauxoo/runbot-addons.git \
    && git clone -b 8.0-vauxoo --depth=1 --single-branch https://github.com/Vauxoo/odoo-extra.git \
    && git clone -b master --depth=1 --single-branch https://github.com/Vauxoo/panama-dv.git \
    && git clone -b master --single-branch --depth=1 https://github.com/vauxoo-dev/gist-vauxoo.git \
    && git clone -b 8.0 --single-branch --depth=1 git@github.com:Vauxoo/odoo-themes.git

ADD files/odoo_runbot.conf /home/runbot/instance/config/odoo_runbot.conf
ADD files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN mkdir -p /home/runbot/.local/share
ENV XDG_DATA_HOME /home/runbot/.local/share
ENV PYTHONPATH $PYTHONPATH:/home/runbot/instance/extra_addons/panama-dv

USER root
ADD files/entry_point.py /entry_point.py
RUN chmod +x /entry_point.py
RUN ln -s /home/runbot/instance/extra_addons/odoo-extra/runbot/static/repo_local /runbot_repo_local
RUN mkdir /external_files
ADD files/odoo_runbot.conf /external_files/odoo_runbot.conf
ADD files/supervisord.conf /external_files/supervisord.conf
RUN mkdir -p /var/log/supervisor
VOLUME ["/var/log/supervisor", "/home/runbot/.local/share/Odoo/filestore", "/home/runbot/instance/extra_addons/odoo-extra/runbot/static", "/tmp"]

EXPOSE 8069
EXPOSE 8072
EXPOSE 8080

CMD /entry_point.py
