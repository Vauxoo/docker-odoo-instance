FROM vauxoo/odoo-80-image
MAINTAINER Leonardo Astros <leonardo@vauxoo.com>
RUN adduser --home=/home/runbot --disabled-password --gecos "" --shell=/bin/bash runbot

RUN apt-get update && apt-get install nginx -q
RUN echo 'root:runbot' |chpasswd
RUN mkdir /home/runbot/.ssh
ADD id_rsa /home/runbot/.ssh/id_rsa
RUN chown runbot:runbot -R /home/runbot \
    && chmod 600 /home/runbot/.ssh/id_rsa
ADD files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
USER runbot
ENV HOME /home/runbot
ENV ODOO_USER runbot
ENV ODOO_CONFIG_FILE /home/runbot/.openerp_serverrc
ENV ODOO_FILESTORE_PATH /home/runbot/.local/share/Odoo/filestore 
RUN ssh-keyscan github.com > /home/runbot/.ssh/known_hosts \
    && ssh-keyscan launchpad.net >> /home/runbot/.ssh/known_hosts \
    && ssh-keyscan bitbucket.org >> /home/runbot/.ssh/known_hosts \
    && ssh-keyscan gitlab.com >> /home/runbot/.ssh/known_hosts
RUN /bin/bash -c "mkdir -p /home/runbot/instance/{config,extra_addons}"
RUN cd /home/runbot/instance && git clone -b 8.0 https://github.com/odoo/odoo.git odoo
RUN cd /home/runbot/instance/extra_addons \
    && git clone -b 8.0-vauxoo --depth=1 --single-branch https://github.com/Vauxoo/runbot-addons.git \
    && git clone -b 8.0-vauxoo --depth=1 --single-branch https://github.com/Vauxoo/odoo-extra.git \
    && git clone -b master --depth=1 --single-branch https://github.com/Vauxoo/panama-dv.git

ADD files/openerp_serverrc /home/runbot/.openerp_serverrc
ADD files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN mkdir -p /home/runbot/.local/share
ENV XDG_DATA_HOME /home/runbot/.local/share
ENV PYTHONPATH $PYTHONPATH:/home/runbot/instance/extra_addons/panama-dv

USER root
RUN mkdir /external_files
ADD files/openerp_serverrc /external_files/openerp_serverrc
ADD files/supervisord.conf /external_files/supervisord.conf
RUN echo 'odoorunbot.vauxoo.com' > /etc/hostname
RUN mkdir -p /var/log/supervisor
VOLUME ["/var/log/supervisor", "/home/odoo/.local/share/Odoo/filestore"]
RUN wget -O /entry_point.py https://raw.githubusercontent.com/Vauxoo/docker_entrypoint/master/entry_point.py \
    && chmod +x /entry_point.py

EXPOSE 8069
EXPOSE 8080

CMD /entry_point.py
