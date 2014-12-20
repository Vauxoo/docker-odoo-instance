FROM quay.io/ruiztulio/odoo-base-image
MAINTAINER Leonardo Astros <leonardo@vauxoo.com>
RUN adduser --home=/home/runbot --disabled-password --gecos "" --shell=/bin/bash runbot

RUN echo 'root:runbot' |chpasswd

USER runbot
RUN /bin/bash -c "mkdir -p /home/runbot/instance/{config,extra_addons}"
RUN cd /home/runbot/instance && git clone -b 8.0 https://github.com/odoo/odoo.git odoo
RUN cd /home/runbot/instance/extra_addons \
    && git clone -b 8.0-vauxoo https://github.com/Vauxoo/runbot-addons.git \
    && git clone -b 8.0-vauxoo https://github.com/Vauxoo/odoo-extra.git \
    && git clone -b master https://github.com/Vauxoo/panama-dv.git

ADD files/odoo.conf /home/runbot/instance/config/
ADD files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN mkdir -p /home/runbot/.local/share
ENV XDG_DATA_HOME /home/runbot/.local/share

USER root
RUN mkdir /external_files
ADD files/odoo.conf /external_files/odoo.conf
ADD files/supervisord.conf /external_files/supervisord.conf
ADD files/entry_point.py /entry_point.py
RUN chmod +x /entry_point.py
RUN mkdir -p /var/log/supervisor
VOLUME ["/var/log/supervisor", "/home/runbot/instance/odoo/openerp/filestore"]

EXPOSE 8069
CMD ["/entry_point.py"]
